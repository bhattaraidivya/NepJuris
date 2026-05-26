import { useState } from "react";
import ChatBox from "../components/ChatBox";
import InputBox from "../components/InputBox";
import { sendMessage } from "../services/api";

export default function Chat() {
  const [messages, setMessages] = useState([]);

  const handleSend = async (text) => {
    if (!text.trim()) return;

    setMessages((prev) => [...prev, { role: "user", text }]);

    const res = await sendMessage(text);

    setMessages((prev) => [
      ...prev,
      { role: "ai", text: res }
    ]);
  };

  return (
    <div className="h-screen flex flex-col bg-zinc-950 text-white">
      <div className="p-4 border-b border-zinc-800 text-center">
        NyayaAI ⚖️
      </div>

      <div className="flex-1 overflow-y-auto p-4">
        <ChatBox messages={messages} />
      </div>

      <InputBox onSend={handleSend} />
    </div>
  );
}