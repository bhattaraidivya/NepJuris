import Message from "./Message";

export default function ChatBox({ messages }) {
  return (
    <div className="space-y-4">
      {messages.map((msg, i) => (
        <Message key={i} message={msg} />
      ))}
    </div>
  );
}