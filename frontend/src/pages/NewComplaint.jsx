import {
  analyzeComplaint,
  getCaseStrength,
  getAuthorities,
} from "../lib/apiClient";
import { useMemo, useRef, useState } from "react";
import {
  ArrowRight,
  Upload,
  FileText,
  X,
  Calendar,
  IndianRupee,
  Hash,
  Building2,
  Sparkles,
  CheckCircle2,
  Loader2,
  ChevronDown,
  Lock,
  ScanSearch,
  Scale,
  Gavel,
  Lightbulb,
  FileSignature,
} from "lucide-react";

const CATEGORIES = [
  "Electronics",
  "E-commerce",
  "Banking",
  "Insurance",
  "Healthcare",
  "Travel",
  "Telecom",
  "Education",
  "Other",
];



const STEPS = [
  { key: "complaint", label: "Complaint" },
  { key: "analysis", label: "AI Analysis" },
  { key: "guidance", label: "Legal Guidance" },
];

const CHECKLIST = [
  { icon: ScanSearch, label: "Complaint Analysis" },
  { icon: Scale, label: "Rights Detection" },
  { icon: Sparkles, label: "Case Strength Prediction" },
  { icon: Gavel, label: "Authority Recommendation" },
  { icon: FileSignature, label: "Complaint Draft Generation" },
];

const DETECTED_CONTEXT = [
  "Product Purchase",
  "Refund Request",
  "Warranty Issue",
  "Possible Right to Redressal",
];

function formatBytes(b) {
  if (b < 1024) return `${b} B`;
  if (b < 1024 * 1024) return `${(b / 1024).toFixed(1)} KB`;
  return `${(b / 1024 / 1024).toFixed(1)} MB`;
}

export default function NewComplaintWorkspace() {
  const [complaintTitle, setComplaintTitle] = useState("");
  const [complaintDescription, setComplaintDescription] = useState("");
  const [category, setCategory] = useState("");
  const [company, setCompany] = useState("");
  const [incidentDate, setIncidentDate] = useState("");
  const [amount, setAmount] = useState("");
  const [orderId, setOrderId] = useState("");
  const [evidenceFiles, setEvidenceFiles] = useState([]);  const [dragOver, setDragOver] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const fileInputRef = useRef(null);

  const descMax = 1500;
  const descCount = complaintDescription.length;

  const completion = useMemo(() => {
    let s = 0;
    if (complaintTitle.trim()) s++;
    if (complaintDescription.trim().length > 30) s++;
    if (category) s++;
    if (company.trim()) s++;
    if (incidentDate) s++;
    return Math.round((s / 5) * 100);
  }, [complaintTitle, complaintDescription, category, company, incidentDate]);

  const canSubmit =
    complaintTitle.trim().length > 0 &&
    complaintDescription.trim().length > 30 &&
    !!category &&
    company.trim().length > 0 &&
    !submitting;

  const handleFiles = (files) => {
    if (!files) return;
    const accepted = Array.from(files).filter((f) =>
      /\.(pdf|png|jpe?g)$/i.test(f.name),
    );
    setEvidenceFiles((prev) => [...prev, ...accepted].slice(0, 8));
  };

  const removeFile = (idx) =>
    setEvidenceFiles((prev) => prev.filter((_, i) => i !== idx));

  const handleSubmit = async (e) => {
  e.preventDefault();

  if (!canSubmit) return;

  setSubmitting(true);

  try {
    const complaintText = `
Complaint Title: ${complaintTitle}

Category: ${category}

Company: ${company}

Date of Incident: ${incidentDate}

Amount: ${amount}

Order ID: ${orderId}

Complaint Description:
${complaintDescription}
`;

    // Call backend APIs
    const analysis = await analyzeComplaint(complaintText);
    const strength = await getCaseStrength(complaintText);
    const authorities = await getAuthorities(complaintText);

    console.log("Analysis:", analysis);
    console.log("Strength:", strength);
    console.log("Authorities:", authorities);

    alert("Complaint analyzed successfully!");

    // We will replace this with navigation in the next step
  } catch (err) {
    console.error(err);
    alert("Something went wrong while analyzing your complaint.");
  } finally {
    setSubmitting(false);
  }
};

  return (
    <section className="relative isolate overflow-hidden pt-28 pb-24">
      {/* Background: layered ivory paper, glow, vignette */}
      <div aria-hidden className="absolute inset-0 -z-10">
        <div
          className="absolute inset-0"
          style={{
            background:
              "radial-gradient(120% 80% at 50% -10%, #FFFFE8 0%, #FBF8DC 45%, #F4F0E2 100%)",
          }}
        />
        <div
          className="absolute -top-32 left-1/2 h-[720px] w-[1100px] -translate-x-1/2 rounded-full opacity-70 blur-3xl"
          style={{
            background:
              "radial-gradient(closest-side, rgba(109,129,150,0.18), rgba(109,129,150,0) 70%)",
          }}
        />
        <div
          className="absolute bottom-0 right-0 h-[480px] w-[620px] rounded-full opacity-60 blur-3xl"
          style={{
            background:
              "radial-gradient(closest-side, rgba(203,203,203,0.35), rgba(203,203,203,0) 70%)",
          }}
        />
        {/* paper noise */}
        <div
          className="absolute inset-0 opacity-[0.07] mix-blend-multiply"
          style={{
            backgroundImage: `url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='220' height='220'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='2' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 0.29 0 0 0 0 0.29 0 0 0 0 0.29 0 0 0 0.7 0'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>")`,
          }}
        />
        {/* vignette */}
        <div
          className="absolute inset-0"
          style={{
            background:
              "radial-gradient(120% 100% at 50% 50%, rgba(74,74,74,0) 60%, rgba(74,74,74,0.08) 100%)",
          }}
        />
        <DriftingLegalText />
      </div>

      <div className="mx-auto max-w-7xl px-6">
        {/* Progress */}
        <Stepper currentIndex={0} />

        {/* Header */}
        <div className="mt-10 max-w-3xl animate-fade-up">
          <span className="inline-flex items-center gap-2 rounded-full border border-[#6D8196]/25 bg-white/60 px-3 py-1 text-[11px] font-semibold uppercase tracking-[0.18em] text-[#6D8196] backdrop-blur">
            <Sparkles className="h-3.5 w-3.5" aria-hidden />
            New Complaint
          </span>
          <h1 className="mt-5 text-4xl font-semibold tracking-tight text-[#4A4A4A] sm:text-5xl">
            Describe Your Consumer Issue
          </h1>
          <p className="mt-4 max-w-2xl text-base leading-relaxed text-[#4A4A4A]/75 sm:text-lg">
            Provide your complaint details and let ConsumerShield AI analyze
            your case, identify applicable rights, estimate case strength, and
            generate intelligent legal guidance.
          </p>
        </div>

        {/* Workspace */}
        <div className="mt-12 grid grid-cols-1 gap-8 lg:grid-cols-[1.85fr_1fr]">
          {/* Complaint workspace */}
          <form
            onSubmit={handleSubmit}
            className="animate-fade-up rounded-[32px] border border-white/60 bg-white/55 p-8 shadow-[0_30px_80px_-40px_rgba(74,74,74,0.35)] backdrop-blur-2xl sm:p-10"
            style={{ animationDelay: "120ms" }}
          >
            <div className="mb-8 flex items-center justify-between">
              <div>
                <h2 className="text-lg font-semibold text-[#4A4A4A]">
                  Complaint Workspace
                </h2>
                <p className="mt-1 text-sm text-[#4A4A4A]/65">
                  Fill in the essentials. The assistant updates as you type.
                </p>
              </div>
              <div className="hidden sm:flex items-center gap-3">
                <div className="text-right">
                  <div className="text-[11px] font-medium uppercase tracking-wider text-[#6D8196]">
                    Completion
                  </div>
                  <div className="text-sm font-semibold text-[#4A4A4A]">
                    {completion}%
                  </div>
                </div>
                <div className="h-2 w-32 overflow-hidden rounded-full bg-[#6D8196]/15">
                  <div
                    className="h-full rounded-full bg-[#6D8196] transition-[width] duration-500"
                    style={{ width: `${completion}%` }}
                  />
                </div>
              </div>
            </div>

            {/* Title */}
            <FloatingField
              id="title"
              label="Complaint Title"
              value={complaintTitle}
              onChange={setComplaintTitle}
              placeholder="e.g. Defective laptop delivered, refund denied"
            />

            {/* Category chips */}
            <div className="mt-7">
              <div className="mb-3 flex items-center justify-between">
                <label className="text-sm font-medium text-[#4A4A4A]">
                  Category
                </label>
                <div className="relative">
                  <select
                    value={category}
                    onChange={(e) => setCategory(e.target.value)}
                    className="appearance-none rounded-lg border border-[#6D8196]/25 bg-white/70 py-1.5 pl-3 pr-8 text-xs font-medium text-[#4A4A4A] backdrop-blur transition-colors hover:bg-white focus:outline-none focus:ring-2 focus:ring-[#6D8196]/40"
                    aria-label="Select category"
                  >
                    <option value="">Select…</option>
                    {CATEGORIES.map((c) => (
                      <option key={c} value={c}>
                        {c}
                      </option>
                    ))}
                  </select>
                  <ChevronDown className="pointer-events-none absolute right-2 top-1/2 h-3.5 w-3.5 -translate-y-1/2 text-[#6D8196]" />
                </div>
              </div>
              <div className="flex flex-wrap gap-2">
                {CATEGORIES.map((c) => {
                  const active = category === c;
                  return (
                    <button
                      type="button"
                      key={c}
                      onClick={() => setCategory(c)}
                      className={`rounded-full border px-3.5 py-1.5 text-xs font-medium transition-all duration-200 ${
                        active
                          ? "border-[#6D8196] bg-[#6D8196] text-[#FFFFE3] shadow-[0_8px_22px_-12px_rgba(109,129,150,0.8)]"
                          : "border-[#6D8196]/25 bg-white/60 text-[#4A4A4A]/80 hover:border-[#6D8196]/50 hover:bg-white"
                      }`}
                    >
                      {c}
                    </button>
                  );
                })}
              </div>
            </div>

            {/* Description */}
            <div className="mt-7">
              <label
                htmlFor="description"
                className="mb-2 flex items-center justify-between text-sm font-medium text-[#4A4A4A]"
              >
                <span>Complaint Description</span>
                <span
                  className={`text-xs ${
                    descCount > descMax
                      ? "text-red-500"
                      : "text-[#4A4A4A]/55"
                  }`}
                >
                  {descCount}/{descMax}
                </span>
              </label>
              <textarea
                id="description"
                value={complaintDescription}
                onChange={(e) => setComplaintDescription(e.target.value)}
                rows={7}
                placeholder="Describe what happened, when, who was involved, what you expected vs. what you received, and any resolution attempts so far…"
                className="w-full resize-y rounded-2xl border border-[#6D8196]/20 bg-white/70 px-4 py-3.5 text-[15px] leading-relaxed text-[#4A4A4A] placeholder:text-[#4A4A4A]/45 transition-all duration-200 focus:border-[#6D8196]/50 focus:bg-white focus:outline-none focus:ring-4 focus:ring-[#6D8196]/15"
              />
            </div>

            {/* Two col details */}
            <div className="mt-7 grid grid-cols-1 gap-5 sm:grid-cols-2">
              <FloatingField
                id="company"
                label="Company Name"
                value={company}
                onChange={setCompany}
                placeholder="e.g. ShopMart India Pvt. Ltd."
                icon={Building2}
              />
              <FloatingField
                id="incidentDate"
                label="Date of Incident"
                value={incidentDate}
                onChange={setIncidentDate}
                type="date"
                icon={Calendar}
              />
              <FloatingField
                id="amount"
                label="Amount (₹)"
                value={amount}
                onChange={setAmount}
                placeholder="e.g. 45,000"
                inputMode="decimal"
                icon={IndianRupee}
              />
              <FloatingField
                id="orderId"
                label="Order ID (optional)"
                value={orderId}
                onChange={setOrderId}
                placeholder="e.g. ORD-58291"
                icon={Hash}
              />
            </div>

            {/* Evidence upload */}
            <div className="mt-8">
              <label className="mb-3 block text-sm font-medium text-[#4A4A4A]">
                Evidence
              </label>
              <div
                onDragOver={(e) => {
                  e.preventDefault();
                  setDragOver(true);
                }}
                onDragLeave={() => setDragOver(false)}
                onDrop={(e) => {
                  e.preventDefault();
                  setDragOver(false);
                  handleFiles(e.dataTransfer.files);
                }}
                onClick={() => fileInputRef.current?.click()}
                role="button"
                tabIndex={0}
                onKeyDown={(e) => {
                  if (e.key === "Enter" || e.key === " ")
                    fileInputRef.current?.click();
                }}
                className={`group flex cursor-pointer flex-col items-center justify-center rounded-2xl border-2 border-dashed px-6 py-10 text-center transition-all duration-300 ${
                  dragOver
                    ? "border-[#6D8196] bg-white shadow-[0_0_0_6px_rgba(109,129,150,0.12)]"
                    : "border-[#6D8196]/30 bg-white/40 hover:border-[#6D8196]/60 hover:bg-white/70"
                }`}
              >
                <div className="grid h-12 w-12 place-items-center rounded-2xl bg-[#6D8196]/10 text-[#6D8196] transition-transform duration-300 group-hover:-translate-y-0.5">
                  <Upload className="h-5 w-5" />
                </div>
                <p className="mt-3 text-sm font-medium text-[#4A4A4A]">
                  Drop files here or{" "}
                  <span className="text-[#6D8196] underline-offset-2 group-hover:underline">
                    browse
                  </span>
                </p>
                <p className="mt-1 text-xs text-[#4A4A4A]/55">
                  PDF, PNG, JPG, JPEG · up to 8 files
                </p>
                <input
                  ref={fileInputRef}
                  type="file"
                  multiple
                  accept=".pdf,.png,.jpg,.jpeg"
                  className="hidden"
                  onChange={(e) => handleFiles(e.target.files)}
                />
              </div>

              {evidenceFiles.length > 0 && (
                <ul className="mt-4 grid grid-cols-1 gap-2 sm:grid-cols-2">
                  {evidenceFiles.map((f, i) => (
                    <li
                      key={`${f.name}-${i}`}
                      className="flex items-center justify-between gap-3 rounded-xl border border-white/70 bg-white/70 px-3.5 py-2.5 backdrop-blur"
                    >
                      <div className="flex min-w-0 items-center gap-3">
                        <div className="grid h-9 w-9 shrink-0 place-items-center rounded-lg bg-[#6D8196]/10 text-[#6D8196]">
                          <FileText className="h-4 w-4" />
                        </div>
                        <div className="min-w-0">
                          <p className="truncate text-sm font-medium text-[#4A4A4A]">
                            {f.name}
                          </p>
                          <p className="text-[11px] text-[#4A4A4A]/55">
                            {formatBytes(f.size)}
                          </p>
                        </div>
                      </div>
                      <button
                        type="button"
                        onClick={() => removeFile(i)}
                        aria-label={`Remove ${f.name}`}
                        className="grid h-7 w-7 place-items-center rounded-md text-[#4A4A4A]/55 transition-colors hover:bg-[#6D8196]/10 hover:text-[#4A4A4A]"
                      >
                        <X className="h-4 w-4" />
                      </button>
                    </li>
                  ))}
                </ul>
              )}
            </div>

            {/* CTA */}
            <div className="mt-10 flex flex-col items-stretch gap-4 sm:flex-row sm:items-center sm:justify-between">
              <p className="text-xs text-[#4A4A4A]/60">
                By analyzing, you consent to processing of complaint details for
                AI analysis only.
              </p>
              <button
                type="submit"
                disabled={!canSubmit}
                className="group inline-flex items-center justify-center gap-2 rounded-2xl bg-[#6D8196] px-7 py-4 text-sm font-semibold text-[#FFFFE3] shadow-[0_14px_36px_-14px_rgba(109,129,150,0.8)] transition-all duration-300 hover:-translate-y-0.5 hover:bg-[#5b6d80] hover:shadow-[0_20px_46px_-14px_rgba(109,129,150,0.95)] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#6D8196] focus-visible:ring-offset-2 focus-visible:ring-offset-[#FFFFE3] disabled:cursor-not-allowed disabled:opacity-50 disabled:hover:translate-y-0"
              >
                {submitting ? (
                  <>
                    <Loader2 className="h-4 w-4 animate-spin" />
                    Analyzing…
                  </>
                ) : (
                  <>
                    Analyze &amp; Generate Legal Guidance
                    <ArrowRight className="h-4 w-4 transition-transform duration-300 group-hover:translate-x-1" />
                  </>
                )}
              </button>
            </div>
          </form>

          {/* AI Assistant Panel */}
          <aside className="lg:sticky lg:top-28 lg:self-start">
            <div
              className="animate-fade-up space-y-5"
              style={{ animationDelay: "260ms" }}
            >
              {/* Ready card */}
              <div className="rounded-3xl border border-white/60 bg-white/55 p-6 shadow-[0_24px_60px_-30px_rgba(74,74,74,0.3)] backdrop-blur-2xl">
                <div className="flex items-start gap-3">
                  <div className="relative grid h-10 w-10 place-items-center rounded-xl bg-[#6D8196]/12 text-[#6D8196]">
                    <Sparkles className="h-5 w-5" />
                    <span className="absolute -right-0.5 -top-0.5 h-2.5 w-2.5 rounded-full bg-emerald-500 ring-2 ring-white" />
                  </div>
                  <div>
                    <h3 className="text-base font-semibold text-[#4A4A4A]">
                      AI Assistant Ready
                    </h3>
                    <p className="mt-1 text-xs leading-relaxed text-[#4A4A4A]/65">
                      Your complaint will be analyzed using AI and consumer
                      protection laws.
                    </p>
                  </div>
                </div>

                <ul className="mt-5 space-y-2.5">
                  {CHECKLIST.map((item, i) => {
                    const Icon = item.icon;
                    return (
                      <li
                        key={item.label}
                        className="flex items-center gap-3 rounded-xl border border-white/60 bg-white/60 px-3 py-2.5 text-sm text-[#4A4A4A] animate-fade-up"
                        style={{ animationDelay: `${320 + i * 90}ms` }}
                      >
                        <div className="grid h-7 w-7 place-items-center rounded-lg bg-[#6D8196]/10 text-[#6D8196]">
                          <Icon className="h-3.5 w-3.5" />
                        </div>
                        <span className="flex-1 text-[13px] font-medium">
                          {item.label}
                        </span>
                        <CheckCircle2 className="h-4 w-4 text-emerald-500/80" />
                      </li>
                    );
                  })}
                </ul>
              </div>

              {/* Detected context */}
              <div className="rounded-3xl border border-white/60 bg-white/55 p-6 shadow-[0_24px_60px_-30px_rgba(74,74,74,0.3)] backdrop-blur-2xl">
                <div className="flex items-center justify-between">
                  <h3 className="text-sm font-semibold text-[#4A4A4A]">
                    Detected Context
                  </h3>
                  <span className="inline-flex items-center gap-1.5 rounded-full bg-[#6D8196]/12 px-2.5 py-1 text-[10px] font-semibold uppercase tracking-wider text-[#6D8196]">
                    <Lightbulb className="h-3 w-3" />
                    Live
                  </span>
                </div>
                <ul className="mt-4 space-y-2">
                  {DETECTED_CONTEXT.map((c, i) => (
                    <li
                      key={c}
                      className="flex items-center gap-2.5 text-[13px] text-[#4A4A4A]/85 animate-fade-up"
                      style={{ animationDelay: `${500 + i * 110}ms` }}
                    >
                      <CheckCircle2 className="h-4 w-4 text-[#6D8196]" />
                      {c}
                    </li>
                  ))}
                </ul>
              </div>

              {/* Analysis time pill */}
              <div className="flex items-center justify-between rounded-2xl border border-white/60 bg-white/55 px-5 py-4 shadow-[0_18px_44px_-30px_rgba(74,74,74,0.3)] backdrop-blur-2xl">
                <div className="flex items-center gap-2.5">
                  <span className="relative flex h-2.5 w-2.5">
                    <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-emerald-400 opacity-60" />
                    <span className="relative inline-flex h-2.5 w-2.5 rounded-full bg-emerald-500" />
                  </span>
                  <span className="text-xs font-semibold text-[#4A4A4A]">
                    AI Ready
                  </span>
                </div>
                <div className="text-right">
                  <div className="text-[10px] font-medium uppercase tracking-wider text-[#4A4A4A]/55">
                    Avg. Analysis
                  </div>
                  <div className="text-xs font-semibold text-[#4A4A4A]">
                    &lt; 10 seconds
                  </div>
                </div>
              </div>

              {/* Privacy */}
              <div className="flex items-start gap-3 rounded-2xl border border-white/50 bg-white/40 px-5 py-4 backdrop-blur">
                <div className="grid h-8 w-8 shrink-0 place-items-center rounded-lg bg-[#6D8196]/10 text-[#6D8196]">
                  <Lock className="h-4 w-4" />
                </div>
                <p className="text-[12px] leading-relaxed text-[#4A4A4A]/70">
                  Your complaint remains private and is processed only for AI
                  analysis.
                </p>
              </div>
            </div>
          </aside>
        </div>
      </div>
    </section>
  );
}

/* ---------- Sub-components ---------- */

function Stepper({ currentIndex }) {
  return (
    <nav aria-label="Workflow progress" className="animate-fade-up">
      <ol className="flex flex-wrap items-center gap-3 sm:gap-5">
        {STEPS.map((s, i) => {
          const active = i === currentIndex;
          const done = i < currentIndex;
          return (
            <li key={s.key} className="flex items-center gap-3">
              <div
                className={`flex items-center gap-2.5 rounded-full border px-3.5 py-1.5 text-xs font-medium backdrop-blur transition-all duration-300 ${
                  active
                    ? "border-[#6D8196]/40 bg-white/80 text-[#4A4A4A] shadow-[0_8px_22px_-14px_rgba(109,129,150,0.6)]"
                    : done
                      ? "border-[#6D8196]/25 bg-white/55 text-[#4A4A4A]/80"
                      : "border-[#6D8196]/15 bg-white/35 text-[#4A4A4A]/45"
                }`}
              >
                <span
                  className={`grid h-5 w-5 place-items-center rounded-full text-[10px] font-semibold ${
                    active
                      ? "bg-[#6D8196] text-[#FFFFE3]"
                      : done
                        ? "bg-emerald-500 text-white"
                        : "bg-[#6D8196]/15 text-[#6D8196]"
                  }`}
                >
                  {done ? <CheckCircle2 className="h-3 w-3" /> : i + 1}
                </span>
                {s.label}
              </div>
              {i < STEPS.length - 1 && (
                <span
                  aria-hidden
                  className="hidden h-px w-10 bg-gradient-to-r from-[#6D8196]/30 to-transparent sm:block"
                />
              )}
            </li>
          );
        })}
      </ol>
    </nav>
  );
}


function FloatingField({
  id,
  label,
  value,
  onChange,
  placeholder,
  type = "text",
  inputMode,
  icon: Icon,
}) {
  const filled = value && value !== "";

  return (
    <div className="relative">
      <input
        id={id}
        type={type}
        value={value}
        inputMode={inputMode}
        onChange={(e) => onChange(e.target.value)}
        placeholder=" "
        className={`peer w-full rounded-2xl border border-[#6D8196]/20 bg-white/70 px-4 pt-6 pb-2 text-[15px] text-[#4A4A4A] transition-all duration-200 focus:border-[#6D8196]/50 focus:bg-white focus:outline-none focus:ring-4 focus:ring-[#6D8196]/15 ${
          Icon ? "pr-11" : ""
        }`}
      />

      <label
        htmlFor={id}
        className={`absolute left-4 transition-all duration-200 pointer-events-none
          ${
            filled
              ? "top-1 text-[11px] text-[#6D8196] font-medium"
              : "top-1/2 -translate-y-1/2 text-sm text-[#4A4A4A]/55 peer-focus:top-1 peer-focus:translate-y-0 peer-focus:text-[11px] peer-focus:text-[#6D8196]"
          }`}
      >
        {label}
      </label>

      {Icon && (
        <Icon className="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 h-4 w-4 text-[#6D8196]/70" />
      )}
    </div>
  );
}
function DriftingLegalText() {
  const text =
    "Consumer Protection Act, 2019 — Every consumer has the right to be protected against the marketing of goods, products or services which are hazardous to life and property. Right to be informed about the quality, quantity, potency, purity, standard and price of goods. Right to be assured wherever possible, access to a variety of goods, products or services at competitive prices. Right to be heard and to be assured that consumers' interests will receive due consideration at appropriate forums. Right to seek redressal against unfair trade practice or restrictive trade practices or unscrupulous exploitation of consumers. Right to consumer awareness.";
  return (
    <div
      aria-hidden
      className="pointer-events-none absolute inset-x-0 top-24 bottom-0 overflow-hidden select-none"
    >
      <div
        className="absolute inset-0 px-10 py-6 text-[#4A4A4A]"
        style={{
          opacity: 0.1,
          columnCount: 3,
          columnGap: "2.5rem",
          fontFamily:
            'ui-serif, Georgia, Cambria, "Times New Roman", Times, serif',
          fontSize: "9px",
          lineHeight: "1.7",
          textAlign: "justify",
          maskImage:
            "radial-gradient(120% 80% at 50% 40%, rgba(0,0,0,0.9) 30%, rgba(0,0,0,0) 80%)",
          WebkitMaskImage:
            "radial-gradient(120% 80% at 50% 40%, rgba(0,0,0,0.9) 30%, rgba(0,0,0,0) 80%)",
        }}
      >
        {Array.from({ length: 6 }).map((_, i) => (
          <p key={i} className="mb-3 break-inside-avoid-column">
            {text}
          </p>
        ))}
      </div>
    </div>
  );
}
