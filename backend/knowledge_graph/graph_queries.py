# backend/knowledge_graph/graph_queries.py
# Member 3 - Query helpers for the knowledge graph

from .graph_builder import build_consumer_graph


def get_full_graph() -> dict:
    """Returns the complete graph."""
    return build_consumer_graph()


def get_rights_of_consumer() -> list:
    """Returns all 6 rights a consumer has."""
    graph = build_consumer_graph()
    right_ids = [
        e["to"] for e in graph["edges"]
        if e["from"] == "consumer" and e["label"] == "has"
    ]
    return [n for n in graph["nodes"] if n["id"] in right_ids]


def get_authorities_for_complaint(complaint_value_lakh: float) -> dict:
    """
    Returns the correct authority based on complaint value (in lakhs).
    e.g. 5.0  → Rs 5 lakh  → District Forum
         150.0 → Rs 1.5 cr  → State Commission
         250.0 → Rs 2.5 cr  → NCDRC
    """
    if complaint_value_lakh <= 100:
        return {
            "primary":       "District Forum",
            "authority_id":  "district_forum",
            "limit":         "Up to Rs 1 Crore",
            "appeal_to":     "State Commission",
        }
    elif complaint_value_lakh <= 200:
        return {
            "primary":       "State Commission",
            "authority_id":  "state_commission",
            "limit":         "Rs 1 Crore to Rs 2 Crore",
            "appeal_to":     "NCDRC",
        }
    else:
        return {
            "primary":       "NCDRC",
            "authority_id":  "ncdrc",
            "limit":         "Above Rs 2 Crore",
            "appeal_to":     "Supreme Court",
        }


def get_laws_protecting_right(right_id: str) -> list:
    """Returns all laws that protect a specific right."""
    graph    = build_consumer_graph()
    law_ids  = [
        e["from"] for e in graph["edges"]
        if e["to"] == right_id and e["label"] == "protects"
    ]
    return [n for n in graph["nodes"] if n["id"] in law_ids]


def get_node_by_id(node_id: str) -> dict:
    """Fetch a single node's details."""
    graph = build_consumer_graph()
    for node in graph["nodes"]:
        if node["id"] == node_id:
            return node
    return {}


def get_connections_of_node(node_id: str) -> dict:
    """Returns all edges (incoming + outgoing) for a given node."""
    graph    = build_consumer_graph()
    incoming = [e for e in graph["edges"] if e["to"]   == node_id]
    outgoing = [e for e in graph["edges"] if e["from"] == node_id]
    return {
        "node_id":           node_id,
        "incoming":          incoming,
        "outgoing":          outgoing,
        "total_connections": len(incoming) + len(outgoing),
    }