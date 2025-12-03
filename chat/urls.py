# chat/urls.py

from django.urls import path
from .views import ChatSessionView

urlpatterns = [
    path('chat/', ChatSessionView.as_view(), name='chat-session'),
]