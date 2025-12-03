from typing import Dict, Set
from app.interfaces.indexing import IInvertedIndex, ITokenizationStrategy


class InvertedIndex(IInvertedIndex):
    def __init__(self, tokenization_strategy: ITokenizationStrategy):
        self._tokenization_strategy = tokenization_strategy
        self.index: Dict[str, Set[int]] = {}

    def _tokenize(self, text: str) -> Set[str]:
        return self._tokenization_strategy.tokenize(text)

    def index_chunk(self, chunk_id: int, text: str) -> None:
        words = self._tokenize(text)
        for word in words:
            if word not in self.index:
                self.index[word] = set()
            self.index[word].add(chunk_id)

    def remove_chunk(self, chunk_id: int, text: str) -> None:
        words = self._tokenize(text)
        for word in words:
            if word in self.index:
                self.index[word].discard(chunk_id)
                if not self.index[word]:
                    del self.index[word]

    def search_word(self, query: str) -> Dict[int, int]:
        query_words = self._tokenize(query)
        if not query_words:
            return {}

        scores: Dict[int, int] = {}
        for word in query_words:
            if word in self.index:
                for chunk_id in self.index[word]:
                    scores[chunk_id] = scores.get(chunk_id, 0) + 1
        return scores
