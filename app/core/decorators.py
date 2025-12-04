import functools
import inspect
from typing import Callable
from app.core.exceptions import EntityNotFoundError


def _get_param_value(param_name: str, args: tuple, kwargs: dict, func: Callable) -> any:
    sig = inspect.signature(func)
    param_names = list(sig.parameters.keys())[1:]
    
    if param_name in kwargs:
        return kwargs.get(param_name)

    if param_name in param_names:
        param_index = param_names.index(param_name)
        if param_index < len(args):
            return args[param_index]
    
    return None


def library_exists(func: Callable) -> Callable:
    """Decorator to validate that a library exists before executing the function."""

    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        library_id = _get_param_value("library_id", args, kwargs, func)
        if library_id is not None:
            if not self._library_repository.get(library_id):
                raise EntityNotFoundError.library(library_id)
        return func(self, *args, **kwargs)

    return wrapper


def document_exists(func: Callable) -> Callable:
    """Decorator to validate that a document exists before executing the function."""

    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        document_id = _get_param_value("document_id", args, kwargs, func)
        if document_id is not None:
            if not self._document_repository.get(document_id):
                raise EntityNotFoundError.document(document_id)
        return func(self, *args, **kwargs)

    return wrapper


def chunk_exists(func: Callable) -> Callable:
    """Decorator to validate that a chunk exists before executing the function."""

    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        chunk_id = _get_param_value("chunk_id", args, kwargs, func)
        if chunk_id is not None:
            if not self._chunk_repository.get(chunk_id):
                raise EntityNotFoundError.chunk(chunk_id)
        return func(self, *args, **kwargs)

    return wrapper
