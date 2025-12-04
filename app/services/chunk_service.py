from typing import List
from app.interfaces.services.chunk_service import IChunkService
from app.interfaces.repositories.chunk_repository import IChunkRepository
from app.interfaces.repositories.document_repository import IDocumentRepository
from app.interfaces.repositories.library_repository import ILibraryRepository
from app.core.exceptions import EntityNotFoundError
from app.db.models import Chunk
from app.schemas.chunk import ChunkCreate, ChunkUpdate


class ChunkService(IChunkService):
    def __init__(
        self,
        chunk_repository: IChunkRepository,
        document_repository: IDocumentRepository,
        library_repository: ILibraryRepository,
    ):
        self._chunk_repository = chunk_repository
        self._document_repository = document_repository
        self._library_repository = library_repository

    def _validate_chunk_exists(self, chunk_id: int) -> None:
        if not self._chunk_repository.get(chunk_id):
            raise EntityNotFoundError.chunk(chunk_id)

    def _validate_document_exists(self, document_id: int) -> None:
        if not self._document_repository.get(document_id):
            raise EntityNotFoundError.document(document_id)

    def _validate_library_exists(self, library_id: int) -> None:
        if not self._library_repository.get(library_id):
            raise EntityNotFoundError.library(library_id)

    def get_chunk(self, chunk_id: int) -> Chunk:
        self._validate_chunk_exists(chunk_id)
        return self._chunk_repository.get(chunk_id)

    def get_chunks_by_document(self, document_id: int) -> List[Chunk]:
        self._validate_document_exists(document_id)
        return self._chunk_repository.get_by_document(document_id)

    def get_chunks_by_library(self, library_id: int) -> List[Chunk]:
        self._validate_library_exists(library_id)
        return self._chunk_repository.get_by_library(library_id)

    def get_all_chunks(self) -> List[Chunk]:
        return self._chunk_repository.get_all()

    def create_chunk(self, chunk: ChunkCreate) -> Chunk:
        self._validate_document_exists(chunk.document_id)
        return self._chunk_repository.create(
            chunk.text, chunk.document_id, chunk.embedding
        )

    def update_chunk(self, chunk_id: int, chunk: ChunkUpdate) -> Chunk:
        self._validate_chunk_exists(chunk_id)
        if chunk.document_id is not None:
            self._validate_document_exists(chunk.document_id)
        updated = self._chunk_repository.update(
            chunk_id, chunk.text, chunk.document_id, chunk.embedding
        )
        if not updated:
            raise EntityNotFoundError.chunk(chunk_id)
        return updated

    def delete_chunk(self, chunk_id: int) -> None:
        self._validate_chunk_exists(chunk_id)
        self._chunk_repository.delete(chunk_id)
