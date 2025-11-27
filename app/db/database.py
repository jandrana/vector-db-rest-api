import threading
from typing import Dict, List, Optional, Set, Tuple
import string
from app.db.models import Library, Document, Chunk
from app.schemas.library import LibraryCreate, LibraryUpdate
from app.schemas.document import DocumentCreate, DocumentUpdate
from app.schemas.chunk import ChunkCreate, ChunkUpdate


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

    def create_library(self, library: LibraryCreate) -> Library:
        with self.lock:
            new_library = Library(id=self.lib_num, name=library.name)
            self.libraries[self.lib_num] = new_library
            self.lib_num += 1
            return new_library

    def update_library(self, lib_id: int, library: LibraryUpdate) -> Optional[Library]:
        with self.lock:
            updated_lib = self.get_library(lib_id)
            if not updated_lib:
                return None
            if library.name is not None:
                updated_lib.name = library.name
            return updated_lib

    def get_library(self, lib_id: int) -> Library:
        with self.lock:
            return self.libraries.get(lib_id)

    def create_document(self, document: DocumentCreate) -> Document:
        with self.lock:
            new_document = Document(
                id=self.doc_num, name=document.name, library_id=document.library_id
            )
            self.documents[self.doc_num] = new_document
            self.doc_num += 1
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

    def create_chunk(self, chunk: ChunkCreate) -> Chunk:
        with self.lock:
            chunk_doc = self.get_document(chunk.document_id)
            if not chunk_doc:
                raise ValueError(f"Document with id {chunk.document_id} not found")

            new_chunk = Chunk(
                id=self.chunk_num,
                text=chunk.text,
                document_id=chunk.document_id,
                library_id=chunk_doc.library_id,
                embedding=chunk.embedding,
            )
            self.chunks[self.chunk_num] = new_chunk
            self.chunk_num += 1
            self._update_inverted_index(new_chunk)
            return new_chunk

    def update_chunk(self, chunk_id: int, chunk: ChunkUpdate) -> Optional[Chunk]:
        with self.lock:
            updated_chunk = self.get_chunk(chunk_id)
            if not updated_chunk:
                return None
            if chunk.text is not None:
                updated_chunk.text = chunk.text
            if chunk.embedding is not None:
                updated_chunk.embedding = chunk.embedding
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
