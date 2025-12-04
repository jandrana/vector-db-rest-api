from typing import Dict, Any
from app.interfaces.services.index_service import IIndexService
from app.interfaces.repositories.chunk_repository import IChunkRepository
from app.interfaces.services.embedding_service import IEmbeddingService
from app.interfaces.repositories.library_repository import ILibraryRepository
from app.core.exceptions import EntityNotFoundError


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

    def _validate_library_exists(self, library_id: int) -> None:
        if not self._library_repository.get(library_id):
            raise EntityNotFoundError.library(library_id)

    def index_library(self, library_id: int) -> Dict[str, Any]:
        self._validate_library_exists(library_id)
        lib_chunks = self._chunk_repository.get_by_library(library_id)
        to_embed = [chunk for chunk in lib_chunks if chunk.embedding is None]
        if not to_embed:
            return {
                "status": "skipped",
                "message": "No chunks to embed",
                "chunks_indexed": 0,
            }
        text_chunks = [chunk.text for chunk in to_embed]
        embeddings = self._embedding_service.generate_embeddings(text_chunks)
        for i, vector in enumerate(embeddings):
            to_embed[i].embedding = vector
        return {
            "status": "success",
            "message": f"Successfully indexed {len(to_embed)} chunks",
            "chunks_indexed": len(to_embed),
        }
