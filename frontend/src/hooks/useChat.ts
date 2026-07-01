import { useState, useEffect, useRef } from "react";
import { sendMessage } from "../services/api";
import { MessageRole, MessageType, createMessage } from "../core/contracts";
import type { ChatMessage, UseChatReturn } from "../types/chat.types";

type Chat = {
  id: string;
  title: string;
  messages: ChatMessage[];
};

const STORAGE_KEY = "nyayaai_conversations";
const ACTIVE_CHAT_KEY = "nyayaai_active_chat";

export default function useChat(): UseChatReturn {
  const [conversations, setConversations] = useState<Chat[]>(() => {
    const saved = localStorage.getItem(STORAGE_KEY);
    try {
      return saved ? (JSON.parse(saved) as Chat[]) : [];
    } catch {
      return [];
    }
  });

  const [currentChatId, setCurrentChatId] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(false);

  const [editingChatId, setEditingChatId] = useState<string | null>(null);
  const [editingTitle, setEditingTitle] = useState<string>("");

  const bottomRef = useRef<HTMLDivElement | null>(null);

  const currentChat: Chat | undefined = conversations.find(
    (c) => c.id === currentChatId
  );

  // =========================
  // TITLE GENERATOR
  // =========================
  const generateTitle = (text: string): string => {
    const cleaned = text
      .replace(/\n/g, " ")
      .trim()
      .toLowerCase();

    const stopWords = [
      "what",
      "why",
      "how",
      "is",
      "are",
      "the",
      "a",
      "an",
      "explain",
      "tell",
      "me",
      "about",
      "can",
      "you",
    ];

    const words = cleaned
      .split(" ")
      .filter((word) => !stopWords.includes(word))
      .slice(0, 5);

    const title = words.join(" ");

    return title
      ? title.charAt(0).toUpperCase() + title.slice(1)
      : "New Chat";
  };

  // =========================
  // PERSISTENCE
  // =========================
  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(conversations));
  }, [conversations]);

  useEffect(() => {
    if (currentChatId) {
      localStorage.setItem(ACTIVE_CHAT_KEY, currentChatId);
    }
  }, [currentChatId]);

  // =========================
  // AUTO SCROLL
  // =========================
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [conversations, currentChatId, loading]);

  // =========================
  // CREATE CHAT
  // =========================
  const createNewChat = (): string => {
    const newChat: Chat = {
      id: Date.now().toString(),
      title: "New Chat",
      messages: [],
    };

    setConversations((prev) => [newChat, ...prev]);
    setCurrentChatId(newChat.id);

    return newChat.id;
  };

  // =========================
  // DELETE CHAT
  // =========================
  const deleteChat = (chatId: string): void => {
    const updated = conversations.filter((chat) => chat.id !== chatId);

    setConversations(updated);

    if (chatId === currentChatId) {
     setCurrentChatId(updated[0]?.id ?? null);
    }
  };

  // =========================
  // RENAME CHAT
  // =========================
  const startRename = (chat: Chat): void => {
    setEditingChatId(chat.id);
    setEditingTitle(chat.title);
  };

  const saveRename = (): void => {
    if (!editingTitle.trim()) return;

    setConversations((prev) =>
      prev.map((chat) =>
        chat.id === editingChatId
          ? { ...chat, title: editingTitle.trim() }
          : chat
      )
    );

    setEditingChatId(null);
    setEditingTitle("");
  };

  const cancelRename = (): void => {
    setEditingChatId(null);
    setEditingTitle("");
  };

  // =========================
  // SEND MESSAGE
  // =========================
  const handleSend = async (text: string): Promise<void> => {
    if (!text.trim()) return;

    let chatId = currentChatId;

    // CREATE CHAT IF NONE EXISTS
    if (!chatId) {
      chatId = Date.now().toString();

      const newChat: Chat = {
        id: chatId,
        title: "New Chat",
        messages: [],
      };

      setConversations((prev) => [newChat, ...prev]);
      setCurrentChatId(chatId);
    }

    const userMessage = createMessage(
      MessageRole.USER,
      text,
      MessageType.TEXT
    );

    // ADD USER MESSAGE + TITLE UPDATE
    setConversations((prev) =>
      prev.map((chat) => {
        if (chat.id !== chatId) return chat;

        const isFirstMessage = chat.messages.length === 0;

        return {
          ...chat,
          messages: [...chat.messages, userMessage],
          title: isFirstMessage
            ? generateTitle(text)
            : chat.title,
        };
      })
    );

    // TYPING MESSAGE
    const typingMessage = createMessage(
      MessageRole.AI,
      "",
      MessageType.TYPING
    );

    setConversations((prev) =>
      prev.map((chat) =>
        chat.id === chatId
          ? {
              ...chat,
              messages: [...chat.messages, typingMessage],
            }
          : chat
      )
    );

    setLoading(true);

    try {
      const response = await sendMessage(text);

      const aiMessage = createMessage(
        MessageRole.AI,
        response.response,
        MessageType.TEXT,
        response.sources
      );

      setConversations((prev) =>
        prev.map((chat) =>
          chat.id === chatId
            ? {
                ...chat,
                messages: chat.messages
                  .filter((m) => m.type !== MessageType.TYPING)
                  .concat(aiMessage),
              }
            : chat
        )
      );
    } catch (err) {
      const errorText =
        err instanceof Error ? err.message : "Error connecting to backend.";

      setConversations((prev) =>
        prev.map((chat) =>
          chat.id === chatId
            ? {
                ...chat,
                messages: chat.messages
                  .filter((m) => m.type !== MessageType.TYPING)
                  .concat(
                    createMessage(MessageRole.AI, errorText, MessageType.ERROR)
                  ),
              }
            : chat
        )
      );
    }

    setLoading(false);
  };

  return {
    conversations,
    currentChatId,
    setCurrentChatId,
    currentChat,
    loading,
    bottomRef,

    editingChatId,
    editingTitle,
    setEditingTitle,

    createNewChat,
    deleteChat,
    startRename,
    saveRename,
    cancelRename,
    handleSend,
  };
}