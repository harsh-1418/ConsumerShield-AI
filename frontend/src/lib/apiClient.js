const BASE_URL = "http://localhost:8000/api/v1";

export async function analyzeComplaint(text) {
  const res = await fetch(`${BASE_URL}/complaints/analyze`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ text }),
  });

  if (!res.ok) throw new Error("Analysis failed");

  return res.json();
}

export async function getCaseStrength(complaint) {
  const res = await fetch(`${BASE_URL}/insights/case-strength`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      complaint,
      relevant_laws: [],
      complaint_value_lakh: 5.0,
    }),
  });

  return res.json();
}

export async function getAuthorities(complaint) {
  const res = await fetch(`${BASE_URL}/insights/authorities`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      complaint,
    }),
  });

  return res.json();
}