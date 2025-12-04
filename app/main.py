from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.interfaces.repositories.replayable_repository import IReplayableRepository
from app.core.containers import AppContainer
from app.core.exceptions import DatabaseError, ValidationError, get_http_status_code
from app.api.routes import library, document, chunk, search


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application startup and shutdown."""
    container = AppContainer()
    app.state.container = container

    from app.api import deps

    container.wire(modules=[deps])

    db_container = container.db()
    registry = db_container.action_handler_registry()
    repositories = db_container.replayable_repositories()

    for repo in repositories:
        if isinstance(repo, IReplayableRepository):
            handlers = repo.get_replay_handlers()
            registry.register_handlers(handlers)

    db_container.persistence_manager().replay_actions(
        handler_provider=registry,
        replay_mode_manager=db_container.replay_mode_manager(),
    )

    chunk_repository = db_container.chunk_repository()
    inverted_index = db_container.inverted_index()
    for chunk in chunk_repository.get_all():
        if chunk.text:
            inverted_index.index_chunk(chunk.id, chunk.text)

    yield


async def database_error_handler(_request: Request, exc: DatabaseError) -> JSONResponse:
    """Convert domain exceptions to HTTP responses."""
    return JSONResponse(
        status_code=get_http_status_code(exc), content={"detail": str(exc)}
    )


async def validation_error_handler(
    _request: Request, exc: ValidationError
) -> JSONResponse:
    """Handle validation errors."""
    return JSONResponse(
        status_code=get_http_status_code(exc),
        content={"detail": str(exc), "field": exc.field},
    )


def get_application() -> FastAPI:
    application = FastAPI(
        title="Vector DB API",
        description="Vector database API with embedding support",
        version="1.0.0",
        lifespan=lifespan,
    )

    application.add_exception_handler(ValidationError, validation_error_handler)
    application.add_exception_handler(DatabaseError, database_error_handler)

    # Register routers
    application.include_router(library.router, prefix="/libraries", tags=["Libraries"])
    application.include_router(document.router, prefix="/documents", tags=["Documents"])
    application.include_router(chunk.router, prefix="/chunks", tags=["Chunks"])
    application.include_router(search.router, tags=["Indexing and Search"])

    @application.get("/", description="Health check endpoint")
    def health_check() -> dict:
        return {"status": "ok", "message": "API is running"}

    return application


app = get_application()
