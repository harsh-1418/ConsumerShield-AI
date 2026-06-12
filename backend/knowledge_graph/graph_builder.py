# backend/knowledge_graph/graph_builder.py
# Member 3 - Static knowledge graph of Indian Consumer Rights ecosystem


def build_consumer_graph() -> dict:
    """
    Builds the knowledge graph of Indian consumer rights.
    Returns nodes + edges for frontend visualization (D3.js / Cytoscape).

    Node types : person | law | authority | right
    Edge labels : has | establishes | protects | appeals_to |
                  handles | governs | refers_to | enforces | can_file_at
    """

    nodes = [
        # ── PERSON ──────────────────────────────────────────────────
        {
            "id": "consumer", "label": "Consumer", "type": "person",
            "description": "Any person who buys goods/services for personal use",
        },

        # ── LAWS ────────────────────────────────────────────────────
        {
            "id": "cpa2019", "label": "Consumer Protection Act 2019",
            "type": "law",
            "description": "Primary law protecting consumer rights in India. Replaced CPA 1986.",
        },
        {
            "id": "ecommerce_rules", "label": "E-Commerce Rules 2020",
            "type": "law",
            "description": "Rules governing online marketplaces, refunds, and seller disclosures.",
        },
        {
            "id": "ecommerce_amendment", "label": "E-Commerce Amendment 2021",
            "type": "law",
            "description": "Amendment strengthening e-commerce consumer protections.",
        },
        {
            "id": "rbi_ombudsman", "label": "RBI Ombudsman Scheme 2021",
            "type": "law",
            "description": "RBI integrated scheme for banking and financial consumer grievances.",
        },

        # ── AUTHORITIES ─────────────────────────────────────────────
        {
            "id": "ncdrc", "label": "NCDRC", "type": "authority",
            "description": "National Consumer Disputes Redressal Commission. Handles claims above Rs 2 crore.",
        },
        {
            "id": "state_commission", "label": "State Commission", "type": "authority",
            "description": "Handles claims between Rs 1 crore and Rs 2 crore.",
        },
        {
            "id": "district_forum", "label": "District Forum", "type": "authority",
            "description": "Handles claims up to Rs 1 crore. First point of redressal.",
        },
        {
            "id": "ccpa", "label": "CCPA", "type": "authority",
            "description": "Central Consumer Protection Authority. Handles unfair trade practices and misleading ads.",
        },
        {
            "id": "nch", "label": "NCH Helpline 1800-11-4000", "type": "authority",
            "description": "National Consumer Helpline — free pre-litigation advice and mediation.",
        },
        {
            "id": "rbi_banking_ombudsman", "label": "RBI Banking Ombudsman", "type": "authority",
            "description": "Handles complaints against banks, NBFCs, and digital payment services.",
        },

        # ── CONSUMER RIGHTS ─────────────────────────────────────────
        {
            "id": "right_safety", "label": "Right to Safety", "type": "right",
            "description": "Protection from goods/services hazardous to life and property.",
        },
        {
            "id": "right_information", "label": "Right to Information", "type": "right",
            "description": "Right to know quality, quantity, price, and standard of goods/services.",
        },
        {
            "id": "right_choice", "label": "Right to Choice", "type": "right",
            "description": "Access to variety of goods at competitive prices.",
        },
        {
            "id": "right_heard", "label": "Right to be Heard", "type": "right",
            "description": "Consumer interests must be considered in relevant forums.",
        },
        {
            "id": "right_redress", "label": "Right to Redress", "type": "right",
            "description": "Right to seek remedy against unfair trade practices or defective goods.",
        },
        {
            "id": "right_education", "label": "Right to Consumer Education", "type": "right",
            "description": "Right to acquire knowledge and skills to make informed choices.",
        },
    ]

    edges = [
        # Consumer → Rights
        {"from": "consumer", "to": "right_safety",      "label": "has"},
        {"from": "consumer", "to": "right_information", "label": "has"},
        {"from": "consumer", "to": "right_choice",      "label": "has"},
        {"from": "consumer", "to": "right_heard",       "label": "has"},
        {"from": "consumer", "to": "right_redress",     "label": "has"},
        {"from": "consumer", "to": "right_education",   "label": "has"},

        # Laws → Authorities (establishes)
        {"from": "cpa2019",        "to": "ncdrc",                  "label": "establishes"},
        {"from": "cpa2019",        "to": "state_commission",        "label": "establishes"},
        {"from": "cpa2019",        "to": "district_forum",          "label": "establishes"},
        {"from": "cpa2019",        "to": "ccpa",                    "label": "establishes"},
        {"from": "rbi_ombudsman",  "to": "rbi_banking_ombudsman",   "label": "establishes"},

        # Laws → Rights (protects)
        {"from": "cpa2019",            "to": "right_safety",      "label": "protects"},
        {"from": "cpa2019",            "to": "right_redress",     "label": "protects"},
        {"from": "cpa2019",            "to": "right_information", "label": "protects"},
        {"from": "ecommerce_rules",    "to": "right_information", "label": "protects"},
        {"from": "ecommerce_rules",    "to": "right_redress",     "label": "protects"},
        {"from": "rbi_ombudsman",      "to": "right_redress",     "label": "protects"},

        # Laws govern consumers
        {"from": "ecommerce_rules",     "to": "consumer", "label": "governs"},
        {"from": "ecommerce_amendment", "to": "consumer", "label": "governs"},

        # Appeal chain
        {"from": "district_forum",   "to": "state_commission", "label": "appeals_to"},
        {"from": "state_commission", "to": "ncdrc",             "label": "appeals_to"},

        # NCH refers
        {"from": "nch", "to": "district_forum", "label": "refers_to"},
        {"from": "nch", "to": "ccpa",           "label": "refers_to"},

        # CCPA enforces
        {"from": "ccpa", "to": "right_safety",      "label": "enforces"},
        {"from": "ccpa", "to": "right_information", "label": "enforces"},

        # Banking path
        {"from": "consumer",              "to": "rbi_banking_ombudsman", "label": "can_file_at"},
        {"from": "rbi_banking_ombudsman", "to": "right_redress",         "label": "enforces"},
    ]

    return {
        "nodes": nodes,
        "edges": edges,
        "meta": {
            "total_nodes": len(nodes),
            "total_edges": len(edges),
            "node_types":  ["person", "law", "authority", "right"],
            "description": "Indian Consumer Rights Knowledge Graph",
        },
    }