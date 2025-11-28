from fastapi import APIRouter, HTTPException, status, Depends

from app.schemas.chunk import ChunkCreate, ChunkUpdate, ChunkResponse, ChunkDetail
from app.api import deps
from app.db.database import Database

router = APIRouter()


@router.post("/", response_model=ChunkResponse, status_code=status.HTTP_201_CREATED)
def create_chunk(chunk: ChunkCreate, db: Database = Depends(deps.get_db)):
    if not db.get_document(chunk.document_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document with id {chunk.document_id} not found",
        )
    return db.create_chunk(chunk)


@router.get("/{chunk_id}", response_model=ChunkDetail, status_code=status.HTTP_200_OK)
def get_chunk(chunk_id: int, db: Database = Depends(deps.get_db)):
    chunk = db.get_chunk(chunk_id)
    if not chunk:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Chunk not found"
        )

    return chunk


@router.patch("/{chunk_id}", response_model=ChunkDetail, status_code=status.HTTP_200_OK)
def update_chunk(
    chunk_id: int, chunk: ChunkUpdate, db: Database = Depends(deps.get_db)
):
    updated_chunk = db.update_chunk(chunk_id, chunk)
    if not updated_chunk:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Chunk not found"
        )
    return updated_chunk
