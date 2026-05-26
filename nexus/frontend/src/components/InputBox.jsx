import { useState } from "react";

export default function InputBox({ onSend }) {
  const [text, setText] = useState("");

  const send = () => {
    onSend(text);
    setText("");
  };

  return (
    <div className="p-4 flex gap-2 border-t border-zinc-800">
      <input
        className="flex-1 bg-zinc-900 px-4 py-2 rounded-xl"
        value={text}
        onChange={(e) => setText(e.target.value)}
        onKeyDown={(e) => e.key === "Enter" && send()}
      />

      <button
        onClick={send}
        className="bg-white text-black px-4 rounded-xl"
      >
        Send
      </button>
    </div>
  );
}