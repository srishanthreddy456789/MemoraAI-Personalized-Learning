import os
import google.generativeai as genai
from ..genai.prompts import SYSTEM_PROMPT

# ✅ FIXED: Replaced hardcoded Ollama localhost call with Google Generative AI
# Set GOOGLE_API_KEY in Render environment variables to enable AI responses
_api_key = os.environ.get("GOOGLE_API_KEY", "")

if _api_key:
    genai.configure(api_key=_api_key)
    _model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=SYSTEM_PROMPT
    )
else:
    _model = None


def call_llm(prompt: str) -> str:
    """Call Google Gemini API, with a graceful fallback if no API key is set."""
    if _model is None:
        return (
            "⚠️ AI responses are not configured yet. "
            "Please set the GOOGLE_API_KEY environment variable on Render."
        )
    try:
        response = _model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Sorry, I encountered an error generating a response: {str(e)}"


def extract_topic(student_message: str) -> str:
    """Extract the main study topic from a student message."""
    prompt = f"""Extract the main study topic from the following message.
Return ONLY a short topic name (2-5 words).
Do not explain anything.

Message: "{student_message}"
Topic:"""
    result = call_llm(prompt)
    # Fallback: use first 30 chars of message if LLM fails
    if result.startswith("⚠️") or result.startswith("Sorry"):
        return student_message[:30].lower().strip()
    return result.lower().strip()


def build_prompt(student_message: str, chat_history: list, weak_topics: list) -> str:
    """Build a prompt for the teacher LLM including history and weak topics context."""
    history_text = ""
    for msg in chat_history[-10:]:  # Last 10 messages for context
        role = "Student" if msg.get("role") == "student" else "Teacher"
        history_text += f"{role}: {msg.get('content', '')}\n"

    weak_text = ""
    if weak_topics:
        weak_text = f"\nStudent's weak topics: {', '.join(weak_topics)}\n"

    return f"""{history_text}{weak_text}Student: {student_message}
Teacher:"""


def teacher_reply(student_message: str, chat_history: list, weak_topics: list) -> str:
    """Generate a teacher reply to the student's message."""
    prompt = build_prompt(student_message, chat_history, weak_topics)
    return call_llm(prompt)


def generate_quiz(topic: str, mastery_score: float) -> str:
    """Generate a quiz question for the given topic based on mastery score."""
    difficulty = "easy" if mastery_score < 0.4 else ("medium" if mastery_score < 0.7 else "hard")
    prompt = f"""Generate a single {difficulty} quiz question about: {topic}

Format:
Question: [your question here]
A) [option]
B) [option]
C) [option]
D) [option]
Answer: [correct letter]"""
    return call_llm(prompt)