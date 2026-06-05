import { layout } from "../../design/layout";

export default function Trust() {
  return (
    <section id="trust" className="w-full bg-zinc-900/30 text-white py-32 border-t border-zinc-800/50">
      <div className={layout.container}>

        {/* ================= CENTERED MISSION ================= */}
        <div className="max-w-4xl mx-auto text-center">

          {/* SMALL LABEL */}
          <p className="text-xs tracking-[0.3em] text-zinc-500 mb-6">
            WHY NEPJURIS EXISTS
          </p>

          {/* MAIN STATEMENT */}
          <h2 className="text-4xl md:text-5xl font-semibold leading-tight tracking-tight">
            Legal systems are complex, but understanding them should not be.
          </h2>

          {/* SUB TEXT */}
          <p className="mt-6 text-zinc-400 text-lg leading-relaxed max-w-2xl mx-auto">
            NepJuris is built to make Nepal’s legal knowledge accessible, structured, and searchable using AI-driven retrieval systems.  
            It does not replace law, it makes it understandable.
          </p>

        </div>

        {/* ================= TRUST INDICATORS ================= */}
        <div className="mt-20 grid md:grid-cols-3 gap-10 text-center">

          <div>
            <p className="text-2xl font-semibold">Retrieval First</p>
            <p className="text-sm text-zinc-500 mt-2">
              Every answer is grounded in real legal documents.
            </p>
          </div>

          <div>
            <p className="text-2xl font-semibold">Unified Legal Corpus</p>
            <p className="text-sm text-zinc-500 mt-2">
              Centralized collection of legal records.</p>
          </div>

          <div>
            <p className="text-2xl font-semibold">Nepal Focused</p>
            <p className="text-sm text-zinc-500 mt-2">
              Built specifically for Nepal’s legal ecosystem.
            </p>
          </div>

        </div>

      </div>
    </section>
  );
}