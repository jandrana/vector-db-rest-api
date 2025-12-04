from app.schemas.library import LibraryCreate
from app.schemas.document import DocumentCreate
from app.schemas.chunk import ChunkCreate
from app.schemas.search import SearchResult


def test_search_keyword_and_knn(test_container):
    """Test keyword and KNN search using the search service."""
    library_service = test_container.library_service
    document_service = test_container.document_service
    chunk_service = test_container.chunk_service
    search_service = test_container.search_service
    inverted_index = test_container.inverted_index

    # Create data
    lib = library_service.create_library(LibraryCreate(name="lib1"))
    doc = document_service.create_document(
        DocumentCreate(name="doc1", library_id=lib.id)
    )
    c1 = chunk_service.create_chunk(
        ChunkCreate(text="apple banana", document_id=doc.id, embedding=[1.0, 0.0])
    )
    c2 = chunk_service.create_chunk(
        ChunkCreate(text="banana cherry", document_id=doc.id, embedding=[0.0, 1.0])
    )

    # Index chunks in the inverted index for keyword search
    inverted_index.index_chunk(c1.id, c1.text)
    inverted_index.index_chunk(c2.id, c2.text)

    # Keyword search
    kres = search_service.search("keyword", lib.id, "apple", k=2)
    assert len(kres) == 1
    assert isinstance(kres[0], SearchResult)
    assert kres[0].chunk is not None
    assert kres[0].score is not None

    # KNN search
    knn = search_service.search("knn", lib.id, "some query", k=2)
    assert len(knn) > 0
    assert isinstance(knn[0], SearchResult)
    assert knn[0].chunk is not None
    assert knn[0].score is not None
    assert knn[0].chunk.id == c1.id
