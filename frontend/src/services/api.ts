import { normalizeChatResponse } from "../core/apicontract";
import type { ChatResponse } from "../types/chat.types";
const BASE_URL = "http://127.0.0.1:8000";

export async function sendMessage(
  message: string
): Promise<ChatResponse> {
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
       return {
        response: "Server error. Try again.",
        sources: [],
      };
      
    }

    const data: unknown = await res.json();

    console.log("RAW BACKEND RESPONSE:", data);

    // backend format: { response: "..." }
    return normalizeChatResponse(data);

  } catch (error) {
    console.error("Network Error:", error);
    return {
      response: "Cannot connect to backend.",
      sources: [],
    };
  }
}