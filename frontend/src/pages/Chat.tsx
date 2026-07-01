import { useEffect, useRef } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import useChat from "../hooks/useChat";
import Sidebar from "../components/chat/Sidebar";
import ChatArea from "../components/chat/ChatArea";

export default function Chat() {
  const chat = useChat();
  const location = useLocation();
  const navigate = useNavigate();
  const hasHandledIncomingMessage = useRef(false);

  // Docs page "Ask AI" navigates here with a pre-filled question via
  // router state. Send it once, then clear the state so a refresh or
  // back-navigation doesn't resend it.
  useEffect(() => {
    const incoming = (location.state as { message?: string } | null)?.message;

    if (incoming && !hasHandledIncomingMessage.current) {
      hasHandledIncomingMessage.current = true;
      chat.handleSend(incoming);
      navigate(location.pathname, { replace: true, state: null });
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [location.state]);

  return (
    <div className="h-screen flex bg-zinc-950 text-white overflow-hidden">
      <Sidebar {...chat} />
      <ChatArea {...chat} />
    </div>
  );
}
