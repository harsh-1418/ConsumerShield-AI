import {
  BrainCircuit,
  Scale,
  FileText,
  Shield,
  Search,
  Building2,
} from "lucide-react";

const features = [
  {
    icon: BrainCircuit,
    title: "AI Complaint Analysis",
    description:
      "Analyze consumer complaints using AI and relevant legal provisions.",
  },
  {
    icon: Scale,
    title: "Case Strength Score",
    description:
      "Estimate the strength of your case before taking legal action.",
  },
  {
    icon: FileText,
    title: "Complaint Generator",
    description:
      "Generate structured complaint drafts ready for submission.",
  },
  {
    icon: Building2,
    title: "Authority Finder",
    description:
      "Identify the correct consumer forum or authority instantly.",
  },
  {
    icon: Shield,
    title: "Rights Detection",
    description:
      "Discover which consumer rights apply to your situation.",
  },
  {
    icon: Search,
    title: "Legal Knowledge Base",
    description:
      "Explore acts, rules, and regulations relevant to your complaint.",
  },
];

export default function Features() {
  return (
    <section
  className="relative py-28 overflow-hidden"
  style={{
    background: `
      radial-gradient(circle at 20% 20%, rgba(109,129,150,0.06), transparent 35%),
      radial-gradient(circle at 80% 80%, rgba(109,129,150,0.05), transparent 35%),
      linear-gradient(
        180deg,
        #FCFAF2 0%,
        #F8F5E8 50%,
        #F4F0E2 100%
      )
    `,
  }}
>

      <div className="mx-auto max-w-7xl px-6">

        <div className="text-center">

          <p className="text-xs font-semibold uppercase tracking-[0.3em] text-[#6D8196]">
            FEATURES
          </p>

          <h2 className="mt-4 text-5xl font-bold text-[#4A4A4A]">
            Everything You Need to
            <br />
            Protect Your Rights
          </h2>

          <p className="mx-auto mt-6 max-w-2xl text-lg text-[#4A4A4A]/70">
            AI-powered legal assistance designed to help consumers
            understand their rights and resolve disputes confidently.
          </p>

        </div>

        <div className="mt-20 grid gap-8 md:grid-cols-2 xl:grid-cols-3">

          {features.map((feature, index) => {
            const Icon = feature.icon;

            return (
              <div
                key={index}
                className="group rounded-3xl border border-[#6D8196]/10 bg-white/70 p-8 backdrop-blur-xl transition-all duration-500 hover:-translate-y-2 hover:shadow-[0_30px_70px_-20px_rgba(74,74,74,0.15)]"
              >
                <Icon className="h-8 w-8 text-[#6D8196] transition-transform duration-500 group-hover:scale-110" />

                <h3 className="mt-6 text-xl font-semibold text-[#4A4A4A]">
                  {feature.title}
                </h3>

                <p className="mt-3 leading-relaxed text-[#4A4A4A]/70">
                  {feature.description}
                </p>
              </div>
            );
          })}

        </div>

      </div>

    </section>
  );
}