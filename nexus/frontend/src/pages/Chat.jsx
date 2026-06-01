import useChat from "../hooks/useChat";
import Sidebar from "../components/Sidebar";
import ChatArea from "../components/ChatArea";

export default function Chat() {
  const chat = useChat();

  return (
    <div className="h-screen flex flex-row bg-zinc-950 text-white overflow-hidden">

      <Sidebar {...chat} />

      <ChatArea {...chat} />

    </div>
  );
}