from fastapi import APIRouter, status, Depends
from typing import List

from app.schemas.document import (
    DocumentCreate,
    DocumentUpdate,
    DocumentResponse,
    DocumentDetail,
)
from app.api import deps
from app.interfaces.services.document_service import IDocumentService

router = APIRouter()


@router.post(
    "/",
    response_model=DocumentResponse,
    status_code=status.HTTP_201_CREATED,
    description="Create a new document in a library",
)
def create_document(
    document: DocumentCreate,
    service: IDocumentService = Depends(deps.get_document_service),
) -> DocumentResponse:
    created_document = service.create_document(document)
    return DocumentResponse.model_validate(created_document.model_dump())


@router.get(
    "/{document_id}",
    response_model=DocumentDetail,
    status_code=status.HTTP_200_OK,
    description="Get a document by ID with all its chunks",
)
def get_document(
    document_id: int,
    service: IDocumentService = Depends(deps.get_document_service),
) -> DocumentDetail:
    return service.get_document_with_details(document_id)


@router.get(
    "/",
    response_model=List[DocumentResponse],
    status_code=status.HTTP_200_OK,
    description="Get all documents",
)
def get_all_documents(service: IDocumentService = Depends(deps.get_document_service)) -> List[DocumentResponse]:
    documents = service.get_all_documents()
    return [DocumentResponse.model_validate(doc.model_dump()) for doc in documents]


@router.patch(
    "/{document_id}",
    response_model=DocumentResponse,
    status_code=status.HTTP_200_OK,
    description="Update a document by ID",
)
def update_document(
    document_id: int,
    document: DocumentUpdate,
    service: IDocumentService = Depends(deps.get_document_service),
) -> DocumentResponse:
    updated_document = service.update_document(document_id, document)
    return DocumentResponse.model_validate(updated_document.model_dump())


@router.delete(
    "/{document_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Delete a document by ID",
)
def delete_document(
    document_id: int,
    service: IDocumentService = Depends(deps.get_document_service),
) -> None:
    service.delete_document(document_id)
