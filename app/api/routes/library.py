from fastapi import APIRouter, status, Depends
from typing import List

from app.schemas.library import (
    LibraryCreate,
    LibraryUpdate,
    LibraryResponse,
    LibraryDetail,
)
from app.api import deps
from app.services.library_service import LibraryService

router = APIRouter()


@router.post(
    "/",
    response_model=LibraryResponse,
    status_code=status.HTTP_201_CREATED,
    description="Create a new library",
)
def create_library(
    library: LibraryCreate, service: LibraryService = Depends(deps.get_library_service)
) -> LibraryResponse:
    return service.create_library(library)


@router.get(
    "/{library_id}",
    response_model=LibraryDetail,
    status_code=status.HTTP_200_OK,
    description="Get a library by ID with all its documents",
)
def get_library(
    library_id: int,
    service: LibraryService = Depends(deps.get_library_service),
) -> LibraryDetail:
    return service.get_library_with_details(library_id)


@router.get(
    "/",
    response_model=List[LibraryResponse],
    status_code=status.HTTP_200_OK,
    description="Get all libraries",
)
def get_all_libraries(service: LibraryService = Depends(deps.get_library_service)) -> List[LibraryResponse]:
    return service.get_all_libraries()


@router.patch(
    "/{library_id}",
    response_model=LibraryResponse,
    status_code=status.HTTP_200_OK,
    description="Update a library by ID",
)
def update_library(
    library_id: int,
    library: LibraryUpdate,
    service: LibraryService = Depends(deps.get_library_service),
) -> LibraryResponse:
    return service.update_library(library_id, library)


@router.delete(
    "/{library_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Delete a library by ID",
)
def delete_library(
    library_id: int,
    service: LibraryService = Depends(deps.get_library_service),
):
    service.delete_library(library_id)
