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
from app.services.document_service import DocumentService

router = APIRouter()


@router.post(
    "/",
    response_model=LibraryResponse,
    status_code=status.HTTP_201_CREATED,
    description="Create a new library",
)
def create_library(
    library: LibraryCreate, service: LibraryService = Depends(deps.get_library_service)
):
    return service.create_library(library)


@router.get(
    "/{library_id}",
    response_model=LibraryDetail,
    status_code=status.HTTP_200_OK,
    description="Get a library by ID with all its documents",
)
def get_library(
    library_id: int,
    library_service: LibraryService = Depends(deps.get_library_service),
    document_service: DocumentService = Depends(deps.get_document_service),
):
    library = library_service.get_library(library_id)
    documents = document_service.get_documents_by_library(library_id)
    return LibraryDetail.model_validate(
        {**library.model_dump(), "documents": documents}
    )


@router.get(
    "/",
    response_model=List[LibraryResponse],
    status_code=status.HTTP_200_OK,
    description="Get all libraries",
)
def get_all_libraries(service: LibraryService = Depends(deps.get_library_service)):
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
):
    return service.update_library(library_id, library)


@router.delete(
    "/{library_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Delete a library by ID",
)
def delete_library(
    library_id: int, service: LibraryService = Depends(deps.get_library_service)
):
    service.delete_library(library_id)
