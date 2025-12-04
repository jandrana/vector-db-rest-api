from typing import List
from app.interfaces.services.library_service import ILibraryService
from app.interfaces.repositories.library_repository import ILibraryRepository
from app.interfaces.repositories.document_repository import IDocumentRepository
from app.core.exceptions import EntityNotFoundError
from app.db.models import Library
from app.schemas.library import LibraryCreate, LibraryUpdate


class LibraryService(ILibraryService):
    def __init__(
        self,
        library_repository: ILibraryRepository,
        document_repository: IDocumentRepository,
    ):
        self._library_repository = library_repository
        self._document_repository = document_repository

    def get_library(self, library_id: int) -> Library:
        library = self._library_repository.get(library_id)
        if not library:
            raise EntityNotFoundError.library(library_id)
        return library

    def get_all_libraries(self) -> List[Library]:
        return self._library_repository.get_all()

    def create_library(self, library: LibraryCreate) -> Library:
        return self._library_repository.create(library.name)

    def update_library(self, library_id: int, library: LibraryUpdate) -> Library:
        if not self._library_repository.get(library_id):
            raise EntityNotFoundError.library(library_id)
        updated = self._library_repository.update(library_id, library.name)
        if not updated:
            raise EntityNotFoundError.library(library_id)
        return updated

    def delete_library(self, library_id: int) -> None:
        if not self._library_repository.get(library_id):
            raise EntityNotFoundError.library(library_id)
        self._library_repository.delete(library_id)
