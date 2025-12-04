from abc import ABC, abstractmethod
from typing import Dict, Any


class IIndexService(ABC):
    @abstractmethod
    def index_library(self, library_id: int) -> Dict[str, Any]:
        pass
