import useChat from "../hooks/useChat";
import Sidebar from "../components/chat/Sidebar";
import ChatArea from "../components/chat/ChatArea";

export default function Chat() {
  const chat = useChat();

  return (
    <div className="h-screen flex bg-zinc-950 text-white overflow-hidden">
      <Sidebar {...chat} />
      <ChatArea {...chat} />
    </div>
  );
}