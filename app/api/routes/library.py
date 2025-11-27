from fastapi import APIRouter, HTTPException, status, Depends
from typing import List

from app.schemas.library import (
    LibraryCreate,
    LibraryUpdate,
    LibraryResponse,
    LibraryDetail,
)
from app.api import deps
from app.db.database import Database

router = APIRouter()


@router.post("/", response_model=LibraryResponse, status_code=status.HTTP_201_CREATED)
def create_library(library: LibraryCreate, db: Database = Depends(deps.get_db)):
    return db.create_library(library)


@router.get(
    "/{library_id}", response_model=LibraryDetail, status_code=status.HTTP_200_OK
)
def get_library(library_id: int, db: Database = Depends(deps.get_db)):
    lib = db.get_library(library_id)
    if not lib:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Library not found"
        )

    documents = db.get_documents_by_library(library_id)

    return {"id": lib.id, "name": lib.name, "documents": documents}


@router.get("/", response_model=List[LibraryResponse], status_code=status.HTTP_200_OK)
def get_all_libraries(db: Database = Depends(deps.get_db)):
    return list(db.libraries.values())


@router.patch(
    "/{library_id}", response_model=LibraryResponse, status_code=status.HTTP_200_OK
)
def update_library(
    library_id: int, library: LibraryUpdate, db: Database = Depends(deps.get_db)
):
    updated_lib = db.update_library(library_id, library)
    if not updated_lib:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Library not found"
        )
    return updated_lib
