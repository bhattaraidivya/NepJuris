frontend structure 
frontend/

├── src/
│
├── pages/
│   ├── Home.jsx
│   └── Chat.jsx
|   |__ Docs.jsx
│
├── components/
│   ├── Sidebar.jsx
│   ├── ChatBox.jsx
│   ├── Message.jsx
│   ├── InputBox.jsx
│   ├── Navbar.jsx
│   └── Features.jsx
|   |__ ChatAre.jsx
│
├── services/
│   └── api.js
│
├── hooks/
│   └── useChat.js 
│
└── core/
├── contracts.js
└── apicontract.js


Chat.jsx 

import useChat from "../hooks/useChat";
import Sidebar from "../components/Sidebar";
import ChatArea from "../components/ChatArea";

export default function Chat() {
  const chat = useChat();


  return (
    <div className="h-screen flex flex-row bg-zinc-950 text-white overflow-hidden">

      <Sidebar {...chat} />

      <ChatArea {...chat} />

    </div>
  );
}
Docs.jsx 

import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

const BASE_URL = "http://127.0.0.1:8000";

export default function Docs() {
  const [documents, setDocuments] = useState([]);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);

  const navigate = useNavigate();

  useEffect(() => {
    fetch(`${BASE_URL}/documents`)
      .then((res) => res.json())
      .then((data) => {
        setDocuments(data.documents || []);
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setLoading(false);
      });
  }, []);

  const filteredDocs = documents.filter((doc) =>
    doc.name.toLowerCase().includes(search.toLowerCase())
  );

  // 💬 Ask AI with context
  const handleAskAI = (doc) => {
    navigate("/chat", {
      state: {
        message: `Ask questions about: "${doc.name}".`
      }
    });
  };

  // ⬇ Download PDF
  const handleDownload = (docId) => {
    window.open(
      `${BASE_URL}/documents/${docId}/download`,
      "_blank"
    );
  };

  return (
    <div className="min-h-screen p-8 bg-gray-50">

      {/* Header */}
      <div className="mb-8">
        <h1 className="text-4xl font-bold">
          📚 Legal Knowledge Base
        </h1>

        <p className="text-gray-600 mt-2">
          Browse Nepal’s legal documents used by NyayaAI.
        </p>
      </div>

      {/* Search */}
      <div className="mb-6">
        <input
          type="text"
          placeholder="Search documents..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="w-full p-3 border rounded-lg"
        />
      </div>

      {/* Loading */}
      {loading ? (
        <p className="text-gray-500">Loading documents...</p>
      ) : (
        <div className="grid gap-5 md:grid-cols-2 lg:grid-cols-3">

          {filteredDocs.map((doc) => (
            <div
              key={doc.id}
              className="bg-white border rounded-xl p-5 shadow-sm hover:shadow-md transition"
            >

              {/* Title */}
              <h2 className="text-xl font-semibold mb-3">
                {doc.name}
              </h2>

              {/* Metadata */}
              <div className="space-y-1 text-sm text-gray-600">
                <p><strong>Category:</strong> {doc.category}</p>
                <p><strong>Language:</strong> {doc.language}</p>
                <p><strong>Type:</strong> {doc.type}</p>
                <p><strong>Status:</strong> {doc.status}</p>
              </div>

              {/* Actions */}
              <div className="mt-4 flex gap-2">

                {/* DOWNLOAD */}
                <button
                  onClick={() => handleDownload(doc.id)}
                  className="px-4 py-2 rounded-lg bg-black text-white"
                >
                  Download
                </button>

                {/* ASK AI */}
                <button
                  onClick={() => handleAskAI(doc)}
                  className="px-4 py-2 rounded-lg border bg-blue-50 hover:bg-blue-100"
                >
                  Ask AI
                </button>

              </div>
            </div>
          ))}

        </div>
      )}
    </div>
  );
}
api.js
import { normalizeChatResponse } from "../core/apiContract";

const BASE_URL = "http://127.0.0.1:8000";

export async function sendMessage(message) {
  try {
    const res = await fetch(`${BASE_URL}/chat`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message }),
    });

    // If backend fails (important for stability)
    if (!res.ok) {
      console.error("HTTP Error:", res.status);
      return "Server error. Try again.";
    }

    const data = await res.json();

    console.log("RAW BACKEND RESPONSE:", data);

    // backend format: { response: "..." }
    return normalizeChatResponse(data).response;

  } catch (error) {
    console.error("Network Error:", error);
    return "Cannot connect to backend.";
  }
}

input box

import { useState } from "react";

export default function InputBox({ onSend }) {

  const [text, setText] = useState("");

  const handleSend = () => {
    if (!text.trim()) return;

    onSend(text);

    setText("");
  };

  return (
    <div className="p-4 border-t border-zinc-800 flex gap-2">

      <input
        className="flex-1 bg-zinc-900 px-4 py-3 rounded-xl outline-none text-sm"
        placeholder="Ask about Nepal law..."
        value={text}
        onChange={(e) => setText(e.target.value)}
        onKeyDown={(e) =>
          e.key === "Enter" && handleSend()
        }
      />

      <button
        onClick={handleSend}
        className="bg-white text-black px-5 rounded-xl text-sm hover:opacity-90 transition-opacity"
      >
        Send
      </button>

    </div>
  );
}

chatare.jsx

import ChatBox from "./ChatBox";
import InputBox from "./InputBox";

export default function ChatArea({
  currentChat,
  loading,
  bottomRef,
  handleSend,
}) {
  return (
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
  );
}

home.jsx 
import Navbar from "../components/Navbar";
import Hero from "../components/Hero";
import Features from "../components/Features";
import Message from "../components/Message";

export default function Home() {
  return (
    <div className="min-h-screen bg-zinc-950 text-white">
      <Navbar />
      <Hero />
      <Features />
      <Message />

    </div>
  );
}