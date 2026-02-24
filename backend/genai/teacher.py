import requests
from ..genai.prompts import SYSTEM_PROMPT

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3"


# -----------------------------
# Internal LLM Caller (HTTP API)
# -----------------------------
def call_llm(prompt: str) -> str:
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False
        },
        timeout=120
    )

    return response.json()["response"].strip()


# -----------------------------
# Topic Extraction
# -----------------------------
def extract_topic(student_message: str) -> str:
    prompt = f"""
Extract the main study topic from the following message.
Return ONLY a short topic name (2-5 words).
Do not explain anything.

Message: "{student_message}"
Topic:
"""
    return call_llm(prompt).lower()


# -----------------------------
# Shared Prompt Builder
# -----------------------------
def build_prompt(student_message, chat_history, weak_topics):
    prompt = SYSTEM_PROMPT

    if weak_topics:
        prompt += (
            f"\nIMPORTANT: The student is likely to forget: {', '.join(weak_topics)}.\n"
            "Focus more on these topics. Ask diagnostic questions before explaining.\n"
            "Generate quizzes to reinforce learning.\n"
        )

    for msg in chat_history:
        prompt += f"{msg['role']}: {msg['content']}\n"

    prompt += f"student: {student_message}\nteacher:"
    return prompt


# -----------------------------
# Normal Response Mode
# -----------------------------
def teacher_reply(student_message, chat_history, weak_topics):
    prompt = build_prompt(student_message, chat_history, weak_topics)
    return call_llm(prompt)


# -----------------------------
# Quiz Generator
# -----------------------------
def generate_quiz(topic, mastery_score=0.5):

    if mastery_score < 0.4:
        difficulty = "Ask a simple recall question."
    elif mastery_score < 0.7:
        difficulty = "Ask an applied understanding question."
    else:
        difficulty = "Ask a challenging conceptual reasoning question."

    prompt = f"""
Topic: {topic}

{difficulty}

Generate:
Question: <one short question>
Answer: <correct short answer>

Return exactly in this format:
Question: ...
Answer: ...
"""

    response = call_llm(prompt)

    question = ""
    answer = ""

    for line in response.splitlines():
        if line.lower().startswith("question:"):
            question = line.split("Question:", 1)[1].strip()
        elif line.lower().startswith("answer:"):
            answer = line.split("Answer:", 1)[1].strip()

    return question, answer