import { layout } from "../../design/layout";
import Card from "../../components/ui/Card";

export default function Features() {
  return (
    <section id="features" className="w-full bg-zinc-950 text-white py-32">
      <div className={layout.container}>

        {/* ================= HEADER ================= */}
        <div className="max-w-3xl mb-20">
          <h2 className="text-4xl md:text-5xl font-semibold leading-tight tracking-tight">
            A complete legal intelligence system.
          </h2>

          <p className="mt-4 text-zinc-400 text-lg leading-relaxed max-w-2xl">
            A retrieval-driven legal intelligence system built to enable semantic search and contextual reasoning over Nepal’s legal documents.
          </p>
        </div>

        {/* ================= GRID ================= */}
        <div className="grid md:grid-cols-3 gap-10">

          {/* CORE INTELLIGENCE */}
          <div className="space-y-6">

            <h3 className="text-xs tracking-[0.3em] text-zinc-500">
              CORE INTELLIGENCE
            </h3>

            <div className="space-y-5">
              <Card
                title="Legal Chat Interface"
                description="Ask legal questions and receive structured, grounded answers."
              />

              <Card
                title="Semantic Search Engine"
                description="Understands intent beyond keywords using embeddings."
              />

              <Card
                title="AI Legal Reasoning"
                description="Generates explanations using retrieved legal context."
              />
            </div>

          </div>

          {/* LEGAL CORPUS ENGINE */}
          <div className="space-y-6">

            <h3 className="text-xs tracking-[0.3em] text-zinc-500">
              LEGAL CORPUS ENGINE
            </h3>

            <div className="space-y-5">
              <Card
                title="PDF Ingestion System"
                description="Extracts structured data from legal documents and statutes."
              />

              <Card
                title="Nepal Legal Corpus"
                description="Constitution, acts, and legal texts indexed and searchable."
              />

              <Card
                title="Vector Knowledge Base"
                description="Stores embeddings for semantic retrieval using FAISS."
              />
            </div>

          </div>

          {/* SYSTEM GUARANTEE */}
          <div className="space-y-6">

            <h3 className="text-xs tracking-[0.3em] text-zinc-500">
              SYSTEM GUARANTEE
            </h3>

            <div className="space-y-5">
              <Card
                title="Citation-Based Answers"
                description="Every response is grounded in retrieved legal sources."
              />

              <Card
                title="Retrieval-First Design"
                description="No response is generated without context retrieval."
              />

              <Card
                title="Local LLM Execution"
                description="Qwen-based local model ensures privacy and control."
              />
            </div>

          </div>

        </div>
      </div>
    </section>
  );
}