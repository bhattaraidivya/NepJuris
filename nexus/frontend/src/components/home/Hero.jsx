import { useEffect, useState } from "react";
import Container from "../ui/Container";
import Button from "../ui/Button";
import { typography } from "../../design/typography";
import { Link } from "react-router-dom";

import hero1 from "../../assets/hero1.jpg";
import hero2 from "../../assets/hero2.jpg";
import hero3 from "../../assets/hero3.jpg";

export default function Hero() {

  // ================= HERO IMAGES =================
  const images = [hero1, hero2, hero3];

  const [currentImage, setCurrentImage] = useState(0);

  // ================= AUTO IMAGE ROTATION =================
  useEffect(() => {

    const interval = setInterval(() => {
      setCurrentImage((prev) => (prev + 1) % images.length);
    }, 5000);

    return () => clearInterval(interval);

  }, []);

  return (
    <div className="relative h-screen w-full overflow-hidden bg-zinc-950">

      {/* ================= BACKGROUND IMAGE LAYER ================= */}
      <div className="absolute inset-0">

        {images.map((image, index) => (
          <div
            key={index}
            className={`
              absolute inset-0
              bg-cover bg-center
              transition-opacity duration-[2000]
              ${currentImage === index ? "opacity-60" : "opacity-0"}
            `}
            style={{
              backgroundImage: `url(${image})`,
            }}
          />
        ))}

        {/* DARK OVERLAY */}
        <div className="absolute inset-0 bg-black/60" />

        {/* COLOR GLOW */}
        <div className="absolute inset-0 bg-linear-to-br from-zinc-950/80 via-black/60 to-zinc-900/40" />

      </div>

      {/* ================= CONTENT ================= */}
      <Container>
        <div className="relative z-10 h-screen flex items-center">

          <div className="w-full md:w-[55%]">

            <h1 className={typography.hero}>
              LEGAL CHAOS → CLARITY
            </h1>

            <p className={`${typography.bodyLarge} mt-6 max-w-xl`}>
              Nepali legal documents were never built for humans to read.
              NepJuris transforms them into structured intelligence using retrieval-based AI.
            </p>

            <div className="mt-8 flex gap-4">

              <Link to="/chat">
                <Button variant="primary">
                  Start Chat
                </Button>
              </Link>

              <Link to="/docs">
                <Button variant="secondary">
                  Explore Docs
                </Button>
              </Link>

            </div>

          </div>

        </div>
      </Container>

      {/* ================= BOTTOM MARQUEE ================= */}
      <div className="absolute bottom-0 left-0 w-full h-14 border-t border-zinc-800 bg-zinc-950/40 backdrop-blur-md overflow-hidden">

        {/* EDGE FADE */}
        <div className="absolute left-0 top-0 h-full w-24 bg-linear-to-r from-zinc-950 to-transparent z-10" />
        <div className="absolute right-0 top-0 h-full w-24 bg-linear-to-l from-zinc-950 to-transparent z-10" />

        {/* TRACK */}
        <div className="flex h-full items-center">
          <div className="flex items-center w-max animate-marquee">

            {[
              "⚖ NepJuris AI",
              "◈ RAG PIPELINE ACTIVE",
              "◉ FAISS VECTOR SEARCH",
              "▣ NEPAL LEGAL CORPUS INDEXED",
              "◈ CONSTITUTION OF NEPAL 2072",
              "◉ CIVIL CODE LOADED",
              "▣ CRIMINAL PROCEDURE ACT",
              "◈ CONTEXT RETRIEVAL ENGINE",
              "◉ LOCAL LLM READY",
              "▣ MULTILINGUAL NLP ACTIVE",
              "◈ DOCUMENT EMBEDDING SYSTEM",

              "⚖ NepJuris AI",
              "◈ RAG PIPELINE ACTIVE",
              "◉ FAISS VECTOR SEARCH",
              "▣ NEPAL LEGAL CORPUS INDEXED",
              "◈ CONSTITUTION OF NEPAL 2072",
              "◉ CIVIL CODE LOADED",
              "▣ CRIMINAL PROCEDURE ACT",
              "◈ CONTEXT RETRIEVAL ENGINE",
              "◉ LOCAL LLM READY",
              "▣ MULTILINGUAL NLP ACTIVE",
              "◈ DOCUMENT EMBEDDING SYSTEM",
            ].map((text, i) => (
              <span
                key={i}
                className="mx-10 text-xs tracking-[0.25em] text-zinc-400 whitespace-nowrap shrink-0"
              >
                {text}
              </span>
            ))}

          </div>
        </div>

      </div>

    </div>
  );
}

