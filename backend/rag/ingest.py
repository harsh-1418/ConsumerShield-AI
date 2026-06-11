import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load .env from backend/ folder (one level up from rag/)
load_dotenv(Path(__file__).parent.parent / ".env")

from pypdf import PdfReader
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from chunking import get_splitter
from embedding import get_embedding

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

# Debug print so we can confirm values are loaded
print(f"Connecting to: {QDRANT_URL}")

client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)

COLLECTION = "consumer_laws"

test_vec = get_embedding("test")
vector_size = len(test_vec)

if not client.collection_exists(COLLECTION):
    client.create_collection(
        collection_name=COLLECTION,
        vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
    )
    print(f"Created collection: {COLLECTION}")
else:
    print(f"Collection already exists: {COLLECTION}")

pdf_folder = Path(__file__).parent.parent.parent / "datasets" / "raw_laws"
print(f"Looking for PDFs in: {pdf_folder}")

splitter = get_splitter()
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

   # Replace the single upsert call at the bottom of the for loop with this:

    # Upload in batches of 10
    batch_size = 10
    for i in range(0, len(points), batch_size):
        batch = points[i:i + batch_size]
        client.upsert(collection_name=COLLECTION, points=batch)
    
    print(f"✅ Ingested: {pdf_file.name} ({len(chunks)} chunks)")