import threading
from typing import Dict, List, Optional, Any, Tuple
from app.db.models import Library, Document, Chunk
from app.schemas.library import LibraryCreate, LibraryUpdate
from app.schemas.document import DocumentCreate, DocumentUpdate
from app.schemas.chunk import ChunkCreate, ChunkUpdate
from app.db.inverted_index import InvertedIndex
from app.db.persistence import Persistence

DB_FILE = "vector_db.jsonl"


class Database:
    def __init__(self):
        self.libraries: Dict[int, Library] = {}
        self.documents: Dict[int, Document] = {}
        self.chunks: Dict[int, Chunk] = {}

        self.inverted_index = InvertedIndex()
        self.persistence = Persistence()
        self.lock = threading.RLock()

        self.lib_num = 0
        self.doc_num = 0
        self.chunk_num = 0

        self.is_loading = False
        self._load_db()

    def _load_db(self):
        self.is_loading = True
        actions = {
            "create_library": lambda data: self.create_library(
                LibraryCreate(**data), disk_id=data["id"]
            ),
            "update_library": lambda data: self.update_library(
                data["id"], LibraryUpdate(**data)
            ),
            "create_document": lambda data: self.create_document(
                DocumentCreate(**data), disk_id=data["id"]
            ),
            "update_document": lambda data: self.update_document(
                data["id"], DocumentUpdate(**data)
            ),
            "create_chunk": lambda data: self.create_chunk(
                ChunkCreate(**data), disk_id=data["id"]
            ),
            "update_chunk": lambda data: self.update_chunk(
                data["id"], ChunkUpdate(**data)
            ),
            "delete_library": lambda data: self.delete_library(data["id"]),
            "delete_document": lambda data: self.delete_document(data["id"]),
            "delete_chunk": lambda data: self.delete_chunk(data["id"]),
        }
        try:
            for action, data in self.persistence.load_actions():
                handler = actions.get(action)
                if handler:
                    handler(data)
            print(f"Database loaded successfully with {len(self.chunks)} chunks")
        except Exception as e:
            print(f"Error loading database: {e}")
        finally:
            self.is_loading = False

    def _persist(self, action: str, data: Dict[str, Any]):
        if not self.is_loading:
            self.persistence.save_action(action, data)

    # --- LIBRARY ---
    def create_library(self, library: LibraryCreate, disk_id: int = None) -> Library:
        with self.lock:
            lib_id = disk_id if disk_id is not None else self.lib_num
            new_library = Library(id=lib_id, name=library.name)
            self.libraries[lib_id] = new_library
            if lib_id >= self.lib_num:
                self.lib_num = lib_id + 1
            data = library.model_dump()
            data["id"] = lib_id
            self._persist("create_library", data)
            return new_library

    def update_library(self, lib_id: int, library: LibraryUpdate) -> Optional[Library]:
        with self.lock:
            updated_lib = self.get_library(lib_id)
            if not updated_lib:
                return None
            if library.name is not None:
                updated_lib.name = library.name
                data = library.model_dump()
                data["id"] = lib_id
                self._persist("update_library", data)
            return updated_lib

    def get_library(self, lib_id: int) -> Library:
        with self.lock:
            return self.libraries.get(lib_id)

    def delete_library(self, lib_id: int):
        with self.lock:
            if lib_id not in self.libraries:
                return 0
            docs = self.get_documents_by_library(lib_id)
            for doc in docs:
                self.delete_document(doc.id)

            del self.libraries[lib_id]
            self._persist("delete_library", {"id": lib_id})
            return 1

    # --- DOCUMENT ---
    def create_document(
        self, document: DocumentCreate, disk_id: int = None
    ) -> Document:
        with self.lock:
            doc_id = disk_id if disk_id is not None else self.doc_num
            new_document = Document(
                id=doc_id, name=document.name, library_id=document.library_id
            )
            self.documents[doc_id] = new_document
            if doc_id >= self.doc_num:
                self.doc_num = doc_id + 1

            data = document.model_dump()
            data["id"] = doc_id
            self._persist("create_document", data)
            return new_document

    def update_document(
        self, doc_id: int, document: DocumentUpdate
    ) -> Optional[Document]:
        with self.lock:
            updated_doc = self.get_document(doc_id)
            if not updated_doc:
                return None
            if document.name is not None:
                updated_doc.name = document.name
                data = document.model_dump()
                data["id"] = doc_id
                self._persist("update_document", data)
            return updated_doc

    def get_document(self, doc_id: int) -> Document:
        with self.lock:
            return self.documents.get(doc_id)

    def get_documents_by_library(self, lib_id: int) -> List[Document]:
        with self.lock:
            return [doc for doc in self.documents.values() if doc.library_id == lib_id]

    def delete_document(self, doc_id: int):
        with self.lock:
            if doc_id not in self.documents:
                return 0
            chunks = self.get_chunks_by_document(doc_id)
            for chunk in chunks:
                self.delete_chunk(chunk.id)
            del self.documents[doc_id]
            self._persist("delete_document", {"id": doc_id})
            return 1

    # --- CHUNK ---
    def create_chunk(self, chunk: ChunkCreate, disk_id: int = None) -> Chunk:
        with self.lock:
            if not self.is_loading:
                chunk_doc = self.get_document(chunk.document_id)
                if not chunk_doc:
                    raise ValueError(f"Document with id {chunk.document_id} not found")
                lib_id = chunk_doc.library_id
            else:
                chunk_doc = self.documents.get(chunk.document_id)
                if chunk_doc:
                    lib_id = chunk_doc.library_id
            chunk_id = disk_id if disk_id is not None else self.chunk_num

            new_chunk = Chunk(
                id=chunk_id,
                text=chunk.text,
                document_id=chunk.document_id,
                library_id=lib_id,
                embedding=chunk.embedding,
            )
            self.chunks[chunk_id] = new_chunk
            if chunk_id >= self.chunk_num:
                self.chunk_num = chunk_id + 1
            self.inverted_index.index_chunk(chunk_id, new_chunk.text)
            data = chunk.model_dump()
            data["id"] = chunk_id
            self._persist("create_chunk", data)
            return new_chunk

    def update_chunk(self, chunk_id: int, chunk: ChunkUpdate) -> Optional[Chunk]:
        with self.lock:
            updated_chunk = self.get_chunk(chunk_id)
            if not updated_chunk:
                return None
            data = chunk.model_dump()
            data["id"] = chunk_id
            changed = False
            if chunk.text is not None:
                old_text = updated_chunk.text
                updated_chunk.text = chunk.text
                data["text"] = chunk.text
                self.inverted_index.remove_chunk(chunk_id, old_text)
                self.inverted_index.index_chunk(chunk_id, updated_chunk.text)
                changed = True
            if chunk.embedding is not None:
                updated_chunk.embedding = chunk.embedding
                data["embedding"] = chunk.embedding
                changed = True
            if changed:
                self._persist("update_chunk", data)
            return updated_chunk

    def get_chunk(self, chunk_id: int) -> Chunk:
        with self.lock:
            return self.chunks.get(chunk_id)

    def get_chunks_by_document(self, doc_id: int) -> List[Chunk]:
        with self.lock:
            return [
                chunk for chunk in self.chunks.values() if chunk.document_id == doc_id
            ]

    def get_chunks_by_library(self, lib_id: int) -> List[Chunk]:
        with self.lock:
            return [
                chunk for chunk in self.chunks.values() if chunk.library_id == lib_id
            ]

    def delete_chunk(self, chunk_id: int):
        with self.lock:
            if chunk_id not in self.chunks:
                return 0
            self.inverted_index.remove_chunk(chunk_id, self.chunks[chunk_id].text)
            del self.chunks[chunk_id]
            self._persist("delete_chunk", {"id": chunk_id})
            return 1

    # --- SEARCH ---
    def search_word(self, query: str) -> List[Tuple[Chunk, int]]:
        with self.lock:
            scores = self.inverted_index.search_word(query)

            results = []
            for chunk_id, score in scores.items():
                chunk = self.chunks[chunk_id]
                results.append((chunk, score))

            results.sort(key=lambda x: x[1], reverse=True)
            return results


db = Database()
