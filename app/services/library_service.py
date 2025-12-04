from typing import List
from app.interfaces.services.library_service import ILibraryService
from app.interfaces.repositories.library_repository import ILibraryRepository
from app.interfaces.repositories.document_repository import IDocumentRepository
from app.core.exceptions import EntityNotFoundError
from app.core.decorators import library_exists
from app.db.models import Library
from app.schemas.library import LibraryCreate, LibraryUpdate, LibraryDetail
from app.schemas.document import DocumentResponse


class LibraryService(ILibraryService):
    def __init__(
        self,
        library_repository: ILibraryRepository,
        document_repository: IDocumentRepository,
    ):
        self._library_repository = library_repository
        self._document_repository = document_repository

    @library_exists
    def get_library(self, library_id: int) -> Library:
        return self._library_repository.get(library_id)

    def get_library_with_details(self, library_id: int) -> LibraryDetail:
        library = self.get_library(library_id)
        documents = self._document_repository.get_by_library(library_id)
        document_responses = [
            DocumentResponse(
                id=doc.id,
                name=doc.name,
                library_id=doc.library_id,
            )
            for doc in documents
        ]
        return LibraryDetail(
            id=library.id,
            name=library.name,
            documents=document_responses,
        )

    def get_all_libraries(self) -> List[Library]:
        return self._library_repository.get_all()

    def create_library(self, library: LibraryCreate) -> Library:
        return self._library_repository.create(library.name)

    @library_exists
    def update_library(self, library_id: int, library: LibraryUpdate) -> Library:
        updated = self._library_repository.update(library_id, library.name)
        if not updated:
            raise EntityNotFoundError.library(library_id)
        return updated

    @library_exists
    def delete_library(self, library_id: int) -> None:
        self._library_repository.delete(library_id)
