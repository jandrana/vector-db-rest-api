from app.schemas.library import LibraryCreate
from app.schemas.document import DocumentCreate
from app.schemas.chunk import ChunkCreate, ChunkUpdate


def test_create_library_document_chunk_and_search(test_container):
    """Test creating library, document, chunk and searching using services."""
    library_service = test_container.services.library_service()
    document_service = test_container.services.document_service()
    chunk_service = test_container.services.chunk_service()
    search_repository = test_container.db.search_repository()
    inverted_index = test_container.db.inverted_index()

    lib = library_service.create_library(LibraryCreate(name="Lib1"))
    assert lib.id == 0

    doc = document_service.create_document(
        DocumentCreate(name="Doc1", library_id=lib.id)
    )
    assert doc.id == 0

    chunk = chunk_service.create_chunk(
        ChunkCreate(text="Hello world", document_id=doc.id, embedding=None)
    )
    assert chunk.id == 0
    inverted_index.index_chunk(chunk.id, chunk.text)

    chunk2 = chunk_service.create_chunk(
        ChunkCreate(text="Another chunk", document_id=doc.id, embedding=None)
    )
    assert chunk2.id == 1
    inverted_index.index_chunk(chunk2.id, chunk2.text)

    results = search_repository.search_word("chunk", library_id=lib.id)
    assert len(results) == 1 and results[0][0].id == chunk2.id

    inverted_index.remove_chunk(chunk.id, "Hello world")
    chunk_service.update_chunk(
        chunk.id, ChunkUpdate(text="Goodbye world", embedding=None)
    )
    inverted_index.index_chunk(chunk.id, "Goodbye world")
    res2 = search_repository.search_word("hello", library_id=lib.id)
    assert res2 == []
