from typing import List, Dict, Any
from app.interfaces.services.search_service import ISearchStrategy
from app.interfaces.repositories.search_repository import ISearchRepository

class KeywordSearchStrategy(ISearchStrategy):
    def __init__(self, search_repository: ISearchRepository):
        self._search_repository = search_repository

    def search(self, library_id: int, query: str, k: int) -> List[Dict[str, Any]]:
        results = self._search_repository.search_word(query, library_id)
        return [{"chunk": chunk, "score": float(score)} for chunk, score in results[:k]]