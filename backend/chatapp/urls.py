from django.urls import path
from . import chat_views, query_views, document_views

urlpatterns = [
    path('api/chats/', chat_views.ChatAPIView.as_view(), name='chat-api'),
    path('api/query/', query_views.QueryAPIView.as_view(), name='query-api'),
    path('api/documents/', document_views.DocumentProcessingView.as_view(), name='document-api'),
    path('api/documents/<int:document_id>/prompt/', document_views.DocumentPromptView.as_view(), name='document-prompt-api'),
]