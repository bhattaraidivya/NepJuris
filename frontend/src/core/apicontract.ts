import type { ChatResponse, Source } from "../types/chat.types";

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
