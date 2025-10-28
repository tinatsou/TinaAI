"""
loaders.py

This module provides helper functions to load data from local directories or external services.
"""
from llama_index.core import SimpleDirectoryReader


def load_local_docs(path: str = "data/docs"):
    """Load documents from the given path using SimpleDirectoryReader."""
    return SimpleDirectoryReader(path).load_data()
