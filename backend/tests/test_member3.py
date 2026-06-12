# backend/tests/test_member3.py
# Member 3 - Complete test suite
#
# Run from backend/ folder:
#   python tests/test_member3.py          ← no dependencies needed
#   python -m pytest tests/test_member3.py -v
#
# Tests are grouped:
#   1. Risk scoring        (no API key needed)
#   2. Knowledge graph     (no API key needed)

#   3. Analytics mock DB   (no MongoDB needed)
#   4. Case strength       (Gemini live test — skipped if no API key)

import sys
import os

# ── Add backend/ to path ──────────────────────────────────────────────
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


# ══════════════════════════════════════════════════════════════════════
# 1. RISK SCORING  (no API key needed)
# ══════════════════════════════════════════════════════════════════════

from prediction.risk_scoring import get_risk_profile, get_resolution_roadmap


def test_risk_high_score():
    r = get_risk_profile(85)
    assert r["risk_level"] == "Low Risk" and r["color"] == "green"
    print("✅  test_risk_high_score")


def test_risk_medium_score():
    r = get_risk_profile(55)
    assert r["risk_level"] == "Medium Risk" and r["color"] == "yellow"
    print("✅  test_risk_medium_score")


def test_risk_low_score():
    r = get_risk_profile(20)
    assert r["risk_level"] == "High Risk" and r["color"] == "red"
    print("✅  test_risk_low_score")


def test_risk_boundary_70():
    assert get_risk_profile(70)["risk_level"] == "Low Risk"
    print("✅  test_risk_boundary_70")


def test_risk_boundary_40():
    assert get_risk_profile(40)["risk_level"] == "Medium Risk"
    print("✅  test_risk_boundary_40")


def test_roadmap_strong_has_5_steps():
    steps = get_resolution_roadmap(80, "District Forum")
    assert len(steps) == 5
    assert "District Forum" in steps[3]["title"]
    print("✅  test_roadmap_strong_has_5_steps")


def test_roadmap_weak_has_5_steps():
    steps = get_resolution_roadmap(30, "NCH Helpline")
    assert len(steps) == 5
    assert steps[3]["title"] == "Consult Legal Aid"
    print("✅  test_roadmap_weak_has_5_steps")


# ══════════════════════════════════════════════════════════════════════
# 2. KNOWLEDGE GRAPH  (no API key needed)
# ══════════════════════════════════════════════════════════════════════

from knowledge_graph.graph_builder import build_consumer_graph
from knowledge_graph.graph_queries import (
    get_rights_of_consumer,
    get_authorities_for_complaint,
    get_laws_protecting_right,
    get_node_by_id,
    get_connections_of_node,
)


def test_graph_structure():
    g = build_consumer_graph()
    assert "nodes" in g and "edges" in g
    assert g["meta"]["total_nodes"] == len(g["nodes"])
    assert g["meta"]["total_edges"] == len(g["edges"])
    print(f"✅  test_graph_structure  ({g['meta']['total_nodes']} nodes, {g['meta']['total_edges']} edges)")


def test_consumer_has_6_rights():
    rights = get_rights_of_consumer()
    labels = [r["label"] for r in rights]
    assert len(rights) == 6
    assert "Right to Safety"  in labels
    assert "Right to Redress" in labels
    print("✅  test_consumer_has_6_rights")


def test_authority_district():
    r = get_authorities_for_complaint(5.0)
    assert r["primary"] == "District Forum"
    print("✅  test_authority_district  (Rs 5 lakh)")


def test_authority_state():
    r = get_authorities_for_complaint(150.0)
    assert r["primary"] == "State Commission"
    print("✅  test_authority_state  (Rs 1.5 cr)")


def test_authority_ncdrc():
    r = get_authorities_for_complaint(250.0)
    assert r["primary"] == "NCDRC"
    print("✅  test_authority_ncdrc  (Rs 2.5 cr)")


def test_laws_protect_right_redress():
    laws = get_laws_protecting_right("right_redress")
    ids  = [l["id"] for l in laws]
    assert "cpa2019" in ids
    print("✅  test_laws_protect_right_redress")


def test_node_by_id_found():
    n = get_node_by_id("consumer")
    assert n["label"] == "Consumer" and n["type"] == "person"
    print("✅  test_node_by_id_found")


def test_node_by_id_missing():
    assert get_node_by_id("does_not_exist") == {}
    print("✅  test_node_by_id_missing")


def test_connections_of_consumer():
    c = get_connections_of_node("consumer")
    assert c["node_id"] == "consumer"
    assert c["total_connections"] > 0
    print(f"✅  test_connections_of_consumer  ({c['total_connections']} connections)")


# ══════════════════════════════════════════════════════════════════════
# 3. ANALYTICS — mock MongoDB  (no real DB needed)
# ══════════════════════════════════════════════════════════════════════

from analytics.metrics      import get_platform_metrics, get_category_breakdown
from analytics.usage_events import log_event, get_recent_events, get_event_counts


class _MockCol:
    """Lightweight in-memory MongoDB collection mock."""
    def __init__(self, docs=None):
        self._docs = docs or []

    def count_documents(self, q):
        if not q:
            return len(self._docs)
        for k, v in q.items():
            return sum(1 for d in self._docs if d.get(k) == v)
        return 0

    def aggregate(self, pipeline):
        nums = [d["strength_score"] for d in self._docs if "strength_score" in d]
        return [{"_id": None, "avg": sum(nums) / len(nums)}] if nums else []

    def insert_one(self, doc):
        self._docs.append(doc)

    def find(self, q=None, proj=None):
        return iter(self._docs)

    def sort(self, *a): return self
    def limit(self, n): return self


class _MockDB:
    def __init__(self):
        self._cols = {}
    def __getitem__(self, name):
        if name not in self._cols:
            self._cols[name] = _MockCol()
        return self._cols[name]


def test_metrics_empty_db():
    r = get_platform_metrics(_MockDB())
    assert r["total_complaints"] == 0
    print("✅  test_metrics_empty_db")


def test_metrics_with_data():
    db = _MockDB()
    db["complaints"]._docs = [
        {"strength_label": "Strong",   "strength_score": 80},
        {"strength_label": "Strong",   "strength_score": 75},
        {"strength_label": "Moderate", "strength_score": 55},
        {"strength_label": "Weak",     "strength_score": 25},
    ]
    r = get_platform_metrics(db)
    assert r["total_complaints"] == 4
    assert r["strong_cases"]     == 2
    assert r["strong_cases_pct"] == 50.0
    print("✅  test_metrics_with_data")


def test_log_event():
    db = _MockDB()
    ok = log_event(db, "complaint_analyzed", {"id": "test123"})
    assert ok is True
    assert db["events"]._docs[0]["event_type"] == "complaint_analyzed"
    print("✅  test_log_event")


def test_get_recent_events_empty():
    assert get_recent_events(_MockDB()) == []
    print("✅  test_get_recent_events_empty")


# ══════════════════════════════════════════════════════════════════════
# 4. CASE STRENGTH  (Gemini — skipped if no API key)
# ══════════════════════════════════════════════════════════════════════

from prediction.case_strength import score_case_strength, batch_score


def test_case_strength_always_returns_valid_dict():
    """
    score_case_strength must NEVER crash — always returns a valid dict
    even when Gemini key is missing.
    Updated: uses "complaint" field (matches Member 2's request model).
    """
    r = score_case_strength(
        complaint="Test complaint",
        relevant_laws=["Section 2(34) CPA 2019: Product liability for defective goods"],
    )
    assert "score"             in r
    assert "label"             in r
    assert "reason"            in r
    assert "winning_chances"   in r
    assert "recommended_forum" in r
    assert r["label"] in ("Weak", "Moderate", "Strong")
    print(f"✅  test_case_strength_always_returns_valid_dict  (score={r['score']}, label={r['label']})")


def test_case_strength_no_laws_uses_fallback():
    """When relevant_laws is empty, fallback laws should be used."""
    r = score_case_strength(complaint="Flipkart refused refund on broken phone", relevant_laws=[])
    assert "score" in r
    print(f"✅  test_case_strength_no_laws_uses_fallback  (score={r['score']})")


def test_batch_score():
    complaints = [
        {"id": "c1", "text": "Flipkart delivered broken phone, refuses replacement", "laws": []},
        {"id": "c2", "text": "Bank charged hidden fees on my account",               "laws": []},
    ]
    results = batch_score(complaints)
    assert len(results) == 2
    assert results[0]["complaint_id"] == "c1"
    assert results[1]["complaint_id"] == "c2"
    print("✅  test_batch_score")


def test_case_strength_live_gemini():
    """
    Live Gemini test — only runs when GEMINI_API_KEY is in .env.
    Also tests Member 2 RAG integration (graceful if RAG not available).
    """
    from dotenv import load_dotenv
    load_dotenv()
    if not os.getenv("GEMINI_API_KEY"):
        print("⏭️   test_case_strength_live_gemini SKIPPED (no GEMINI_API_KEY in .env)")
        return

    r = score_case_strength(
        complaint=(
            "I ordered a phone from Flipkart. It arrived with a cracked screen. "
            "They refused to replace it saying the damage is customer-caused."
        ),
        relevant_laws=[
            "Section 2(34) CPA 2019: Product liability — responsibility of "
            "manufacturer for defective product",
            "Rule 7 E-Commerce Rules 2020: E-commerce entity must not deny "
            "return/refund for defective goods",
        ],
    )
    assert isinstance(r["score"], int)
    assert 0 <= r["score"] <= 100
    assert r["label"] in ("Weak", "Moderate", "Strong")
    print(
        f"✅  test_case_strength_live_gemini  "
        f"(score={r['score']}, label={r['label']}, chances={r['winning_chances']})"
    )


# ══════════════════════════════════════════════════════════════════════
# RUNNER
# ══════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("\n" + "═" * 62)
    print("  ConsumerShield AI — Member 3 Test Suite")
    print("  (Updated to match Member 2 handoff)")
    print("═" * 62)

    tests = [
        test_risk_high_score, test_risk_medium_score, test_risk_low_score,
        test_risk_boundary_70, test_risk_boundary_40,
        test_roadmap_strong_has_5_steps, test_roadmap_weak_has_5_steps,
        test_graph_structure, test_consumer_has_6_rights,
        test_authority_district, test_authority_state, test_authority_ncdrc,
        test_laws_protect_right_redress,
        test_node_by_id_found, test_node_by_id_missing,
        test_connections_of_consumer,
        test_metrics_empty_db, test_metrics_with_data,
        test_log_event, test_get_recent_events_empty,
        test_case_strength_always_returns_valid_dict,
        test_case_strength_no_laws_uses_fallback,
        test_batch_score,
        test_case_strength_live_gemini,
    ]

    passed = failed = 0
    for fn in tests:
        try:
            fn()
            passed += 1
        except Exception as e:
            print(f"❌  {fn.__name__}  FAILED: {e}")
            failed += 1

    print("\n" + "─" * 62)
    print(f"  {passed} passed  |  {failed} failed  |  {len(tests)} total")
    print("─" * 62 + "\n")