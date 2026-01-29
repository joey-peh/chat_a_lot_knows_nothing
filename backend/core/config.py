import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Folders
CHROMA_PATH = BASE_DIR / "chroma_db"
UPLOAD_SUBDIR = "uploads"

# Chroma
COLLECTION_NAME = "documents_collection"

# Embedding
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# Chunking
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100

# Ollama
OLLAMA_MODEL = "llama3.2:3b-instruct-q6_K"         
OLLAMA_BASE_URL = os.getenv("OLLAMA_HOST", "http://localhost:11434")