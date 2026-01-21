from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .agents import graph
from .models import ChatThread, Message
from langchain_core.messages import HumanMessage
import uuid


class ChatAPIView(APIView):
    def post(self, request):
        if not request.user.is_authenticated:
            return Response({"error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)

        message = request.data.get("message")
        thread_id = request.data.get("thread_id")

        if not thread_id:
            thread_id = str(uuid.uuid4())
            ChatThread.objects.create(user=request.user, thread_id=thread_id)

        # # Invoke graph with thread memory
        config = {"configurable": {"thread_id": thread_id}}
        input_message = HumanMessage(content=message)
        result = graph.invoke({"messages": [input_message]}, config=config)

        response_content = result["messages"][-1].content

        # Save messages to DB
        thread = ChatThread.objects.get(thread_id=thread_id)
        Message.objects.create(thread=thread, role="user", content=message)
        Message.objects.create(
            thread=thread, role="assistant", content=response_content
        )

        return Response({"response": response_content, "thread_id": thread_id})
