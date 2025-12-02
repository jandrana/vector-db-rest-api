from app.schemas.library import LibraryCreate
from app.schemas.document import DocumentCreate
from app.schemas.chunk import ChunkCreate, ChunkUpdate


def test_create_library_document_chunk_and_search(test_db):
    db = test_db

    lib = db.create_library(LibraryCreate(name="Lib1"))
    assert lib.id == 0

    doc = db.create_document(DocumentCreate(name="Doc1", library_id=lib.id))
    assert doc.id == 0

    chunk = db.create_chunk(ChunkCreate(text="Hello world", document_id=doc.id, embedding=None))
    assert chunk.id == 0

    chunk2 = db.create_chunk(ChunkCreate(text="Another chunk", document_id=doc.id, embedding=None))
    assert chunk2.id == 1

    # search by keyword
    results = db.search_word("chunk")
    assert len(results) == 1 and results[0][0].id == chunk2.id

    # update chunk text and ensure index updates
    db.update_chunk(chunk.id, ChunkUpdate(text="Goodbye world", embedding=None))
    res2 = db.search_word("hello")
    assert res2 == []
