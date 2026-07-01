import { normalizeChatResponse } from "../core/apicontract";
import type { ChatResponse } from "../types/chat.types";
import type { DocumentMeta, UploadResult } from "../types/document.types";

const BASE_URL = import.meta.env.VITE_API_BASE_URL;

async function extractErrorMessage(res: Response, fallback: string): Promise<string> {
  const body = await res.json().catch(() => null);
  return body?.detail || fallback;
}

export async function sendMessage(message: string): Promise<ChatResponse> {
  let res: Response;
  try {
    res = await fetch(`${BASE_URL}/chat`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message }),
    });
  } catch {
    throw new Error("Cannot connect to the backend. Is the server running?");
  }

  if (!res.ok) {
    throw new Error(await extractErrorMessage(res, `Server error (${res.status})`));
  }

  const data: unknown = await res.json();
  return normalizeChatResponse(data);
}

export async function getDocuments(): Promise<{ count: number; documents: DocumentMeta[] }> {
  const res = await fetch(`${BASE_URL}/documents`);
  if (!res.ok) {
    throw new Error(await extractErrorMessage(res, `Failed to load documents (${res.status})`));
  }
  return res.json();
}

export async function uploadDocument(
  file: File,
  name: string,
  category: string
): Promise<UploadResult> {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("name", name);
  formData.append("category", category);

  let res: Response;
  try {
    res = await fetch(`${BASE_URL}/documents/upload`, {
      method: "POST",
      body: formData,
    });
  } catch {
    throw new Error("Cannot connect to the backend. Is the server running?");
  }

  if (!res.ok) {
    throw new Error(await extractErrorMessage(res, `Upload failed (${res.status})`));
  }

  return res.json();
}
