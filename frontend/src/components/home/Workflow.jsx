import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { layout } from "../../design/layout";

export default function Workflow() {
  const steps = [
    {
      title: "Understanding Query",
      desc: "NepJuris interprets the legal question into semantic embeddings."
    },
    {
      title: "Retrieving Legal Context",
      desc: "FAISS searches Nepal’s legal corpus for relevant statutes and cases."
    },
    {
      title: "Building Context Window",
      desc: "Top-ranked legal chunks are structured into a grounded prompt."
    },
    {
      title: "Generating Response",
      desc: "Local LLM (Qwen) generates legally grounded explanation."
    },
    {
      title: "Final Output",
      desc: "Response is returned with citations from Nepal legal documents."
    }
  ];

  const [index, setIndex] = useState(0);
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    const stepInterval = setInterval(() => {
      setIndex((prev) => (prev + 1) % steps.length);
      setProgress(0);
    }, 4200);

    return () => clearInterval(stepInterval);
  }, []);

  useEffect(() => {
    const progressInterval = setInterval(() => {
      setProgress((p) => (p >= 100 ? 100 : p + 1.2));
    }, 70);

    return () => clearInterval(progressInterval);
  }, []);

  const current = steps[index];

  return (
    <section id="workflow" className="w-full bg-white text-black py-32">
      <div className={layout.container}>

        {/* ================= HEADER (CENTERED + CONTROLLED WIDTH) ================= */}
            <div className="max-w-3xl mb-20">
                <h2 className="text-4xl md:text-5xl font-semibold leading-tight tracking-tight">
  
  <span className="text-black">
    Law is only useful when it is understood.
  </span>

  <span className="text-zinc-500 font-normal ml-2">
    Advance your expertise on a secure platform.
  </span>

</h2>

                {/* <p className="mt-4 text-zinc-500 text-lg md:text-xl leading-relaxed max-w-2xl">
                    Advance your expertise on a secure platform.
                </p> */}
            </div>

        {/* ================= GRID (BETTER ALIGNMENT) ================= */}
        <div className="grid md:grid-cols-2 gap-20 items-start">

          {/* ================= LEFT SIDE ================= */}
          <div className="max-w-lg space-y-10">

            <div>
              <h3 className="text-lg font-semibold">Retrieval-Augmented System</h3>
              <p className="text-zinc-600 text-sm mt-2 leading-relaxed">
                Every query is grounded in Nepal’s legal corpus using vector search.
              </p>
            </div>

            <div>
              <h3 className="text-lg font-semibold">LLM Reasoning Layer</h3>
              <p className="text-zinc-600 text-sm mt-2 leading-relaxed">
                A local model transforms retrieved law into structured explanations.
              </p>
            </div>

            <div>
              <h3 className="text-lg font-semibold">Verified Legal Output</h3>
              <p className="text-zinc-600 text-sm mt-2 leading-relaxed">
                Every response is backed by actual legal sources, not hallucinations.
              </p>
            </div>

          </div>

          {/* ================= RIGHT SIDE ================= */}
          <div className="flex justify-center">

            <div className="w-full max-w-2xl  sticky top-24">

              <motion.div
                className="bg-zinc-950 text-white rounded-2xl border border-zinc-800 shadow-2xl p-10"
              >

                {/* HEADER */}
                <div className="text-xs text-zinc-400 tracking-widest mb-6">
                  NEPJURIS INTELLIGENCE FLOW
                </div>

                {/* TITLE */}
                <motion.h3
                  key={current.title}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.8, ease: "easeOut" }}
                  className="text-xl font-semibold mb-3"
                >
                  {current.title}
                </motion.h3>

                {/* DESC */}
                <motion.p
                  key={current.desc}
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ duration: 0.9 }}
                  className="text-sm text-zinc-300 leading-relaxed"
                >
                  {current.desc}
                </motion.p>

                {/* PROGRESS */}
                <div className="mt-6 h-1 bg-zinc-800 rounded-full overflow-hidden">
                  <motion.div
                    className="h-full bg-white"
                    animate={{ width: `${progress}%` }}
                    transition={{ ease: "linear" }}
                  />
                </div>

              </motion.div>

            </div>
          </div>

        </div>
      </div>
    </section>
  );
}