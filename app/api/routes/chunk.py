from fastapi import APIRouter, status, Depends
from typing import List
from app.schemas.chunk import ChunkCreate, ChunkUpdate, ChunkResponse, ChunkDetail
from app.api import deps
from app.services.chunk_service import ChunkService

router = APIRouter()


@router.post(
    "/",
    response_model=ChunkResponse,
    status_code=status.HTTP_201_CREATED,
    description="Create a new chunk in a document",
)
def create_chunk(
    chunk: ChunkCreate, service: ChunkService = Depends(deps.get_chunk_service)
) -> ChunkResponse:
    return service.create_chunk(chunk)


@router.get(
    "/{chunk_id}",
    response_model=ChunkDetail,
    status_code=status.HTTP_200_OK,
    description="Get a chunk by ID with full details",
)
def get_chunk(
    chunk_id: int,
    service: ChunkService = Depends(deps.get_chunk_service),
) -> ChunkDetail:
    chunk = service.get_chunk(chunk_id)
    return ChunkDetail(
        id=chunk.id,
        text=chunk.text,
        document_id=chunk.document_id,
        library_id=chunk.library_id,
        embedding=chunk.embedding,
    )


@router.get(
    "/",
    response_model=List[ChunkResponse],
    status_code=status.HTTP_200_OK,
    description="Get all chunks",
)
def get_all_chunks(service: ChunkService = Depends(deps.get_chunk_service)) -> List[ChunkResponse]:
    return service.get_all_chunks()


@router.patch(
    "/{chunk_id}",
    response_model=ChunkDetail,
    status_code=status.HTTP_200_OK,
    description="Update a chunk by ID",
)
def update_chunk(
    chunk_id: int,
    chunk: ChunkUpdate,
    service: ChunkService = Depends(deps.get_chunk_service),
) -> ChunkDetail:
    updated_chunk = service.update_chunk(chunk_id, chunk)
    return ChunkDetail(
        id=updated_chunk.id,
        text=updated_chunk.text,
        document_id=updated_chunk.document_id,
        library_id=updated_chunk.library_id,
        embedding=updated_chunk.embedding,
    )


@router.delete(
    "/{chunk_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Delete a chunk by ID",
)
def delete_chunk(
    chunk_id: int,
    service: ChunkService = Depends(deps.get_chunk_service),
) -> None:
    service.delete_chunk(chunk_id)
