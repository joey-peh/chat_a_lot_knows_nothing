from django.db import models
from django.contrib.auth.models import User

class ChatThread(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    thread_id = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    thread = models.ForeignKey(ChatThread, on_delete=models.CASCADE)
    role = models.CharField(max_length=10)  # 'user' or 'assistant'
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class Document(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class DocumentMetadata(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    priority_score = models.FloatField(default=0.0)  # Priority score from AI model
    processed_text = models.TextField(null=True, blank=True)  # Optional, store processed text if needed
    tags = models.JSONField(default=dict)  # Tags or categories determined by the AI