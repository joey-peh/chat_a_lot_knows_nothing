import sys
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from core.retrieval_utils import get_retriever_with_keywords
from core.vectorstore import get_vectorstore
from ..models import LocalChat
from ..agents import graph
from langchain_core.messages import HumanMessage


@method_decorator(csrf_exempt, name="dispatch")
class ChatAPIView(APIView):

    def post(self, request, *args, **kwargs):
        """Process user query with relevant document context from ChromaDB and save to database"""
        try:
            message = request.data.get("message")

            if not message:
                return Response(
                    {"error": "Message is required"}, status=status.HTTP_400_BAD_REQUEST
                )
                
            # Get the Chroma vector store
            vectorstore = get_vectorstore()
            retriever = get_retriever_with_keywords(vectorstore, message, k=6)
            
            # Retrieve relevant chunks
            retrieved_docs = retriever.invoke(message)
            # for i, doc in enumerate(retrieved_docs, 1):
            #     print(f"Rank {i}: {doc.page_content[:200]}... (source: {doc.metadata.get('file_name')})", file=sys.stderr)

            # Build context from retrieved chunks
            doc_context = ""
            used_documents = []

            if retrieved_docs:
                doc_context = (
                    "\n\n=== RELEVANT DOCUMENT CONTEXT (PRIORITIZE THIS) ===\n"
                )
                seen_sources = set()

                for doc in retrieved_docs:
                    meta = doc.metadata
                    source = (
                        meta.get("file_name") or meta.get("document_id") or "unknown"
                    )

                    if source not in seen_sources:
                        seen_sources.add(source)
                        used_documents.append(source)

                    doc_context += f"\n📄 Source: {source} (chunk {meta.get('chunk_index', '?')})\n"
                    doc_context += f"{doc.page_content}\n---\n"

            else:
                doc_context = "No relevant documents found in the knowledge base."
                
            print(f"Document context built with {len(used_documents)} unique source(s).", file=sys.stderr)
            print(f"Context: {doc_context}", file=sys.stderr)

            # Create system message with retrieved context
            system_message = f"""You are a helpful assistant that answers questions based on the provided document context.
            
            IMPORTANT RULES:
            - Prioritize and ONLY use information from the provided context above.
            - If the answer is not in the context, say "I don't have information about that in the uploaded documents."
            - When referencing information, mention the source file name clearly.
            - Be concise, accurate and helpful.

            {doc_context}

            User question:"""

            # Build messages for your LangGraph / agent
            messages = [
                HumanMessage(content=system_message),
                HumanMessage(content=message),
            ]

            # Invoke your graph/agent
            response = graph.invoke(
                {"messages": messages},
                config={
                    "configurable": {"thread_id": "main"}
                },  # or use user/session id
            )

            # Extract assistant's final response
            assistant_response = (
                response["messages"][-1].content
                if response["messages"]
                else "No response generated"
            )

            # Save user message
            user_chat = LocalChat.objects.create(role="user", message=message)

            # Save assistant response with used documents
            assistant_chat = LocalChat.objects.create(
                role="assistant",
                message=assistant_response,
                used_documents=used_documents,
            )

            return Response(
                {
                    "message": "Query processed successfully",
                    "user_chat_id": user_chat.id,
                    "assistant_chat_id": assistant_chat.id,
                    "response": assistant_response,
                    "documents_used": used_documents,
                    "context_length": len(doc_context),
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {"error": f"Failed to process query: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def get(self, request, *args, **kwargs):
        """Retrieve chat history"""
        try:
            chats = LocalChat.objects.all().order_by("timestamp")

            chat_data = []
            for chat in chats:
                print(chat.used_documents, file=sys.stderr)
                chat_info = {
                    "id": chat.id,
                    "role": chat.role,
                    "message": chat.message,
                    "timestamp": chat.timestamp,
                    "used_documents": chat.used_documents
                }
                chat_data.append(chat_info)

            return Response(
                {"chat_history": chat_data, "count": len(chat_data)},
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {"error": f"Failed to retrieve chats: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def delete(self, request, *args, **kwargs):
        """Delete a specific chat or all chats"""
        try:
            chat_id = request.data.get("chat_id")  # Optional: delete specific chat

            if chat_id:
                try:
                    chat = LocalChat.objects.get(id=chat_id)
                    chat.delete()
                    return Response(
                        {"message": "Chat deleted successfully"},
                        status=status.HTTP_200_OK,
                    )
                except LocalChat.DoesNotExist:
                    return Response(
                        {"error": "Chat not found"}, status=status.HTTP_404_NOT_FOUND
                    )
            else:
                LocalChat.objects.all().delete()
                return Response(
                    {"message": "All chats deleted successfully"},
                    status=status.HTTP_200_OK,
                )

        except Exception as e:
            return Response(
                {"error": f"Failed to delete chat: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
