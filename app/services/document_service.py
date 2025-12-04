from typing import List
from app.interfaces.services.document_service import IDocumentService
from app.interfaces.repositories.document_repository import IDocumentRepository
from app.interfaces.repositories.chunk_repository import IChunkRepository
from app.interfaces.repositories.library_repository import ILibraryRepository
from app.core.exceptions import EntityNotFoundError
from app.core.decorators import document_exists, library_exists
from app.db.models import Document
from app.schemas.document import DocumentCreate, DocumentUpdate, DocumentDetail
from app.schemas.chunk import ChunkResponse


class DocumentService(IDocumentService):
    def __init__(
        self,
        document_repository: IDocumentRepository,
        library_repository: ILibraryRepository,
        chunk_repository: IChunkRepository,
    ):
        self._document_repository = document_repository
        self._library_repository = library_repository
        self._chunk_repository = chunk_repository

    @document_exists
    def get_document(self, document_id: int) -> Document:
        return self._document_repository.get(document_id)

    @library_exists
    def get_documents_by_library(self, library_id: int) -> List[Document]:
        return self._document_repository.get_by_library(library_id)

    def get_all_documents(self) -> List[Document]:
        return self._document_repository.get_all()

    def get_document_with_details(self, document_id: int) -> DocumentDetail:
        document = self.get_document(document_id)
        chunks = self._chunk_repository.get_by_document(document_id)
        chunk_responses = [
            ChunkResponse(
                id=chunk.id,
                text=chunk.text,
                document_id=chunk.document_id,
            )
            for chunk in chunks
        ]
        return DocumentDetail(
            id=document.id,
            name=document.name,
            library_id=document.library_id,
            chunks=chunk_responses,
        )

    @library_exists
    def create_document(self, document: DocumentCreate) -> Document:
        return self._document_repository.create(document.name, document.library_id)

    @document_exists
    def update_document(self, document_id: int, document: DocumentUpdate) -> Document:
        updated = self._document_repository.update(document_id, document.name)
        if not updated:
            raise EntityNotFoundError.document(document_id)
        return updated

    @document_exists
    def delete_document(self, document_id: int) -> None:
        self._document_repository.delete(document_id)
