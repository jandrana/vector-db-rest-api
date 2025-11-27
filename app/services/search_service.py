import cohere
from app.db.database import Database
from app.core.config import settings
from app.services.index_service import generate_embeddings
from app.core.math_utils import cosine_similarity

cohere_client = cohere.Client(settings.COHERE_API_KEY)


def knn_search(db: Database, lib_id: int, query: str, k: int = 3):
    query_embedding = generate_embeddings([query], input_type="search_query")[0]

    lib_chunks = db.get_chunks_by_library(lib_id)

    results = []

    for chunk in lib_chunks:
        if chunk.embedding is None:
            continue
        score = cosine_similarity(query_embedding, chunk.embedding)
        results.append({"chunk": chunk, "score": score})

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:k]
