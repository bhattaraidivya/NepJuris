import {MessageRole,MessageType,} from "../../core/contracts";
import type { ChatMessage } from "../../types/chat.types";

type MessageProps = {
  message: ChatMessage;
};

export default function Message({
  message,
}: MessageProps) {
  const isUser =
    message.role === MessageRole.USER;

  // =========================
  // TYPING MESSAGE
  // =========================
  if (message.type === MessageType.TYPING) {
    return (
      <div className="flex justify-start">
        <div
          className="
            max-w-[75%]
            px-4 py-3
            rounded-2xl
            text-sm
            bg-zinc-800
            text-white
            rounded-bl-sm
            italic
            opacity-70
          "
        >
          Typing...
        </div>
      </div>
    );
  }

  // =========================
  // ERROR MESSAGE
  // =========================
  if (message.type === MessageType.ERROR) {
    return (
      <div className="flex justify-start">
        <div
          className="
            max-w-[75%]
            px-4 py-3
            rounded-2xl
            text-sm
            bg-red-500/20
            text-red-300
            rounded-bl-sm
          "
        >
          {message.content}
        </div>
      </div>
    );
  }

  // =========================
  // NORMAL MESSAGE
  // =========================
  return (
    <div
      className={`flex ${
        isUser
          ? "justify-end"
          : "justify-start"
      }`}
    >
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
        {message.content}
      </div>
    </div>
  );
}