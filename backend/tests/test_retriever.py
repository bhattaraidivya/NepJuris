from unittest.mock import patch

from rag.retriever import MIN_RELEVANCE_SCORE, Retriever, RetrieverNotReadyError


class FakeStore:
    """Stands in for VectorStore.search() with pre-scored candidates,
    so filtering logic can be tested without a real FAISS index."""

    def __init__(self, candidates):
        self.candidates = candidates

    def search(self, query_embedding, top_k):
        return self.candidates[:top_k]


def make_retriever(candidates):
    r = Retriever.__new__(Retriever)  # skip __init__, no real index needed
    r.loaded = True
    r.store = FakeStore(candidates)
    return r


def test_retrieve_raises_when_index_not_loaded():
    r = Retriever.__new__(Retriever)
    r.loaded = False

    try:
        r.retrieve("anything")
        assert False, "expected RetrieverNotReadyError"
    except RetrieverNotReadyError:
        pass


@patch("rag.retriever.create_embedding", return_value=[0.0])
def test_retrieve_filters_out_chunks_below_relevance_threshold(_mock_embed):
    candidates = [
        {"text": "clearly relevant", "score": MIN_RELEVANCE_SCORE + 0.2},
        {"text": "borderline", "score": MIN_RELEVANCE_SCORE},
        {"text": "irrelevant", "score": MIN_RELEVANCE_SCORE - 0.1},
    ]
    r = make_retriever(candidates)

    results = r.retrieve("some query")

    assert [c["text"] for c in results] == ["clearly relevant", "borderline"]


@patch("rag.retriever.create_embedding", return_value=[0.0])
def test_retrieve_returns_empty_for_generic_non_legal_queries(_mock_embed):
    # Mirrors real observed scores for greetings/small talk against the
    # legal corpus (well below the relevance threshold).
    candidates = [
        {"text": "unrelated chunk 1", "score": 0.23},
        {"text": "unrelated chunk 2", "score": 0.19},
    ]
    r = make_retriever(candidates)

    results = r.retrieve("hello, how are you?")

    assert results == []


@patch("rag.retriever.create_embedding", return_value=[0.0])
def test_retrieve_caps_results_at_top_k(_mock_embed):
    candidates = [{"text": str(i), "score": 0.9} for i in range(10)]
    r = make_retriever(candidates)

    results = r.retrieve("query", top_k=3)

    assert len(results) == 3
