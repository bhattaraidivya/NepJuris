import Button from "../ui/Button";

export default function DocumentCard({
  doc,
  onView,
  onAskAI,
  onDownload,
}) {
  return (
    <div
      className="
        bg-white
        border border-zinc-200
        rounded-2xl
        p-5

        shadow-sm
        hover:shadow-md
        hover:-translate-y-0.5

        transition-all duration-200
      "
    >
      {/* TITLE */}
      <h2 className="text-zinc-900 font-semibold text-lg">
        {doc.name}
      </h2>

      {/* META */}
      <p className="text-zinc-500 text-sm mt-2">
        {doc.category} • {doc.language}
      </p>

      {/* ACTIONS */}
      <div className="flex gap-2 mt-5">

        <Button
          variant="secondary"
          onClick={() => onDownload(doc.id)}
        >
          Download
        </Button>

        <Button
          variant="accent"
          onClick={() => onAskAI(doc)}
        >
          Ask AI
        </Button>

      </div>
    </div>
  );
}