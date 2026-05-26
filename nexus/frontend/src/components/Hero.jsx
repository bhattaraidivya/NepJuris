import { useNavigate } from "react-router-dom";

export default function Hero() {
  const navigate = useNavigate();

  return (
    <div className="text-center mt-24 px-6">
      <h1 className="text-5xl font-bold">
        Nepal AI Legal Assistant
      </h1>

      <p className="text-zinc-400 mt-4">
        Ask legal questions in English or नेपाली
      </p>

      <button
        onClick={() => navigate("/chat")}
        className="mt-10 bg-white text-black px-6 py-2 rounded-xl"
      >
        Start Chat
      </button>
    </div>
  );
}