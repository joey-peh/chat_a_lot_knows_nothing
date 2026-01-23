from django.db import models

class File(models.Model):
    name = models.CharField(max_length=255)
    content = models.TextField()
    file_type = models.CharField(max_length=50, default='text')  # pdf, docx, csv, etc.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"

class LocalChat(models.Model):
    message = models.TextField()
    role = models.CharField(max_length=10, choices=[("user", "user"), ("assistant", "assistant")])
    timestamp = models.DateTimeField(auto_now_add=True)
    documents_used = models.ManyToManyField(File, blank=True, related_name='chats_using_this')  # Track which documents were used for this response

    def __str__(self):
        return f"Message by {self.role} at {self.timestamp}"
