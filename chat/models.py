# chat/models.py

from django.db import models
from django.utils import timezone

class ChatSession(models.Model):
    session_id = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.session_id

class ChatMessage(models.Model):
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name="messages")
    sender = models.CharField(max_length=10, choices=[("user", "User"), ("ai", "AI")])
    message = models.TextField()
    emotion_label = models.CharField(max_length=32, blank=True, null=True)
    emotion_score = models.FloatField(blank=True, null=True)
    risk_level = models.CharField(
        max_length=16,
        choices=[("none", "None"), ("low", "Low"), ("medium", "Medium"), ("high", "High")],
        default="none"
    )
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.sender}: {self.message[:50]}"