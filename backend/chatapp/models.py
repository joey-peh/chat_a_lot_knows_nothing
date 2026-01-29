from django.db import models

class LocalChat(models.Model):
    message = models.TextField()
    role = models.CharField(max_length=10, choices=[("user", "user"), ("assistant", "assistant")])
    timestamp = models.DateTimeField(auto_now_add=True)
    used_documents = models.JSONField(default=list, blank=True)
    
    def __str__(self):
        return f"Message by {self.role} at {self.timestamp}"

class Document(models.Model):
    """Temporary storage for uploaded file during processing"""
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name