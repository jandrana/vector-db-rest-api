from fastapi import status


class DatabaseError(Exception):
    def __init__(self, message: str, details: dict = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}

    def __str__(self) -> str:
        if self.details:
            return f"{self.message} | Details: {self.details}"
        return self.message


class RepositoryError(DatabaseError):
    def __init__(self, message: str, details: dict = None):
        super().__init__(f"Repository error: {message}", details)


class EntityNotFoundError(RepositoryError):
    def __init__(self, entity_type: str, entity_id: int, details: dict = None):
        message = f"{entity_type} with id {entity_id} not found"
        super().__init__(message, details)
        self.entity_type = entity_type
        self.entity_id = entity_id

    @classmethod
    def library(cls, library_id: int) -> "EntityNotFoundError":
        return cls("Library", library_id)

    @classmethod
    def document(cls, document_id: int) -> "EntityNotFoundError":
        return cls("Document", document_id)

    @classmethod
    def chunk(cls, chunk_id: int) -> "EntityNotFoundError":
        return cls("Chunk", chunk_id)


class ServiceError(DatabaseError):
    def __init__(self, message: str, details: dict = None):
        super().__init__(f"Service error: {message}", details)


class ValidationError(ServiceError):
    def __init__(
        self, message: str, field: str = None, value: any = None, details: dict = None
    ):
        if field:
            message = f"Validation error for field '{field}': {message}"
            if value is not None:
                message += f" (value: {value})"

        super().__init__(message, details)
        self.field = field
        self.value = value


class EmbeddingProviderError(ServiceError):
    def __init__(self, message: str, provider: str = None, details: dict = None):
        if provider:
            message = f"Embedding provider error ({provider}): {message}"
        super().__init__(message, details)
        self.provider = provider


def get_http_status_code(exception: DatabaseError) -> int:
    if isinstance(exception, EntityNotFoundError):
        return status.HTTP_404_NOT_FOUND
    elif isinstance(exception, ValidationError):
        return status.HTTP_422_UNPROCESSABLE_CONTENT
    elif isinstance(exception, EmbeddingProviderError):
        return status.HTTP_502_BAD_GATEWAY
    elif isinstance(exception, ServiceError):
        return status.HTTP_400_BAD_REQUEST
    elif isinstance(exception, RepositoryError):
        return status.HTTP_500_INTERNAL_SERVER_ERROR
    else:
        return status.HTTP_500_INTERNAL_SERVER_ERROR
