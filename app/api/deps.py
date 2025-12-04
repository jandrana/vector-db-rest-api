from fastapi import Depends, Request
from app.core.containers import AppContainer
from app.interfaces.services.library_service import ILibraryService
from app.interfaces.services.document_service import IDocumentService
from app.interfaces.services.chunk_service import IChunkService
from app.interfaces.services.index_service import IIndexService
from app.interfaces.services.embedding_service import IEmbeddingService
from app.interfaces.services.search_service import ISearchService


def get_container(request: Request) -> AppContainer:
    return request.app.state.container


def get_library_service(
    container: AppContainer = Depends(get_container),
) -> ILibraryService:
    return container.services.library_service()


def get_document_service(
    container: AppContainer = Depends(get_container),
) -> IDocumentService:
    return container.services.document_service()


def get_chunk_service(
    container: AppContainer = Depends(get_container),
) -> IChunkService:
    return container.services.chunk_service()


def get_index_service(
    container: AppContainer = Depends(get_container),
) -> IIndexService:
    return container.services.index_service()


def get_embedding_service(
    container: AppContainer = Depends(get_container),
) -> IEmbeddingService:
    return container.services.embedding_service()


def get_search_service(
    container: AppContainer = Depends(get_container),
) -> ISearchService:
    return container.services.search_service()
