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
):
    return service.create_chunk(chunk)


@router.get(
    "/{chunk_id}",
    response_model=ChunkDetail,
    status_code=status.HTTP_200_OK,
    description="Get a chunk by ID with full details",
)
def get_chunk(chunk_id: int, service: ChunkService = Depends(deps.get_chunk_service)):
    chunk = service.get_chunk(chunk_id)
    return ChunkDetail.model_validate(
        {
            **chunk.model_dump(),
        }
    )


@router.get(
    "/",
    response_model=List[ChunkResponse],
    status_code=status.HTTP_200_OK,
    description="Get all chunks",
)
def get_all_chunks(service: ChunkService = Depends(deps.get_chunk_service)):
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
):
    return service.update_chunk(chunk_id, chunk)


@router.delete(
    "/{chunk_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Delete a chunk by ID",
)
def delete_chunk(
    chunk_id: int, service: ChunkService = Depends(deps.get_chunk_service)
):
    service.delete_chunk(chunk_id)
