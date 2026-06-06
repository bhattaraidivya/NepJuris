import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import DocumentCard from "../components/docs/DocumentCard";

const BASE_URL = "http://127.0.0.1:8000";

export default function Docs() {
  const [documents, setDocuments] = useState([]);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);

  const navigate = useNavigate();

  useEffect(() => {
    fetch(`${BASE_URL}/documents`)
      .then((res) => res.json())
      .then((data) => {
        setDocuments(data.documents || []);
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setLoading(false);
      });
  }, []);

  const filteredDocs = documents.filter((doc) =>
    doc.name.toLowerCase().includes(search.toLowerCase())
  );

  const handleAskAI = (doc) => {
    navigate("/chat", {
      state: {
        message: `Ask questions about: "${doc.name}".`,
      },
    });
  };

  const handleDownload = (docId) => {
    window.open(
      `${BASE_URL}/documents/${docId}/download`,
      "_blank"
    );
  };

  return (
    <div className="min-h-screen text-zinc-900 relative overflow-hidden bg-linear-to-b from-zinc-50 via-white to-zinc-100">
    
      
      
      {/* FLOATING BACK CHIP (NEW NAVIGATION STYLE) */}
      <button
        onClick={() => navigate(-1)}
        className="
          fixed top-6 left-6
          flex items-center gap-2

          px-4 py-2
          rounded-full

          bg-white
          border border-zinc-200
          shadow-sm

          text-sm text-zinc-700

          hover:bg-zinc-100
          hover:text-zinc-900

          transition
        "
      >
        ← Back
      </button>

      {/* HEADER */}
      <div className="max-w-5xl mx-auto pt-20 px-6">

        <h1 className="text-3xl font-semibold text-zinc-900">
          NepJuris Docs
        </h1>

        <p className="text-zinc-500 mt-2">
          Legal documents and statutes indexed for AI search.
        </p>

        {/* SEARCH (CLEAN + MODERN) */}
        <div className="mt-6">
          <input
            type="text"
            placeholder="Search legal documents..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="
              w-full
              px-4 py-3

              rounded-xl

              bg-white
              border border-zinc-200

              shadow-sm

              outline-none

              focus:ring-2
              focus:ring-zinc-300
            "
          />
        </div>

        {/* LOADING */}
        {loading ? (
          <p className="text-zinc-500 mt-6">
            Loading documents...
          </p>
        ) : (
          <div className="grid gap-5 md:grid-cols-2 lg:grid-cols-3 mt-8">

            {filteredDocs.map((doc) => (
              <DocumentCard
                key={doc.id}
                doc={doc}
                onDownload={handleDownload}
                onAskAI={handleAskAI}
              />
            ))}

          </div>
        )}

      </div>
      
    </div>
  );
}