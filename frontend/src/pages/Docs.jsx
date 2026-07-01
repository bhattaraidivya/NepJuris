import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import DocumentCard from "../components/docs/DocumentCard";
import UploadDocumentModal from "../components/docs/UploadDocumentModal";
import Button from "../components/ui/Button";
import { getDocuments } from "../services/api";

const BASE_URL = import.meta.env.VITE_API_BASE_URL;
const IS_DEMO_MODE = import.meta.env.VITE_DEMO_MODE === "true";

export default function Docs() {
  const [documents, setDocuments] = useState([]);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);
  const [loadError, setLoadError] = useState("");
  const [showUpload, setShowUpload] = useState(false);

  const navigate = useNavigate();

  const fetchDocuments = () => {
    getDocuments()
      .then((data) => {
        setDocuments(data.documents || []);
        setLoadError("");
      })
      .catch((err) => {
        setLoadError(err instanceof Error ? err.message : "Failed to load documents.");
      })
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchDocuments();
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

  const handleUploaded = () => {
    // Re-fetch rather than optimistically append, since the backend
    // may adjust fields (id, status) during ingestion.
    setLoading(true);
    fetchDocuments();
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

        <div className="flex items-start justify-between gap-4">
          <div>
            <h1 className="text-3xl font-semibold text-zinc-900">
              NepJuris Docs
            </h1>

            <p className="text-zinc-500 mt-2">
              Legal documents and statutes indexed for AI search.
            </p>
          </div>

          <Button variant="secondary" onClick={() => setShowUpload(true)}>
            + Add Document
          </Button>
        </div>

        {IS_DEMO_MODE && (
          <div className="mt-4 px-4 py-3 rounded-xl bg-amber-50 border border-amber-200 text-amber-800 text-sm">
            Demo mode: uploaded documents are temporary and reset when this
            instance restarts. Clone the repo and run{" "}
            <code className="font-mono">docker compose up</code> for
            persistent storage.
          </div>
        )}

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

        {/* LOADING / ERROR */}
        {loading ? (
          <p className="text-zinc-500 mt-6">
            Loading documents...
          </p>
        ) : loadError ? (
          <p className="text-red-600 mt-6">{loadError}</p>
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

      {showUpload && (
        <UploadDocumentModal
          onClose={() => setShowUpload(false)}
          onUploaded={handleUploaded}
        />
      )}

    </div>
  );
}
