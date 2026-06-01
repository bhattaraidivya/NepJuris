import { normalizeChatResponse } from "../core/apiContract";

const BASE_URL = "http://127.0.0.1:8000";

export async function sendMessage(message) {
  try {
    const res = await fetch(`${BASE_URL}/chat`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message }),
    });

    // If backend fails (important for stability)
    if (!res.ok) {
      console.error("HTTP Error:", res.status);
      return "Server error. Try again.";
    }

    const data = await res.json();

    console.log("RAW BACKEND RESPONSE:", data);

    // backend format: { response: "..." }
    return normalizeChatResponse(data).response;

  } catch (error) {
    console.error("Network Error:", error);
    return "Cannot connect to backend.";
  }
}