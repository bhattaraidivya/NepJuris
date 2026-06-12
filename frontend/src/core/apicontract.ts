import type { ChatResponse } from "../types/chat.types";

export function normalizeChatResponse(data: any): ChatResponse {
  return {
    response: data?.response || "",
    sources: data?.sources || [],
  };
}