import string
from typing import Set
from app.interfaces.indexing import ITokenizationStrategy


class DefaultTokenizationStrategy(ITokenizationStrategy):
    def tokenize(self, text: str) -> Set[str]:
        normalized_text = text.lower().translate(
            str.maketrans("", "", string.punctuation)
        )
        return set(normalized_text.split())
