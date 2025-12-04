from app.schemas.library import LibraryCreate
from app.schemas.document import DocumentCreate
from app.schemas.chunk import ChunkCreate


def test_index_library_assigns_embeddings(test_container):
    """Test that indexing a library assigns embeddings to chunks."""
    library_service = test_container.services.library_service()
    document_service = test_container.services.document_service()
    chunk_service = test_container.services.chunk_service()
    index_service = test_container.services.index_service()

    lib = library_service.create_library(LibraryCreate(name="lib1"))
    doc = document_service.create_document(
        DocumentCreate(name="doc1", library_id=lib.id)
    )
    c1 = chunk_service.create_chunk(
        ChunkCreate(text="a", document_id=doc.id, embedding=None)
    )
    c2 = chunk_service.create_chunk(
        ChunkCreate(text="b", document_id=doc.id, embedding=None)
    )

    res = index_service.index_library(lib.id)
    assert res["status"] == "success"

    chunks = chunk_service.get_chunks_by_library(lib.id)
    assert all(chunk.embedding is not None for chunk in chunks)
