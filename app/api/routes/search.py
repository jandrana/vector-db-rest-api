from fastapi import APIRouter, status, Depends
from typing import List, Dict, Any

from app.schemas.search import SearchRequest, SearchResult
from app.api import deps
from app.services.search.search_service import SearchService
from app.services.index_service import IndexService

router = APIRouter()


@router.post("/libraries/{lib_id}/index", status_code=status.HTTP_200_OK)
def index_library(
    lib_id: int, service: IndexService = Depends(deps.get_index_service)
) -> Dict[str, Any]:
    return service.index_library(lib_id)


@router.post(
    "/libraries/{lib_id}/search",
    response_model=List[SearchResult],
    status_code=status.HTTP_200_OK,
)
def search_library(
    lib_id: int,
    request: SearchRequest,
    service: SearchService = Depends(deps.get_search_service),
) -> List[SearchResult]:
    return service.search(request.search_type, lib_id, request.query, request.k)
