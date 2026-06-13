import {
  Scale,
  ArrowUpRight,
  Globe,
  Mail,
  Link,
} from "lucide-react";

export default function Footer() {
  return (
    <footer className="relative overflow-hidden bg-[#F4F0E2] border-t border-[#6D8196]/10">

      {/* Background Glow */}
      <div
        className="absolute inset-0 pointer-events-none"
        style={{
          background:
            "radial-gradient(circle at center, rgba(255,255,227,0.5) 0%, transparent 70%)",
        }}
      />

      <div className="relative mx-auto max-w-7xl px-6 py-20">

        {/* Top Section */}
        <div className="grid gap-14 md:grid-cols-2 lg:grid-cols-4">

          {/* Brand */}
          <div>

            <div className="flex items-center gap-3">

              <div className="grid h-12 w-12 place-items-center rounded-2xl bg-[#6D8196] text-[#FFFFE3] shadow-lg transition hover:scale-105">
                <Scale className="h-6 w-6" />
              </div>

              <div>
                <h3 className="text-2xl font-bold text-[#4A4A4A]">
                  ConsumerShield AI
                </h3>

                <p className="text-sm text-[#6D8196]">
                  AI Legal Assistant
                </p>
              </div>

            </div>

            <p className="mt-6 max-w-sm leading-8 text-[#4A4A4A]/70">
              Empowering consumers through AI-powered legal guidance,
              intelligent complaint analysis, and consumer rights awareness.
            </p>

          </div>

          {/* Navigation */}
          <div>

            <h4 className="mb-6 text-lg font-semibold text-[#4A4A4A]">
              Navigation
            </h4>

            <div className="space-y-4">

              {[
                "Home",
                "New Complaint",
                "Case Insights",
                "How It Works",
                "About",
              ].map((item) => (
                <a
                  key={item}
                  href="#"
                  className="group flex items-center gap-2 text-[#4A4A4A]/70 transition hover:text-[#6D8196]"
                >
                  <span className="transition group-hover:translate-x-1">
                    {item}
                  </span>

                  <ArrowUpRight className="h-4 w-4 opacity-0 transition group-hover:opacity-100" />
                </a>
              ))}

            </div>

          </div>

          {/* Connect */}

<div>

  <h4 className="mb-6 text-lg font-semibold text-[#4A4A4A]">
    Connect
  </h4>

  <div className="space-y-4">

    <a
      href="#"
      className="group flex items-center gap-3 text-[#4A4A4A]/70 transition hover:text-[#6D8196]"
    >
      <Mail className="h-4 w-4" />
      Email
    </a>

    <a
      href="#"
      target="_blank"
      rel="noreferrer"
      className="group flex items-center gap-3 text-[#4A4A4A]/70 transition hover:text-[#6D8196]"
    >
      <Link className="h-4 w-4" />
      GitHub
    </a>

    <a
      href="#"
      target="_blank"
      rel="noreferrer"
      className="group flex items-center gap-3 text-[#4A4A4A]/70 transition hover:text-[#6D8196]"
    >
      <Globe className="h-4 w-4" />
      LinkedIn
    </a>

  </div>

</div>

          {/* Tech Stack */}
          <div>

            <h4 className="mb-6 text-lg font-semibold text-[#4A4A4A]">
              Built With
            </h4>

            <div className="flex flex-wrap gap-3">

              {[
                "React",
                "Tailwind",
                "Python",
                "Flask",
                "AI",
              ].map((tech) => (
                <span
                  key={tech}
                  className="rounded-full border border-[#6D8196]/10 bg-white/40 px-5 py-2 text-sm text-[#4A4A4A]/80 backdrop-blur-md transition hover:-translate-y-1 hover:bg-white/70"
                >
                  {tech}
                </span>
              ))}

            </div>

          </div>

        </div>

        {/* Quote */}

        <div className="my-16 text-center">

          <p className="italic tracking-wide text-[#6D8196]/70">
            “Justice begins with awareness.”
          </p>

        </div>

        {/* Bottom */}

        <div className="flex flex-col items-center justify-between gap-4 border-t border-[#6D8196]/10 pt-8 text-sm text-[#4A4A4A]/60 md:flex-row">

          <p>
            © 2026 ConsumerShield AI. All rights reserved.
          </p>

          <p>
            Built for HackBharat 🚀
          </p>

        </div>

      </div>

    </footer>
  );
}