from abc import ABC, abstractmethod
from typing import List, Tuple, Optional
from app.db.models import Chunk


class ISearchRepository(ABC):
    @abstractmethod
    def search_word(
        query: str, library_id: Optional[int] = None
    ) -> List[Tuple[Chunk, int]]:
        pass
