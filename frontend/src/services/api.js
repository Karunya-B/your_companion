const BASE_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000/api/v1";

export async function fetchDailyGuidance() {
  const res = await fetch(`${BASE_URL}/generate_daily_guidance`);
  if (!res.ok) throw new Error("Failed to fetch guidance");
  return res.json();
}

export async function sendChatMessage(message) {
  const res = await fetch(`${BASE_URL}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message }),
  });
  if (!res.ok) throw new Error("Failed to send chat message");
  return res.json();
}

export async function getChatHistory() {
  const res = await fetch(`${BASE_URL}/chat/history`);
  if (!res.ok) throw new Error("Failed to fetch chat history");
  return res.json();
}

export async function saveChatMessage(role, content) {
  const res = await fetch(`${BASE_URL}/chat/save`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ role, content }),
  });
  if (!res.ok) throw new Error("Failed to save chat message");
  return res.json();
}

export async function resetData() {
  const res = await fetch(`${BASE_URL}/reset`, {
    method: "DELETE",
  });
  if (!res.ok) throw new Error("Failed to reset data");
  return res.json();
}

export async function logReflection(content) {
  const res = await fetch(`${BASE_URL}/log_reflection`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ content }),
  });
  if (!res.ok) throw new Error("Failed to log reflection");
  return res.json();
}

export async function logSleepData(data) {
  const res = await fetch(`${BASE_URL}/log_sleep_data`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error("Failed to log sleep data");
  return res.json();
}

export async function logScreenTime(data) {
  const res = await fetch(`${BASE_URL}/log_screen_time`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error("Failed to log screen time");
  return res.json();
}
