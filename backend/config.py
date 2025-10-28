"""
config.py

Loads configuration and environment variables for the backend.
"""
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "YOUR_API_KEY_HERE")
VECTOR_STORE_URL = os.getenv("VECTOR_STORE_URL", "postgresql://user:pw@host:port/dbname")
PERSIST_DIR = os.getenv("PERSIST_DIR", "./storage")
