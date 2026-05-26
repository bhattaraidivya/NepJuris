import { useState } from "react";
import ChatBox from "../components/ChatBox";
import InputBox from "../components/InputBox";
import { sendMessage } from "../services/api";

export default function Chat() {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSend = async (text) => {
    if (!text.trim()) return;

    // add user message
    setMessages((prev) => [
      ...prev,
      { role: "user", text:text }
    ]);

    setLoading(true);

    try {
      // get AI response
      const response = await sendMessage(text);
      

      // add AI message
      setMessages((prev) => [
        ...prev,
        { role: "ai", text: response }
      ]);

    } catch (error) {
      
      setMessages((prev) => [
        ...prev,
        {
          role: "ai",
          text: "Error connecting to backend."
        }
      ]);
    }

    setLoading(false);
  };

  return (
    <div className="h-screen bg-zinc-950 text-white flex flex-col">

      {/* HEADER */}
      <div className="p-4 border-b border-zinc-800 text-center font-bold">
        NyayaAI ⚖️
      </div>

      {/* CHAT AREA */}
      <div className="flex-1 overflow-y-auto p-4">
        <ChatBox messages={messages} />

        {loading && (
          <div className="text-zinc-500 mt-2">
            AI is thinking...
          </div>
        )}
      </div>

      {/* INPUT */}
      <InputBox onSend={handleSend} />
    </div>
  );
}