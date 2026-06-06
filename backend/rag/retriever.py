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

        # 1. Expand query (VERY IMPORTANT)
        enhanced_query = self._expand_query(query)

        # 2. Create embedding
        query_embedding = create_embedding(enhanced_query)

        # 3. Retrieve more than needed, then trim (better ranking stability)
        results = self.store.search(query_embedding, top_k * 2)

        return results[:top_k]

    # =========================
    # QUERY EXPANSION LAYER
    # (MAKES AI FEEL SMARTER)
    # =========================
    def _expand_query(self, query: str) -> str:
        query = query.lower().strip()

        expansions = {
            # core legal concepts
            "citizenship": "Nepal citizenship constitutional law citizenship by descent naturalization eligibility provisions",
            "cybercrime": "Nepal cybercrime electronic transaction act digital offences hacking fraud online crime law",
            "constitution": "Constitution of Nepal fundamental rights state structure federalism governance articles provisions",
            "murder": "Nepal criminal code homicide murder punishment criminal law penalties section",
            "theft": "Nepal criminal code theft property crime punishment legal definition",
            "divorce": "Nepal civil code marriage divorce separation family law legal procedure",

            # general improvements
            "law": "Nepal legal system statutes acts regulations constitution judiciary",
            "rights": "fundamental rights Nepal constitution human rights legal protections",
        }

        return expansions.get(query, query)

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