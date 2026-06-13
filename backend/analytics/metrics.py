# backend/analytics/metrics.py
# Member 3 - Platform statistics from MongoDB
# Updated: uses complaints_col from Member 2's db.mongo

from datetime import datetime


def get_platform_metrics(db) -> dict:
    """
    Returns complaint statistics for the dashboard.
    db = MongoDB database object (from motor or pymongo).
    """
    try:
        complaints = db["complaints"]

        total    = complaints.count_documents({})
        strong   = complaints.count_documents({"strength_label": "Strong"})
        moderate = complaints.count_documents({"strength_label": "Moderate"})
        weak     = complaints.count_documents({"strength_label": "Weak"})

        avg_pipeline = [
            {"$group": {"_id": None, "avg": {"$avg": "$strength_score"}}}
        ]
        avg_result  = list(complaints.aggregate(avg_pipeline))
        _raw_avg    = avg_result[0]["avg"] if avg_result else None
        avg_score   = round(_raw_avg, 1) if _raw_avg is not None else 0.0

        return {
            "total_complaints":       total,
            "strong_cases":           strong,
            "moderate_cases":         moderate,
            "weak_cases":             weak,
            "strong_cases_pct":       round((strong   / total) * 100, 1) if total else 0,
            "moderate_cases_pct":     round((moderate / total) * 100, 1) if total else 0,
            "weak_cases_pct":         round((weak     / total) * 100, 1) if total else 0,
            "average_strength_score": avg_score,
            "last_updated":           datetime.utcnow().isoformat(),
        }

    except Exception as e:
        return {
            "error":                  str(e),
            "total_complaints":       0,
            "strong_cases":           0,
            "moderate_cases":         0,
            "weak_cases":             0,
            "strong_cases_pct":       0,
            "moderate_cases_pct":     0,
            "weak_cases_pct":         0,
            "average_strength_score": 0,
            "last_updated":           datetime.utcnow().isoformat(),
        }


def get_category_breakdown(db) -> dict:
    """Complaints grouped by category (e-commerce, banking, etc.)"""
    try:
        pipeline = [
            {"$group": {"_id": "$category", "count": {"$sum": 1}}},
            {"$sort":  {"count": -1}},
        ]
        result = list(db["complaints"].aggregate(pipeline))
        return {
            "categories": [
                {"name": r["_id"] or "Uncategorized", "count": r["count"]}
                for r in result
            ]
        }
    except Exception as e:
        return {"categories": [], "error": str(e)}