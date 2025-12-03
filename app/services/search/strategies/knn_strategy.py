from typing import List, Dict, Any
from app.interfaces.services.search_service import ISearchStrategy
from app.interfaces.repositories.chunk_repository import IChunkRepository
from app.interfaces.services.embedding_service import IEmbeddingService
from app.core.math_utils import cosine_similarity

class KnnSearchStrategy(ISearchStrategy):
    def __init__(self, chunk_repository: IChunkRepository, embedding_service: IEmbeddingService):
        self._chunk_repository = chunk_repository
        self._embedding_service = embedding_service

    def _calculate_similarity(self, query_embedding: List[float], chunk_embedding: List[float]) -> float:
        return cosine_similarity(query_embedding, chunk_embedding)

    def search(self, library_id: int, query: str, k: int) -> List[Dict[str, Any]]:
        query_embedding = self._embedding_service.generate_embeddings([query], input_type="search_query")
        if not query_embedding:
            return []
        query_embedding = query_embedding[0]
        chunks = self._chunk_repository.get_by_library(library_id)
        results = []
        for chunk in chunks:
            if chunk.embedding is None:
                continue
            score = self._calculate_similarity(query_embedding, chunk.embedding)
            results.append({"chunk": chunk, "score": score})
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:k]