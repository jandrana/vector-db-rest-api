from abc import ABC, abstractmethod
from typing import List, Dict, Any


class ISearchStrategy(ABC):
    @abstractmethod
    def search(self, library_id: int, query: str, k: int) -> List[Dict[str, Any]]:
        pass


class ISearchService(ABC):
    @abstractmethod
    def register_strategy(self, name: str, strategy: ISearchStrategy) -> None:
        pass

    @abstractmethod
    def search(
        self, strategy: str, library_id: int, query: str, k: int
    ) -> List[Dict[str, Any]]:
        pass
