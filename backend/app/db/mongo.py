import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv("MONGODB_URI"))
db = client["consumershield"]

complaints_col = db["complaints"]
authorities_col = db["authorities"]