from app.services import index_service
from app.schemas.library import LibraryCreate
from app.schemas.document import DocumentCreate
from app.schemas.chunk import ChunkCreate


def test_index_library_assigns_embeddings(test_db):
    # create library, document and chunks
    lib = test_db.create_library(LibraryCreate(name="lib1"))
    doc = test_db.create_document(DocumentCreate(name="doc1", library_id=lib.id))
    test_db.create_chunk(ChunkCreate(text="a", document_id=doc.id, embedding=None))
    test_db.create_chunk(ChunkCreate(text="b", document_id=doc.id, embedding=None))

    res = index_service.index_library(test_db, lib.id)
    assert res["status"] == "success"
    chunks = test_db.get_chunks_by_library(lib.id)
    assert all(chunk.embedding is not None for chunk in chunks)
