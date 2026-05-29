import sentence_transformers

# load pretrained embedding model
model = sentence_transformers.SentenceTransformer("all-MiniLM-L6-v2")

def create_embedding(text):
    embedding = model.encode(text)

    return embedding.tolist()