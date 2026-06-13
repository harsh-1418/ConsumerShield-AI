import { useEffect, useRef, useState } from "react";
import {
  Shield,
  Scale,
  Gavel,
  FileText,
  ArrowRight,
  BookOpen,
  FileSearch,
  CheckCircle2,
  BrainCircuit,
  BadgeCheck,
} from "lucide-react";

const FEATURE_PILLS = [
  { label: "Know Your Rights", icon: BookOpen },
  { label: "Analyze My Case", icon: FileSearch },
  { label: "Check Consumer Rights", icon: CheckCircle2 },
];

const LEGAL_PARAGRAPHS = [
  "Consumer Protection Act, 2019 — Section 2(7). 'Consumer' means any person who buys any goods for a consideration which has been paid or promised or partly paid and partly promised, or under any system of deferred payment, and includes any user of such goods other than the person who buys such goods for consideration paid or promised or partly paid or partly promised, or under any system of deferred payment, when such use is made with the approval of such person, but does not include a person who obtains such goods for resale or for any commercial purpose.",
  "Section 2(11). 'Defect' means any fault, imperfection or shortcoming in the quality, quantity, potency, purity or standard which is required to be maintained by or under any law for the time being in force or under any contract, express or implied, or as is claimed by the trader in any manner whatsoever in relation to any goods or product and the expression 'defective' shall be construed accordingly.",
  "Section 2(47). 'Unfair trade practice' means a trade practice which, for the purpose of promoting the sale, use or supply of any goods or for the provision of any service, adopts any unfair method or unfair or deceptive practice including the practice of making any statement, whether orally or in writing or by visible representation which falsely represents that the goods are of a particular standard, quality, quantity, grade, composition, style or model.",
  "Section 17. A complaint relating to violation of consumer rights or unfair trade practices or misleading advertisements which are prejudicial to the interests of consumers as a class, may be forwarded either in writing or in electronic mode, to any one of the authorities, namely, the District Collector or the Commissioner of regional office or the Central Authority.",
  "Consumer Protection (E-Commerce) Rules, 2020 — Rule 4(2). Every e-commerce entity shall provide the following information in a clear and accessible manner, displayed prominently to its users, namely: legal name of the e-commerce entity; principal geographic address of its headquarters and all branches; name and details of its website; contact details like e-mail address, fax, landline and mobile numbers of customer care as well as of grievance officer.",
  "Rule 4(5). Every e-commerce entity shall establish an adequate grievance redressal mechanism having regard to the number of grievances ordinarily received by such entity from India, and shall display the name, contact details, and designation of the grievance officer on its platform. The grievance officer shall acknowledge the receipt of any consumer complaint within forty-eight hours and redress the complaint within a period of one month from the date of receipt of the complaint.",
  "Rule 5(3). No seller offering goods or services through a marketplace e-commerce entity shall refuse to take back goods, or withdraw or discontinue services purchased or agreed to be purchased, or refuse to refund consideration, if paid, if such goods or services are defective, deficient or spurious, or if the goods or services are not of the characteristics or features as advertised or as agreed to, or if such goods or services are delivered late from the stated delivery schedule.",
  "Consumer Protection (E-Commerce) Amendment Rules, 2021 — Rule 5(16). No e-commerce entity shall manipulate the price of the goods or services offered on its platform in such a manner as to gain unreasonable profit by imposing on consumers any unjustified price having regard to the prevailing market conditions, the essential nature of the good or service, any extraordinary circumstances under which the good or service is offered, and any other relevant consideration in determining whether the price charged is justified.",
  "RBI Integrated Ombudsman Scheme, 2021 — Clause 10. Any customer aggrieved by an act or omission of a Regulated Entity resulting in deficiency in service may, himself or through an authorised representative, make a complaint to the Ombudsman within whose jurisdiction the branch or office of the Regulated Entity complained against, is located. The complaint shall be in writing duly signed by the complainant or his authorised representative and may also be filed electronically through the portal designed for the purpose.",
  "Clause 11. The Ombudsman shall not entertain a complaint if the complainant had not made a written complaint to the Regulated Entity named in the complaint and the Regulated Entity had rejected the complaint, or the complainant had not received any reply within a period of thirty days after the Regulated Entity received the complaint, or the complainant is not satisfied with the reply given to him by the Regulated Entity.",
  "Clause 12. The Ombudsman may, at any stage of the proceedings, endeavour to promote a settlement of the complaint by agreement between the complainant and the Regulated Entity through facilitation or conciliation or mediation. For this purpose, the Ombudsman may follow such procedure as he may consider appropriate and the proceedings before the Ombudsman shall be summary in nature and shall not be bound by any rules of evidence.",
];

function LegalTextLayer() {
  const repeated = [
    ...LEGAL_PARAGRAPHS,
    ...LEGAL_PARAGRAPHS,
    ...LEGAL_PARAGRAPHS,
    ...LEGAL_PARAGRAPHS,
  ];

  return (
    <div
      aria-hidden
      className="pointer-events-none absolute inset-0 overflow-hidden select-none"
    >
      {/* First copy */}
      <div
        className="absolute left-0 top-0 w-full animate-legal-scroll px-6 py-7 text-[#4A4A4A]"
        style={{
          opacity: 0.2,
          columnCount: 2,
          columnGap: "1.25rem",
          columnRule: "1px solid rgba(74,74,74,0.05)",
          fontFamily:
            'ui-serif, Georgia, Cambria, "Times New Roman", Times, serif',
          fontSize: "7.5px",
          lineHeight: "1.55",
          textAlign: "justify",
          hyphens: "auto",
          WebkitHyphens: "auto",
        }}
      >
        {repeated.map((t, i) => (
          <p key={i} className="mb-2 break-inside-avoid-column">
            {t}
          </p>
        ))}
      </div>

      {/* Second copy for seamless infinite loop */}
      <div
        className="absolute left-0 top-full w-full animate-legal-scroll px-6 py-7 text-[#4A4A4A]"
        style={{
          opacity: 0.03,
          columnCount: 2,
          columnGap: "1.25rem",
          columnRule: "1px solid rgba(74,74,74,0.05)",
          fontFamily:
            'ui-serif, Georgia, Cambria, "Times New Roman", Times, serif',
          fontSize: "7.5px",
          lineHeight: "1.55",
          textAlign: "justify",
          hyphens: "auto",
          WebkitHyphens: "auto",
        }}
      >
        {repeated.map((t, i) => (
          <p key={`copy-${i}`} className="mb-2 break-inside-avoid-column">
            {t}
          </p>
        ))}
      </div>

      {/* Fade edges */}
      <div
        className="absolute inset-0"
        style={{
          background:
            "radial-gradient(120% 100% at 50% 50%, rgba(255,255,235,0) 55%, rgba(255,255,235,0.85) 100%)",
        }}
      />
    </div>
  );
}

export default function Hero() {
  const ref = useRef(null);
  const [p, setP] = useState({ x: 0, y: 0 });
  const [reduced, setReduced] = useState(false);

  useEffect(() => {
    const mq = window.matchMedia("(prefers-reduced-motion: reduce)");
    const u = () => setReduced(mq.matches);
    u();
    mq.addEventListener("change", u);
    return () => mq.removeEventListener("change", u);
  }, []);

  useEffect(() => {
    if (reduced) return;
    const onMove = (e) => {
      const el = ref.current;
      if (!el) return;
      const r = el.getBoundingClientRect();
      setP({
        x: (e.clientX - r.left) / r.width - 0.5,
        y: (e.clientY - r.top) / r.height - 0.5,
      });
    };
    window.addEventListener("mousemove", onMove);
    return () => window.removeEventListener("mousemove", onMove);
  }, [reduced]);

  const par = (d) => ({
    transform: reduced ? undefined : `translate3d(${p.x * d}px, ${p.y * d}px, 0)`,
  });

  return (
    <section
      id="home"
      ref={ref}
      aria-label="ConsumerShield AI hero"
      className="relative isolate min-h-svh overflow-hidden text-[#4A4A4A]"
style={{
  background: `
    radial-gradient(circle at 72% 18%, rgba(109,129,150,0.08) 0%, transparent 35%),
    linear-gradient(
      180deg,
      #F8F5E8 0%,
      #F3EFD9 45%,
      #ECE6D2 100%
    )
  `,
}}
    >
      {/* Background — editorial paper surface */}
      <div aria-hidden className="pointer-events-none absolute inset-0 -z-10">
        {/* Base atmospheric gradient — ivory blended into warm light gray */}
        <div
          className="absolute inset-0"
          style={{
            background:
              "radial-gradient(120% 80% at 50% 0%, #FFFFE8 0%, #FBF8DC 45%, #F1EED2 100%)",
          }}
        />

        {/* Large soft slate-blue glow behind illustration (left/center) */}
        <div
          className="absolute -left-24 top-1/4 h-[44rem] w-[44rem] rounded-full blur-[120px]"
          style={{ background: "radial-gradient(closest-side, rgba(109,129,150,0.08), transparent 70%)" }}
        />
        {/* Warm light gray bloom right */}
        <div
          className="absolute -right-32 top-1/3 h-[40rem] w-[40rem] rounded-full blur-[120px]"
          style={{ background: "radial-gradient(closest-side, rgba(203,203,203,0.35), transparent 70%)" }}
        />
        {/* Subtle bottom bloom for depth */}
        <div
          className="absolute -bottom-40 left-1/4 h-[34rem] w-[34rem] rounded-full blur-[120px]"
          style={{ background: "radial-gradient(closest-side, rgba(109,129,150,0.06), transparent 70%)" }}
        />

        {/* Crumpled paper texture — fine SVG noise, almost invisible */}
        <div
          className="absolute inset-0 opacity-[0.07] mix-blend-multiply"
          style={{
            backgroundImage:
              "url(\"data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='220' height='220'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='2' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 0.29 0 0 0 0 0.29 0 0 0 0 0.29 0 0 0 0.55 0'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>\")",
            backgroundSize: "220px 220px",
          }}
        />
        {/* Soft irregular crease shadows — barely-there paper folds */}
        <div
          className="absolute inset-0 opacity-[0.5]"
          style={{
            background:
              "radial-gradient(900px 280px at 18% 30%, rgba(79, 24, 24, 0.04), transparent 60%), radial-gradient(700px 220px at 82% 65%, rgba(74,74,74,0.03), transparent 60%), radial-gradient(500px 180px at 55% 85%, rgba(74,74,74,0.025), transparent 60%)",
          }}
        />
        {/* Gentle edge vignette — light falloff without darkening */}
        <div
          className="absolute inset-0"
          style={{
            background:
              "radial-gradient(140% 100% at 50% 50%, transparent 55%, rgba(74,74,74,0.06) 100%)",
          }}
        />

        <svg
          viewBox="0 0 400 400"
          className="absolute inset-[15%] h-[70%] w-[70%] transition-all duration-700 group-hover:scale-105"
          preserveAspectRatio="none"
        >
          <defs>
            <linearGradient id="orgA" x1="0" y1="0" x2="1" y2="1">
              <stop offset="0%" stopColor="#6D8196" stopOpacity="0.10" />
              <stop offset="100%" stopColor="#6D8196" stopOpacity="0" />
            </linearGradient>
            <linearGradient id="orgB" x1="0" y1="1" x2="1" y2="0">
              <stop offset="0%" stopColor="#CBCBCB" stopOpacity="0.6" />
              <stop offset="100%" stopColor="#CBCBCB" stopOpacity="0" />
            </linearGradient>
          </defs>
          <path
            d="M0,520 C260,420 520,640 820,520 C1080,420 1240,580 1440,470 L1440,900 L0,900 Z"
            fill="url(#orgA)"
          />
          <path
            d="M0,300 C220,220 460,360 720,280 C980,200 1200,340 1440,260"
            stroke="url(#orgB)"
            strokeWidth="1.2"
            fill="none"
          />
        </svg>
      </div>

      <div className="mx-auto grid min-h-svh max-w-7xl grid-cols-1 items-center gap-14 px-6 pt-28 pb-16 lg:grid-cols-[60fr_40fr] lg:gap-12 lg:pt-24 lg:pb-24">
        {/* LEFT — Illustration + feature pills */}
        <div className="order-1 flex flex-col items-center gap-8 lg:order-1 lg:items-stretch">
          <div className="group relative mx-auto aspect-square w-full max-w-[640px]">
            {/* Focal light behind illustration */}
            <div
              aria-hidden
              className="pointer-events-none absolute inset-[-8%] -z-10"
              style={{
                background:
                  "radial-gradient(closest-side, rgba(255,255,235,0.95), rgba(255,255,227,0.4) 55%, transparent 75%)",
              }}
            />
            {/* Ambient ground shadow */}
            <div
              aria-hidden
              className="pointer-events-none absolute left-[8%] right-[8%] bottom-[2%] h-10 rounded-[50%] blur-2xl"
              style={{ background: "rgba(74,74,74,0.18)" }}
            />
            {/* Soft paper layers */}
            <div
              className="absolute inset-[6%] overflow-hidden rounded-[2.5rem] bg-gradient-to-br from-white/85 to-white/60 shadow-[0_40px_90px_-30px_rgba(74,74,74,0.4),inset_0_1px_0_0_rgba(255,255,255,0.9)] ring-1 ring-[#6D8196]/10 backdrop-blur-sm"
              style={par(-6)}
            >
              <LegalTextLayer />
            </div>
            <div
              className="absolute inset-[14%] rounded-[2rem] bg-[#CBCBCB]/30 ring-1 ring-[#6D8196]/10"
              style={par(-12)}
            />

            {/* Concentric minimal rings */}
            <div
                className="orbit-slow absolute inset-0 rounded-full border-2 border-[#6D8196]/30 transition-all duration-700 group-hover:border-[#6D8196]/70"
                style={par(8)}
              />

              <div
                className="orbit-fast absolute inset-[10%] rounded-full border border-[#6D8196]/25 transition-all duration-700 group-hover:border-[#6D8196]/60"
                style={par(14)}
              />
            {/* Minimal network lines */}
            <svg viewBox="0 0 400 400" className="absolute inset-[15%] h-[70%] w-[70%]" aria-hidden style={par(6)}>
              {[
                [60, 90, 200, 200],
                [340, 80, 200, 200],
                [80, 320, 200, 200],
                [330, 320, 200, 200],
                [200, 40, 200, 200],
                [200, 360, 200, 200],
              ].map(([x1, y1, x2, y2], i) => (
                <line
                  key={i}
                  x1={x1}
                  y1={y1}
                  x2={x2}
                  y2={y2}
                  stroke="#6D8196"
                  strokeOpacity="0.5"
                  strokeWidth="0.8"
                />
              ))}
              {[
                [60, 90],
                [340, 80],
                [80, 320],
                [330, 320],
                [200, 40],
                [200, 360],
              ].map(([cx, cy], i) => (
                <circle key={i} cx={cx} cy={cy} r="4" fill="#6D8196" fillOpacity="0.6" />
              ))}
            </svg>

            {/* Center shield */}
                <div
                  className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 animate-float"
                  style={par(-14)}
                >
                  <div className="relative">

                    {/* Ambient glow */}
                    <div
                      className="absolute inset-0 scale-150 rounded-full blur-3xl"
                      style={{
                        background:
                          "radial-gradient(circle, rgba(255,255,227,0.45), transparent 70%)",
                      }}
                    />

                    {/* Shield box */}
                    <div
                      className="relative grid h-36 w-36 place-items-center rounded-3xl text-[#FFFFE3]"
                      style={{
                        background:
                          "linear-gradient(135deg,#8397AA 0%,#6D8196 45%,#556879 100%)",
                        boxShadow:
                          "0 30px 80px -20px rgba(109,129,150,0.45)",
                      }}
                    >
                      <div
                className="relative grid h-36 w-36 place-items-center rounded-3xl text-[#FFFFE3]"
                style={{
                  background:
                    "linear-gradient(135deg,#8397AA 0%,#6D8196 45%,#556879 100%)",
                  boxShadow:
                    "0 30px 80px -20px rgba(109,129,150,0.45)",
                }}
              >

                <div
                  className="absolute h-28 w-28 rounded-full blur-3xl"
                  style={{
                    background:
                      "radial-gradient(circle, rgba(255,255,227,0.45), transparent 70%)",
                  }}
                />

                <Shield
                  className="relative z-10 h-16 w-16"
                  strokeWidth={1.4}
                  style={{
                    filter:
                      "drop-shadow(0 0 6px rgba(255,255,227,0.8)) drop-shadow(0 0 18px rgba(255,255,227,0.4))",
                  }}
                />

              </div>
                    </div>

                  </div>
                </div>
                              
                          

            {/* Scales of justice */}
            <div className="absolute left-[4%] top-[44%] animate-float [animation-delay:0.8s]" style={par(-22)}>
              <div className="grid h-16 w-16 place-items-center rounded-2xl bg-white shadow-[0_14px_40px_-16px_rgba(74,74,74,0.35)] ring-1 ring-[#6D8196]/15">
                <Scale className="h-8 w-8 text-[#6D8196]" />
              </div>
            </div>

            {/* Gavel */}
            <div className="absolute right-[4%] top-[16%] animate-float [animation-delay:1.4s]" style={par(-18)}>
              <div className="grid h-16 w-16 place-items-center rounded-2xl bg-white shadow-[0_14px_40px_-16px_rgba(74,74,74,0.35)] ring-1 ring-[#6D8196]/15">
                <Gavel className="h-8 w-8 text-[#6D8196]" />
              </div>
            </div>

            {/* Floating legal document cards */}
            <div
              className="absolute left-[2%] top-[6%] w-48 -rotate-2 animate-float [animation-delay:0.4s] rounded-xl bg-white/85 p-3.5 shadow-[0_18px_50px_-20px_rgba(74,74,74,0.35)] ring-1 ring-[#6D8196]/15 backdrop-blur-md"
              style={par(-28)}
            >
              <div className="flex items-center gap-2">
                <FileText className="h-4 w-4 text-[#6D8196]" aria-hidden />
                <span className="text-[11px] font-semibold uppercase tracking-wider text-[#6D8196]">
                  Complaint Draft
                </span>
              </div>
              <p className="mt-2 text-xs font-medium text-[#4A4A4A]">Refund request · Sec. 2(7) CPA</p>
              <div className="mt-2 space-y-1.5">
                <div className="h-1 w-full rounded bg-[#CBCBCB]/70" />
                <div className="h-1 w-3/4 rounded bg-[#CBCBCB]/70" />
                <div className="h-1 w-2/3 rounded bg-[#CBCBCB]/70" />
              </div>
            </div>

            <div
              className="absolute right-[2%] bottom-[18%] w-48 rotate-2 animate-float [animation-delay:1.8s] rounded-xl bg-white/85 p-3.5 shadow-[0_18px_50px_-20px_rgba(74,74,74,0.35)] ring-1 ring-[#6D8196]/15 backdrop-blur-md"
              style={par(-30)}
            >
              <div className="flex items-center gap-2">
                <BrainCircuit className="h-4 w-4 text-[#6D8196]" aria-hidden />
                <span className="text-[11px] font-semibold uppercase tracking-wider text-[#6D8196]">
                  AI Analysis
                </span>
              </div>
              <p className="mt-2 text-xs font-medium text-[#4A4A4A]">Case strength · 92% match</p>
              <div className="mt-2 h-1.5 w-full overflow-hidden rounded-full bg-[#CBCBCB]/60">
                <div className="h-full w-[92%] rounded-full bg-[#6D8196]" />
              </div>
            </div>

            {/* Rights Identified card */}
            <div
              className="absolute left-[6%] bottom-[4%] w-52 -rotate-1 animate-float [animation-delay:1.2s] rounded-xl bg-white/85 p-3.5 shadow-[0_18px_50px_-20px_rgba(74,74,74,0.35)] ring-1 ring-[#6D8196]/15 backdrop-blur-md"
              style={par(-26)}
            >
              <div className="flex items-center gap-2">
                <BadgeCheck className="h-4 w-4 text-[#6D8196]" aria-hidden />
                <span className="text-[11px] font-semibold uppercase tracking-wider text-[#6D8196]">
                  Rights Identified
                </span>
              </div>
              <p className="mt-2 text-xs font-medium text-[#4A4A4A]">Replacement Eligible</p>
              <p className="mt-0.5 text-[11px] text-[#4A4A4A]/70">Consumer Protection Act</p>
            </div>
          </div>

          {/* Feature pills under illustration */}
          <div className="flex w-full flex-wrap items-center justify-center gap-3 animate-fade-up [animation-delay:420ms]">
            {FEATURE_PILLS.map(({ label, icon: Icon }) => (
              <button
                key={label}
                type="button"
                className="group inline-flex items-center gap-2 rounded-full border border-[#6D8196]/30 bg-white/60 px-5 py-2.5 text-sm font-medium text-[#4A4A4A] shadow-sm backdrop-blur-md transition-all duration-300 hover:-translate-y-0.5 hover:bg-[#6D8196] hover:text-[#FFFFE3] hover:shadow-md focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#6D8196] focus-visible:ring-offset-2 focus-visible:ring-offset-[#FFFFE3]"
              >
                <Icon className="h-4 w-4 transition-transform duration-300 group-hover:scale-110" aria-hidden />
                {label}
              </button>
            ))}
          </div>
        </div>

        {/* RIGHT — Content */}
        <div className="order-2 flex flex-col justify-center lg:order-2">
          <div className="animate-fade-up">
            <span className="inline-flex items-center gap-2 rounded-full bg-[#6D8196] px-4 py-1.5 text-xs font-medium text-[#FFFFE3] shadow-sm">
              <Scale className="h-3.5 w-3.5" aria-hidden />
              AI Powered Consumer Rights Assistant
            </span>
          </div>

          <h1 className="mt-6 text-4xl font-bold leading-[1.08] tracking-tight text-[#4A4A4A] sm:text-5xl lg:text-[3.5rem] animate-fade-up [animation-delay:120ms]">
            Protect Your Consumer Rights with Intelligent AI Assistance
          </h1>

          <p className="mt-6 max-w-[520px] text-base leading-relaxed text-[#4A4A4A]/75 sm:text-lg animate-fade-up [animation-delay:220ms]">
            Analyze complaints, discover your rights, and generate AI-powered legal guidance in seconds.
          </p>

          <div className="mt-9 animate-fade-up [animation-delay:320ms]" id="get-started">
            <button
              type="button"
              className="group inline-flex items-center gap-2 rounded-xl bg-[#6D8196] px-8 py-4 text-base font-semibold text-[#FFFFE3] shadow-[0_14px_36px_-14px_rgba(109,129,150,0.7)] transition-all duration-300 hover:-translate-y-0.5 hover:scale-[1.03] hover:bg-[#5b6d80] hover:shadow-[0_22px_50px_-16px_rgba(109,129,150,0.8)] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#6D8196] focus-visible:ring-offset-2 focus-visible:ring-offset-[#FFFFE3]"
            >
              Get Started
              <ArrowRight className="h-5 w-5 transition-transform duration-300 group-hover:translate-x-1" />
            </button>
          </div>
        </div>
      </div>
    </section>
  );
}