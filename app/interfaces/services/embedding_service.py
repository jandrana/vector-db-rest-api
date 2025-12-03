from typing import List
from abc import ABC, abstractmethod


class IEmbeddingService(ABC):
    @abstractmethod
    def generate_embeddings(
        self, texts: List[str], input_type: str = "search_document"
    ) -> List[List[float]]:
        pass


# Where to move this?
class IEmbeddingProvider(ABC):
    @abstractmethod
    def generate_embeddings(
        self, texts: List[str], input_type: str = "search_document"
    ) -> List[List[float]]:
        pass
