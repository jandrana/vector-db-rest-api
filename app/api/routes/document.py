from fastapi import APIRouter, HTTPException, status, Depends
from typing import List

from app.schemas.document import (
    DocumentCreate,
    DocumentUpdate,
    DocumentResponse,
    DocumentDetail,
)
from app.api import deps
from app.db.database import Database

router = APIRouter()


@router.post("/", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
def create_document(document: DocumentCreate, db: Database = Depends(deps.get_db)):
    if not db.get_library(document.library_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Library with id {document.library_id} not found",
        )
    return db.create_document(document)


@router.get(
    "/{document_id}", response_model=DocumentDetail, status_code=status.HTTP_200_OK
)
def get_document(document_id: int, db: Database = Depends(deps.get_db)):
    doc = db.get_document(document_id)
    if not doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Document not found"
        )

    chunks = db.get_chunks_by_document(document_id)

    return {
        "id": doc.id,
        "name": doc.name,
        "library_id": doc.library_id,
        "chunks": chunks,
    }


@router.get("/", response_model=List[DocumentResponse], status_code=status.HTTP_200_OK)
def get_all_documents(db: Database = Depends(deps.get_db)):
    return list(db.documents.values())


@router.patch(
    "/{document_id}", response_model=DocumentResponse, status_code=status.HTTP_200_OK
)
def update_document(
    document_id: int, document: DocumentUpdate, db: Database = Depends(deps.get_db)
):
    updated_doc = db.update_document(document_id, document)
    if not updated_doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Document not found"
        )
    return updated_doc


@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_document(document_id: int, db: Database = Depends(deps.get_db)):
    res = db.delete_document(document_id)
    if res == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Document not found"
        )
    return None