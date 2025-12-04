import functools
from typing import Callable
from app.core.exceptions import EntityNotFoundError


def library_exists(func: Callable) -> Callable:
    """Decorator to validate that a library exists before executing the function."""

    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        library_id = kwargs.get("library_id")
        if library_id is not None:
            if not self._library_repository.get(library_id):
                raise EntityNotFoundError.library(library_id)
        return func(self, *args, **kwargs)

    return wrapper


def document_exists(func: Callable) -> Callable:
    """Decorator to validate that a document exists before executing the function."""

    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        document_id = kwargs.get("document_id")
        if document_id is not None:
            if not self._document_repository.get(document_id):
                raise EntityNotFoundError.document(document_id)
        return func(self, *args, **kwargs)

    return wrapper


def chunk_exists(func: Callable) -> Callable:
    """Decorator to validate that a chunk exists before executing the function."""

    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        chunk_id = kwargs.get("chunk_id")
        if chunk_id is not None:
            if not self._chunk_repository.get(chunk_id):
                raise EntityNotFoundError.chunk(chunk_id)
        return func(self, *args, **kwargs)

    return wrapper
