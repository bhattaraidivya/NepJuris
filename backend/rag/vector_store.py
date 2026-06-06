import faiss
import numpy as np
import json


class VectorStore:
    def __init__(self, dim=384):
        self.dim = dim
        self.index = faiss.IndexFlatL2(dim)
        self.metadata = []

    def add(self, embedding, metadata):
        vector = np.array(embedding).astype("float32").reshape(1, -1)
        self.index.add(vector)
        self.metadata.append(metadata)

    def search(self, query_embedding, top_k=5):
        query_vector = np.array(query_embedding).astype("float32").reshape(1, -1)

        distances, indices = self.index.search(query_vector, top_k)

        results = []
        for idx in indices[0]:
            if idx < len(self.metadata):
                results.append(self.metadata[idx])

        return results

    def save(self, path="data/faiss_index"):
        faiss.write_index(self.index, path + ".index")

        with open(path + "_meta.json", "w", encoding="utf-8") as f:
            json.dump(self.metadata, f, ensure_ascii=False)

    def load(self, path="data/faiss_index"):
        self.index = faiss.read_index(path + ".index")

        with open(path + "_meta.json", "r", encoding="utf-8") as f:
            self.metadata = json.load(f)