import { useState, useEffect, useRef } from "react";
import { sendMessage } from "../services/api";
import { MessageRole, createMessage } from "../core/contracts";

const STORAGE_KEY = "nyayaai_conversations";
const ACTIVE_CHAT_KEY = "nyayaai_active_chat";

export default function useChat() {
  const [conversations, setConversations] = useState(() => {
    const saved = localStorage.getItem(STORAGE_KEY);
    return saved ? JSON.parse(saved) : [];
  });

  const [currentChatId, setCurrentChatId] = useState(null);
  

  const [loading, setLoading] = useState(false);

  const [editingChatId, setEditingChatId] = useState(null);
  const [editingTitle, setEditingTitle] = useState("");

  const bottomRef = useRef(null);

  const currentChat = conversations.find(
    (c) => c.id === currentChatId
  );

  // =========================
  // TITLE GENERATOR
  // =========================
  const generateTitle = (text) => {
    const cleaned = text
      .replace(/\n/g, " ")
      .trim()
      .toLowerCase();

    const stopWords = [
      "what", "why", "how", "is", "are", "the", "a", "an",
      "explain", "tell", "me", "about", "can", "you"
    ];

    const words = cleaned
      .split(" ")
      .filter(word => !stopWords.includes(word))
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
  // CREATE CHAT (FIXED)
  // =========================
  const createNewChat = () => {
    const newChat = {
      id: Date.now().toString(),
      title: "New Chat", // fallback only
      messages: [],
    };

    setConversations((prev) => [newChat, ...prev]);
    setCurrentChatId(newChat.id);

    return newChat.id;
  };

  // =========================
  // DELETE CHAT
  // =========================
  const deleteChat = (chatId) => {
    const updated = conversations.filter(
      (chat) => chat.id !== chatId
    );

    setConversations(updated);

    if (chatId === currentChatId) {
      setCurrentChatId(updated.length ? updated[0].id : null);
    }
  };

  // =========================
  // RENAME CHAT
  // =========================
  const startRename = (chat) => {
    setEditingChatId(chat.id);
    setEditingTitle(chat.title);
  };

  const saveRename = () => {
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

  const cancelRename = () => {
    setEditingChatId(null);
    setEditingTitle("");
  };

  // =========================
  // SEND MESSAGE (FIXED TITLE LOGIC)
  // =========================
  const handleSend = async (text) => {
    if (!text.trim()) return;

    let chatId = currentChatId;

    // 1. CREATE CHAT IF NONE EXISTS
    if (!chatId) {
      chatId = Date.now().toString();

      const newChat = {
        id: chatId,
        title: "New Chat",
        messages: [],
      };

      setConversations((prev) => [newChat, ...prev]);
      setCurrentChatId(chatId);
    }

    const userMessage = createMessage(MessageRole.USER, text);

    // 2. ADD USER MESSAGE + UPDATE TITLE HERE (IMPORTANT FIX)
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

    // 3. TYPING INDICATOR
    const typingMessage = {
      id: "typing",
      role: MessageRole.AI,
      type: "typing",
      text: "",
    };

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
        response
      );

      setConversations((prev) =>
        prev.map((chat) =>
          chat.id === chatId
            ? {
                ...chat,
                messages: chat.messages
                  .filter((m) => m.type !== "typing")
                  .concat(aiMessage),
              }
            : chat
        )
      );

    } catch (err) {
      setConversations((prev) =>
        prev.map((chat) =>
          chat.id === chatId
            ? {
                ...chat,
                messages: chat.messages
                  .filter((m) => m.type !== "typing")
                  .concat(
                    createMessage(
                      MessageRole.AI,
                      "Error connecting to backend."
                    )
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