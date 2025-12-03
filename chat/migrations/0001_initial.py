# chat/migrations/0001_initial.py

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name='ChatSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_id', models.CharField(max_length=64, unique=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ChatMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sender', models.CharField(choices=[('user', 'User'), ('ai', 'AI')], max_length=10)),
                ('message', models.TextField()),
                ('emotion_label', models.CharField(blank=True, max_length=32, null=True)),
                ('emotion_score', models.FloatField(blank=True, null=True)),
                ('risk_level', models.CharField(choices=[('none', 'None'), ('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], default='none', max_length=16)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='chat.chatsession')),
            ],
        ),
    ]