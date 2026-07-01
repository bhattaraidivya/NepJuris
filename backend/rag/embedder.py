from sentence_transformers import SentenceTransformer

# load pretrained embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


def create_embedding(text):
    # Normalized so the vector store can use cosine similarity (inner
    # product on unit vectors) instead of raw L2 distance — cosine is
    # the metric this model was trained/evaluated against, and it also
    # gives a bounded, interpretable score for relevance filtering.
    embedding = model.encode(text, normalize_embeddings=True)

    return embedding.tolist()
