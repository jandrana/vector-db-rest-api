from fastapi import APIRouter, status, Depends
from typing import List

from app.schemas.search import SearchRequest, SearchResult, IndexResponse
from app.api import deps
from app.interfaces.services.search_service import ISearchService
from app.interfaces.services.index_service import IIndexService

router = APIRouter()


@router.post(
    "/libraries/{lib_id}/index",
    response_model=IndexResponse,
    status_code=status.HTTP_200_OK,
    description="Index all chunks in a library by generating embeddings for chunks without them",
)
def index_library(
    lib_id: int,
    service: IIndexService = Depends(deps.get_index_service),
) -> IndexResponse:
    result = service.index_library(lib_id)
    return IndexResponse(**result)


@router.post(
    "/libraries/{lib_id}/search",
    response_model=List[SearchResult],
    status_code=status.HTTP_200_OK,
    description="Search a library using either keyword or k-NN vector search",
)
def search_library(
    lib_id: int,
    request: SearchRequest,
    service: ISearchService = Depends(deps.get_search_service),
) -> List[SearchResult]:
    return service.search(request.search_type, lib_id, request.query, request.k)
