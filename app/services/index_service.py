from typing import Dict, Any, List
from app.interfaces.services.index_service import IIndexService
from app.interfaces.repositories.chunk_repository import IChunkRepository
from app.interfaces.services.embedding_service import IEmbeddingService
from app.interfaces.repositories.library_repository import ILibraryRepository
from app.core.decorators import library_exists
from app.db.models import Chunk


class IndexService(IIndexService):
    def __init__(
        self,
        chunk_repository: IChunkRepository,
        embedding_service: IEmbeddingService,
        library_repository: ILibraryRepository,
    ):
        self._chunk_repository = chunk_repository
        self._embedding_service = embedding_service
        self._library_repository = library_repository

    @library_exists
    def index_library(self, library_id: int) -> Dict[str, Any]:
        chunks_to_index = self._get_unindexed_chunks(library_id)
        if not chunks_to_index:
            return self._skip_response()

        embeddings = self._generate_embeddings(chunks_to_index)
        self._update_chunks_with_embeddings(chunks_to_index, embeddings)
        return self._success_response(len(chunks_to_index))

    def _get_unindexed_chunks(self, library_id: int) -> List[Chunk]:
        """Get all chunks in the library that don't have embeddings."""
        lib_chunks = self._chunk_repository.get_by_library(library_id)
        return [chunk for chunk in lib_chunks if chunk.embedding is None]

    def _generate_embeddings(self, chunks: List[Chunk]) -> List[List[float]]:
        """Generate embeddings for chunk texts."""
        text_chunks = [chunk.text for chunk in chunks]
        return self._embedding_service.generate_embeddings(text_chunks)

    def _update_chunks_with_embeddings(
        self, chunks: List[Chunk], embeddings: List[List[float]]
    ) -> None:
        """Update chunks with their generated embeddings."""
        for chunk, embedding in zip(chunks, embeddings):
            self._chunk_repository.update(
                chunk.id, text=None, document_id=None, embedding=embedding
            )

    def _skip_response(self) -> Dict[str, Any]:
        return {
            "status": "skipped",
            "message": "No chunks to embed",
            "chunks_indexed": 0,
        }

    def _success_response(self, chunks_indexed: int) -> Dict[str, Any]:
        return {
            "status": "success",
            "message": f"Successfully indexed {chunks_indexed} chunks",
            "chunks_indexed": chunks_indexed,
        }
