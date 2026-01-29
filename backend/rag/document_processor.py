import uuid
from datetime import datetime
from core.text_splitter import get_text_splitter
from core.vectorstore import get_vectorstore

def store_document_in_chroma(
    file_name: str,
    file_type: str,
    extracted_text: str,
    document_id: str
) -> int:
    if not extracted_text.strip():
        return 0

    splitter = get_text_splitter()
    chunks = splitter.split_text(extracted_text)

    vectorstore = get_vectorstore()

    documents = []
    metadatas = []
    ids = []

    for i, chunk in enumerate(chunks):
        chunk_id = str(uuid.uuid4())
        metadata = {
            "file_name": file_name,
            "file_type": file_type,
            "chunk_index": i,
            "total_chunks": len(chunks),
            "upload_timestamp": datetime.utcnow().isoformat(),
            "source": "user_upload",
            "document_id": document_id
        }
        documents.append(chunk)
        metadatas.append(metadata)
        ids.append(chunk_id)

    vectorstore.add_texts(
        texts=documents,
        metadatas=metadatas,
        ids=ids
    )

    return len(chunks)