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