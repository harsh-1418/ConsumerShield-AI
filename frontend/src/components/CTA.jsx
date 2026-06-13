import React, { useRef, useEffect, useState } from "react";
import { ShieldCheck, Lock, Zap, Scale, ArrowRight } from "lucide-react";

/**
 * ConsumerShield AI — Final CTA Section
 * Sits between "How It Works" and the Footer.
 * Continues the Hero / Features / How It Works design system.
 *
 * Palette:
 *  - Backgrounds: #FCFAF2, #F8F5E8, #F4F0E2
 *  - Accent:      #6D8196
 *  - Text:        #4A4A4A
 */

const LEGAL_TEXT = `Consumer Protection Act, 2019 — Section 2(7) "consumer" means any person who buys any goods for a consideration... Right to be heard, Right to seek redressal, Right to consumer awareness, Right to safety, Right to choose... RBI Integrated Ombudsman Scheme, 2021 — Clause 9: The Ombudsman shall endeavour to promote, through conciliation or mediation, a settlement between the complainant and the Regulated Entity... No fee shall be charged by the Office of the Ombudsman for any complaint... Rule 4(5): Every e-commerce entity shall establish an adequate grievance redressal mechanism... `;

const TRUST_ITEMS = [
  { icon: Lock, label: "Secure" },
  { icon: Zap, label: "Instant AI Analysis" },
  { icon: Scale, label: "Consumer Rights Focused" },
];

export default function CTASection() {
  const [visible, setVisible] = useState(false);
  const [hovered, setHovered] = useState(false);
  const sectionRef = useRef(null);

  useEffect(() => {
    const obs = new IntersectionObserver(
      ([entry]) => entry.isIntersecting && setVisible(true),
      { threshold: 0.2 }
    );
    if (sectionRef.current) obs.observe(sectionRef.current);
    return () => obs.disconnect();
  }, []);

  <div
  className="absolute top-0 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[1200px] h-[500px] rounded-full blur-3xl -z-10"
  style={{
    background:
      "radial-gradient(circle, rgba(255,255,227,0.65), transparent 70%)",
  }}
/>

  return (
    <section
      ref={sectionRef}
      className="relative w-full overflow-hidden flex items-center justify-center py-24 px-6"
      style={{
        minHeight: "80vh",
        background: "linear-gradient(180deg, #F4F0E2 0%, #F8F5E8 50%, #FCFAF2 100%)",
      }}
    >
      <BackgroundTexture />

      {/* Glass card */}
      <div
  className="absolute inset-0 rounded-[40px] pointer-events-none"
  style={{
    background:
      "linear-gradient(180deg, rgba(255,255,255,0.30) 0%, transparent 25%, transparent 75%, rgba(109,129,150,0.04) 100%)",
  }}
/>

    
      <div
        onMouseEnter={() => setHovered(true)}
        onMouseLeave={() => setHovered(false)}
        className="relative z-10 w-full max-w-5xl mx-auto rounded-[40px] border backdrop-blur-xl px-8 sm:px-14 py-16 sm:py-20 text-center overflow-hidden transition-all duration-700 ease-out"
        style={{
          background: `
            linear-gradient(
            135deg,
            rgba(255,255,255,0.42) 0%,
            rgba(255,255,255,0.60) 35%,
            rgba(255,255,255,0.50) 65%,
            rgba(255,255,255,0.38) 100%
            )
            `,
          borderColor: hovered ? "#6D819670" : "#6D819625",
          boxShadow: hovered
            ? "0 24px 60px -20px #6D819660"
            : "0 12px 40px -20px #6D819635",
          opacity: visible ? 1 : 0,
          translate: visible ? "0 0" : "0 32px",
          transitionProperty: "all, opacity, translate",
        }}
      >
        {/* Watermark shield */}
        <ShieldCheck
          className="absolute inset-0 m-auto pointer-events-none transition-opacity duration-700"
          style={{
            width: "70%",
            height: "70%",
            color: "#6D8196",
            opacity: hovered ? 0.035 : 0.018,
          }}
          strokeWidth={1}
        />

        {/* Inner glow that responds to hover */}
        <div
  className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[700px] h-[700px] rounded-full pointer-events-none transition-opacity duration-700"
  style={{
    background:
      "radial-gradient(circle, rgba(109,129,150,0.08) 0%, transparent 75%)",
    opacity: 1,
  }}
/>

        {/* Content */}
        <div className="relative z-10">
          <h2
            className={`text-4xl sm:text-5xl lg:text-6xl font-extrabold leading-[1.1] mb-6 transition-all duration-700 ease-out ${
              visible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-6"
            }`}
            style={{ color: "#4A4A4A", transitionDelay: "100ms" }}
          >
            Ready to Protect
            <br />
            Your Consumer Rights?
          </h2>

          <p
            className={`text-base sm:text-lg leading-relaxed max-w-2xl mx-auto mb-10 transition-all duration-700 ease-out ${
              visible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-6"
            }`}
            style={{ color: "#6D8196", transitionDelay: "200ms" }}
          >
            Get AI-powered legal guidance, analyze complaints, discover your
            rights, and generate professional complaint drafts within seconds.
          </p>

          {/* Buttons */}
          <div
            className={`flex flex-col sm:flex-row items-center justify-center gap-4 mb-12 transition-all duration-700 ease-out ${
              visible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-6"
            }`}
            style={{ transitionDelay: "300ms" }}
          >
            <button
              className="group relative inline-flex items-center justify-center gap-2 px-8 py-4 rounded-full font-semibold text-base sm:text-lg w-full sm:w-auto transition-all duration-500 ease-out hover:-translate-y-0.5 hover:scale-[1.02]"
              style={{
                background: "#6D8196",
                color: "#FCFAF2",
                boxShadow: "0 8px 24px -8px #6D819670",
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.boxShadow = "0 14px 36px -10px #6D8196a0";
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.boxShadow = "0 8px 24px -8px #6D819670";
              }}
            >
              Analyze My Complaint
              <ArrowRight className="w-5 h-5 transition-transform duration-500 ease-out group-hover:translate-x-1.5" />
            </button>

            <button
              className="inline-flex items-center justify-center px-8 py-4 rounded-full font-semibold text-base sm:text-lg w-full sm:w-auto border transition-all duration-500 ease-out hover:-translate-y-0.5"
              style={{
                color: "#4A4A4A",
                borderColor: "rgba(109,129,150,0.12)",
                background: "transparent",
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.background = "#6D819615";
                e.currentTarget.style.borderColor = "#6D8196";
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.background = "transparent";
                e.currentTarget.style.borderColor = "#6D819650";
              }}
            >
              Learn More
            </button>
          </div>

          {/* Trust indicators */}
          <div
            className={`flex flex-col sm:flex-row items-center justify-center gap-6 sm:gap-10 transition-all duration-700 ease-out ${
              visible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-6"
            }`}
            style={{ transitionDelay: "400ms" }}
          >
            {TRUST_ITEMS.map(({ icon: Icon, label }) => (
              <div key={label} className="flex items-center gap-2">
                <Icon className="w-4 h-4" style={{ color: "#6D8196" }} strokeWidth={1.75} />
                <span className="text-sm font-medium" style={{ color: "#6D8196" }}>
                  {label}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}

/* ---------------------------------------------------------------------- */
/* Background: faint scrolling legal text + soft lighting + vignette       */
/* ---------------------------------------------------------------------- */

function BackgroundTexture() {
  const repeated = Array.from({ length: 8 }).fill(LEGAL_TEXT).join(" ");
  return (
    <div className="absolute inset-0 overflow-hidden pointer-events-none select-none">
      {/* Scrolling legal text columns */}
      <div className="absolute inset-0 flex gap-16 opacity-[0.1]" style={{ color: "#4A4A4A" }}>
        {[0, 1, 2, 3].map((col) => (
          <div
            key={col}
            className="flex-1 font-serif text-[11px] leading-6 whitespace-pre-wrap animate-legal-scroll"
            style={{ animationDuration: `${190 + col * 12}s`, animationDelay: `${col * -40}s` }}
          >
            {repeated}
          </div>
        ))}
      </div>

      {/* Soft radial light */}
      <div
        className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[900px] h-[900px] rounded-full opacity-50"
        style={{ background: "radial-gradient(circle, #FCFAF2 0%, transparent 70%)" }}
      />

      {/* Continuation depth gradient from How It Works section */}
      <div
        className="absolute top-0 left-0 right-0 h-40"
        style={{ background: "linear-gradient(180deg, #F4F0E2 0%, transparent 100%)" }}
      />

      {/* Vignette */}
      <div
        className="absolute inset-0"
        style={{
          background:
            "radial-gradient(ellipse at center, transparent 55%, rgba(74,74,74,0.05) 100%)",
        }}
      />
    </div>
  );
}

/* ---------------------------------------------------------------------- */
/* Add to global stylesheet (e.g. index.css) — reuse if already added      */
/* ---------------------------------------------------------------------- */

/*
@keyframes legal-scroll {
  from { transform: translateY(0); }
  to   { transform: translateY(-50%); }
}
@keyframes breathe {
  0%, 100% { transform: scale(1); opacity: 0.8; }
  50% { transform: scale(1.08); opacity: 1; }
}

.animate-legal-scroll { animation: legal-scroll linear infinite; }
.animate-breathe { animation: breathe 6s ease-in-out infinite; }
*/
