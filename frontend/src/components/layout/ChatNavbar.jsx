import { Link } from "react-router-dom";
import Button from "../ui/Button";

export default function ChatNavbar({ currentChatTitle }) {
  return (
    <div className="h-16 flex items-center justify-between px-6 md:px-10 border-b border-zinc-800 bg-zinc-950/80 backdrop-blur-xl">

      {/* LEFT — matches global navbar style */}
      <Link
        to="/"
        className="text-sm text-zinc-400 hover:text-white transition"
      >
        ← Home
      </Link>

      {/* CENTER — same typography system */}
      <div className="text-sm text-white font-medium tracking-tight truncate">
        {currentChatTitle || "NepJuris AI Workspace"}
      </div>

      {/* RIGHT — consistent CTA style (same Button system) */}
      <Link to="/docs">
        <Button variant="primary" className="text-sm px-4 py-2">
          Docs
        </Button>
      </Link>

    </div>
  );
}