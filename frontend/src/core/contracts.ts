import type { ChatMessage, Source } from "../types/chat.types";

/**
 * =========================
 * SINGLE SOURCE OF TRUTH (RUNTIME)
 * =========================
 */

export const MessageRole = {
  USER: "user",
  AI: "ai",
} as const;

export const MessageType = {
  TEXT: "text",
  TYPING: "typing",
  ERROR: "error",
} as const;

/**
 * =========================
 * DERIVED TYPES (NO DUPLICATION)
 * =========================
 */

export type MessageRoleType =
  (typeof MessageRole)[keyof typeof MessageRole];

export type MessageTypeType =
  (typeof MessageType)[keyof typeof MessageType];

/**
 * =========================
 * MESSAGE FACTORY
 * =========================
 */

export function createMessage(
  role: MessageRoleType,
  content: string,
  type: MessageTypeType = MessageType.TEXT,
  sources?: Source[]
): ChatMessage {
  return {
    id: Date.now().toString(),
    role,
    content,
    type,
    timestamp: Date.now(),
    ...(sources ? { sources } : {}),
  };
}