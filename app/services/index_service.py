import cohere
from typing import List, Dict, Any
from app.core.config import settings
from app.db.database import Database

cohere_client = cohere.Client(settings.COHERE_API_KEY)


def generate_embeddings(
    texts: List[str], input_type: str = "search_document"
) -> List[List[float]]:
    if not texts:
        return []

    response = cohere_client.embed(
        model="embed-english-v3.0", texts=texts, input_type=input_type
    )
    return response.embeddings


def index_library(db: Database, lib_id: int) -> Dict[str, Any]:
    lib_chunks = db.get_chunks_by_library(lib_id)
    to_embed = [chunk for chunk in lib_chunks if chunk.embedding is None]
    if not to_embed:
        return {
            "status": "skipped",
            "message": "No chunks to embed",
            "chunks_indexed": 0,
        }

    text_chunks = [chunk.text for chunk in to_embed]

    embeddings = generate_embeddings(text_chunks)

    for i, vector in enumerate(embeddings):
        to_embed[i].embedding = vector

    return {
        "status": "success",
        "message": f"Successfully indexed {len(to_embed)} chunks",
        "chunks_indexed": len(to_embed),
    }
