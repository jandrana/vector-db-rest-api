def test_full_api_flow(client):
    create_library = client.post("/libraries", json={"name": "lib1"})
    assert create_library.status_code == 201
    lib = create_library.json()

    create_document = client.post(
        "/documents", json={"name": "doc1", "library_id": lib["id"]}
    )
    assert create_document.status_code == 201
    doc = create_document.json()

    create_chunk = client.post(
        "/chunks", json={"text": "hello world", "document_id": doc["id"]}
    )
    assert create_chunk.status_code == 201

    index_lib = client.post(f"/libraries/{lib['id']}/index")
    assert index_lib.status_code == 200
    index_data = index_lib.json()
    assert index_data["status"] == "success"

    search_keyword = client.post(
        f"/libraries/{lib['id']}/search",
        json={"query": "hello", "k": 3, "search_type": "keyword"},
    )
    assert search_keyword.status_code == 200
    data = search_keyword.json()
    assert isinstance(data, list)

    knn_search = client.post(
        f"/libraries/{lib['id']}/search",
        json={"query": "hello", "k": 3, "search_type": "knn"},
    )
    assert knn_search.status_code == 200
    knn_data = knn_search.json()
    assert isinstance(knn_data, list)
