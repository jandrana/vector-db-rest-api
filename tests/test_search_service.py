from app.services import search_service
from app.schemas.library import LibraryCreate
from app.schemas.document import DocumentCreate
from app.schemas.chunk import ChunkCreate


def test_search_keyword_and_knn(monkeypatch, test_db):
    # create data
    lib = test_db.create_library(LibraryCreate(name="lib1"))
    doc = test_db.create_document(DocumentCreate(name="doc1", library_id=lib.id))
    c1 = test_db.create_chunk(ChunkCreate(text="apple banana", document_id=doc.id, embedding=[1.0, 0.0]))
    test_db.create_chunk(ChunkCreate(text="banana cherry", document_id=doc.id, embedding=[0.0, 1.0]))

    # keyword search
    kres = search_service.search_keyword(test_db, "apple", k=2)
    assert len(kres) == 1

    # knn search: mock generate_embeddings for the query to [1,0]
    monkeypatch.setattr(search_service, "generate_embeddings", lambda texts, input_type="search_query": [[1.0, 0.0]])
    knn = search_service.knn_search(test_db, lib.id, "some query", k=2)
    # first result should be c1 (results are list of dicts with keys 'chunk' and 'score')
    assert knn[0]["chunk"].id == c1.id
