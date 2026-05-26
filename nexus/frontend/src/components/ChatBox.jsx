import Message from "./Message";

export default function ChatBox({ messages }) {
  return (
    <div className="space-y-3">
      {messages.map((m, i) => (
        <Message key={i} message={m} />
      ))}
    </div>
  );
}