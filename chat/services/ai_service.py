import google.generativeai as genai
from decouple import config
from .emotion_classifier import classify_emotion
from .safety_layer import detect_risk_level, trigger_escalation
import logging

logger = logging.getLogger(__name__)
AI_PROVIDER = config("AI_PROVIDER", default="gemini").lower()

def get_ai_response(prompt: str) -> str:
    if AI_PROVIDER == "gemini":
        return _call_gemini(prompt)
    else:
        return "Terima kasih sudah berbagi. Saya di sini untuk mendengarkan."

def _call_gemini(prompt: str) -> str:
    api_key = config("GEMINI_API_KEY")
    if not api_key:
        return "Maaf, layanan AI sedang tidak tersedia."

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(
            "gemini-2.5-flash",
            system_instruction=(
                "You are a compassionate, non-judgmental mental health support companion. "
                "Respond with empathy, validation, and gentle guidance. "
                "Never give medical advice. Encourage professional help if needed. "
                "Keep responses short (1–3 sentences)."
            )
        )
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(max_output_tokens=150, temperature=0.7),
            safety_settings={
                genai.types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: genai.types.HarmBlockThreshold.BLOCK_NONE,
                genai.types.HarmCategory.HARM_CATEGORY_HATE_SPEECH: genai.types.HarmBlockThreshold.BLOCK_NONE,
                genai.types.HarmCategory.HARM_CATEGORY_HARASSMENT: genai.types.HarmBlockThreshold.BLOCK_NONE,
                genai.types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: genai.types.HarmBlockThreshold.BLOCK_NONE,
            }
        )
        return response.text.strip() if response.text else "Saya mendengarkan. Boleh ceritakan lebih lanjut?"
    except Exception as e:
        logger.error(f"Gemini error: {e}")
        return "Maaf, terjadi gangguan teknis. Tapi aku tetap di sini untukmu."

def process_user_message(user_message: str, session_id: str) -> dict:
    emotion_label, emotion_score = classify_emotion(user_message)
    risk_level = detect_risk_level(user_message)
    if risk_level == "high":
        trigger_escalation(session_id, user_message, risk_level)

    ai_reply = get_ai_response(user_message)

    if risk_level == "high":
        emergency_msg = (
            "\n\n⚠️ **Jika kamu sedang dalam krisis, segera hubungi layanan darurat:**\n"
            "- Indonesia: 119 atau 112\n"
            "- Layanan Konseling: 0800-100-1001\n"
            "- Kamu berharga. Ada yang peduli."
        )
        full_reply = ai_reply + emergency_msg
    else:
        full_reply = ai_reply  # ❌ TANPA self-care

    return {
        "reply": full_reply,
        "emotion_label": emotion_label,
        "emotion_score": round(emotion_score, 3) if emotion_score else 0.0,
        "risk_level": risk_level
    }
