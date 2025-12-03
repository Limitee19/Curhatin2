# chat/services/emotion_classifier.py

import requests
from decouple import config

HF_MODEL = "j-hartmann/emotion-english-distilroberta-base"
HF_API_URL = f"https://api-inference.huggingface.co/models/{HF_MODEL}"
HF_TOKEN = config("HF_API_TOKEN", default=None)

def classify_emotion(text: str) -> tuple[str, float]:
    headers = {"Authorization": f"Bearer {HF_TOKEN}"} if HF_TOKEN else {}
    payload = {"inputs": text}
    try:
        response = requests.post(HF_API_URL, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        predictions = response.json()
        if isinstance(predictions, list) and len(predictions) > 0:
            top = predictions[0][0]
            return top["label"], top["score"]
        else:
            return "neutral", 0.0
    except Exception as e:
        print(f"Emotion classification failed: {e}")
        return "neutral", 0.0