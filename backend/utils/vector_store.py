"""
vector_store.py

Utility functions for creating and loading vector stores using PostgreSQL or other backends.
"""
from llama_index.core import StorageContext, VectorStoreIndex
from llama_index.vector_stores.postgres import PGVectorStore
from .loaders import load_local_docs


def build_index(documents, vector_store_url: str, persist_dir: str):
    """Build a vector index using the provided documents and configuration."""
    vector_store = PGVectorStore(
        embedding_function=None,  # replace with actual embedding function
        connection_string=vector_store_url,
    )
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    index = VectorStoreIndex.from_documents(documents, storage_context=storage_context)
    storage_context.persist(persist_dir=persist_dir)
    return index
