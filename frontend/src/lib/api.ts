// frontend/src/lib/api.ts
// ✅ FIXED: Use environment variable for API base URL instead of hardcoded localhost
// In Vite, env vars must be prefixed with VITE_ to be available in the browser

const API_BASE =
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

export { API_BASE };

export async function fetchSessions(token: string): Promise<{ id: string; title: string }[]> {
  const res = await fetch(`${API_BASE}/sessions`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) throw new Error("Failed to fetch sessions");
  return res.json();
}

export async function sendMessage(
  session_id: string | null,
  message: string,
  token: string
): Promise<{ reply: string; session_id: string }> {
  const res = await fetch(`${API_BASE}/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ session_id, message }),
  });
  if (!res.ok) throw new Error("Failed to send message");
  return res.json();
}
