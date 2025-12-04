from fastapi import APIRouter, status, Depends
from typing import List

from app.schemas.document import (
    DocumentCreate,
    DocumentUpdate,
    DocumentResponse,
    DocumentDetail,
)
from app.api import deps
from app.services.document_service import DocumentService

router = APIRouter()


@router.post(
    "/",
    response_model=DocumentResponse,
    status_code=status.HTTP_201_CREATED,
    description="Create a new document in a library",
)
def create_document(
    document: DocumentCreate,
    service: DocumentService = Depends(deps.get_document_service),
):
    return service.create_document(document)


@router.get(
    "/{document_id}",
    response_model=DocumentDetail,
    status_code=status.HTTP_200_OK,
    description="Get a document by ID with all its chunks",
)
def get_document(
    document_id: int,
    service: DocumentService = Depends(deps.get_document_service),
):
    return service.get_document_with_details(document_id)


@router.get(
    "/",
    response_model=List[DocumentResponse],
    status_code=status.HTTP_200_OK,
    description="Get all documents",
)
def get_all_documents(service: DocumentService = Depends(deps.get_document_service)):
    return service.get_all_documents()


@router.patch(
    "/{document_id}",
    response_model=DocumentResponse,
    status_code=status.HTTP_200_OK,
    description="Update a document by ID",
)
def update_document(
    document_id: int,
    document: DocumentUpdate,
    service: DocumentService = Depends(deps.get_document_service),
):
    return service.update_document(document_id, document)


@router.delete(
    "/{document_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Delete a document by ID",
)
def delete_document(
    document_id: int,
    service: DocumentService = Depends(deps.get_document_service),
):
    service.delete_document(document_id)
