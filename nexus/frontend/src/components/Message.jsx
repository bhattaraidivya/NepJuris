export default function Message({ message }) {

  const isUser = message.role === "user";

  return (
    <div
      className={`flex ${
        isUser
          ? "justify-end"
          : "justify-start"
      }`}
    >
      <div
        className={`max-w-xl px-4 py-3 rounded-2xl ${
          isUser
            ? "bg-white text-black"
            : "bg-zinc-800 text-white"
        }`}
      >
        {message.text}
      </div>
    </div>
  );
}