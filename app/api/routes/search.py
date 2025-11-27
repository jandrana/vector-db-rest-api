from fastapi import APIRouter, HTTPException, status, Depends
from typing import List, Dict, Any

from app.schemas.search import SearchRequest, SearchResult
from app.services import search_service, index_service
from app.api import deps
from app.db.database import Database

router = APIRouter()


@router.post("/libraries/{lib_id}/index", status_code=status.HTTP_200_OK)
def index_library(lib_id: int, db: Database = Depends(deps.get_db)) -> Dict[str, Any]:
    if not db.get_library(lib_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Library not found"
        )

    return index_service.index_library(db, lib_id)


@router.post(
    "/libraries/{lib_id}/search",
    response_model=List[SearchResult],
    status_code=status.HTTP_200_OK,
)
def search_library(
    lib_id: int, request: SearchRequest, db: Database = Depends(deps.get_db)
) -> List[SearchResult]:
    if not db.get_library(lib_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Library not found"
        )

    results = search_service.knn_search(db, lib_id, request.query, request.k)
    return results
