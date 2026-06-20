import os
from rag.embedder import create_embedding
from rag.vector_store import VectorStore


class Retriever:
    def __init__(self, index_path=None):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        # FAISS index path
        self.index_path = index_path or os.path.join(
            BASE_DIR,
            "data",
            "embeddings",
            "faiss_index"
        )

        self.store = VectorStore(dim=384)
        self.loaded = False

    # =========================
    # LOAD FAISS INDEX
    # =========================
    def load(self):
        try:
            self.store.load(self.index_path)
            self.loaded = True
            print("✅ FAISS index loaded successfully")
        except Exception as e:
            print("⚠️ FAISS index not loaded:", e)
            self.loaded = False

    # =========================
    # MAIN RETRIEVAL FUNCTION
    # =========================
    def retrieve(self, query, top_k=5):
        if not self.loaded:
            raise Exception("FAISS index not loaded. Call load() first.")

        # Embed the raw query directly. SentenceTransformer models are
        # trained on full natural-language input, so no manual expansion
        # is needed here.
        query_embedding = create_embedding(query)

        results = self.store.search(query_embedding, top_k)

        return results

    # =========================
    # OPTIONAL: DEBUG HELPERS
    # =========================
    def debug_retrieval(self, query):
        """Use this to test retrieval quality"""
        results = self.retrieve(query)

        print("\n🔍 QUERY:", query)
        print("\n📚 RESULTS:")

        for i, r in enumerate(results):
            print(f"\n--- Chunk {i+1} ---")
            print(r["text"][:300])

        return results