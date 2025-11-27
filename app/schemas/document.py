from pydantic import BaseModel, Field
from typing import List, Optional
from app.schemas.chunk import ChunkBase


class DocumentBase(BaseModel):
    name: str = Field(..., description="Name of the document")
    library_id: int = Field(..., description="Library ID")


class DocumentCreate(DocumentBase):
    pass


class DocumentUpdate(DocumentBase):
    name: Optional[str] = Field(None, description="New document name")


class DocumentResponse(DocumentBase):
    id: int


class DocumentDetail(DocumentBase):
    chunks: List[ChunkBase] = Field(..., description="List of chunks in the document")
