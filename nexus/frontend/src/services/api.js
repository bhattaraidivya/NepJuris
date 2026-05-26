const BASE_URL = "http://127.0.0.1:8000";

export async function sendMessage(message) {
  const response = await fetch(`${BASE_URL}/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ message }),
  });

  const data = await response.json();


  return data.response;
}
