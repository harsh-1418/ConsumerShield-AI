from sentence_transformers import SentenceTransformer

model = None

def get_embedding(text: str):
    global model
    if model is None:
        model = SentenceTransformer(
            "BAAI/bge-small-en-v1.5"
        )
    return model.encode(
        text,
        normalize_embeddings=True
    ).tolist()