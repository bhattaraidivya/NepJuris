import { layout } from "../../design/layout";
import Button from "../ui/Button";
import { Link } from "react-router-dom";

export default function CorpusPreview() {
  const docs = [
    "Constitution of Nepal",
    "Civil Code 2074",
    "Criminal Procedure Act",
    "Supreme Court Precedents",
    "Legal PDF Archives",
    "Statutory Interpretations",
  ];

  // duplicate for seamless animation
  const list = [...docs, ...docs];

  return (
    <section className="w-full min-h-screen bg-white flex items-center relative overflow-hidden">
      
      {/* BACKGROUND */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute top-[-20%] left-[-10%] w-150600px] bg-zinc-100 blur-3xl rounded-full opacity-60" />

        <div className="absolute bottom-[-20%] right-[-10%] w-150 h-150 bg-zinc-200 blur-3xl rounded-full opacity-40" />
      </div>

      {/* CONTENT */}
      <div
        className={`
          ${layout.container}
          relative
          z-10
          grid
          grid-cols-1
          md:grid-cols-12
          gap-12
          items-center
          py-20
        `}
      >
        {/* LEFT */}
        <div className="md:col-span-3 space-y-4 text-center md:text-left">
          <p className="text-xs tracking-[0.3em] text-zinc-500">
            LEGAL CORPUS
          </p>

          <p className="text-zinc-700 text-sm leading-relaxed">
            Structured Nepal legal knowledge base powering retrieval and
            reasoning.
          </p>
        </div>

        {/* CENTER */}
        <div className="md:col-span-6 flex justify-center">
          
          {/* WINDOW */}
          <div className="relative h-100 md:h-105 w-full max-w-md overflow-hidden">
            
            {/* TOP FADE */}
            <div className="absolute top-0 left-0 right-0 h-24 bg-linear-to-brom-white to-transparent z-10" />

            {/* BOTTOM FADE */}
            <div className="absolute bottom-0 left-0 right-0 h-24 bg-linear-to-t from-white to-transparent z-10" />

            {/* SCROLL TRACK */}
            <div className="absolute w-full animate-scrollY flex flex-col">
              {list.map((doc, i) => (
                <div
                  key={i}
                  className="h-20 flex items-center justify-center"
                >
                  <div
                    className="
                      w-[90%]
                      text-center
                      px-6
                      py-4
                      rounded-xl
                      border
                      border-zinc-200
                      bg-zinc-50
                      text-zinc-900
                      shadow-sm
                    "
                  >
                    {doc}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* RIGHT */}
        <div className="md:col-span-3 flex justify-center md:justify-end">
          <Link to="/docs">
            <Button variant="secondary">
              Explore Documents
            </Button>
          </Link>
        </div>
      </div>
    </section>
  );
}