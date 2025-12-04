import threading
from typing import Dict, List, Optional, Any, Callable
from app.db.models import Library
from app.interfaces.repositories.library_repository import ILibraryRepository
from app.interfaces.repositories.replayable_repository import IReplayableRepository
from app.interfaces.id_generation import IIdGenerator
from app.interfaces.persistence import IPersistenceManager

ReplayHandler = Callable[[str, Dict[str, Any]], None]


class LibraryRepository(ILibraryRepository, IReplayableRepository):
    def __init__(
        self,
        storage: Dict[int, Library],
        id_generator: IIdGenerator,
        persistence_manager: IPersistenceManager,
        lock: threading.RLock,
    ):
        self.libraries: Dict[int, Library] = storage
        self.id_generator = id_generator
        self.persistence_manager = persistence_manager
        self.lock = lock
        self._replay_mode = False

    def _persist(self, action: str, data: Dict[str, Any]) -> None:
        if not self._replay_mode:
            self.persistence_manager.save_action(action, data)

    def get(self, library_id: int) -> Optional[Library]:
        with self.lock:
            return self.libraries.get(library_id)

    def get_all(self) -> List[Library]:
        with self.lock:
            return list(self.libraries.values())

    def create(self, name: str, disk_id: Optional[int] = None) -> Library:
        with self.lock:
            new_id = (
                disk_id
                if disk_id is not None
                else self.id_generator.get_new_library_id()
            )
            new_library = Library(id=new_id, name=name)
            self.libraries[new_id] = new_library
            if disk_id is not None:
                self.id_generator.set_library_id(disk_id)
            self._persist("create_library", {"id": new_id, "name": name})
            return new_library

    def update(self, library_id: int, name: Optional[str]) -> Optional[Library]:
        with self.lock:
            library = self.get(library_id)
            if not library:
                return None
            if name is not None:
                library.name = name
            self._persist("update_library", {"id": library_id, "name": name})
            return library

    def delete(self, library_id: int) -> bool:
        with self.lock:
            if library_id not in self.libraries:
                return False
            del self.libraries[library_id]
            self._persist("delete_library", {"id": library_id})
            return True

    def get_replay_handlers(self) -> Dict[str, ReplayHandler]:
        return {
            "create_library": lambda _action, data: self.create(
                data["name"], disk_id=data["id"]
            ),
            "update_library": lambda _action, data: self.update(
                data["id"], data.get("name")
            ),
            "delete_library": lambda _action, data: self.delete(data["id"]),
        }
