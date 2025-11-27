from pydantic import BaseModel, Field
from typing import List, Optional


class ChunkBase(BaseModel):
    text: str = Field(..., description="Text of the chunk")
    document_id: int = Field(..., description="Document ID")


class ChunkCreate(ChunkBase):
    embedding: Optional[List[float]] = Field(None, description="Embedding of the chunk")


class ChunkUpdate(ChunkBase):
    text: Optional[str] = Field(None, description="New text of the chunk")
    document_id: Optional[int] = Field(None, description="New document ID")
    embedding: Optional[List[float]] = Field(
        None, description="New embedding of the chunk"
    )


class ChunkResponse(ChunkBase):
    id: int


class ChunkDetail(ChunkBase):
    id: int
    library_id: int
    embedding: Optional[List[float]] = Field(None, description="Embedding of the chunk")
