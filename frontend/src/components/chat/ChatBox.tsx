import Message from "./Message";
import type { ChatMessage } from "../../types/chat.types";

type Props = {
  messages: ChatMessage[];
};

export default function ChatBox({ messages }: Props) {
  return (
    <div className="space-y-4">
      {messages.map((msg) => (
        <Message key={msg.id} message={msg} />
      ))}
    
    </div>
  );
}