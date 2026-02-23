import subprocess
from ..genai.prompts import SYSTEM_PROMPT


# -----------------------------
# Topic Extraction (NEW)
# -----------------------------
def extract_topic(student_message: str) -> str:
    prompt = f"""
Extract the main study topic from the following message.
Return ONLY a short topic name (2-5 words).
Do not explain anything.

Message: "{student_message}"
Topic:
"""

    result = subprocess.run(
        ["ollama", "run", "llama3"],
        input=prompt,
        text=True,
        capture_output=True
    )

    return result.stdout.strip().lower()


# -----------------------------
# Shared Prompt Builder
# -----------------------------
def build_prompt(student_message, chat_history, weak_topics):
    prompt = SYSTEM_PROMPT

    if weak_topics:
        prompt += (
            f"IMPORTANT: The student is likely to forget: {', '.join(weak_topics)}. "
            "Focus more on these topics. Ask diagnostic questions before explaining.\n"
            "Generate quizzes to reinforce learning.\n"
        )

    for msg in chat_history:
        prompt += f"{msg['role']}: {msg['content']}\n"

    prompt += f"student: {student_message}\nteacher:"

    return prompt


# -----------------------------
# Normal (Full) Response Mode
# -----------------------------
def call_llm(prompt: str) -> str:
    result = subprocess.run(
        ["ollama", "run", "llama3"],
        input=prompt,
        text=True,
        capture_output=True
    )
    return result.stdout.strip()


def teacher_reply(student_message, chat_history, weak_topics):
    prompt = build_prompt(student_message, chat_history, weak_topics)
    return call_llm(prompt)


# -----------------------------
# Streaming Mode
# -----------------------------
def call_llm_stream(prompt: str):
    process = subprocess.Popen(
        ["ollama", "run", "llama3"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="ignore",
        bufsize=1
    )

    process.stdin.write(prompt)
    process.stdin.close()

    for line in process.stdout:
        yield line

    process.stdout.close()
    process.wait()


def teacher_reply_stream(student_message, chat_history, weak_topics):
    prompt = build_prompt(student_message, chat_history, weak_topics)
    return call_llm_stream(prompt)

def generate_quiz(topic: str) -> str:
    prompt = f"""
Generate 1 short quiz question about {topic}.
Provide the correct answer clearly.
Format:

Question:
...
Answer:
...
"""
    return call_llm(prompt)