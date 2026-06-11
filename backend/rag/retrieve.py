import os
from pathlib import Path
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from embedding import get_embedding

load_dotenv(Path(__file__).parent.parent / ".env")

client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY")
)

def retrieve(query: str, top_k: int = 5):
    vector = get_embedding(query)
    results = client.query_points(
        collection_name="consumer_laws",
        query=vector,
        limit=top_k
    ).points
    return [
        {
            "source": r.payload["source"],
            "text": r.payload["text"],
            "score": r.score
        }
        for r in results
    ]

if __name__ == "__main__":
    query = "Amazon delivered a damaged product and denied replacement"
    print(f"Query: {query}\n")
    hits = retrieve(query)
    for i, hit in enumerate(hits):
        print(f"--- Result {i+1} [{hit['source']}] (score: {hit['score']:.3f}) ---")
        print(hit["text"][:300])
        print()