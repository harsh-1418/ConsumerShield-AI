# backend/rag/reset_and_ingest.py
import os
from pathlib import Path
from dotenv import load_dotenv
from pypdf import PdfReader
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from langchain_text_splitters import RecursiveCharacterTextSplitter
from embedding import get_embedding

load_dotenv(Path(__file__).parent.parent / ".env")

client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY")
)

COLLECTION = "consumer_laws"

# Delete old collection
if client.collection_exists(COLLECTION):
    client.delete_collection(COLLECTION)
    print("Deleted old collection")

# Get new vector size from Gemini
test_vec = get_embedding("test")
vector_size = len(test_vec)
print(f"Gemini vector size: {vector_size}")

# Create new collection
client.create_collection(
    collection_name=COLLECTION,
    vectors_config=VectorParams(
        size=vector_size,
        distance=Distance.COSINE
    )
)

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

pdf_folder = Path(__file__).parent.parent.parent / "datasets" / "raw_laws"
point_id = 0

for pdf_file in pdf_folder.glob("*.pdf"):
    reader = PdfReader(str(pdf_file))
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text

    chunks = splitter.split_text(text)
    points = []

    for chunk in chunks:
        points.append(PointStruct(
            id=point_id,
            vector=get_embedding(chunk),
            payload={"source": pdf_file.name, "text": chunk}
        ))
        point_id += 1

    # Upload in batches of 5
    for i in range(0, len(points), 5):
        batch = points[i:i+5]
        for attempt in range(3):
            try:
                client.upsert(collection_name=COLLECTION, points=batch)
                break
            except Exception as e:
                if attempt == 2:
                    print(f"Failed batch: {e}")
                import time; time.sleep(2)

    print(f"✅ {pdf_file.name} ({len(chunks)} chunks)")

print(f"\n✅ Total: {point_id} points with Gemini embeddings")