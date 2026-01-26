from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from ..models import LocalChat, File
from ..agents import graph
from langchain_core.messages import HumanMessage, AIMessage

@method_decorator(csrf_exempt, name='dispatch')
class ChatAPIView(APIView):
    
    def post(self, request, *args, **kwargs):
        """Process user query with document context and save to database"""
        try:
            message = request.data.get('message')
            
            if not message:
                return Response({"error": "Message is required"}, status=status.HTTP_400_BAD_REQUEST)

            # Retrieve all documents for context
            all_documents = File.objects.all()
            
            # Build document context
            doc_context = ""
            document_ids_used = []
            if all_documents.exists():
                doc_context = "\n\n=== KNOWLEDGE BASE (PRIORITIZE THIS INFO) ===\n"
                for doc in all_documents:
                    doc_context += f"\n📄 {doc.name}:\n{doc.content}\n---"
                    document_ids_used.append(doc.id)
            
            # Create system message with document context
            system_message = f"""You are a helpful assistant that answers questions based on the uploaded documents.
            
            IMPORTANT: When answering questions, prioritize and reference information from the documents.
            If the user asks about something in the documents, cite which document it came from.

            {doc_context if doc_context else "No documents have been uploaded yet."}

            Now, answer the user's question:"""

            # Build message list for the agent
            messages = [
                HumanMessage(content=system_message),
                HumanMessage(content=message)
            ]
            
            # Invoke the agent with document context
            response = graph.invoke(
                {"messages": messages},
                config={"configurable": {"thread_id": "main"}}
            )
            
            # Extract assistant response
            assistant_response = response["messages"][-1].content if response["messages"] else "No response generated"
            
            # Save user message
            user_chat = LocalChat.objects.create(
                role="user",
                message=message
            )
            
            # Save assistant response
            assistant_chat = LocalChat.objects.create(
                role="assistant",
                message=assistant_response
            )
            
            # Track which documents were used for this exchange
            assistant_chat.documents_used.set(document_ids_used)
            
            return Response({
                "message": "Query processed successfully",
                "user_chat_id": user_chat.id,
                "assistant_chat_id": assistant_chat.id,
                "response": assistant_response,
                "documents_used": len(document_ids_used)
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"error": f"Failed to process query: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def get(self, request, *args, **kwargs):
        """Retrieve chat history"""
        try:
            chats = LocalChat.objects.all().order_by('timestamp')
            
            chat_data = []
            for chat in chats:
                chat_info = {
                    'id': chat.id,
                    'role': chat.role,
                    'message': chat.message,
                    'timestamp': chat.timestamp,
                    'documents_used': list(chat.documents_used.values_list('name', flat=True))
                }
                chat_data.append(chat_info)
            
            return Response({
                'chat_history': chat_data,
                'count': len(chat_data)
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"error": f"Failed to retrieve chats: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def delete(self, request, *args, **kwargs):
        """Delete a specific chat or all chats"""
        try:
            chat_id = request.data.get('chat_id')  # Optional: delete specific chat
            
            if chat_id:
                try:
                    chat = LocalChat.objects.get(id=chat_id)
                    chat.delete()
                    return Response({"message": "Chat deleted successfully"}, status=status.HTTP_200_OK)
                except LocalChat.DoesNotExist:
                    return Response({"error": "Chat not found"}, status=status.HTTP_404_NOT_FOUND)
            else:
                LocalChat.objects.all().delete()
                return Response({"message": "All chats deleted successfully"}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"error": f"Failed to delete chat: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)