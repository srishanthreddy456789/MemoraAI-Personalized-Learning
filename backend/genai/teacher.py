import subprocess
from genai.prompts import SYSTEM_PROMPT

def call_llm(prompt: str) -> str:
    result = subprocess.run(
        ["ollama", "run", "llama3"],
        input=prompt,
        text=True,
        capture_output=True
    )
    return result.stdout.strip()


def teacher_reply(student_message, chat_history, weak_topics):
    prompt = SYSTEM_PROMPT
    prompt += f"\nStudent weak topics: {weak_topics}\n\n"

    for msg in chat_history:
        prompt += f"{msg['role']}: {msg['content']}\n"

    prompt += f"student: {student_message}\nteacher:"

    return call_llm(prompt)