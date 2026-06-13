# backend/test_mongo_quick.py
# Run: python test_mongo_quick.py  (from backend/ folder)

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

_env = Path(__file__).resolve().parent / ".env"
load_dotenv(_env)
print(f"[1] .env loaded from: {_env}")

username = os.getenv("MONGODB_USER", "")
password = os.getenv("MONGODB_PASS", "")
cluster  = os.getenv("MONGODB_CLUSTER", "")

print(f"[2] MONGODB_USER    : {'OK -> ' + username[:3] + '***' if username else 'MISSING'}")
print(f"[3] MONGODB_CLUSTER : {'OK -> ' + cluster if cluster else 'MISSING'}")

if not username or not cluster:
    print("\nSTOP: Fix .env first")
    sys.exit(1)

from urllib.parse import quote_plus
from pymongo import MongoClient

uri = (
    f"mongodb+srv://{quote_plus(username)}:{quote_plus(password)}"
    f"@{cluster}/consumershield?retryWrites=true&w=majority"
)

# ── Attempt 1: certifi (best fix for Python 3.14) ─────────────────────
print("\n[4] Trying FIX 1: certifi tlsCAFile...")
try:
    import certifi
    client = MongoClient(uri, serverSelectionTimeoutMS=15000, tlsCAFile=certifi.where())
    result = client.admin.command("ping")
    print(f"[5] CONNECTED with certifi! ping = {result}")
    db   = client["consumershield"]
    cols = db.list_collection_names()
    print(f"[6] Collections: {cols}")
    print("\nFIX 1 (certifi) WORKS - use this in mongo.py")
    sys.exit(0)
except ImportError:
    print("[5] certifi not installed - run: pip install certifi")
except Exception as e:
    print(f"[5] certifi fix failed: {type(e).__name__}: {str(e)[:120]}")

# ── Attempt 2: directConnection=False + longer timeout ────────────────
print("\n[6] Trying FIX 2: standard connection with longer timeout...")
try:
    client2 = MongoClient(uri, serverSelectionTimeoutMS=30000, directConnection=False)
    result2 = client2.admin.command("ping")
    print(f"[7] CONNECTED! ping = {result2}")
    print("\nFIX 2 WORKS")
    sys.exit(0)
except Exception as e:
    print(f"[7] FIX 2 failed: {type(e).__name__}: {str(e)[:120]}")

# ── Attempt 3: DNS SRV disabled (use standard URI) ────────────────────
print("\n[8] Trying FIX 3: standard URI without SRV...")
try:
    # Try standard URI format instead of +srv
    uri3 = f"mongodb://{quote_plus(username)}:{quote_plus(password)}@{cluster}:27017/consumershield?authSource=admin&tls=true"
    client3 = MongoClient(uri3, serverSelectionTimeoutMS=15000, tlsAllowInvalidCertificates=True)
    result3 = client3.admin.command("ping")
    print(f"[9] CONNECTED with standard URI! ping = {result3}")
    print("\nFIX 3 WORKS - use standard URI")
    sys.exit(0)
except Exception as e:
    print(f"[9] FIX 3 failed: {type(e).__name__}: {str(e)[:120]}")

print("\nAll fixes failed. Options:")
print("  1. Run: pip install --upgrade pymongo certifi")
print("  2. Ask Member 2 if Atlas cluster allows connections from your IP")
print("  3. Check Atlas Network Access — add 0.0.0.0/0 to IP whitelist")