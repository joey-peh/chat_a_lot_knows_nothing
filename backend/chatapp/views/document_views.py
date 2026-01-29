import os
import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from chatapp.models import Document
from core.vectorstore import get_vectorstore
from core.extraction_utils import (
    extract_text_from_pdf,
    extract_text_from_docx,
    process_csv,
    process_image,
)
from rag.document_processor import store_document_in_chroma
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.vectorstore import (
    get_vectorstore,
)
from django.core.files.storage import default_storage
import os


@method_decorator(csrf_exempt, name="dispatch")
class DocumentProcessingView(APIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def post(self, request, *args, **kwargs):
        """Process uploaded documents and store in File model"""
        try:
            # Get the uploaded file from the request
            uploaded_file = request.FILES.get("file")

            if not uploaded_file:
                return Response(
                    {"error": "File is required"}, status=status.HTTP_400_BAD_REQUEST
                )

            # Determine file type and extract content
            file_type = uploaded_file.content_type
            extracted_text = ""
            file_name = uploaded_file.name

            # Save the file temporarily to process
            document = Document.objects.create(file=uploaded_file)
            file_path = document.file.path

            try:
                if file_type == "text/csv":
                    # Process CSV file
                    result = process_csv(uploaded_file)
                    if "error" in result:
                        document.delete()
                        return Response(result, status=status.HTTP_400_BAD_REQUEST)
                    extracted_text = str(result)  # Convert CSV data to string

                elif file_type == "application/pdf":
                    # Process PDF file
                    extracted_text = extract_text_from_pdf(file_path)

                elif file_type in ["image/png", "image/jpeg", "image/jpg"]:
                    # Process Image file (for OCR)
                    result = process_image(uploaded_file)
                    if "error" in result:
                        document.delete()
                        return Response(result, status=status.HTTP_400_BAD_REQUEST)
                    extracted_text = result.get("text", "")

                elif file_type in [
                    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    "application/msword",
                ]:
                    # Process Word documents (.docx and .doc)
                    extracted_text = extract_text_from_docx(file_path)

                else:
                    # Delete the saved document if file type is unsupported
                    document.delete()
                    return Response(
                        {"error": "Unsupported file type"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                doc_id = str(uuid.uuid4())
                chunks_stored = store_document_in_chroma(
                    file_name=uploaded_file.name,
                    file_type=uploaded_file.content_type,
                    extracted_text=extracted_text,
                    document_id=doc_id,
                )

                # Delete temporary document
                document.delete()

                return Response(
                    {
                        "message": "File processed successfully",
                        "file_name": uploaded_file.name,
                        "chunks": chunks_stored,
                        "document_id": doc_id,
                    },
                    status=status.HTTP_200_OK,
                )

            except Exception as e:
                document.delete()
                raise e

        except Exception as e:
            return Response(
                {"error": f"Failed to process document: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def get(self, request):
        try:
            vectorstore = get_vectorstore()
            collection = vectorstore._collection

            results = collection.get(include=["metadatas"])

            unique_docs = {}

            for meta in results["metadatas"]:
                if not meta:
                    continue
                doc_id = meta.get("document_id")
                file_name = meta.get("file_name")

                if doc_id and file_name and doc_id not in unique_docs:
                    unique_docs[doc_id] = {
                        "document_id": doc_id,
                        "file_name": file_name,
                        # # Optional extra fields you might want to show
                        # "file_type": meta.get("file_type", "unknown"),
                        # "upload_time": meta.get("upload_timestamp", None),
                    }

            # Convert to list (you can sort by upload_time if you want)
            documents_list = list(unique_docs.values())

            return Response(
                {"documents": documents_list, "count": len(documents_list)},
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {"error": f"Failed to list documents: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def delete(self, request, *args, **kwargs):
        """Delete a document - removes it from the chatbot's knowledge"""
        document_id = request.data.get("document_id")

        try:
            # 1. Delete chunks from ChromaDB using metadata filter
            vectorstore = get_vectorstore()
            collection = vectorstore._collection  # access underlying Chroma collection

            # Delete all items where metadata["document_id"] matches
            collection.delete(where={"document_id": document_id})

            # Alternative raw Chroma way (if not using LangChain wrapper):
            # client = get_chroma_client()
            # collection = client.get_collection(COLLECTION_NAME)
            # collection.delete(where={"file_name": file_name})

            # 2. Optional: Delete physical file if you kept it
            # If you saved files in media/uploads/ and know the path pattern
            possible_path = os.path.join("uploads", document_id)
            if default_storage.exists(possible_path):
                default_storage.delete(possible_path)
                file_deleted = True
            else:
                file_deleted = False  # or raise warning if you expect it to exist

            return Response(
                {
                    "message": f"Document '{document_id}' deleted successfully",
                    "chroma_chunks_deleted": True,
                    "physical_file_deleted": file_deleted,
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {"error": f"Deletion failed: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
