# chat/services/safety_layer.py

import logging
from decouple import config
import requests

logger = logging.getLogger("safety")

HIGH_RISK_KEYWORDS = [
    "bunuh diri", "akhiri hidup", "mati saja", "tidak mau hidup",
    "suicide", "kill myself", "end my life", "no reason to live",
    "better off dead", "wish i were dead", "sayat", "lukai diri"
]

def detect_risk_level(text: str) -> str:
    text_lower = text.lower()
    for phrase in HIGH_RISK_KEYWORDS:
        if phrase in text_lower:
            return "high"
    hopeless_terms = ["putus asa", "tak berdaya", "hopeless", "helpless"]
    if any(term in text_lower for term in hopeless_terms):
        return "medium"
    return "none"

def log_safety_event(session_id: str, message: str, risk_level: str):
    logger.warning(f"[SAFETY] {risk_level.upper()} | Session: {session_id} | Msg: {message[:100]}...")

def trigger_escalation(session_id: str, message: str, risk_level: str):
    log_safety_event(session_id, message, risk_level)
    if risk_level == "high":
        webhook_url = config("SAFETY_WEBHOOK_URL", default=None)
        if webhook_url:
            try:
                requests.post(webhook_url, json={
                    "alert_type": "high_risk_mental_health",
                    "session_id": session_id,
                    "message_snippet": message[:200],
                    "timestamp": __import__('datetime').datetime.utcnow().isoformat(),
                }, timeout=5)
            except Exception as e:
                logger.error(f"Webhook failed: {e}")