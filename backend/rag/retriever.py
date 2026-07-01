import logging
import os

from rag.embedder import create_embedding
from rag.vector_store import VectorStore

logger = logging.getLogger(__name__)

# Cosine similarity (via normalized embeddings + IndexFlatIP) below this
# score is treated as "not actually about the corpus" — greetings, small
# talk, and out-of-domain questions naturally score low against a legal
# corpus, so this is what keeps retrieval (and citations) from firing on
# non-legal queries instead of a hand-maintained keyword/greeting list.
MIN_RELEVANCE_SCORE = float(os.getenv("RETRIEVAL_MIN_SCORE", "0.35"))

DEFAULT_TOP_K = 5
DEFAULT_FETCH_K = 10  # candidate pool fetched before relevance filtering


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
    def retrieve(self, query, top_k=DEFAULT_TOP_K, fetch_k=DEFAULT_FETCH_K):
        if not self.loaded:
            raise RetrieverNotReadyError(
                "FAISS index not loaded. Ingest documents before querying."
            )

        # Embed the raw query directly. SentenceTransformer models are
        # trained on full natural-language input, so no manual expansion
        # is needed here.
        query_embedding = create_embedding(query)

        # Fetch a wider candidate pool than we intend to keep, since
        # filtering by relevance below may discard some of them.
        candidates = self.store.search(query_embedding, fetch_k)

        relevant = [c for c in candidates if c.get("score", 0.0) >= MIN_RELEVANCE_SCORE]

        if not relevant:
            top_score = candidates[0]["score"] if candidates else float("-inf")
            logger.info(
                "No chunks met the relevance threshold (%.2f) for query %r — top score was %.3f. "
                "Treating as a non-legal / out-of-corpus query.",
                MIN_RELEVANCE_SCORE, query, top_score,
            )

        return relevant[:top_k]

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
