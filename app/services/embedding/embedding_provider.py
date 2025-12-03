import cohere
from typing import List
from app.interfaces.services.embedding_service import IEmbeddingProvider


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
        response = self.cohere_client.embed(
            model=model, texts=texts, input_type=input_type
        )
        return response.embeddings
