# admin_dashboard/views.py

from django.shortcuts import render
from django.db.models import Count, Q
from django.utils import timezone
from chat.models import ChatMessage
import json

def dashboard_view(request):
    today = timezone.now().date()
    last_7_days = [today - timezone.timedelta(days=i) for i in range(7)][::-1]

    emotion_data = []
    risk_data = []

    for day in last_7_days:
        start = timezone.datetime.combine(day, timezone.datetime.min.time())
        end = start + timezone.timedelta(days=1)
        messages = ChatMessage.objects.filter(
            sender="user",
            timestamp__gte=start,
            timestamp__lt=end
        )

        # Emosi (hanya yang terklasifikasi)
        emotion_counts = messages.exclude(emotion_label__isnull=True).values(
            'emotion_label').annotate(count=Count('id'))
        emotion_dict = {item['emotion_label']: item['count'] for item in emotion_counts}

        # Risiko
        high_risk = messages.filter(risk_level="high").count()
        medium_risk = messages.filter(risk_level="medium").count()

        emotion_data.append({
            "date": day.isoformat(),
            "emotions": emotion_dict
        })
        risk_data.append({
            "date": day.isoformat(),
            "high": high_risk,
            "medium": medium_risk
        })

    context = {
        "emotion_data_json": json.dumps(emotion_data),
        "risk_data_json": json.dumps(risk_data)
    }
    return render(request, 'admin_dashboard/dashboard.html', context)