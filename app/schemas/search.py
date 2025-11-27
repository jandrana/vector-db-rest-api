from pydantic import BaseModel, Field
from app.schemas.chunk import ChunkResponse


class SearchResult(BaseModel):
    score: float = Field(..., description="Similarity score")
    chunk: ChunkResponse


class SearchRequest(BaseModel):
    query: str = Field(..., description="Query text")
    k: int = Field(default=3, gt=0, description="Number of results")
