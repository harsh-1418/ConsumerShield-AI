# backend/app/db/mongo.py
# FINAL WORKING VERSION - certifi fix confirmed working on Python 3.14
# Connected to: consumershield.5jlklhx.mongodb.net
# Collections: complaints, authorities

import os
import certifi
from urllib.parse import quote_plus
from pymongo import MongoClient
from dotenv import load_dotenv
from pathlib import Path

# Load .env from backend/ (3 levels up from app/db/mongo.py)
_env_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(_env_path)

username = quote_plus(os.getenv("MONGODB_USER", ""))
password = quote_plus(os.getenv("MONGODB_PASS", ""))
cluster  = os.getenv("MONGODB_CLUSTER", "")

if not username or not cluster:
    raise EnvironmentError(
        f"MONGODB_USER or MONGODB_CLUSTER missing from .env\n"
        f".env path: {_env_path}"
    )

uri = (
    f"mongodb+srv://{username}:{password}@{cluster}"
    f"/consumershield?retryWrites=true&w=majority"
)

# certifi fix — confirmed working on Python 3.14 + MongoDB Atlas
client = MongoClient(
    uri,
    serverSelectionTimeoutMS=15000,
    tlsCAFile=certifi.where(),
)

db              = client["consumershield"]
complaints_col  = db["complaints"]
authorities_col = db["authorities"]