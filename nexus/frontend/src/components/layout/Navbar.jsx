import { useEffect, useState } from "react";
import { Link, useLocation } from "react-router-dom";

import Button from "../ui/Button";

const navLinks = [
  { label: "Home", path: "/" },
  { label: "Docs", path: "/docs" },
  { label: "Chat", path: "/chat" },
];

export default function Navbar() {
  const [scrolled, setScrolled] = useState(false);
  const [hidden, setHidden] = useState(false);
  const [menuOpen, setMenuOpen] = useState(false);

  const location = useLocation();

  useEffect(() => {
    let lastY = window.scrollY;

    const handleScroll = () => {
      const currentY = window.scrollY;

      setScrolled(currentY > 30);

      if (currentY > lastY && currentY > 80) {
        setHidden(true);
      } else {
        setHidden(false);
      }

      lastY = currentY;
    };

    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  return (
    <header
      className={`
        fixed top-0 left-0 w-full z-50
        transition-all duration-300

        ${hidden ? "-translate-y-full" : "translate-y-0"}

        ${
          scrolled
            ? "bg-zinc-950/80 backdrop-blur-xl border-b border-zinc-800"
            : "bg-transparent"
        }
      `}
    >
      <div className="h-20 flex items-center justify-between px-6 md:px-10 lg:px-16">

        {/* LEFT — BRAND */}
        <Link
          to="/"
          className="text-white text-xl font-semibold tracking-tight"
        >
          NepJuris
        </Link>

        {/* CENTER — NAVIGATION (DESKTOP ONLY) */}
        <nav className="hidden md:flex items-center gap-10">
          {navLinks.map((item) => {
            const active = location.pathname === item.path;

            return (
              <Link
                key={item.path}
                to={item.path}
                className={`
                  text-sm transition-colors
                  ${
                    active
                      ? "text-white"
                      : "text-zinc-400 hover:text-white"
                  }
                `}
              >
                {item.label}
              </Link>
            );
          })}
        </nav>

        {/* RIGHT — CTA (DESKTOP ONLY) */}
        <div className="hidden md:flex items-center">
          <Link to="/chat">
            <Button variant="primary">
              Open Workspace
            </Button>
          </Link>
        </div>

        {/* MOBILE MENU BUTTON */}
        <button
          className="md:hidden text-white text-2xl"
          onClick={() => setMenuOpen(!menuOpen)}
        >
          ☰
        </button>
      </div>

      {/* MOBILE DROPDOWN */}
      {menuOpen && (
        <div className="md:hidden bg-zinc-950 border-t border-zinc-800 px-6 py-4 space-y-4">
          {navLinks.map((item) => {
            const active = location.pathname === item.path;

            return (
              <Link
                key={item.path}
                to={item.path}
                onClick={() => setMenuOpen(false)}
                className={`
                  block text-sm transition-colors
                  ${
                    active
                      ? "text-white"
                      : "text-zinc-400"
                  }
                `}
              >
                {item.label}
              </Link>
            );
          })}

          {/* CTA in mobile menu */}
          <Link to="/chat" onClick={() => setMenuOpen(false)}>
            <div className="mt-4">
              <Button variant="primary" className="w-full">
                Open Workspace
              </Button>
            </div>
          </Link>
        </div>
      )}
    </header>
  );
}

