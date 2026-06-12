import { useState } from "react";

type Props = {
  onSend: (text: string) => void;
  loading?: boolean;
};

export default function InputBox({ onSend, loading }: Props) {
  const [text, setText] = useState<string>("");

  const handleSend = () => {
    if (!text.trim() || loading) return;
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
        onKeyDown={(e) => {
          if (e.key === "Enter") handleSend();
        }}
      />

      <button
        onClick={handleSend}
        disabled={loading}
        className="bg-white text-black px-4 py-2 rounded-xl text-sm hover:opacity-90 transition disabled:opacity-50"
      >
        Send
      </button>

    </div>
  );
}