import threading
from typing import List, Tuple, Optional
from app.db.models import Chunk
from app.interfaces.repositories.search_repository import ISearchRepository
from app.interfaces.repositories.chunk_repository import IChunkRepository
from app.interfaces.indexing import IInvertedIndex


class SearchRepository(ISearchRepository):
    def __init__(
        self,
        chunk_repository: IChunkRepository,
        inverted_index: IInvertedIndex,
        lock: threading.RLock,
    ):
        self.chunk_repository = chunk_repository
        self.inverted_index = inverted_index
        self.lock = lock

    def search_word(
        self, query: str, library_id: Optional[int] = None
    ) -> List[Tuple[Chunk, int]]:
        with self.lock:
            scores = self.inverted_index.search_word(query)
            results = []
            for chunk_id, score in scores.items():
                chunk = self.chunk_repository.get(chunk_id)
                if library_id is not None and chunk.library_id != library_id:
                    continue
                results.append((chunk, score))
            results.sort(key=lambda x: x[1], reverse=True)
            return results
