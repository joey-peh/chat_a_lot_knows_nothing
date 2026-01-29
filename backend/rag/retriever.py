from langchain_community.vectorstores import Chroma
from core.vectorstore import get_vectorstore

def get_filtered_retriever(file_name: str | None = None, k: int = 5):
    vectorstore = get_vectorstore()
    
    search_kwargs = {"k": k}
    if file_name:
        search_kwargs["filter"] = {"file_name": file_name}

    return vectorstore.as_retriever(search_kwargs=search_kwargs)