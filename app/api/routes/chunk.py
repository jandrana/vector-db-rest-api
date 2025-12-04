from fastapi import APIRouter, status, Depends
from typing import List
from app.schemas.chunk import ChunkCreate, ChunkUpdate, ChunkResponse, ChunkDetail
from app.api import deps
from app.interfaces.services.chunk_service import IChunkService

router = APIRouter()


@router.post(
    "/",
    response_model=ChunkResponse,
    status_code=status.HTTP_201_CREATED,
    description="Create a new chunk in a document",
)
def create_chunk(
    chunk: ChunkCreate, service: IChunkService = Depends(deps.get_chunk_service)
) -> ChunkResponse:
    created_chunk = service.create_chunk(chunk)
    return ChunkResponse.model_validate(created_chunk.model_dump())


@router.get(
    "/{chunk_id}",
    response_model=ChunkDetail,
    status_code=status.HTTP_200_OK,
    description="Get a chunk by ID with full details",
)
def get_chunk(
    chunk_id: int,
    service: IChunkService = Depends(deps.get_chunk_service),
) -> ChunkDetail:
    chunk = service.get_chunk(chunk_id)
    return ChunkDetail.model_validate(chunk.model_dump())


@router.get(
    "/",
    response_model=List[ChunkResponse],
    status_code=status.HTTP_200_OK,
    description="Get all chunks",
)
def get_all_chunks(service: IChunkService = Depends(deps.get_chunk_service)) -> List[ChunkResponse]:
    chunks = service.get_all_chunks()
    return [ChunkResponse.model_validate(chunk.model_dump()) for chunk in chunks]


@router.patch(
    "/{chunk_id}",
    response_model=ChunkDetail,
    status_code=status.HTTP_200_OK,
    description="Update a chunk by ID",
)
def update_chunk(
    chunk_id: int,
    chunk: ChunkUpdate,
    service: IChunkService = Depends(deps.get_chunk_service),
) -> ChunkDetail:
    updated_chunk = service.update_chunk(chunk_id, chunk)
    return ChunkDetail.model_validate(updated_chunk.model_dump())


@router.delete(
    "/{chunk_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Delete a chunk by ID",
)
def delete_chunk(
    chunk_id: int,
    service: IChunkService = Depends(deps.get_chunk_service),
) -> None:
    service.delete_chunk(chunk_id)
