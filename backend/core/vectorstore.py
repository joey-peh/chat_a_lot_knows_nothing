import chromadb
from langchain_community.vectorstores import Chroma
from core.config import CHROMA_PATH, COLLECTION_NAME
from core.embeddings import LocalSentenceTransformersEmbeddings

def get_chroma_client():
    return chromadb.PersistentClient(path=str(CHROMA_PATH))

def get_vectorstore():
    embedding_function = LocalSentenceTransformersEmbeddings("all-MiniLM-L6-v2")
    return Chroma(
        client=get_chroma_client(),
        collection_name=COLLECTION_NAME,
        embedding_function=embedding_function,
    )