from abc import ABC, abstractmethod
from typing import List, Optional
from app.db.models import Document


class IDocumentRepository(ABC):
    @abstractmethod
    def get(self, document_id: int) -> Optional[Document]:
        pass

    @abstractmethod
    def get_by_library(self, library_id: int) -> List[Document]:
        pass

    @abstractmethod
    def get_all(self) -> List[Document]:
        pass

    @abstractmethod
    def create(
        self, name: str, library_id: int, disk_id: Optional[int] = None
    ) -> Document:
        pass

    @abstractmethod
    def update(self, document_id: int, name: Optional[str]) -> Optional[Document]:
        pass

    @abstractmethod
    def delete(self, document_id: int) -> bool:
        pass
