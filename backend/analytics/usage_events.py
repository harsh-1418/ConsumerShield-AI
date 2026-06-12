# backend/analytics/usage_events.py
# Member 3 - Event logging for tracking user actions

from datetime import datetime


def log_event(db, event_type: str, payload: dict) -> bool:
    """
    Logs a usage event to MongoDB events collection.

    event_type examples:
        "complaint_analyzed"
        "knowledge_graph_viewed"
        "document_generated"
        "rag_searched"
    """
    try:
        db["events"].insert_one({
            "event_type": event_type,
            "payload":    payload,
            "timestamp":  datetime.utcnow(),
            "date":       datetime.utcnow().strftime("%Y-%m-%d"),
        })
        return True
    except Exception as e:
        print(f"[EVENT LOG ERROR] {e}")
        return False


def get_recent_events(db, limit: int = 20) -> list:
    """Fetches recent events for admin/demo purposes."""
    try:
        return list(
            db["events"]
            .find({}, {"_id": 0})
            .sort("timestamp", -1)
            .limit(limit)
        )
    except Exception as e:
        print(f"[FETCH EVENTS ERROR] {e}")
        return []


def get_event_counts(db) -> dict:
    """Returns count of each event type — useful for analytics dashboard."""
    try:
        pipeline = [
            {"$group": {"_id": "$event_type", "count": {"$sum": 1}}},
            {"$sort":  {"count": -1}},
        ]
        result = list(db["events"].aggregate(pipeline))
        return {
            "event_counts": [
                {"event_type": r["_id"], "count": r["count"]}
                for r in result
            ]
        }
    except Exception as e:
        return {"event_counts": [], "error": str(e)}