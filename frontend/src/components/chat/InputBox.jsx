import { useState } from "react";

export default function InputBox({ onSend }) {
  const [text, setText] = useState("");

  const handleSend = () => {
    if (!text.trim()) return;
    onSend(text);
    setText("");
  };

  return (
    <div className="flex items-center gap-2 p-3">

      <input
        className="flex-1 bg-transparent outline-none text-sm text-white placeholder:text-zinc-500"
        placeholder="Ask about Nepal law..."
        value={text}
        onChange={(e) => setText(e.target.value)}
        onKeyDown={(e) => e.key === "Enter" && handleSend()}
      />

      <button
        onClick={handleSend}
        className="bg-white text-black px-4 py-2 rounded-xl text-sm hover:opacity-90 transition"
      >
        Send
      </button>

    </div>
  );
}