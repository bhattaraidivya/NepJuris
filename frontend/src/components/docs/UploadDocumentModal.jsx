import { useState } from "react";
import Button from "../ui/Button";
import { uploadDocument } from "../../services/api";

export default function UploadDocumentModal({ onClose, onUploaded }) {
  const [file, setFile] = useState(null);
  const [name, setName] = useState("");
  const [category, setCategory] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    if (!file) {
      setError("Please choose a PDF file.");
      return;
    }
    if (!name.trim()) {
      setError("Please give the document a name.");
      return;
    }

    setSubmitting(true);
    try {
      const result = await uploadDocument(file, name.trim(), category.trim());
      onUploaded(result.document);
      onClose();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Upload failed.");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 px-4">
      <div className="w-full max-w-md bg-white border border-zinc-200 rounded-2xl shadow-lg p-6">
        <h2 className="text-lg font-semibold text-zinc-900">Add Document</h2>
        <p className="text-sm text-zinc-500 mt-1">
          Uploads a PDF and indexes it into the search corpus automatically.
        </p>

        <form onSubmit={handleSubmit} className="mt-5 space-y-4">
          <div>
            <label className="block text-sm text-zinc-700 mb-1">PDF file</label>
            <input
              type="file"
              accept="application/pdf"
              onChange={(e) => setFile(e.target.files?.[0] ?? null)}
              className="w-full text-sm text-zinc-700 file:mr-3 file:px-3 file:py-2 file:rounded-lg file:border-0 file:bg-zinc-100 file:text-zinc-700 hover:file:bg-zinc-200"
            />
          </div>

          <div>
            <label className="block text-sm text-zinc-700 mb-1">Name</label>
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="e.g. Consumer Protection Act"
              className="w-full px-3 py-2 rounded-xl bg-white border border-zinc-200 outline-none focus:ring-2 focus:ring-zinc-300"
            />
          </div>

          <div>
            <label className="block text-sm text-zinc-700 mb-1">Category (optional)</label>
            <input
              type="text"
              value={category}
              onChange={(e) => setCategory(e.target.value)}
              placeholder="e.g. law"
              className="w-full px-3 py-2 rounded-xl bg-white border border-zinc-200 outline-none focus:ring-2 focus:ring-zinc-300"
            />
          </div>

          {error && <p className="text-sm text-red-600">{error}</p>}

          <div className="flex gap-2 justify-end pt-2">
            <Button
              type="button"
              variant="ghost"
              className="text-zinc-700"
              onClick={onClose}
              disabled={submitting}
            >
              Cancel
            </Button>
            <Button type="submit" variant="secondary" disabled={submitting}>
              {submitting ? "Indexing..." : "Upload & Index"}
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
}
