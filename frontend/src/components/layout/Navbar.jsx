import { useEffect, useState } from "react";
import { Scale, Menu, X } from "lucide-react";

const NAV_LINKS = [
  { label: "Home", href: "#home" },
  { label: "New Complaint", href: "#new-complaint" },
  { label: "Case Insights", href: "#case-insights" },
  { label: "How It Works", href: "#how-it-works" },
  { label: "About", href: "#about" },
];

export default function Navbar() {
  const [scrolled, setScrolled] = useState(false);
  const [open, setOpen] = useState(false);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 16);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  return (
    <header
      className={`fixed inset-x-0 top-0 z-50 transition-all duration-[400ms] ease-out ${
        scrolled
          ? "border-b border-[#6D8196]/20 bg-[#FFFFE3]/70 backdrop-blur-xl backdrop-saturate-150 shadow-[0_8px_30px_-12px_rgba(74,74,74,0.18)]"
          : "border-b border-transparent bg-transparent backdrop-blur-0"
      }`}
    >
      <nav
        aria-label="Primary"
        className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4"
      >
        <a
          href="#home"
          className="flex items-center gap-2.5 text-[#4A4A4A] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#6D8196] focus-visible:ring-offset-2 focus-visible:ring-offset-[#FFFFE3] rounded-md"
        >
          <span className="grid h-9 w-9 place-items-center rounded-lg bg-[#6D8196] text-[#FFFFE3] shadow-sm">
            <Scale className="h-5 w-5" aria-hidden />
          </span>
          <span className="text-base font-semibold tracking-tight">
            ConsumerShield <span className="text-[#6D8196]">AI</span>
          </span>
        </a>

        <ul className="hidden items-center gap-1 md:flex">
          {NAV_LINKS.map((l) => (
            <li key={l.label}>
              <a
                href={l.href}
                className="rounded-md px-3.5 py-2 text-sm font-medium text-[#4A4A4A]/80 transition-colors duration-200 hover:bg-[#6D8196]/10 hover:text-[#4A4A4A] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#6D8196]"
              >
                {l.label}
              </a>
            </li>
          ))}
        </ul>

        <div className="hidden md:block">
          <a
            href="#get-started"
            className="inline-flex items-center rounded-xl bg-[#6D8196] px-5 py-2.5 text-sm font-semibold text-[#FFFFE3] shadow-sm transition-all duration-300 hover:-translate-y-0.5 hover:bg-[#5b6d80] hover:shadow-md focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#6D8196] focus-visible:ring-offset-2 focus-visible:ring-offset-[#FFFFE3]"
          >
            Get Started
          </a>
        </div>

        <button
          type="button"
          aria-label={open ? "Close menu" : "Open menu"}
          aria-expanded={open}
          onClick={() => setOpen((v) => !v)}
          className="grid h-10 w-10 place-items-center rounded-lg border border-[#6D8196]/30 text-[#4A4A4A] md:hidden focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#6D8196]"
        >
          {open ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
        </button>
      </nav>

      {open && (
        <div className="border-t border-[#6D8196]/15 bg-[#FFFFE3]/95 backdrop-blur-xl md:hidden">
          <ul className="mx-auto flex max-w-7xl flex-col gap-1 px-6 py-4">
            {NAV_LINKS.map((l) => (
              <li key={l.label}>
                <a
                  href={l.href}
                  onClick={() => setOpen(false)}
                  className="block rounded-md px-3 py-2.5 text-sm font-medium text-[#4A4A4A] hover:bg-[#6D8196]/10"
                >
                  {l.label}
                </a>
              </li>
            ))}
            <li className="pt-2">
              <a
                href="#get-started"
                onClick={() => setOpen(false)}
                className="block rounded-xl bg-[#6D8196] px-5 py-3 text-center text-sm font-semibold text-[#FFFFE3] shadow-sm hover:bg-[#5b6d80]"
              >
                Get Started
              </a>
            </li>
          </ul>
        </div>
      )}
    </header>
  );
}