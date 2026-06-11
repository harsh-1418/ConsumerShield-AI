import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "app"))

from db.mongo import authorities_col

authorities = [
    {
        "name": "National Consumer Helpline",
        "phone": "1800-11-4000",
        "type": "helpline",
        "handles": ["product defect", "refund", "ecommerce", "service deficiency"]
    },
    {
        "name": "District Consumer Commission",
        "type": "court",
        "handles": ["compensation up to 50 lakh", "product liability", "service deficiency"]
    },
    {
        "name": "RBI Banking Ombudsman",
        "website": "https://cms.rbi.org.in",
        "type": "ombudsman",
        "handles": ["banking", "loan", "credit card", "UPI", "insurance"]
    },
    {
        "name": "ASCI",
        "website": "https://ascionline.in",
        "type": "regulator",
        "handles": ["misleading ads", "false advertising"]
    },
    {
        "name": "TRAI",
        "website": "https://www.trai.gov.in",
        "type": "regulator",
        "handles": ["telecom", "internet", "broadband", "mobile"]
    }
]

authorities_col.delete_many({})
authorities_col.insert_many(authorities)
print(f"✅ Seeded {len(authorities)} authorities")