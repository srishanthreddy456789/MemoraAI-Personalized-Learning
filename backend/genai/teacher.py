import os
from groq import Groq
from ..genai.prompts import SYSTEM_PROMPT

# ✅ Using Groq — free tier, works globally, no billing required
# Get your free key at: https://console.groq.com
# Set GROQ_API_KEY in Render environment variables

_api_key = os.environ.get("GROQ_API_KEY", "")
_client = Groq(api_key=_api_key) if _api_key else None

# Fast, free model options on Groq
MODEL_NAME = "llama-3.3-70b-versatile"  # Free, 14,400 req/day


def call_llm(prompt: str) -> str:
    """Call Groq API with the given prompt."""
    if _client is None:
        return (
            "⚠️ AI responses not configured. "
            "Please set GROQ_API_KEY in Render environment variables. "
            "Get a free key at: https://console.groq.com"
        )
    try:
        response = _client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            max_tokens=1024,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Sorry, I encountered an error: {str(e)}"


def extract_topic(student_message: str) -> str:
    """Extract the main study topic from a student message."""
    if _client is None:
        return student_message[:30].lower().strip()
    try:
        response = _client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "user",
                    "content": (
                        f"Extract the main study topic from this message. "
                        f"Return ONLY a short topic name (2-5 words), nothing else.\n\n"
                        f"Message: \"{student_message}\"\nTopic:"
                    )
                }
            ],
            max_tokens=20,
            temperature=0.1,
        )
        topic = response.choices[0].message.content.strip().lower()
        return topic[:50] if topic else student_message[:30].lower()
    except Exception:
        return student_message[:30].lower().strip()


def build_prompt(student_message: str, chat_history: list, weak_topics: list) -> str:
    """Build a prompt including chat history context."""
    history_text = ""
    for msg in chat_history[-10:]:
        role = "Student" if msg.get("role") == "student" else "Teacher"
        history_text += f"{role}: {msg.get('content', '')}\n"

    weak_text = ""
    if weak_topics:
        weak_text = f"\nNote: Student's weak topics: {', '.join(weak_topics)}\n"

    return f"{history_text}{weak_text}Student: {student_message}"


def teacher_reply(student_message: str, chat_history: list, weak_topics: list) -> str:
    """Generate a teacher reply using Groq."""
    if _client is None:
        return call_llm("")  # Returns the not-configured message

    try:
        # Build message history for Groq
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]

        # Add last 10 messages of history
        for msg in chat_history[-10:]:
            role = "user" if msg.get("role") == "student" else "assistant"
            messages.append({"role": role, "content": msg.get("content", "")})

        # Add weak topics context if any
        user_msg = student_message
        if weak_topics:
            user_msg = f"[Student's weak topics: {', '.join(weak_topics)}]\n\n{student_message}"

        messages.append({"role": "user", "content": user_msg})

        response = _client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            max_tokens=1024,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Sorry, I encountered an error: {str(e)}"


def generate_quiz(topic: str, mastery_score: float) -> str:
    """Generate a quiz question for the given topic."""
    difficulty = "easy" if mastery_score < 0.4 else ("medium" if mastery_score < 0.7 else "hard")
    prompt = (
        f"Generate a single {difficulty} multiple choice quiz question about: {topic}\n\n"
        f"Format exactly like this:\n"
        f"Question: [question here]\n"
        f"A) [option]\nB) [option]\nC) [option]\nD) [option]\n"
        f"Answer: [correct letter]"
    )
    return call_llm(prompt)