from fastapi import FastAPI
from app.api.routes import library, document, chunk, search

app = FastAPI()

app.include_router(library.router, prefix="/libraries", tags=["Libraries"])
app.include_router(document.router, prefix="/documents", tags=["Documents"])
app.include_router(chunk.router, prefix="/chunks", tags=["Chunks"])
app.include_router(search.router, tags=["Indexing and Search"])


@app.get("/")
def health_check():
    return {"status": "ok", "message": "API is running"}
