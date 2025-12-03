from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.core.config import get_settings
from app.core.events import create_startup_handler
from app.core.exceptions import DatabaseError, ValidationError, get_http_status_code
from app.api.routes import library, document, chunk, search


async def database_error_handler(_request: Request, exc: DatabaseError):
    """Convert domain exceptions to HTTP responses."""
    return JSONResponse(
        status_code=get_http_status_code(exc), content={"detail": str(exc)}
    )


async def validation_error_handler(_request: Request, exc: ValidationError):
    """Handle validation errors."""
    return JSONResponse(
        status_code=get_http_status_code(exc),
        content={"detail": str(exc), "field": exc.field},
    )


def get_application() -> FastAPI:
    settings = get_settings()

    application = FastAPI(
        title="Vector DB API",
        description="Vector database API with embedding support",
        version="1.0.0",
    )

    application.add_event_handler(
        "startup", create_startup_handler(application, settings)
    )

    application.add_exception_handler(ValidationError, validation_error_handler)
    application.add_exception_handler(DatabaseError, database_error_handler)

    # Register routers
    application.include_router(library.router, prefix="/libraries", tags=["Libraries"])
    application.include_router(document.router, prefix="/documents", tags=["Documents"])
    application.include_router(chunk.router, prefix="/chunks", tags=["Chunks"])
    application.include_router(search.router, tags=["Indexing and Search"])

    @application.get("/")
    def health_check():
        return {"status": "ok", "message": "API is running"}

    return application


app = get_application()
