import { useLocation, Navigate } from "react-router-dom";

export default function CaseInsights() {
  const { state } = useLocation();

  if (!state) {
  return (
    <div className="min-h-screen flex items-center justify-center">
      <h2>No case analysis available. Please analyze a complaint first.</h2>
    </div>
  );
}

  const { analysis, strength, authorities } = state;

  const score =
    strength?.score ||
    strength?.case_strength_score ||
    strength?.strength_score ||
    0;

  const label =
    strength?.label ||
    strength?.case_strength ||
    strength?.verdict ||
    "Pending";

  const authorityList =
    authorities?.recommended_authorities ||
    authorities?.authorities ||
    authorities?.results ||
    [];

  return (
    <div className="min-h-screen bg-[#FFFFE3] py-24 px-6">
      <div className="mx-auto max-w-6xl space-y-8">

        <div>
  <h1 className="text-4xl font-bold text-[#4A4A4A]">
    Case Insights
  </h1>
  <button
  onClick={() => window.history.back()}
  className="rounded-xl bg-[#6D8196] px-5 py-2 text-white transition hover:bg-[#5b6d80]"
>
  ← Back to Complaint
</button>

  <p className="mt-2 text-gray-600">
    AI-powered legal analysis, case strength prediction and authority recommendations.
  </p>
</div>
        {/* AI Analysis */}

        <div className="rounded-3xl bg-white p-8 shadow-lg border border-[#6D8196]/10">
          <h2 className="mb-6 text-2xl font-bold text-[#4A4A4A]">
            AI Legal Analysis
          </h2>

          <div className="whitespace-pre-wrap leading-8 text-[#4A4A4A]/90">
            {analysis?.ai_analysis || "No analysis available."}
          </div>
        </div>

        {/* Case Strength */}

        <div className="rounded-3xl bg-white p-8 shadow-lg border border-[#6D8196]/10">

          <h2 className="text-2xl font-bold text-[#4A4A4A] mb-6">
            Case Strength
          </h2>

          <div className="flex items-center justify-between">

            <div>

              <div className="text-6xl font-bold text-[#6D8196]">
                {score}
              </div>

              <div className="text-lg text-gray-600">
                out of 100
              </div>

            </div>

            <div
  className={`rounded-full px-6 py-3 text-xl font-semibold
    ${
      score >= 75
        ? "bg-green-100 text-green-700"
        : score >= 50
        ? "bg-yellow-100 text-yellow-700"
        : "bg-red-100 text-red-700"
    }`}
>
  {label}
</div>

          </div>

          <div className="mt-6 h-4 w-full overflow-hidden rounded-full bg-gray-200">

            <div
              className="h-full rounded-full bg-[#6D8196]"
              style={{
                width: `${Math.min(score,100)}%`
              }}
            />

          </div>

        </div>

        {/* Authorities */}

        <div className="rounded-3xl bg-white p-8 shadow-lg border border-[#6D8196]/10">

          <h2 className="mb-6 text-2xl font-bold text-[#4A4A4A]">
            Recommended Authorities
          </h2>

          <div className="grid gap-4">

            {authorityList.length > 0 ? (

              authorityList.map((item, index) => (

                <div
                  key={index}
                  className="rounded-2xl border border-[#6D8196]/20 bg-[#FFFFE3] p-5"
                >

                  <div className="text-lg font-semibold text-[#4A4A4A]">
                    {item.name || item.authority || `Authority ${index + 1}`}
                  </div>

                  <div className="mt-2 text-sm text-gray-600">
                    {item.reason || item.description || ""}
                  </div>

                </div>

              ))

            ) : (

              <div className="text-gray-500">
                No authority recommendations available.
              </div>

            )}

          </div>

        </div>

        {/* Raw Data */}

        <div className="rounded-3xl bg-white p-8 shadow-lg border border-[#6D8196]/10">

          <h2 className="mb-6 text-2xl font-bold text-[#4A4A4A]">
            Technical Details
          </h2>

          <pre className="overflow-auto rounded-xl bg-gray-100 p-4 text-sm">
            {JSON.stringify(
              {
                analysis,
                strength,
                authorities,
              },
              null,
              2
            )}
          </pre>

        </div>

      </div>
    </div>
  );
}