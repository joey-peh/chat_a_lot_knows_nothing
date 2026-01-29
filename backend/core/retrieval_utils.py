import re
import sys
from typing import List
from langchain_community.vectorstores import Chroma
from sentence_transformers import CrossEncoder

# Load once at startup
reranker = CrossEncoder(
    'cross-encoder/ms-marco-MiniLM-L-6-v2',
    device='cpu',  # change to 'cuda' if available
    max_length=512
)

def extract_keywords(question: str) -> List[str]:
    """Extract meaningful keywords from a user question."""
    stop_words = {
        "what",
        "which",
        "who",
        "where",
        "when",
        "why",
        "how",
        "is",
        "are",
        "was",
        "were",
        "do",
        "does",
        "did",
        "the",
        "a",
        "an",
        "in",
        "on",
        "at",
        "to",
        "for",
        "of",
        "with",
        "about",
        "this",
        "that",
        "these",
        "those",
        "me",
        "you",
    }
    cleaned = re.sub(r"[^\w\s]", "", question.lower())
    words = cleaned.split()
    keywords = [w for w in words if len(w) > 3 and w not in stop_words]
    return list(set(keywords))

def get_retriever_with_keywords(vectorstore: Chroma, question: str, k: int = 6):
    """Returns a filtered retriever (still returns retriever object)"""
    keywords = extract_keywords(question)
    
    if keywords:
        conditions = [{"$regex": f"(?i){re.escape(kw)}"} for kw in keywords]
        where_document = {"$or": conditions} if len(conditions) > 1 else conditions[0]
        
        return vectorstore.as_retriever(
            search_kwargs={
                "k": k,                     
                "where_document": where_document
            }
        )
    else:
        return vectorstore.as_retriever(search_kwargs={"k": k})

def rerank_documents(query: str, documents, top_k: int = 6):
    """
    Re-rank retrieved documents using cross-encoder.
    Returns top_k most relevant docs.
    """
    if not documents:
        return []

    pairs = [[query, doc.page_content] for doc in documents]
    scores = reranker.predict(pairs)

    # Sort by score descending
    ranked = sorted(zip(scores, documents), key=lambda x: x[0], reverse=True)
    print(f"Ranking after re-ranker! {ranked}", file=sys.stderr)
    return [doc for _, doc in ranked[:top_k]]