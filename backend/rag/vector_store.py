import faiss
import numpy as np
import json


class VectorStore:
    def __init__(self, dim=384):
        self.dim = dim
        # Inner product over normalized vectors == cosine similarity.
        # Embeddings must be normalized at encoding time (see embedder.py).
        self.index = faiss.IndexFlatIP(dim)
        self.metadata = []

    def add(self, embedding, metadata):
        vector = np.array(embedding).astype("float32").reshape(1, -1)
        self.index.add(vector)
        self.metadata.append(metadata)

    def search(self, query_embedding, top_k=5):
        query_vector = np.array(query_embedding).astype("float32").reshape(1, -1)

        scores, indices = self.index.search(query_vector, top_k)

        results = []
        for score, idx in zip(scores[0], indices[0]):
            # FAISS pads with -1 when the index holds fewer than top_k
            # vectors; without this check that would wrap to metadata[-1]
            # and silently return an unrelated chunk as a "match".
            if idx == -1:
                continue
            if idx < len(self.metadata):
                results.append({**self.metadata[idx], "score": float(score)})

        return results

    def save(self, path="data/faiss_index"):
        faiss.write_index(self.index, path + ".index")

        with open(path + "_meta.json", "w", encoding="utf-8") as f:
            json.dump(self.metadata, f, ensure_ascii=False)

    def load(self, path="data/faiss_index"):
        self.index = faiss.read_index(path + ".index")

        with open(path + "_meta.json", "r", encoding="utf-8") as f:
            self.metadata = json.load(f)
