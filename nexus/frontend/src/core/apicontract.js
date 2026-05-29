export function normalizeChatResponse(data) {
  return {
    response: data?.response || "",
  };
}