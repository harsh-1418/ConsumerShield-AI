# backend/tests/test_member2_integration.py
# Member 3 - Integration tests: MongoDB + Qdrant + RAG + Gemini
# All fixes applied — certifi for MongoDB, Python 3.14 compatible
# Run from backend/ folder: python tests/test_member2_integration.py

import sys
import os

_THIS_FILE   = os.path.abspath(__file__)
_BACKEND_DIR = os.path.abspath(os.path.join(os.path.dirname(_THIS_FILE), ".."))

if _BACKEND_DIR not in sys.path:
    sys.path.insert(0, _BACKEND_DIR)

from dotenv import load_dotenv
load_dotenv(os.path.join(_BACKEND_DIR, ".env"))


def test_mongo_connection():
    print("\n=== TEST 1: MongoDB Connection ===")
    from app.db.mongo import db, complaints_col, authorities_col
    result = db.client.admin.command("ping")
    assert result.get("ok") == 1.0, "MongoDB ping failed"
    print("ping:", result)
    print("authorities :", authorities_col.count_documents({}), "docs")
    print("complaints  :", complaints_col.count_documents({}), "docs")
    print("PASSED")


def test_authorities_seed_data():
    print("\n=== TEST 2: Authorities Seed Data ===")
    from app.db.mongo import authorities_col
    names = [a["name"] for a in authorities_col.find({}, {"_id": 0, "name": 1})]
    print("Found:", names)
    expected = [
        "National Consumer Helpline",
        "District Consumer Commission",
        "RBI Banking Ombudsman",
        "ASCI",
        "TRAI",
    ]
    for e in expected:
        assert e in names, "Missing authority: " + e
    print("PASSED")


def test_qdrant_connection():
    print("\n=== TEST 3: Qdrant Connection ===")
    from qdrant_client import QdrantClient
    client = QdrantClient(
        url=os.getenv("QDRANT_URL"),
        api_key=os.getenv("QDRANT_API_KEY"),
    )
    info = client.get_collection("consumer_laws")
    print("consumer_laws points:", info.points_count)
    assert info.points_count >= 200
    print("PASSED")


def test_rag_retrieve():
    print("\n=== TEST 4: RAG Retrieve (live Qdrant) ===")
    rag_dir = os.path.join(_BACKEND_DIR, "rag")
    if rag_dir not in sys.path:
        sys.path.insert(0, rag_dir)
    from retrieve import retrieve
    results = retrieve("insurance claim rejected", top_k=3)
    print("Got", len(results), "results")
    for r in results:
        print("  -", r["source"], "score:", round(r["score"], 3))
    assert len(results) > 0
    print("PASSED")


def test_platform_metrics_live():
    print("\n=== TEST 5: Platform Metrics (live MongoDB) ===")
    from app.db.mongo import db
    from analytics.metrics import get_platform_metrics
    result = get_platform_metrics(db)
    print(result)
    assert "total_complaints" in result
    assert "error" not in result, "Error: " + str(result.get("error", ""))
    print("PASSED")


def test_case_strength_with_live_rag():
    print("\n=== TEST 6: Case Strength with Live RAG ===")
    from prediction.case_strength import score_case_strength, _fetch_laws_via_rag
    laws = _fetch_laws_via_rag("insurance claim rejected without reason")
    print("Fetched", len(laws), "laws from RAG")
    result = score_case_strength(
        "My insurance claim was rejected without any valid reason "
        "after paying premiums for 3 years.",
        relevant_laws=laws,
    )
    print("score:", result["score"], " label:", result["label"])
    print("forum:", result.get("recommended_forum", "N/A"))
    assert result["score"] >= 0
    assert result["label"] in ("Weak", "Moderate", "Strong")
    print("PASSED")


def run_all():
    print("=" * 60)
    print("MEMBER 2 INTEGRATION TEST SUITE")
    print("MongoDB(certifi) + Qdrant + RAG + Gemini")
    print("=" * 60)

    tests = [
        test_mongo_connection,
        test_authorities_seed_data,
        test_qdrant_connection,
        test_rag_retrieve,
        test_platform_metrics_live,
        test_case_strength_with_live_rag,
    ]

    passed = 0
    failed = 0
    for t in tests:
        try:
            t()
            passed += 1
        except Exception as e:
            print("FAILED:", e)
            failed += 1

    print("\n" + "=" * 60)
    print(str(passed) + " passed | " + str(failed) + " failed | " + str(passed + failed) + " total")
    print("=" * 60)


run_all()