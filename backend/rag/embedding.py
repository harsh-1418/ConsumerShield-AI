# backend/rag/embedding.py

import os
import time
from dotenv import load_dotenv
from pathlib import Path
from google import genai

load_dotenv(Path(__file__).parent.parent / ".env")

_client = None

def get_embedding(text: str):
    global _client

    if _client is None:
        _client = genai.Client(
            api_key=os.getenv("GEMINI_API_KEY")
        )

    for attempt in range(5):
        try:
            result = _client.models.embed_content(
                model="models/gemini-embedding-001",
                contents=text
            )

            return result.embeddings[0].values

        except Exception as e:

            print(
                f"Embedding failed (Attempt {attempt+1}/5): {e}"
            )

            time.sleep(5)

    raise Exception(
        "Failed to generate embedding after 5 retries."
    )