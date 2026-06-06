import { layout } from "../../design/layout";
import { typography } from "../../design/typography";
import { colors } from "../../design/colors";
import { Link } from "react-router-dom";

export default function Footer() {
  return (
    <footer className={`w-full ${colors.bgPrimary} text-white border-t border-zinc-800/50 py-20`}>
      <div className={layout.container}>

        {/* ================= TOP SECTION ================= */}
        <div className="flex flex-col md:flex-row md:items-start md:justify-between gap-12">

          {/* BRAND BLOCK */}
          <div className="max-w-md">
            <h2 className={typography.heading3}>
              NepJuris
            </h2>

            <p className="mt-4 text-sm text-zinc-400 leading-relaxed">
              A legal intelligence system built for Nepal.  
              Designed to make law accessible through retrieval-driven AI systems.
            </p>
          </div>

          {/* NAV LINKS */}
          <div className="grid grid-cols-2 gap-10 text-sm">

            {/* PLATFORM (PAGE ROUTES) */}
            <div className="space-y-3">
              <p className={`${typography.label} text-zinc-500`}>
                PLATFORM
              </p>

              <Link to="/" className="block text-zinc-300 hover:text-white transition">
                Home
              </Link>

              <Link to="/docs" className="block text-zinc-300 hover:text-white transition">
                Docs
              </Link>

              <Link to="/chat" className="block text-zinc-300 hover:text-white transition">
                Chat
              </Link>
            </div>

            {/* SYSTEM (PAGE SECTIONS) */}
            <div className="space-y-3">
              <p className={`${typography.label} text-zinc-500`}>
                SYSTEM
              </p>

              <a href="#workflow" className="block text-zinc-300 hover:text-white transition">
                Workflow
              </a>

              <a href="#features" className="block text-zinc-300 hover:text-white transition">
                Features
              </a>

              <a href="#trust" className="block text-zinc-300 hover:text-white transition">
                Trust
              </a>
            </div>

          </div>

        </div>

        {/* ================= DIVIDER ================= */}
        <div className="my-10 border-t border-zinc-800/60" />

        {/* ================= BOTTOM ================= */}
        <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-6">

          <p className="text-xs text-zinc-500">
            © {new Date().getFullYear()} NepJuris. All rights reserved.
          </p>

          <p className="text-xs text-zinc-600 tracking-wide">
            BUILT FOR LEGAL CLARITY • NEPAL AI SYSTEMS
          </p>

        </div>

      </div>
    </footer>
  );
}

