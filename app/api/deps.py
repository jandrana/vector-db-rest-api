from fastapi import Depends, Request, HTTPException, status
from app.core.container import DIContainer
from app.interfaces.services.library_service import ILibraryService
from app.interfaces.services.document_service import IDocumentService
from app.interfaces.services.chunk_service import IChunkService
from app.interfaces.services.index_service import IIndexService
from app.interfaces.services.embedding_service import IEmbeddingService
from app.interfaces.services.search_service import ISearchService


def get_container(request: Request) -> DIContainer:
    if (
        not hasattr(request.app.state, "container")
        or request.app.state.container is None
    ):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Application container not initialized.",
        )
    return request.app.state.container


def get_library_service(
    container: DIContainer = Depends(get_container),
) -> ILibraryService:
    return container.library_service


def get_document_service(
    container: DIContainer = Depends(get_container),
) -> IDocumentService:
    return container.document_service


def get_chunk_service(
    container: DIContainer = Depends(get_container),
) -> IChunkService:
    return container.chunk_service


def get_index_service(
    container: DIContainer = Depends(get_container),
) -> IIndexService:
    return container.index_service


def get_embedding_service(
    container: DIContainer = Depends(get_container),
) -> IEmbeddingService:
    return container.embedding_service


def get_search_service(
    container: DIContainer = Depends(get_container),
) -> ISearchService:
    return container.search_service
