from typing import List
from app.interfaces.services.chunk_service import IChunkService
from app.interfaces.repositories.chunk_repository import IChunkRepository
from app.interfaces.repositories.document_repository import IDocumentRepository
from app.interfaces.repositories.library_repository import ILibraryRepository
from app.interfaces.indexing import IInvertedIndex
from app.core.exceptions import EntityNotFoundError
from app.core.decorators import chunk_exists, document_exists, library_exists
from app.db.models import Chunk
from app.schemas.chunk import ChunkCreate, ChunkUpdate


class ChunkService(IChunkService):
    def __init__(
        self,
        chunk_repository: IChunkRepository,
        document_repository: IDocumentRepository,
        library_repository: ILibraryRepository,
        inverted_index: IInvertedIndex,
    ):
        self._chunk_repository = chunk_repository
        self._document_repository = document_repository
        self._library_repository = library_repository
        self._inverted_index = inverted_index

    @chunk_exists
    def get_chunk(self, chunk_id: int) -> Chunk:
        return self._chunk_repository.get(chunk_id)

    @document_exists
    def get_chunks_by_document(self, document_id: int) -> List[Chunk]:
        return self._chunk_repository.get_by_document(document_id)

    @library_exists
    def get_chunks_by_library(self, library_id: int) -> List[Chunk]:
        return self._chunk_repository.get_by_library(library_id)

    def get_all_chunks(self) -> List[Chunk]:
        return self._chunk_repository.get_all()

    @document_exists
    def create_chunk(self, chunk: ChunkCreate) -> Chunk:
        created_chunk = self._chunk_repository.create(
            chunk.text, chunk.document_id, chunk.embedding
        )
        self._inverted_index.index_chunk(created_chunk.id, created_chunk.text)
        return created_chunk

    @chunk_exists
    def update_chunk(self, chunk_id: int, chunk: ChunkUpdate) -> Chunk:
        if chunk.document_id is not None:
            if not self._document_repository.get(chunk.document_id):
                raise EntityNotFoundError.document(chunk.document_id)

        existing_chunk = self._chunk_repository.get(chunk_id)
        old_text = existing_chunk.text if existing_chunk else None

        updated = self._chunk_repository.update(
            chunk_id, chunk.text, chunk.document_id, chunk.embedding
        )
        if updated is None:
            raise EntityNotFoundError.chunk(chunk_id)

        if chunk.text is not None and old_text and chunk.text != old_text:
            self._inverted_index.remove_chunk(chunk_id, old_text)
            self._inverted_index.index_chunk(chunk_id, chunk.text)

        return updated

    @chunk_exists
    def delete_chunk(self, chunk_id: int) -> None:
        chunk = self._chunk_repository.get(chunk_id)
        if chunk:
            self._inverted_index.remove_chunk(chunk_id, chunk.text)
        self._chunk_repository.delete(chunk_id)
