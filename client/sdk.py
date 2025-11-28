import requests
from typing import List, Dict, Any, Optional, Literal


class Client:
    def __init__(self):
        self.base_url = "http://localhost:8000"
        self.session = requests.Session()

    def _request(self, method: str, endpoint: str, **kwargs):
        url = f"{self.base_url}{endpoint}"
        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return None

    def get_all_libraries(self) -> List[Dict[str, Any]]:
        return self._request("GET", "/libraries")

    def create_library(self, name: str) -> Dict[str, Any]:
        return self._request("POST", "/libraries", json={"name": name})

    def get_library(self, library_id: int) -> Dict[str, Any]:
        return self._request("GET", f"/libraries/{library_id}")

    def update_library(self, library_id: int, name: str) -> Dict[str, Any]:
        return self._request("PATCH", f"/libraries/{library_id}", json={"name": name})

    def create_document(self, library_id: int, name: str) -> Dict[str, Any]:
        data = {"name": name, "library_id": library_id}
        return self._request("POST", "/documents", json=data)

    def get_document(self, document_id: int) -> Dict[str, Any]:
        return self._request("GET", f"/documents/{document_id}")

    def update_document(self, document_id: int, name: str) -> Dict[str, Any]:
        return self._request("PATCH", f"/documents/{document_id}", json={"name": name})

    def create_chunk(self, document_id: int, text: str) -> Dict[str, Any]:
        return self._request(
            "POST", "/chunks", json={"text": text, "document_id": document_id}
        )

    def get_chunk(self, chunk_id: int) -> Dict[str, Any]:
        return self._request("GET", f"/chunks/{chunk_id}")

    def update_chunk(
        self,
        chunk_id: int,
        text: Optional[str] = None,
        embedding: Optional[List[float]] = None,
    ) -> Dict[str, Any]:
        data = {}
        if text is not None:
            data["text"] = text
        if embedding is not None:
            data["embedding"] = embedding
        if not data:
            return None
        return self._request("PATCH", f"/chunks/{chunk_id}", json=data)

    def index_library(self, library_id: int) -> Dict[str, Any]:
        return self._request("POST", f"/libraries/{library_id}/index")

    def search_library(
        self,
        library_id: int,
        query: str,
        k: int = 10,
        search_type: Literal["knn", "keyword"] = "knn",
    ) -> List[Dict[str, Any]]:
        data = {"query": query, "k": k, "search_type": search_type}
        return self._request("POST", f"/libraries/{library_id}/search", json=data)
