from abc import ABC, abstractmethod
from typing import Dict, Set


class IInvertedIndex(ABC):
    @abstractmethod
    def index_chunk(self, chunk_id: int, text: str) -> None:
        pass

    @abstractmethod
    def remove_chunk(self, chunk_id: int, text: str) -> None:
        pass

    @abstractmethod
    def search_word(self, query: str) -> Dict[int, int]:
        pass


class ITokenizationStrategy(ABC):
    @abstractmethod
    def tokenize(self, text: str) -> Set[str]:
        pass
