from fastapi import Depends, Request, HTTPException
from app.core.container import DIContainer
from app.core.exceptions import ValidationError


def get_container(request: Request) -> DIContainer:
    if hasattr(request.app.state, "startup_error"):
        error = request.app.state.startup_error
        if isinstance(error, ValidationError):
            raise HTTPException(
                status_code=422, detail={"detail": str(error), "field": error.field}
            )
        raise HTTPException(status_code=500, detail=str(error))

    if (
        not hasattr(request.app.state, "container")
        or request.app.state.container is None
    ):
        raise HTTPException(
            status_code=500,
            detail="Application container not initialized. Check server logs for startup errors.",
        )

    return request.app.state.container


def get_library_service(container: DIContainer = Depends(get_container)):
    return container.library_service


def get_document_service(container: DIContainer = Depends(get_container)):
    return container.document_service


def get_chunk_service(container: DIContainer = Depends(get_container)):
    return container.chunk_service


def get_index_service(container: DIContainer = Depends(get_container)):
    return container.index_service


def get_embedding_service(container: DIContainer = Depends(get_container)):
    return container.embedding_service


def get_search_service(container: DIContainer = Depends(get_container)):
    return container.search_service
