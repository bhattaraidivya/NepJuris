export type MessageRole = "user" | "ai";
export type MessageType = "text" | "typing" | "error";

export interface ChatMessage {
  id: string;
  role: MessageRole;
  content: string;
  type: MessageType;
  timestamp: number;
}

export interface Chat {
  id: string;
  title: string;
  messages: ChatMessage[];
}

export interface Source {
  title: string;
  page?: number;
  chunk?: string;
}

export interface ChatResponse {
  response: string;
  sources?: Source[];
}

/**
 * IMPORTANT: Use contracts.ts for runtime logic
 */
export interface UseChatReturn {
  conversations: Chat[];
  currentChatId: string | null;
  setCurrentChatId: (id: string | null) => void;
  currentChat: Chat | undefined;
  loading: boolean;
  bottomRef: React.RefObject<HTMLDivElement | null>;

  editingChatId: string | null;
  editingTitle: string;
  setEditingTitle: (v: string) => void;

  createNewChat: () => string;
  deleteChat: (id: string) => void;

  startRename: (chat: Chat) => void;
  saveRename: () => void;
  cancelRename: () => void;

  handleSend: (text: string) => Promise<void>;
}