# chat/views.py

from django.shortcuts import get_object_or_404
from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ChatSession, ChatMessage
from .serializers import ChatSessionSerializer
from .services.ai_service import process_user_message
import uuid

class ChatSessionView(APIView):
    def post(self, request):
        session_id = request.data.get("session_id")
        user_message = request.data.get("message", "").strip()

        if not user_message:
            return Response({"error": "Pesan tidak boleh kosong."}, status=400)

        # Rate limiting: max 10 pesan per 5 menit per session
        rate_key = f"chat_rate_{session_id or 'new'}"
        request_count = cache.get(rate_key, 0)
        if request_count >= 10:
            return Response({"error": "Terlalu banyak permintaan. Silakan coba lagi nanti."}, status=429)
        cache.set(rate_key, request_count + 1, timeout=300)

        if not session_id:
            session_id = str(uuid.uuid4().hex)
            session = ChatSession.objects.create(session_id=session_id)
        else:
            session = get_object_or_404(ChatSession, session_id=session_id)

        # Simpan pesan user
        ChatMessage.objects.create(
            session=session,
            sender="user",
            message=user_message
        )

        # Proses dengan AI
        ai_response = process_user_message(user_message, session_id)

        # Simpan respons AI
        ChatMessage.objects.create(
            session=session,
            sender="ai",
            message=ai_response["reply"],
            emotion_label=ai_response.get("emotion_label"),
            emotion_score=ai_response.get("emotion_score"),
            risk_level=ai_response.get("risk_level", "none")
        )

        serializer = ChatSessionSerializer(session)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request):
        session_id = request.query_params.get("session_id")
        if not session_id:
            return Response({"error": "session_id required"}, status=400)
        session = get_object_or_404(ChatSession, session_id=session_id)
        serializer = ChatSessionSerializer(session)
        return Response(serializer.data)