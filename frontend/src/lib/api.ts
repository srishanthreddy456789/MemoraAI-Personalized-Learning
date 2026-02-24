// frontend/src/lib/api.ts

const API_BASE = "http://127.0.0.1:8000";

export async function fetchSessions(): Promise<string[]> {
  const res = await fetch(`${API_BASE}/sessions`);
  return res.json();
}

export async function sendMessage(
  session_id: string,
  message: string
): Promise<{ reply: string }> {
  const res = await fetch(
    `${API_BASE}/chat?session_id=${session_id}&message=${encodeURIComponent(
      message
    )}`,
    { method: "POST" }
  );

  return res.json();
}