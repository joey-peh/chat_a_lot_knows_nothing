from django.urls import path
from .views import chat_views
from .views.document_processing import document_views

urlpatterns = [
    path('chats/', chat_views.ChatAPIView.as_view(), name='chat-api'),
    path('documents/', document_views.DocumentProcessingView.as_view(), name='document-api'),
]