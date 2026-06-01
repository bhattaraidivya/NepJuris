import os
from rag.embedder import create_embedding
from rag.vector_store import VectorStore


class Retriever:
    def __init__(self, index_path=None):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        # ✅ FIXED PATH (your actual location)
        self.index_path = index_path or os.path.join(
            BASE_DIR,
            "data",
            "embeddings",
            "faiss_index"
        )

        self.store = VectorStore(dim=384)
        self.loaded = False

    def load(self):
        try:
            self.store.load(self.index_path)
            self.loaded = True
        except Exception as e:
            print("⚠️ FAISS index not loaded:", e)
            self.loaded = False

    def retrieve(self, query, top_k=5):
        if not self.loaded:
            raise Exception("FAISS index not loaded. Call load() first.")

        query_embedding = create_embedding(query)
        return self.store.search(query_embedding, top_k)