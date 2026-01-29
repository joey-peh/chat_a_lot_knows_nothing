from langchain.embeddings.base import Embeddings
from sentence_transformers import SentenceTransformer

class LocalSentenceTransformersEmbeddings(Embeddings):
    # Apparently, intfloat/e5-large-v2 is currently (2026) the best open-source embedding model for RAG — 
    # it beats BGE, nomic, and even some paid ones on short/factual retrieval.
    def __init__(self, model_name: str = "intfloat/e5-large-v2"):
        self.model = SentenceTransformer(
            model_name,
            device="cpu", 
            trust_remote_code=True
        )

    def embed_documents(self, texts):
        texts = [f"passage: {text}" for text in texts]
        return self.model.encode(texts, normalize_embeddings=True, show_progress_bar=False).tolist()

    def embed_query(self, text: str):
        return self.model.encode(f"query: {text}", normalize_embeddings=True, show_progress_bar=False).tolist()