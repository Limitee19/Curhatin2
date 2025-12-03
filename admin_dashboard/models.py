from django.db import models

class DailyEmotionStats(models.Model):
    date = models.DateField(unique=True)
    emotion_counts = models.JSONField()  # {"sadness": 12, "joy": 5, ...}
    high_risk_count = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)
