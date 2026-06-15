import { useEffect, useRef, useState } from "react";
import { FileText, Brain, Scale, Building2, ArrowRight } from "lucide-react";

const STEPS = [
  {
    num: "01",
    title: "Submit Complaint",
    Icon: FileText,
    desc: "Describe your consumer issue and upload supporting details. ConsumerShield AI extracts key information to prepare your complaint.",
  },
  {
    num: "02",
    title: "AI Legal Analysis",
    Icon: Brain,
    desc: "The AI analyzes your complaint using consumer protection laws and legal reasoning to identify rights and applicable provisions.",
  },
  {
    num: "03",
    title: "Case Strength Prediction",
    Icon: Scale,
    desc: "Receive an intelligent estimate of your case strength along with legal insights and supporting consumer rights.",
  },
  {
    num: "04",
    title: "Authority Recommendation",
    Icon: Building2,
    desc: "Get recommendations on the appropriate authority, complaint process, and actionable next steps.",
  },
];

const LEGAL_TERMS = [
  "Consumer Protection Act",
  "Consumer Rights",
  "Legal Notice",
  "District Consumer Commission",
  "Consumer Complaint",
  "Digital Commerce",
  "Compensation",
  "Grievance Redressal",
  "AI Legal Analysis",
  "Consumer Handbook",
  "National Consumer Helpline",
  "Unfair Trade Practice",
  "Product Liability",
  "Restitution",
  "Adjudication",
];

function DriftingLegalBg() {
  const line = LEGAL_TERMS.join("  •  ");
  const columns = Array.from({ length: 4 });
  return (
    <div
      aria-hidden
      className="pointer-events-none absolute inset-0 overflow-hidden select-none"
      style={{
        maskImage:
          "radial-gradient(ellipse at center, rgba(0,0,0,0.9) 30%, rgba(0,0,0,0.4) 70%, transparent 100%)",
        WebkitMaskImage:
          "radial-gradient(ellipse at center, rgba(0,0,0,0.9) 30%, rgba(0,0,0,0.4) 70%, transparent 100%)",
      }}
    >
      <style>{`
        @keyframes legalScrollUp {
          from { transform: translateY(0); }
          to { transform: translateY(-50%); }
        }
      `}</style>

      {columns.map((_, i) => (
        <div
          key={i}
          className="absolute top-0 bottom-0 overflow-hidden"
          style={{
            left: `${i * 25}%`,
            width: "25%",
            opacity: 0.1,
          }}
        >
          <div
            className="font-serif text-[10px] tracking-wide text-[#4A4A4A]"
            style={{
              whiteSpace: "pre-wrap",
              lineHeight: "2.4",
              animation: `legalScrollUp ${120 + i * 25}s linear infinite`,
              animationDelay: `${-i * 30}s`,
            }}
          >
            {Array(40).fill(line).join("\n\n")}
          </div>
        </div>
      ))}
    </div>
  );
}

function useInView(opts = {}) {
  const ref = useRef(null);
  const [inView, setInView] = useState(false);
  useEffect(() => {
    if (!ref.current || inView) return;
    const obs = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setInView(true);
          obs.disconnect();
        }
      },
      { threshold: 0.18, ...opts }
    );
    obs.observe(ref.current);
    return () => obs.disconnect();
  }, [inView, opts]);
  return { ref, inView };
}

export default function HowItWorks() {
  const { ref, inView } = useInView();
  const [hovered, setHovered] = useState(null);

  return (
    <section
      id="how-it-works"
      ref={ref}
      className="relative w-full overflow-hidden py-28 sm:py-36"
      style={{
        background:
          "radial-gradient(ellipse at top, #FCFAF2 0%, #F8F5E8 60%, #F3EFDC 100%)",
      }}
    >
      <DriftingLegalBg />

      {/* soft ambient blooms */}
      <div
        aria-hidden
        className="pointer-events-none absolute -top-32 left-1/2 -translate-x-1/2 h-[520px] w-[860px] rounded-full blur-3xl"
        style={{ background: "radial-gradient(closest-side, rgba(109,129,150,0.12), transparent)" }}
      />

      <div className="relative z-10 mx-auto max-w-7xl px-6">
        {/* Heading */}
        <div className="mx-auto max-w-3xl text-center">
          <div
            className="inline-flex items-center gap-2 rounded-full border border-[#6D8196]/20 bg-white/50 px-4 py-1.5 text-xs font-medium tracking-wider uppercase text-[#6D8196] backdrop-blur-sm"
            style={{
              opacity: inView ? 1 : 0,
              filter: inView ? "blur(0)" : "blur(8px)",
              transform: inView ? "translateY(0)" : "translateY(12px)",
              transition: "all 700ms cubic-bezier(0.22,1,0.36,1)",
            }}
          >
            <span className="h-1.5 w-1.5 rounded-full bg-[#6D8196]" />
            Process
          </div>
          <h2
            className="mt-6 text-4xl font-bold leading-[1.08] tracking-tight text-[#4A4A4A] sm:text-5xl lg:text-[3.5rem]"
            style={{
              opacity: inView ? 1 : 0,
              filter: inView ? "blur(0)" : "blur(10px)",
              transform: inView ? "translateY(0)" : "translateY(16px)",
              transition: "all 800ms cubic-bezier(0.22,1,0.36,1) 100ms",
            }}
          >
            How It Works
          </h2>
          <p
            className="mt-5 text-lg text-[#4A4A4A]/80 leading-relaxed"
            style={{
              opacity: inView ? 1 : 0,
              filter: inView ? "blur(0)" : "blur(8px)",
              transform: inView ? "translateY(0)" : "translateY(14px)",
              transition: "all 800ms cubic-bezier(0.22,1,0.36,1) 220ms",
            }}
          >
            From complaint submission to legal guidance in four intelligent steps.
          </p>
        </div>

        {/* Cards */}
        <div
          className="mt-20 grid grid-cols-1 lg:grid-cols-[1fr_auto_1fr_auto_1fr_auto_1fr] gap-y-10 lg:gap-y-0 lg:gap-x-2 items-stretch"
          onMouseLeave={() => setHovered(null)}
        >
          {STEPS.map((step, idx) => {
            const isHovered = hovered === idx;
            const dimmed = false;

            return (
              <div key={step.num} className="contents">
                <div
                  onMouseEnter={() => setHovered(idx)}
                  className="group relative"
                  style={{
                    opacity: inView ? 1 : 0,
                    transform: inView ? "translateY(0)" : "translateY(24px)",
                    transition: `opacity 700ms cubic-bezier(0.22,1,0.36,1) ${
                      400 + idx * 140
                    }ms, transform 700ms cubic-bezier(0.22,1,0.36,1) ${
                      400 + idx * 140
                    }ms`,
                  }}
                >
                  <article
                    aria-label={`Step ${step.num}: ${step.title}`}
                    className={`relative h-full overflow-hidden rounded-3xl border backdrop-blur-xl ${
                      isHovered
                        ? "border-[#D4AF37]/40 bg-white/70"
                        : "border-white/60 bg-white/55"
                    }`}
                    style={{
                      transition:
                        "transform 450ms cubic-bezier(0.22,1,0.36,1), box-shadow 450ms ease, background 450ms ease, opacity 450ms ease",
                      transform: isHovered
                        ? "translateY(-12px) scale(1.06)"
                        : "scale(1)",
                      opacity: dimmed && !isNeighbor ? 0.78 : 1,
                      boxShadow: isHovered
                        ? "0 30px 70px -30px rgba(212,175,55,0.45), 0 0 0 1px rgba(212,175,55,0.25), inset 0 1px 0 rgba(255,255,255,0.9)"
                        : "0 12px 30px -18px rgba(74,74,74,0.25), inset 0 1px 0 rgba(255,255,255,0.8)",
                      minHeight: isHovered ? 360 : 300,
                    }}
                  >
                    {/* radial hover glow */}
                    <div
                      aria-hidden
                      className="pointer-events-none absolute inset-0"
                      style={{
                        background:
                          "radial-gradient(circle at 50% 0%, rgba(212,175,55,0.18), transparent 60%)",
                        opacity: isHovered ? 1 : 0,
                        transition: "opacity 450ms ease",
                      }}
                    />

                    <div className="relative flex h-full flex-col p-8">
                      {/* Step number */}
                      <div
                        className="font-serif text-5xl text-[#6D8196]/70"
                        style={{
                          transition: "color 450ms ease, transform 450ms ease",
                          color: isHovered ? "#6D8196" : "rgba(109,129,150,0.55)",
                        }}
                      >
                        {step.num}
                      </div>

                      {/* Icon */}
                      <div
                        className="mt-6 inline-flex h-14 w-14 items-center justify-center rounded-2xl border border-[#6D8196]/20 bg-gradient-to-br from-white to-[#F8F5E8]"
                        style={{
                          transition:
                            "transform 450ms cubic-bezier(0.22,1,0.36,1), box-shadow 450ms ease",
                          transform: isHovered
                            ? "rotate(-4deg) scale(1.08) translateY(-4px)"
                            : "rotate(0deg) scale(1)",
                          boxShadow: isHovered
                            ? "0 25px 60px rgba(0,0,0,0.12), 0 0 30px rgba(212,175,55,0.20), inset 0 1px 0 rgba(255,255,255,0.9)"
                            : "none",
                        }}
                      >
                        <step.Icon className="h-6 w-6 text-[#4A4A4A]" strokeWidth={1.5} />
                      </div>

                      {/* Title */}
                      <h3
                        className="text-2xl font-bold leading-tight tracking-tight text-[#4A4A4A]"
                        style={{
                          transition: "margin 450ms cubic-bezier(0.22,1,0.36,1)",
                          marginTop: isHovered ? "1.25rem" : "auto",
                          paddingTop: isHovered ? 0 : "1.5rem",
                        }}
                      >
                        {step.title}
                      </h3>

                      {/* Description */}
                      <p
                        className="mt-4 text-base leading-7 text-[#4A4A4A]/80"
                        style={{
                          opacity: isHovered ? 1 : 0,
                          maxHeight: isHovered ? 200 : 0,
                          transform: isHovered
                            ? "translateY(0)"
                            : "translateY(8px)",
                          marginTop: isHovered ? "0.75rem" : 0,
                          transition:
                            "opacity 400ms ease 80ms, transform 450ms cubic-bezier(0.22,1,0.36,1) 80ms, max-height 450ms ease, margin 450ms ease",
                          overflow: "hidden",
                        }}
                      >
                        {step.desc}
                      </p>
                    </div>
                  </article>
                </div>

                {/* Connector */}
                {idx < STEPS.length - 1 && (
                  <div
                    aria-hidden
                    className="hidden lg:flex items-center justify-center px-1"
                    style={{
                      opacity: inView ? 1 : 0,
                      transition: `opacity 600ms ease ${
                        900 + idx * 140
                      }ms`,
                    }}
                  >
                    <Connector
                      glow={hovered === idx || hovered === idx + 1}
                    />
                  </div>
                )}

                {/* Mobile down arrow */}
                {idx < STEPS.length - 1 && (
                  <div
                    aria-hidden
                    className="flex lg:hidden items-center justify-center"
                    style={{
                      opacity: inView ? 1 : 0,
                      transition: `opacity 600ms ease ${
                        900 + idx * 140
                      }ms`,
                    }}
                  >
                    <div className="h-10 w-px bg-gradient-to-b from-transparent via-[#6D8196]/40 to-transparent" />
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}

function Connector({ glow }) {
  return (
    <div
      className="relative flex items-center"
      style={{
        transition: "filter 400ms ease, opacity 400ms ease",
        filter: glow
          ? "drop-shadow(0 0 8px rgba(212,175,55,0.45))"
          : "none",
        opacity: glow ? 1 : 0.55,
      }}
    >
      <div
        className="h-px w-10"
        style={{
          background:
            "linear-gradient(to right, rgba(109,129,150,0.15), rgba(109,129,150,0.65))",
        }}
      />
      <ArrowRight
        className="h-4 w-4 -ml-1 text-[#6D8196]"
        strokeWidth={1.75}
      />
    </div>
  );
}
