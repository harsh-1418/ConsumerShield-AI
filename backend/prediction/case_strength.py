# backend/prediction/case_strength.py
# Member 3 - AI-powered case strength scoring using Gemini
# Updated to match Member 2's handoff:
#   - uses retrieve() from rag/retrieve.py for live law fetching
#   - request field is "complaint" (not complaint_text)
#   - Gemini client uses google.genai (new SDK style Member 2 uses)

import os
import json
import re
import sys

from dotenv import load_dotenv

# ── Load .env before anything else ────────────────────────────────────
load_dotenv()

# ── Add rag/ to path so retrieve.py is importable (Member 2's file) ──
_backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
_rag_dir     = os.path.join(_backend_dir, "rag")
for _p in [_backend_dir, _rag_dir]:
    if _p not in sys.path:
        sys.path.insert(0, _p)

# ── Gemini setup (matches Member 2's usage style) ─────────────────────
try:
    from google import genai as _genai_new
    _USE_NEW_SDK = True
except ImportError:
    _USE_NEW_SDK = False

import google.generativeai as genai

_api_key = os.getenv("GEMINI_API_KEY", "")
if not _api_key:
    print("⚠️  WARNING: GEMINI_API_KEY not found in .env — Gemini calls will fall back.")
else:
    genai.configure(api_key=_api_key)

# ── Try to import Member 2's retriever (graceful fallback if not ready) ─
try:
    from retrieve import retrieve as _rag_retrieve
    _RAG_AVAILABLE = True
except ImportError:
    _RAG_AVAILABLE = False


def _fetch_laws_via_rag(complaint_text: str, top_k: int = 5) -> list:
    """
    Calls Member 2's retrieve() to get relevant law chunks.
    Returns list of law strings ready for the prompt.
    Falls back silently if RAG isn't available yet.
    """
    if not _RAG_AVAILABLE:
        return []
    try:
        results = _rag_retrieve(complaint_text, top_k=top_k)
        # results shape: [{"source": "...", "text": "...", "score": 0.65}, ...]
        return [f"[{r['source']}] {r['text']}" for r in results]
    except Exception as e:
        print(f"⚠️  RAG retrieve failed: {e}")
        return []


def _call_gemini(prompt: str) -> str:
    """
    Calls Gemini using whichever SDK version is available.
    Member 2 uses: client.models.generate_content(model=..., contents=...)
    We support both styles.
    """
    if _USE_NEW_SDK and _api_key:
        client = _genai_new.Client(api_key=_api_key)
        response = client.models.generate_content(
            model="models/gemini-2.0-flash",
            contents=prompt,
        )
        return response.text.strip()
    else:
        model    = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(prompt)
        return response.text.strip()


def score_case_strength(complaint: str, relevant_laws: list = None) -> dict:
    """
    Analyzes a consumer complaint and scores its legal strength.

    Args:
        complaint      : The user's complaint text
                         (field name matches Member 2's InsightRequest)
        relevant_laws  : Law snippets from RAG — if empty, fetches live via
                         Member 2's retrieve() or uses built-in fallback

    Returns:
        dict with score, label, reason, winning_chances,
             key_rights_violated, applicable_sections, recommended_forum
    """
    if relevant_laws is None:
        relevant_laws = []

    # 1. Try live RAG fetch if no laws passed in
    if not relevant_laws:
        relevant_laws = _fetch_laws_via_rag(complaint)

    # 2. Static fallback if RAG also returns nothing
    if not relevant_laws:
        relevant_laws = [
            "Section 2(34) CPA 2019: Product liability means responsibility "
            "of manufacturer for defective product",
            "Section 47 CPA 2019: District Commission handles complaints up to Rs 1 crore",
            "Rule 7 E-Commerce Rules 2020: E-commerce entity must not deny "
            "return/refund for defective goods",
        ]

    law_context = "\n".join([f"- {law}" for law in relevant_laws])

    prompt = f"""You are an expert Indian consumer rights legal analyst.

A consumer has filed the following complaint:
\"\"\"{complaint}\"\"\"

Relevant Indian Consumer Laws:
{law_context}

Analyze this complaint and rate its legal strength from 0 to 100.

Respond ONLY with valid JSON, no extra text, no markdown backticks:
{{
  "score": <integer between 0 and 100>,
  "label": "<exactly one of: Weak, Moderate, Strong>",
  "reason": "<2-3 sentences explaining the score based on the laws>",
  "winning_chances": "<percentage range like 60-70%>",
  "key_rights_violated": ["<right1>", "<right2>"],
  "applicable_sections": ["<section1>", "<section2>"],
  "recommended_forum": "<District Forum / State Commission / NCDRC / RBI Ombudsman / NCH Helpline>"
}}"""

    try:
        raw = _call_gemini(prompt)

        # Strip markdown fences if Gemini wraps in ```json ... ```
        raw = re.sub(r"```json|```", "", raw).strip()

        json_match = re.search(r"\{.*\}", raw, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
        raise ValueError("No JSON object found in Gemini response")

    except Exception as e:
        # Safe fallback — never crashes Member 1's pipeline
        return {
            "score":               50,
            "label":               "Moderate",
            "reason":              f"Automated analysis unavailable. Error: {str(e)}",
            "winning_chances":     "50%",
            "key_rights_violated": ["Right to Redress"],
            "applicable_sections": ["Section 2(34) CPA 2019"],
            "recommended_forum":   "NCH Helpline",
        }


def batch_score(complaints: list) -> list:
    """
    Score multiple complaints at once.
    Each item: {"id": "...", "text": "...", "laws": [...]}
    """
    results = []
    for c in complaints:
        result = score_case_strength(
            complaint=c.get("text", ""),
            relevant_laws=c.get("laws", []),
        )
        result["complaint_id"] = c.get("id", "unknown")
        results.append(result)
    return results