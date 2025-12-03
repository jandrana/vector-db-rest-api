import threading
from typing import Dict, List, Optional, Any, Callable
from app.db.models import Document
from app.interfaces.repositories.document_repository import IDocumentRepository
from app.interfaces.repositories.replayable_repository import IReplayableRepository
from app.interfaces.id_generation import IIdGenerator
from app.interfaces.persistence import IPersistenceManager

# Type alias for replay handler functions
ReplayHandler = Callable[[str, Dict[str, Any]], None]


class DocumentRepository(IDocumentRepository, IReplayableRepository):
    def __init__(
        self,
        storage: Dict[int, Document],
        id_generator: IIdGenerator,
        persistence_manager: IPersistenceManager,
        lock: threading.RLock,
    ):
        self.documents: Dict[int, Document] = storage
        self.id_generator = id_generator
        self.persistence_manager = persistence_manager
        self.lock = lock
        self._replay_mode = False  # Skip persistence during replay

    def _persist(self, action: str, data: Dict[str, Any]) -> None:
        if not self._replay_mode:
            self.persistence_manager.save_action(action, data)

    def get(self, document_id: int) -> Optional[Document]:
        with self.lock:
            return self.documents.get(document_id)

    def get_by_library(self, library_id: int) -> List[Document]:
        with self.lock:
            return [
                doc for doc in self.documents.values() if doc.library_id == library_id
            ]

    def get_all(self) -> List[Document]:
        with self.lock:
            return list(self.documents.values())

    def create(
        self, name: str, library_id: int, disk_id: Optional[int] = None
    ) -> Document:
        with self.lock:
            new_id = (
                disk_id
                if disk_id is not None
                else self.id_generator.get_new_document_id()
            )
            new_document = Document(id=new_id, name=name, library_id=library_id)
            self.documents[new_id] = new_document
            if disk_id is not None:
                self.id_generator.set_document_id(disk_id)
            self._persist(
                "create_document",
                {"id": new_id, "name": name, "library_id": library_id},
            )
            return new_document

    def update(self, document_id: int, name: Optional[str]) -> Optional[Document]:
        with self.lock:
            document = self.get(document_id)
            if not document:
                return None
            if name is not None:
                document.name = name
            self._persist("update_document", {"id": document_id, "name": name})
            return document

    def delete(self, document_id: int) -> int:
        with self.lock:
            if document_id not in self.documents:
                return 0
            del self.documents[document_id]
            self._persist("delete_document", {"id": document_id})
            return 1

    def get_replay_handlers(self) -> Dict[str, ReplayHandler]:
        return {
            "create_document": lambda _action, data: self.create(
                data["name"], data["library_id"], disk_id=data["id"]
            ),
            "update_document": lambda _action, data: self.update(
                data["id"], data.get("name")
            ),
            "delete_document": lambda _action, data: self.delete(data["id"]),
        }
