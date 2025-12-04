from typing import List, Dict, Any
from app.interfaces.services.search_service import ISearchService, ISearchStrategy
from app.core.exceptions import ValidationError
from app.schemas.search import SearchResult
from app.schemas.chunk import ChunkResponse


class SearchService(ISearchService):
    def __init__(self):
        self._strategies: Dict[str, ISearchStrategy] = {}

    def register_strategy(self, name: str, strategy: ISearchStrategy) -> None:
        self._strategies[name] = strategy

    def search(
        self, strategy: str, library_id: int, query: str, k: int
    ) -> List[SearchResult]:
        if strategy not in self._strategies:
            raise ValidationError(
                f"Strategy '{strategy}' not found. Available strategies: {list(self._strategies.keys())}"
            )
        raw_results = self._strategies[strategy].search(library_id, query, k)
        return [
            SearchResult(
                score=result["score"],
                chunk=ChunkResponse(
                    id=result["chunk"].id,
                    text=result["chunk"].text,
                    document_id=result["chunk"].document_id,
                ),
            )
            for result in raw_results
        ]
