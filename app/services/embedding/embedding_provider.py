import cohere
from typing import List
from app.interfaces.services.embedding_service import IEmbeddingProvider
from app.core.exceptions import EmbeddingProviderError, ServiceError


class CohereEmbeddingProvider(IEmbeddingProvider):
    def __init__(self, api_key: str, model: str = "embed-english-v3.0"):
        self.api_key = api_key
        self.model = model
        self.cohere_client = cohere.Client(self.api_key)

    def generate_embeddings(
        self,
        texts: List[str],
        input_type: str = "search_document",
        model: str = "embed-english-v3.0",
    ) -> List[List[float]]:
        try:
            response = self.cohere_client.embed(
                model=model, texts=texts, input_type=input_type
            )
            return response.embeddings
        except Exception as e:
            error_type = type(e)
            is_cohere_error = (
                "cohere" in error_type.__module__.lower()
                or "Cohere" in error_type.__name__
            )

            if is_cohere_error:
                raise EmbeddingProviderError(str(e), provider="Cohere") from e
            raise ServiceError(
                f"Unexpected error during embedding generation: {str(e)}"
            ) from e
