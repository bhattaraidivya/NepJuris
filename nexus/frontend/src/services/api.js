import { normalizeChatResponse } from "../core/apiContract";

const BASE_URL = "http://127.0.0.1:8000";

export async function sendMessage(message) {

  const res = await fetch(`${BASE_URL}/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ message }),
  });

  const data = await res.json();

  console.log("RAW API:", data);

  return normalizeChatResponse(data).response;
}