# backend/prediction/risk_scoring.py
# Member 3 - Risk profiling based on case strength score


def get_risk_profile(score: int) -> dict:
    """
    Converts numeric score (0-100) to risk label + actionable advice.
    """
    if score >= 70:
        return {
            "risk_level": "Low Risk",
            "color": "green",
            "emoji": "✅",
            "recommendation": "Strong case. You have solid legal grounds to file a complaint.",
            "immediate_steps": [
                "Gather all purchase receipts and communication records",
                "File complaint at District Consumer Forum",
                "Call NCH Helpline 1800-11-4000 for free guidance",
                "Case should resolve within 90-150 days",
            ],
            "suggested_forum": "District Consumer Forum",
            "time_to_resolve": "90-150 days",
            "success_probability": "High (70-85%)",
        }

    elif score >= 40:
        return {
            "risk_level": "Medium Risk",
            "color": "yellow",
            "emoji": "⚠️",
            "recommendation": "Moderate case. Strengthen your evidence before filing.",
            "immediate_steps": [
                "Collect more evidence: photos, screenshots, emails",
                "Send a formal legal notice to the company first",
                "Try NCH Helpline 1800-11-4000 for pre-litigation mediation",
                "If unresolved in 30 days, file at District Forum",
            ],
            "suggested_forum": "NCH Helpline → District Forum",
            "time_to_resolve": "120-180 days",
            "success_probability": "Moderate (40-65%)",
        }

    else:
        return {
            "risk_level": "High Risk",
            "color": "red",
            "emoji": "❌",
            "recommendation": "Weak case currently. Consult a legal expert before proceeding.",
            "immediate_steps": [
                "Consult a consumer rights lawyer or Legal Aid Services",
                "Gather stronger documented evidence",
                "Check if issue falls under a specific regulator (SEBI, TRAI, IRDAI)",
                "Consider filing under a different law or section",
            ],
            "suggested_forum": "Legal Aid Services or Specialized Regulator",
            "time_to_resolve": "180+ days",
            "success_probability": "Low (20-40%)",
        }


def get_resolution_roadmap(score: int, forum: str) -> list:
    """
    Step-by-step resolution roadmap based on score and recommended forum.
    """
    base_steps = [
        {
            "step": 1,
            "title": "Document Everything",
            "description": "Save receipts, screenshots, emails, and all communication with the company.",
            "duration": "1-2 days",
        },
        {
            "step": 2,
            "title": "Send Legal Notice",
            "description": "Send a formal written complaint to the company via registered post.",
            "duration": "1 day (then wait 15 days for response)",
        },
        {
            "step": 3,
            "title": "Contact NCH Helpline",
            "description": "Call 1800-11-4000 (free). They mediate before you go to court.",
            "duration": "3-7 days",
        },
    ]

    if score >= 70:
        base_steps += [
            {
                "step": 4,
                "title": f"File at {forum}",
                "description": f"Submit complaint with all documents to {forum}. Pay nominal filing fee.",
                "duration": "1 day to file",
            },
            {
                "step": 5,
                "title": "Hearing & Resolution",
                "description": "Attend hearings. Commission typically resolves in 3-5 months.",
                "duration": "90-150 days",
            },
        ]
    else:
        base_steps += [
            {
                "step": 4,
                "title": "Consult Legal Aid",
                "description": "Visit District Legal Services Authority (DLSA) for free legal advice.",
                "duration": "1-3 days",
            },
            {
                "step": 5,
                "title": "Strengthen & Refile",
                "description": "With legal guidance, gather missing evidence and file a stronger complaint.",
                "duration": "15-30 days",
            },
        ]

    return base_steps