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

  const [currentChatId, setCurrentChatId] = useState(() => {
    return localStorage.getItem(ACTIVE_CHAT_KEY) || null;
  });

  const [loading, setLoading] = useState(false);

  const [editingChatId, setEditingChatId] = useState(null);
  const [editingTitle, setEditingTitle] = useState("");

  const bottomRef = useRef(null);

  const currentChat = conversations.find(
    (c) => c.id === currentChatId
  );

  // persist chats
  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(conversations));
  }, [conversations]);

  // persist active chat
  useEffect(() => {
    if (currentChatId) {
      localStorage.setItem(ACTIVE_CHAT_KEY, currentChatId);
    }
  }, [currentChatId]);

  // auto scroll
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [conversations, currentChatId, loading]);

  const createNewChat = () => {
    const newChat = {
      id: Date.now().toString(),
      title: "New Chat",
      messages: [],
    };

    setConversations((prev) => [newChat, ...prev]);
    setCurrentChatId(newChat.id);
  };

  const deleteChat = (chatId) => {
    const updated = conversations.filter(
      (chat) => chat.id !== chatId
    );

    setConversations(updated);

    if (chatId === currentChatId) {
      setCurrentChatId(updated.length ? updated[0].id : null);
    }
  };

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

  const handleSend = async (text) => {
    if (!text.trim()) return;

    let chatId = currentChatId;

    if (!chatId) {
      chatId = Date.now().toString();

      const newChat = {
        id: chatId,
        title: text.slice(0, 25),
        messages: [],
      };

      setConversations((prev) => [newChat, ...prev]);
      setCurrentChatId(chatId);
    }

    const userMessage = createMessage(MessageRole.USER, text);

    setConversations((prev) =>
      prev.map((chat) =>
        chat.id === chatId
          ? { ...chat, messages: [...chat.messages, userMessage] }
          : chat
      )
    );

    const typingMessage = {
      id: "typing",
      role: MessageRole.AI,
      type: "typing",
      text: "",
    };

    setConversations((prev) =>
      prev.map((chat) =>
        chat.id === chatId
          ? { ...chat, messages: [...chat.messages, typingMessage] }
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