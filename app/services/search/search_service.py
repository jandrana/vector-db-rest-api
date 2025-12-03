from typing import List, Dict, Any
from app.interfaces.services.search_service import ISearchService, ISearchStrategy
from app.core.exceptions import ValidationError


class SearchService(ISearchService):
    def __init__(self):
        self._strategies: Dict[str, ISearchStrategy] = {}

    def register_strategy(self, name: str, strategy: ISearchStrategy) -> None:
        self._strategies[name] = strategy

    def search(
        self, strategy: str, library_id: int, query: str, k: int
    ) -> List[Dict[str, Any]]:
        if strategy not in self._strategies:
            raise ValidationError(
                f"Strategy '{strategy}' not found. Available strategies: {list(self._strategies.keys())}"
            )
        return self._strategies[strategy].search(library_id, query, k)
