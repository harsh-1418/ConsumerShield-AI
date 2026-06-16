const BASE_URL = import.meta.env.VITE_API_URL
  ? `${import.meta.env.VITE_API_URL}/api/v1`
  : "http://127.0.0.1:8000/api/v1";

export async function analyzeComplaint(text, category = "others", amount_involved = 0) {
  const res = await fetch(`${BASE_URL}/complaints/analyze`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ text, category, amount_involved }),
  });

  if (!res.ok) {
    const errorText = await res.text();
    throw new Error(errorText);
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
    const errorText = await res.text();
    throw new Error(errorText);
  }

  return res.json();
}

export async function getAuthorities(complaint) {
  const res = await fetch(`${BASE_URL}/insights/authorities`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ complaint }),
  });

  if (!res.ok) {
    const errorText = await res.text();
    throw new Error(errorText);
  }

  return res.json();
}

export async function getRoadmap(complaint) {
  const res = await fetch(`${BASE_URL}/insights/roadmap`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      complaint,
      relevant_laws: [],
    }),
  });

  if (!res.ok) {
    const errorText = await res.text();
    throw new Error(errorText);
  }

  return res.json();
}

export async function getKnowledgeGraph() {
  const res = await fetch(`${BASE_URL}/knowledge-graph`);

  if (!res.ok) {
    const errorText = await res.text();
    throw new Error(errorText);
  }

  return res.json();
}

export async function getAnalytics() {
  const res = await fetch(`${BASE_URL}/analytics/metrics`);

  if (!res.ok) {
    const errorText = await res.text();
    throw new Error(errorText);
  }

  return res.json();
}

export async function ragSearch(query, top_k = 5) {
  const res = await fetch(`${BASE_URL}/rag/search`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ query, top_k }),
  });

  if (!res.ok) {
    const errorText = await res.text();
    throw new Error(errorText);
  }

  return res.json();
}