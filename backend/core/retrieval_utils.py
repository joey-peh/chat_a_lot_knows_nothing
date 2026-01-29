import re
from typing import List
from langchain_community.vectorstores import Chroma


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
    """Create a retriever filtered by keywords from the question."""
    keywords = extract_keywords(question)

    if not keywords:
        return vectorstore.as_retriever(search_kwargs={"k": k})

    # Case-insensitive substring match on content
    conditions = [{"$regex": f"(?i){re.escape(kw)}"} for kw in keywords]
    where_document_filter = (
        {"$or": conditions} if len(conditions) > 1 else conditions[0]
    )

    return vectorstore.as_retriever(
        search_kwargs={"k": k, "where_document": where_document_filter}
    )
