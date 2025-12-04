from typing import List
from app.interfaces.services.embedding_service import (
    IEmbeddingService,
    IEmbeddingProvider,
)


class EmbeddingService(IEmbeddingService):
    def __init__(
        self, embedding_provider: IEmbeddingProvider, model: str = "embed-english-v3.0"
    ):
        self.embedding_provider = embedding_provider
        self.model = model

    def generate_embeddings(
        self, texts: List[str], input_type: str = "search_document"
    ) -> List[List[float]]:
        return self.embedding_provider.generate_embeddings(
            texts, input_type, model=self.model
        )
