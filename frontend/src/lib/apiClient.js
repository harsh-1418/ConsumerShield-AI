const BASE_URL = "http://127.0.0.1:8000/api/v1";

export async function analyzeComplaint(text) {
  const res = await fetch(`${BASE_URL}/complaints/analyze`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ text }),
  });

  if (!res.ok) {
  const text = await res.text();
  throw new Error(text);
}

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

  if (!res.ok) {
    const text = await res.text();
    throw new Error(text);
  }

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

  if (!res.ok) {
    const text = await res.text();
    throw new Error(text);
  }

  return res.json();
}