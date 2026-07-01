import logging
import os

from rag.embedder import create_embedding
from rag.vector_store import VectorStore

logger = logging.getLogger(__name__)


class RetrieverNotReadyError(Exception):
    """Raised when retrieve() is called before the FAISS index has loaded."""


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
    # LOAD / RELOAD FAISS INDEX
    # =========================
    def load(self):
        """Loads (or reloads) the on-disk FAISS index + metadata into memory.

        Safe to call again after ingestion writes a new index, since callers
        share a single Retriever instance via get_retriever().
        """
        try:
            self.store.load(self.index_path)
            self.loaded = True
            logger.info("FAISS index loaded successfully (%d chunks)", len(self.store.metadata))
        except Exception:
            logger.exception("FAISS index failed to load from %s", self.index_path)
            self.loaded = False

    # =========================
    # MAIN RETRIEVAL FUNCTION
    # =========================
    def retrieve(self, query, top_k=5):
        if not self.loaded:
            raise RetrieverNotReadyError(
                "FAISS index not loaded. Ingest documents before querying."
            )

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


# =========================
# SHARED SINGLETON
# =========================
# Both chat serving and document ingestion need to see the same in-memory
# index: ingestion writes a fresh index to disk, then calls get_retriever()
# to hot-reload it so new documents are searchable immediately, with no
# backend restart required.
_shared_retriever: Retriever | None = None


def get_retriever() -> Retriever:
    global _shared_retriever
    if _shared_retriever is None:
        _shared_retriever = Retriever()
        _shared_retriever.load()
    return _shared_retriever
