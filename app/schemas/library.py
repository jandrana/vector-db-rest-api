from pydantic import BaseModel, Field
from typing import List, Optional
from app.schemas.document import DocumentBase


class LibraryBase(BaseModel):
    name: str = Field(..., description="Library name")


class LibraryCreate(LibraryBase):
    pass


class LibraryUpdate(LibraryBase):
    name: Optional[str] = Field(None, description="New library name")


class LibraryResponse(LibraryBase):
    id: int


class LibraryDetail(LibraryBase):
    documents: List[DocumentBase] = Field(
        ..., description="List of documents in the library"
    )
