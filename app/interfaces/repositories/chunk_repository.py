from abc import ABC, abstractmethod
from typing import List, Optional
from app.db.models import Chunk


class IChunkRepository(ABC):
    @abstractmethod
    def get(self, chunk_id: int) -> Optional[Chunk]:
        pass

    @abstractmethod
    def get_by_document(self, document_id: int) -> List[Chunk]:
        pass

    @abstractmethod
    def get_by_library(self, library_id: int) -> List[Chunk]:
        pass

    @abstractmethod
    def get_all(self) -> List[Chunk]:
        pass

    @abstractmethod
    def create(
        self,
        text: str,
        document_id: int,
        embedding: Optional[List[float]] = None,
        disk_id: Optional[int] = None,
    ) -> Chunk:
        pass

    @abstractmethod
    def update(
        self,
        chunk_id: int,
        text: Optional[str],
        document_id: Optional[int],
        embedding: Optional[List[float]],
    ) -> Optional[Chunk]:
        pass

    @abstractmethod
    def delete(self, chunk_id: int) -> int:
        pass
