export default function Message({ message }) {
  if (!message) return null;

  const isUser = message.role === "user";

  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"}`}>

      <div
        className={`
          max-w-[75%]
          px-4 py-3
          rounded-2xl
          text-sm
          leading-relaxed
          ${
            isUser
              ? "bg-white text-black rounded-br-sm"
              : "bg-zinc-800 text-white rounded-bl-sm"
          }
        `}
      >
        {message.text || ""}
      </div>

    </div>
  );
}