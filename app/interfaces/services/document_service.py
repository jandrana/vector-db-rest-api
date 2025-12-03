from abc import ABC, abstractmethod
from typing import List
from app.db.models import Document
from app.schemas.document import DocumentCreate, DocumentUpdate


class IDocumentReader(ABC):
    @abstractmethod
    def get_document(self, document_id: int) -> Document:
        pass

    @abstractmethod
    def get_documents_by_library(self, library_id: int) -> List[Document]:
        pass

    @abstractmethod
    def get_all_documents(self) -> List[Document]:
        pass


class IDocumentWriter(ABC):
    @abstractmethod
    def create_document(self, document: DocumentCreate) -> Document:
        pass

    @abstractmethod
    def update_document(self, document_id: int, document: DocumentUpdate) -> Document:
        pass

    @abstractmethod
    def delete_document(self, document_id: int) -> None:
        pass


class IDocumentService(IDocumentReader, IDocumentWriter):
    pass
