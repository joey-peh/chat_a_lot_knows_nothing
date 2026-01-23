from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import ChatThread, Message
from langchain_core.messages import HumanMessage
from ..agents import graph
import uuid

class ChatAPIView(APIView):
    def post(self, request):
        if not request.user.is_authenticated:
            return Response({"error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)

        message = request.data.get("message")
        thread_id = request.data.get("thread_id")

        if not message:
            return Response({"error": "Message is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new thread if no thread_id is provided
        if not thread_id:
            thread_id = str(uuid.uuid4())
            ChatThread.objects.create(user=request.user, thread_id=thread_id)

        # Prepare the input message and invoke the graph
        input_message = HumanMessage(content=message)
        config = {"configurable": {"thread_id": thread_id}}
        result = graph.invoke({"messages": [input_message]}, config=config)
        
        response_content = result["messages"][-1].content

        # Save both user and assistant messages to the database
        thread = ChatThread.objects.get(thread_id=thread_id)
        Message.objects.create(thread=thread, role="user", content=message)
        Message.objects.create(thread=thread, role="assistant", content=response_content)

        return Response({
            "response": response_content, 
            "thread_id": thread_id
        })
