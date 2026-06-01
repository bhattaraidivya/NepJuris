import ChatBox from "./ChatBox";
import InputBox from "./InputBox";

export default function ChatArea({
  currentChat,
  loading,
  bottomRef,
  handleSend,
}) {
  return (
    <div className="flex-1 flex flex-col overflow-hidden">

      <div className="flex-1 overflow-y-auto py-6">
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
            <div className="text-zinc-500 text-center mt-10">
              Start a new conversation
            </div>
          )}

        </div>
      </div>

      <div className="border-t border-zinc-800 p-4">
        <div className="max-w-3xl mx-auto">
          <InputBox onSend={handleSend} loading={loading} />
        </div>
      </div>

    </div>
  );
}