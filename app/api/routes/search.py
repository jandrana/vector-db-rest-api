from fastapi import APIRouter, status, Depends
from typing import List

from app.schemas.search import SearchRequest, SearchResult, IndexResponse
from app.schemas.chunk import ChunkResponse
from app.api import deps
from app.services.search.search_service import SearchService
from app.services.index_service import IndexService

router = APIRouter()


@router.post(
    "/libraries/{lib_id}/index",
    response_model=IndexResponse,
    status_code=status.HTTP_200_OK,
    description="Index all chunks in a library by generating embeddings for chunks without them",
)
def index_library(
    lib_id: int,
    service: IndexService = Depends(deps.get_index_service),
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
    service: SearchService = Depends(deps.get_search_service),
) -> List[SearchResult]:
    results = service.search(request.search_type, lib_id, request.query, request.k)
    return [
        SearchResult(
            score=result["score"],
            chunk=ChunkResponse(
                id=result["chunk"].id,
                text=result["chunk"].text,
                document_id=result["chunk"].document_id,
            ),
        )
        for result in results
    ]
