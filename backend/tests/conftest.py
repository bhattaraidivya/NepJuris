import os
import sys
import types

# Allow `import pipeline.x` / `import rag.x` regardless of the directory
# pytest is invoked from.
BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

# rag.embedder loads a real SentenceTransformer model at import time, and
# rag.retriever imports rag.embedder — so merely importing the retriever
# would otherwise download a model from HuggingFace Hub during test
# collection. Stub it out; tests that exercise retrieval logic patch
# rag.retriever.create_embedding directly instead of needing real vectors.
if "sentence_transformers" not in sys.modules:
    stub = types.ModuleType("sentence_transformers")

    class _StubSentenceTransformer:
        def __init__(self, *args, **kwargs):
            pass

        def encode(self, *args, **kwargs):
            raise NotImplementedError("SentenceTransformer is stubbed in tests")

    stub.SentenceTransformer = _StubSentenceTransformer
    sys.modules["sentence_transformers"] = stub
