from app.db.inverted_index import InvertedIndex
from app.db.tokenization import DefaultTokenizationStrategy


def test_index_and_search_single_word():
    tokenization_strategy = DefaultTokenizationStrategy()
    idx = InvertedIndex(tokenization_strategy=tokenization_strategy)
    idx.index_chunk(1, "Hello world")
    res = idx.search_word("hello")
    assert 1 in res and res[1] == 1


def test_index_and_search_multiple_chunks():
    tokenization_strategy = DefaultTokenizationStrategy()
    idx = InvertedIndex(tokenization_strategy=tokenization_strategy)
    idx.index_chunk(1, "apple banana")
    idx.index_chunk(2, "banana cherry")
    res = idx.search_word("banana")
    assert res[1] == 1 and res[2] == 1
    res2 = idx.search_word("apple banana")
    assert res2[1] == 2 and res2.get(2) == 1
