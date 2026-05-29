import { useState, useEffect, useRef } from "react";
import ChatBox from "../components/ChatBox";
import InputBox from "../components/InputBox";
import { sendMessage } from "../services/api";
import { MessageRole, createMessage } from "../core/contracts";

const STORAGE_KEY = "nyayaai_conversations";
const ACTIVE_CHAT_KEY = "nyayaai_active_chat";

export default function Chat() {
  const [conversations, setConversations] = useState(() => {
    const saved = localStorage.getItem(STORAGE_KEY);
    return saved ? JSON.parse(saved) : [];
  });

  const [currentChatId, setCurrentChatId] = useState(() => {
    return localStorage.getItem(ACTIVE_CHAT_KEY) || null;
  });

  const [loading, setLoading] = useState(false);

  const bottomRef = useRef(null);

  // 🆕 rename states
  const [editingChatId, setEditingChatId] = useState(null);
  const [editingTitle, setEditingTitle] = useState("");

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

  // 🗑 DELETE CHAT
  const deleteChat = (chatId) => {
    const updated = conversations.filter(
      (chat) => chat.id !== chatId
    );

    setConversations(updated);

    if (chatId === currentChatId) {
      if (updated.length > 0) {
        setCurrentChatId(updated[0].id);
      } else {
        setCurrentChatId(null);
      }
    }
  };

  // ✏ START RENAME
  const startRename = (chat) => {
    setEditingChatId(chat.id);
    setEditingTitle(chat.title);
  };

  // 💾 SAVE RENAME
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

  // ❌ CANCEL RENAME
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
          ? {
              ...chat,
              messages: [...chat.messages, userMessage],
            }
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
                messages: [
                  ...chat.messages.filter(
                    (m) => m.type !== "typing"
                  ),
                  aiMessage,
                ],
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
                messages: [
                  ...chat.messages.filter(
                    (m) => m.type !== "typing"
                  ),
                  createMessage(
                    MessageRole.AI,
                    "Error connecting to backend."
                  ),
                ],
              }
            : chat
        )
      );
    }

    setLoading(false);
  };

  return (
    <div className="h-screen flex flex-row bg-zinc-950 text-white overflow-hidden">

      {/* SIDEBAR */}
      <div className="w-64 h-full border-r border-zinc-800 flex flex-col">

        <div className="p-3 border-b border-zinc-800">
          <button
            onClick={createNewChat}
            className="w-full bg-white text-black py-2 rounded-lg text-sm font-medium"
          >
            + New Chat
          </button>
        </div>

        <div className="flex-1 overflow-y-auto px-2 py-2 space-y-1">

          {conversations.length === 0 && (
            <div className="text-xs text-zinc-500 p-2">
              No conversations yet
            </div>
          )}

          {conversations.map((chat) => (
            <div
              key={chat.id}
              onClick={() => setCurrentChatId(chat.id)}
              className={`
                group
                flex items-center justify-between
                p-2 rounded
                cursor-pointer
                text-sm
                transition
                ${
                  chat.id === currentChatId
                    ? "bg-zinc-800"
                    : "hover:bg-zinc-900"
                }
              `}
            >

              {/* TITLE / INLINE EDIT */}
              <div className="flex-1 truncate">
                {editingChatId === chat.id ? (
                  <input
                    autoFocus
                    value={editingTitle}
                    onChange={(e) =>
                      setEditingTitle(e.target.value)
                    }
                    onBlur={saveRename}
                    onKeyDown={(e) => {
                      if (e.key === "Enter") saveRename();
                      if (e.key === "Escape") cancelRename();
                    }}
                    className="w-full bg-zinc-900 text-white px-2 py-1 rounded outline-none"
                  />
                ) : (
                  chat.title
                )}
              </div>

              {/* ACTIONS */}
              {editingChatId !== chat.id && (
                <div className="hidden group-hover:flex items-center gap-2 ml-2">

                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      startRename(chat);
                    }}
                    className="text-zinc-400 hover:text-white"
                  >
                    ✏
                  </button>

                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      deleteChat(chat.id);
                    }}
                    className="text-zinc-400 hover:text-red-400"
                  >
                    🗑
                  </button>

                </div>
              )}

            </div>
          ))}
        </div>
      </div>

      {/* CHAT AREA */}
      <div className="flex-1 flex flex-col overflow-hidden">

        <div className="flex-1 overflow-y-auto py-6">
          <div className="max-w-3xl mx-auto w-full px-4">

            {currentChat ? (
              <>
                <ChatBox messages={currentChat.messages} />

                {loading && (
                  <div className="mt-3 flex gap-1">
                    <span className="w-2 h-2 bg-zinc-500 rounded-full animate-bounce"></span>
                    <span className="w-2 h-2 bg-zinc-500 rounded-full animate-bounce [animation-delay:0.2s]"></span>
                    <span className="w-2 h-2 bg-zinc-500 rounded-full animate-bounce [animation-delay:0.4s]"></span>
                  </div>
                )}

                <div ref={bottomRef} />
              </>
            ) : (
              <div className="text-zinc-500 text-center mt-10">
                Start a new conversation
              </div>
            )}

          </div>
        </div>

        <div className="border-t border-zinc-800 p-4">
          <div className="max-w-3xl mx-auto">
            <InputBox onSend={handleSend} loading={loading} />
          </div>
        </div>

      </div>
    </div>
  );
}