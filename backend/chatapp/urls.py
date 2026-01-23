from django.urls import path
from .views import ChatAPIView, DocumentProcessingView

urlpatterns = [
    path('chat/', ChatAPIView.as_view(), name='chat'),
    path('document/', DocumentProcessingView.as_view(), name='document')
]