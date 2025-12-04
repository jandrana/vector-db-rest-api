from abc import ABC, abstractmethod
from typing import List
from app.db.models import Chunk
from app.schemas.chunk import ChunkCreate, ChunkUpdate


class IChunkReader(ABC):
    @abstractmethod
    def get_chunk(self, chunk_id: int) -> Chunk:
        pass

    @abstractmethod
    def get_chunks_by_document(self, document_id: int) -> List[Chunk]:
        pass

    @abstractmethod
    def get_chunks_by_library(self, library_id: int) -> List[Chunk]:
        pass

    @abstractmethod
    def get_all_chunks(self) -> List[Chunk]:
        pass


class IChunkWriter(ABC):
    @abstractmethod
    def create_chunk(self, chunk: ChunkCreate) -> Chunk:
        pass

    @abstractmethod
    def update_chunk(self, chunk_id: int, chunk: ChunkUpdate) -> Chunk:
        pass

    @abstractmethod
    def delete_chunk(self, chunk_id: int) -> None:
        pass


class IChunkService(IChunkReader, IChunkWriter):
    pass
