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

export function normalizeChatResponse(data: any): ChatResponse {
  const rawSources = Array.isArray(data?.sources) ? data.sources : [];

  return {
    response: data?.response || "",
    sources: rawSources.map(normalizeSource),
  };
}
