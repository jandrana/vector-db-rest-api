from fastapi import FastAPI
from app.api.routes import library, document, chunk, search

app = FastAPI()

app.include_router(library.router, prefix="/libraries", tags=["libraries"])
app.include_router(document.router, prefix="/documents", tags=["documents"])
app.include_router(chunk.router, prefix="/chunks", tags=["chunks"])
app.include_router(search.router, tags=["Search"])


@app.get("/")
def health_check():
    return {"status": "ok", "message": "API is running"}
