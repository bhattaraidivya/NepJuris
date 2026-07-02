import { MessageRole, MessageType } from "./contracts";
import type { ChatHistoryTurn, ChatMessage, ChatResponse, Source } from "../types/chat.types";

interface BackendSource {
  source?: string;
  page?: string | null;
  section?: string | null;
  article?: string | null;
}

function normalizeSource(s: BackendSource): Source {
  return {
    title: s.source || "Unknown Document",
    ...(s.page ? { page: s.page } : {}),
    ...(s.section ? { section: s.section } : {}),
    ...(s.article ? { article: s.article } : {}),
  };
}

interface BackendChatResponse {
  response?: string;
  sources?: BackendSource[];
}

export function normalizeChatResponse(data: unknown): ChatResponse {
  const parsed = data as BackendChatResponse | null | undefined;
  const rawSources = Array.isArray(parsed?.sources) ? parsed.sources : [];

  return {
    response: parsed?.response || "",
    sources: rawSources.map(normalizeSource),
  };
}

/**
 * Reverse direction of normalizeChatResponse: turns our internal message
 * list into the wire shape the backend's /chat history field expects.
 */
export function toHistoryTurns(messages: ChatMessage[], maxTurns: number): ChatHistoryTurn[] {
  return messages
    .filter((m) => m.type === MessageType.TEXT)
    .slice(-maxTurns)
    .map((m) => ({
      role: m.role === MessageRole.AI ? "assistant" : "user",
      content: m.content,
    }));
}
