"""
api.py

This module defines the API server using FastAPI. It should expose endpoints to query the LlamaIndex index.
"""
from fastapi import FastAPI

app = FastAPI()

@app.post("/query")
async def query(question: str):
    """Placeholder endpoint for querying the index."""
    return {"answer": "This is a placeholder response. The index is not yet implemented."}
