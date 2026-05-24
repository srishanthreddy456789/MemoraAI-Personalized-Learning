import os
import google.generativeai as genai
from ..genai.prompts import SYSTEM_PROMPT

# ✅ Configure Gemini API
_api_key = os.environ.get("GOOGLE_API_KEY", "")

if _api_key:
    genai.configure(api_key=_api_key)

# Free-tier flash models to try in order of preference
_MODEL_CANDIDATES = [
    "gemini-2.0-flash",
    "gemini-2.0-flash-lite",
    "gemini-1.5-flash",
    "gemini-1.5-flash-8b",
    "gemini-1.5-flash-latest",
]

def _get_model_name() -> str:
    """Find first available FREE flash model — never fall back to paid pro models."""
    if not _api_key:
        return ""
    try:
        available = [m.name for m in genai.list_models()
                     if "generateContent" in m.supported_generation_methods]
        # Only match flash/free models from our candidates list
        for candidate in _MODEL_CANDIDATES:
            for avail in available:
                if candidate in avail:
                    return avail
        # If no flash model found, use hardcoded fallback (never auto-pick first)
        return "models/gemini-1.5-flash"
    except Exception:
        return "models/gemini-1.5-flash"


_resolved_model = None

def _get_model():
    """Lazy-load the model."""
    global _resolved_model
    if not _api_key:
        return None
    if _resolved_model is None:
        model_name = _get_model_name()
        if model_name:
            # Don't use system_instruction — not supported by all models
            _resolved_model = genai.GenerativeModel(model_name=model_name)
    return _resolved_model


def call_llm(prompt: str) -> str:
    """Call Gemini API. System prompt is prepended to the user message."""
    model = _get_model()

    if model is None:
        return (
            "⚠️ AI responses are not configured. "
            "Please set GOOGLE_API_KEY in Render environment variables."
        )
    try:
        # Prepend system prompt directly in the message (works with all models)
        full_prompt = f"{SYSTEM_PROMPT}\n\n{prompt}"
        response = model.generate_content(full_prompt)
        return response.text.strip()
    except Exception as e:
        return f"Sorry, I encountered an error: {str(e)}"


def extract_topic(student_message: str) -> str:
    """Extract the main study topic from a student message."""
    prompt = f"""Extract the main study topic from this message.
Return ONLY a short topic name (2-5 words), nothing else.

Message: "{student_message}"
Topic:"""
    result = call_llm(prompt)
    if result.startswith("⚠️") or result.startswith("Sorry"):
        return student_message[:30].lower().strip()
    return result.lower().strip()[:50]


def build_prompt(student_message: str, chat_history: list, weak_topics: list) -> str:
    """Build a prompt including chat history context."""
    history_text = ""
    for msg in chat_history[-10:]:
        role = "Student" if msg.get("role") == "student" else "Teacher"
        history_text += f"{role}: {msg.get('content', '')}\n"

    weak_text = ""
    if weak_topics:
        weak_text = f"\nNote: Student's weak topics are: {', '.join(weak_topics)}\n"

    return f"{history_text}{weak_text}Student: {student_message}\nTeacher:"


def teacher_reply(student_message: str, chat_history: list, weak_topics: list) -> str:
    """Generate a teacher reply."""
    prompt = build_prompt(student_message, chat_history, weak_topics)
    return call_llm(prompt)


def generate_quiz(topic: str, mastery_score: float) -> str:
    """Generate a quiz question based on topic and mastery."""
    difficulty = "easy" if mastery_score < 0.4 else ("medium" if mastery_score < 0.7 else "hard")
    prompt = f"""Generate a single {difficulty} multiple choice quiz question about: {topic}

Format exactly like this:
Question: [question here]
A) [option]
B) [option]
C) [option]
D) [option]
Answer: [correct letter]"""
    return call_llm(prompt)