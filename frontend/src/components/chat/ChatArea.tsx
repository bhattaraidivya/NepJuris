import ChatBox from "./ChatBox";
import InputBox from "./InputBox";
import type { UseChatReturn } from "../../types/chat.types";


type ChatAreaProps = Pick<
  UseChatReturn,
  "currentChat" | "loading" | "bottomRef" | "handleSend"
>;

export default function ChatArea({
  currentChat,
  loading,
  bottomRef,
  handleSend,
}: ChatAreaProps) {
  return (
    <div className="flex-1 relative flex flex-col overflow-hidden">

      {/* MESSAGES AREA */}
      <div className="flex-1 overflow-y-auto py-28">
        <div className="max-w-3xl mx-auto w-full px-4">

          {currentChat ? (
            <>
              <ChatBox messages={currentChat.messages} />

              {loading && (
                <div className="mt-3 flex gap-1">
                  <span className="w-2 h-2 bg-zinc-500 rounded-full animate-bounce"></span>
                  <span className="w-2 h-2 bg-zinc-500 rounded-full animate-bounce [animation-delay:0.2s]"></span>
                  <span className="w-2 h-2 bg-zinc-500 rounded-full animate-bounce [animation-delay:0.4s]"></span>
                </div>
              )}

              <div ref={bottomRef} />
            </>
          ) : (
          <div className="flex flex-col items-center justify-center h-full text-center px-6">
    
    <h1 className="text-2xl font-semibold text-white">
      Welcome to NepJuris
    </h1>

    <p className="text-zinc-500 mt-2 max-w-md">
      Ask anything about Nepali law, constitution, or legal procedures.
      Start a new chat or select an existing one from the sidebar.
    </p>

 

  </div>
          )}

        </div>
      </div>

      {/* FLOATING INPUT (CHATGPT STYLE) */}
      <div className="absolute bottom-4 left-0 w-full flex justify-center">
        <div className="w-full max-w-3xl px-4">

          <div className="backdrop-blur-xl bg-zinc-900/60 border border-zinc-800 rounded-2xl shadow-lg">
            <InputBox onSend={handleSend} loading={loading} />
          </div>

        </div>
      </div>

    </div>
  );
}