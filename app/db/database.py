import threading
import json
import os
import string
from typing import Dict, List, Optional, Set, Tuple
from app.db.models import Library, Document, Chunk
from app.schemas.library import LibraryCreate, LibraryUpdate
from app.schemas.document import DocumentCreate, DocumentUpdate
from app.schemas.chunk import ChunkCreate, ChunkUpdate


DB_FILE = "vector_db.jsonl"


class Database:
    def __init__(self):
        self.libraries: Dict[int, Library] = {}
        self.documents: Dict[int, Document] = {}
        self.chunks: Dict[int, Chunk] = {}

        self.lib_num = 0
        self.doc_num = 0
        self.chunk_num = 0

        self.inverted_index: Dict[str, Set[int]] = {}

        self.lock = threading.RLock()
        self.db_file = DB_FILE
        self.is_loading = False

        self._load_handler = {
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
        }

        self._load_db()

    def _save_action(self, action: str, data: Dict):
        if self.is_loading:
            return
        log = {"action": action, "data": data}
        with open(self.db_file, "a") as f:
            f.write(json.dumps(log) + "\n")

    def _load_db(self):
        if not os.path.exists(DB_FILE):
            return
        self.is_loading = True
        try:
            with open(DB_FILE, "r") as f:
                for line in f:
                    if not line.strip():
                        continue
                    try:
                        log = json.loads(line)
                        action = log["action"]
                        data = log["data"]
                        handler = self._load_handler.get(action)
                        if handler:
                            handler(data)
                        else:
                            print(f"Unknown action: {action}")
                    except Exception as e:
                        print(f"Skipping invalid log: {e}")
            print(
                f"Database loaded successfully from {DB_FILE} with {len(self.chunks)} chunks"
            )
        except Exception as e:
            print(f"Error loading database: {e}")
        finally:
            self.is_loading = False

    def create_library(self, library: LibraryCreate, disk_id: int = None) -> Library:
        with self.lock:
            lib_id = disk_id if disk_id is not None else self.lib_num
            new_library = Library(id=lib_id, name=library.name)
            self.libraries[lib_id] = new_library
            if lib_id >= self.lib_num:
                self.lib_num = lib_id + 1
            data = library.model_dump()
            data["id"] = lib_id
            self._save_action("create_library", data)
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
                self._save_action("update_library", data)
            return updated_lib

    def get_library(self, lib_id: int) -> Library:
        with self.lock:
            return self.libraries.get(lib_id)

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
            self._save_action("create_document", data)
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
                self._save_action("update_document", data)
            return updated_doc

    def get_document(self, doc_id: int) -> Document:
        with self.lock:
            return self.documents.get(doc_id)

    def get_documents_by_library(self, lib_id: int) -> List[Document]:
        with self.lock:
            return [doc for doc in self.documents.values() if doc.library_id == lib_id]

    def _tokenize(self, text: str) -> Set[str]:
        normalized_text = text.lower().translate(
            str.maketrans("", "", string.punctuation)
        )
        return set(normalized_text.split())

    def _update_inverted_index(self, chunk: Chunk):
        words = self._tokenize(chunk.text)
        for word in words:
            if word not in self.inverted_index:
                self.inverted_index[word] = set()
            self.inverted_index[word].add(chunk.id)

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
            self._update_inverted_index(new_chunk)
            data = chunk.model_dump()
            data["id"] = chunk_id
            self._save_action("create_chunk", data)
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
                updated_chunk.text = chunk.text
                data["text"] = chunk.text
                changed = True
            if chunk.embedding is not None:
                updated_chunk.embedding = chunk.embedding
                data["embedding"] = chunk.embedding
                changed = True
            if changed:
                self._save_action("update_chunk", data)
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

    def search_word(self, query: str) -> List[Tuple[Chunk, int]]:
        with self.lock:
            query_words = self._tokenize(query)
            if not query_words:
                return []

            scores: Dict[int, int] = {}

            for word in query_words:
                if word in self.inverted_index:
                    for chunk_id in self.inverted_index[word]:
                        scores[chunk_id] = scores.get(chunk_id, 0) + 1

            results = []

            for chunk_id, score in scores.items():
                chunk = self.chunks[chunk_id]
                results.append((chunk, score))

            results.sort(key=lambda x: x[1], reverse=True)

            return results


db = Database()
