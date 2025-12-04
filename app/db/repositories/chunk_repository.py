import threading
from typing import Dict, List, Optional, Any, Callable
from app.db.models import Chunk
from app.interfaces.repositories.chunk_repository import IChunkRepository
from app.interfaces.repositories.replayable_repository import IReplayableRepository
from app.interfaces.id_generation import IIdGenerator
from app.interfaces.persistence import IPersistenceManager
from app.interfaces.repositories.document_repository import IDocumentRepository

ReplayHandler = Callable[[str, Dict[str, Any]], None]


class ChunkRepository(IChunkRepository, IReplayableRepository):
    def __init__(
        self,
        storage: Dict[int, Chunk],
        id_generator: IIdGenerator,
        persistence_manager: IPersistenceManager,
        document_repository: IDocumentRepository,
        lock: threading.RLock,
    ):
        self.chunks: Dict[int, Chunk] = storage
        self.id_generator = id_generator
        self.persistence_manager = persistence_manager
        self.document_repository = document_repository
        self.lock = lock
        self._replay_mode = False

    def _persist(self, action: str, data: Dict[str, Any]) -> None:
        if not self._replay_mode:
            self.persistence_manager.save_action(action, data)

    def _get_lib_id_from_document(self, document_id: int) -> int:
        document = self.document_repository.get(document_id)
        if document is None:
            from app.core.exceptions import EntityNotFoundError

            raise EntityNotFoundError.document(document_id)
        return document.library_id

    def get(self, chunk_id: int) -> Optional[Chunk]:
        with self.lock:
            return self.chunks.get(chunk_id)

    def get_by_document(self, document_id: int) -> List[Chunk]:
        with self.lock:
            return [
                chunk
                for chunk in self.chunks.values()
                if chunk.document_id == document_id
            ]

    def get_by_library(self, library_id: int) -> List[Chunk]:
        with self.lock:
            return [
                chunk
                for chunk in self.chunks.values()
                if chunk.library_id == library_id
            ]

    def get_all(self) -> List[Chunk]:
        with self.lock:
            return list(self.chunks.values())

    def create(
        self,
        text: str,
        document_id: int,
        embedding: Optional[List[float]] = None,
        disk_id: Optional[int] = None,
    ) -> Chunk:
        with self.lock:
            new_id = (
                disk_id if disk_id is not None else self.id_generator.get_new_chunk_id()
            )
            new_chunk = Chunk(
                id=new_id,
                text=text,
                document_id=document_id,
                library_id=self._get_lib_id_from_document(document_id),
                embedding=embedding,
            )
            self.chunks[new_id] = new_chunk
            if disk_id is not None:
                self.id_generator.set_chunk_id(disk_id)
            if not self._replay_mode:
                self._persist(
                    "create_chunk",
                    {
                        "id": new_id,
                        "text": text,
                        "document_id": document_id,
                        "library_id": self._get_lib_id_from_document(document_id),
                        "embedding": embedding,
                    },
                )
            return new_chunk

    def update(
        self,
        chunk_id: int,
        text: Optional[str],
        document_id: Optional[int],
        embedding: Optional[List[float]],
    ) -> Optional[Chunk]:
        with self.lock:
            chunk = self.get(chunk_id)
            if not chunk:
                return None
            if text is not None:
                chunk.text = text
            if document_id is not None:
                chunk.document_id = document_id
            if embedding is not None:
                chunk.embedding = embedding
            if not self._replay_mode:
                self._persist(
                    "update_chunk",
                    {
                        "id": chunk_id,
                        "text": text,
                        "document_id": document_id,
                        "embedding": embedding,
                    },
                )
            return chunk

    def delete(self, chunk_id: int) -> bool:
        with self.lock:
            if chunk_id not in self.chunks:
                return False
            del self.chunks[chunk_id]
            if not self._replay_mode:
                self._persist("delete_chunk", {"id": chunk_id})
            return True

    def get_replay_handlers(self) -> Dict[str, ReplayHandler]:
        return {
            "create_chunk": lambda _action, data: self.create(
                data["text"],
                data["document_id"],
                embedding=data.get("embedding"),
                disk_id=data["id"],
            ),
            "update_chunk": lambda _action, data: self.update(
                data["id"],
                data.get("text"),
                data.get("document_id"),
                data.get("embedding"),
            ),
            "delete_chunk": lambda _action, data: self.delete(data["id"]),
        }
