import chromadb
from langchain_community.vectorstores import Chroma
from core.embeddings import LocalSentenceTransformersEmbeddings
from core.config import CHROMA_PATH, COLLECTION_NAME

_chroma_client = None

def get_chroma_client():
    global _chroma_client
    if _chroma_client is None:
        _chroma_client = chromadb.PersistentClient(path=str(CHROMA_PATH))
    return _chroma_client

def get_vectorstore(model_name="intfloat/e5-large-v2"):
    """Get Chroma vector store with lazy client initialization"""
    embedding_function = LocalSentenceTransformersEmbeddings(model_name)
    
    return Chroma(
        client=get_chroma_client(),
        collection_name=COLLECTION_NAME,
        embedding_function=embedding_function
    )