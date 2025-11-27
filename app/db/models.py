from pydantic import BaseModel
from typing import Optional, List


class Library(BaseModel):
    id: int
    name: str


class Document(BaseModel):
    id: int
    name: str
    library_id: int


class Chunk(BaseModel):
    id: int
    text: str
    document_id: int
    library_id: int
    embedding: Optional[List[float]] = None
