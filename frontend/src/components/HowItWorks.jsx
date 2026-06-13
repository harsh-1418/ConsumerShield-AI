import React, { useRef, useEffect, useState } from "react";
import { PenLine, BrainCircuit, Scale, FileText } from "lucide-react";

/**
 * ConsumerShield AI — "How It Works" Section
 * Continuation of Hero / Features design system.
 *
 * Palette:
 *  - Backgrounds: #FCFAF2, #F8F5E8, #F4F0E2
 *  - Accent:      #6D8196
 *  - Text:        #4A4A4A
 */

const STEPS = [
  {
    id: "01",
    title: "Describe Your Issue",
    desc: "Enter your complaint naturally with supporting details.",
    icon: PenLine,
  },
  {
    id: "02",
    title: "AI Analysis",
    desc: "ConsumerShield AI analyzes your complaint using AI and legal reasoning.",
    icon: BrainCircuit,
  },
  {
    id: "03",
    title: "Rights Detection",
    desc: "Applicable consumer rights and legal provisions are automatically identified.",
    icon: Scale,
  },
  {
    id: "04",
    title: "Receive Guidance",
    desc: "Receive complaint drafts, recommendations and suggested next actions.",
    icon: FileText,
  },
];

const LEGAL_TEXT = `Consumer Protection Act, 2019 — Section 2(7) "consumer" means any person who buys any goods for a consideration... Right to be heard, Right to seek redressal, Right to consumer awareness, Right to safety, Right to choose... RBI Integrated Ombudsman Scheme, 2021 — Clause 9: The Ombudsman shall endeavour to promote, through conciliation or mediation, a settlement between the complainant and the Regulated Entity... No fee shall be charged by the Office of the Ombudsman for any complaint... Rule 4(5): Every e-commerce entity shall establish an adequate grievance redressal mechanism... `;

export default function HowItWorks() {
  const [visible, setVisible] = useState(false);
  const [activeIndex, setActiveIndex] = useState(null);
  const sectionRef = useRef(null);

  useEffect(() => {
    const obs = new IntersectionObserver(
      ([entry]) => entry.isIntersecting && setVisible(true),
      { threshold: 0.15 }
    );
    if (sectionRef.current) obs.observe(sectionRef.current);
    return () => obs.disconnect();
  }, []);

  return (
    <section
      ref={sectionRef}
      className="relative min-h-screen w-full overflow-hidden flex flex-col items-center justify-center py-24 px-6"
      style={{ background: "linear-gradient(180deg, #FCFAF2 0%, #F8F5E8 55%, #F4F0E2 100%)" }}
    >
      <BackgroundTexture />

      {/* Header */}
      <div
        className={`relative z-10 text-center max-w-3xl mx-auto mb-20 transition-all duration-1000 ease-out ${
          visible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-8"
        }`}
      >
        <p
          className="text-sm font-semibold tracking-[0.2em] mb-4"
          style={{ color: "#6D8196" }}
        >
          HOW IT WORKS
        </p>
        <h2
          className="text-4xl sm:text-5xl lg:text-6xl font-extrabold leading-[1.1] mb-6"
          style={{ color: "#4A4A4A" }}
        >
          From Complaint
          <br />
          To Resolution
        </h2>
        <p className="text-base sm:text-lg leading-relaxed" style={{ color: "#6D8196" }}>
          ConsumerShield AI transforms consumer complaints into actionable legal
          guidance using AI-powered analysis and consumer protection intelligence.
        </p>
      </div>

      {/* Workflow */}
      <div className="relative z-10 w-full max-w-7xl mx-auto">
        {/* Desktop / large tablet: horizontal row with connectors */}
        <div className="hidden lg:flex items-stretch justify-between gap-0">
          {STEPS.map((step, i) => (
            <React.Fragment key={step.id}>
              <StepCard
                step={step}
                index={i}
                visible={visible}
                isActive={activeIndex === i}
                onHover={() => setActiveIndex(i)}
                onLeave={() => setActiveIndex(null)}
                className="flex-1"
              />
              {i < STEPS.length - 1 && (
                <Connector
                  visible={visible}
                  index={i}
                  active={activeIndex === i || activeIndex === i + 1}
                />
              )}
            </React.Fragment>
          ))}
        </div>

        {/* Tablet: 2x2 grid */}
        <div className="hidden md:grid lg:hidden grid-cols-2 gap-6">
          {STEPS.map((step, i) => (
            <StepCard
              key={step.id}
              step={step}
              index={i}
              visible={visible}
              isActive={activeIndex === i}
              onHover={() => setActiveIndex(i)}
              onLeave={() => setActiveIndex(null)}
            />
          ))}
        </div>

        {/* Mobile: vertical timeline */}
        <div className="flex md:hidden flex-col items-center gap-0">
          {STEPS.map((step, i) => (
            <React.Fragment key={step.id}>
              <StepCard
                step={step}
                index={i}
                visible={visible}
                isActive={activeIndex === i}
                onHover={() => setActiveIndex(i)}
                onLeave={() => setActiveIndex(null)}
                className="w-full"
              />
              {i < STEPS.length - 1 && (
                <VerticalConnector visible={visible} index={i} active={activeIndex === i} />
              )}
            </React.Fragment>
          ))}
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
            style={{ animationDuration: `${100 + col * 8}s`, animationDelay: `${col * -25}s` }}
          >
            {repeated}
          </div>
        ))}
      </div>

      {/* Soft radial light */}
      <div
        className="absolute top-1/3 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[1000px] h-[1000px] rounded-full opacity-50"
        style={{ background: "radial-gradient(circle, #FCFAF2 0%, transparent 70%)" }}
      />

      {/* Continuation depth gradient from Features section */}
      <div
        className="absolute top-0 left-0 right-0 h-40"
        style={{ background: "linear-gradient(180deg, #F8F5E8 0%, transparent 100%)" }}
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
/* Step card                                                                */
/* ---------------------------------------------------------------------- */

function StepCard({ step, index, visible, isActive, onHover, onLeave, className = "" }) {
  const Icon = step.icon;
  return (
    <div
      onMouseEnter={onHover}
      onMouseLeave={onLeave}
      className={`group relative rounded-[32px] p-8 border backdrop-blur-md transition-all duration-500 ease-out cursor-default ${className}`}
      style={{
        background: "rgba(255,255,255,0.6)",
        borderColor: isActive ? "#6D819670" : "#6D819620",
        boxShadow: isActive
          ? "0 20px 40px -16px #6D819650"
          : "0 6px 20px -12px #6D819620",
        transform: isActive ? "translateY(-4px) scale(1.02)" : "translateY(0) scale(1)",
        opacity: visible ? 1 : 0,
        transitionProperty: "all, opacity, transform",
        transitionDelay: `${index * 150 + 200}ms`,
        translate: visible ? "0 0" : "0 24px",
      }}
    >
      <div className="flex items-center justify-between mb-6">
        <span className="text-xs font-bold tracking-widest" style={{ color: "#6D8196" }}>
          {step.id}
        </span>
        <div
          className="w-12 h-12 rounded-2xl flex items-center justify-center transition-transform duration-500"
          style={{
            background: "#F4F0E2",
            transform: isActive ? "scale(1.15) rotate(6deg)" : "scale(1) rotate(0deg)",
          }}
        >
          <Icon className="w-6 h-6" style={{ color: "#6D8196" }} strokeWidth={1.75} />
        </div>
      </div>
      <h3 className="text-lg font-bold mb-2" style={{ color: "#4A4A4A" }}>
        {step.title}
      </h3>
      <p className="text-sm leading-relaxed" style={{ color: "#6D8196" }}>
        {step.desc}
      </p>
    </div>
  );
}

/* ---------------------------------------------------------------------- */
/* Horizontal connector (desktop)                                          */
/* ---------------------------------------------------------------------- */

function Connector({ visible, index, active }) {
  return (
    <div className="flex items-center justify-center w-12 lg:w-16 shrink-0">
      <div className="relative w-full h-px overflow-hidden" style={{ background: "#6D819625" }}>
        <div
          className="absolute inset-y-0 left-0 h-px transition-all duration-700 ease-out"
          style={{
            background: "#6D8196",
            opacity: active ? 0.6 : 0.3,
            width: visible ? "100%" : "0%",
            transitionDelay: `${index * 150 + 400}ms`,
          }}
        />
        {visible && (
          <div
            className="absolute top-1/2 -translate-y-1/2 w-2 h-2 rounded-full"
            style={{
              background: "#6D8196",
              boxShadow: "0 0 8px 2px #6D819680",
              animation: `connector-travel ${active ? "1.4s" : "3s"} linear infinite`,
              animationDelay: `${index * 0.3}s`,
            }}
          />
        )}
      </div>
    </div>
  );
}

/* ---------------------------------------------------------------------- */
/* Vertical connector (mobile)                                              */
/* ---------------------------------------------------------------------- */

function VerticalConnector({ visible, index, active }) {
  return (
    <div className="flex items-center justify-center h-10 w-px relative">
      <div className="relative w-px h-full overflow-hidden" style={{ background: "#6D819625" }}>
        <div
          className="absolute inset-x-0 top-0 w-px transition-all duration-700 ease-out"
          style={{
            background: "#6D8196",
            opacity: active ? 0.6 : 0.3,
            height: visible ? "100%" : "0%",
            transitionDelay: `${index * 150 + 400}ms`,
          }}
        />
        {visible && (
          <div
            className="absolute left-1/2 -translate-x-1/2 w-2 h-2 rounded-full"
            style={{
              background: "#6D8196",
              boxShadow: "0 0 8px 2px #6D819680",
              animation: `connector-travel-vertical ${active ? "1.4s" : "3s"} linear infinite`,
              animationDelay: `${index * 0.3}s`,
            }}
          />
        )}
      </div>
    </div>
  );
}

/* ---------------------------------------------------------------------- */
/* Add to global stylesheet (e.g. index.css)                               */
/* ---------------------------------------------------------------------- */

/*
@keyframes legal-scroll {
  from { transform: translateY(0); }
  to   { transform: translateY(-50%); }
}
@keyframes connector-travel {
  from { left: 0%; opacity: 0; }
  10%  { opacity: 1; }
  90%  { opacity: 1; }
  to   { left: 100%; opacity: 0; }
}
@keyframes connector-travel-vertical {
  from { top: 0%; opacity: 0; }
  10%  { opacity: 1; }
  90%  { opacity: 1; }
  to   { top: 100%; opacity: 0; }
}

.animate-legal-scroll { animation: legal-scroll linear infinite; }
*/
