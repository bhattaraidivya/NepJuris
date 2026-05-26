import os
from .embedder import create_embedding

DOCUMENTS_PATH = "documents"


def simple_chunk(text):
    """
    Better deterministic chunking for legal RAG:
    split by paragraph breaks.
    """
    chunks = text.split("\n\n")
    return [c.strip() for c in chunks if c.strip()]


def load_documents():
    documents = []

    for filename in os.listdir(DOCUMENTS_PATH):
        filepath = os.path.join(DOCUMENTS_PATH, filename)

        with open(filepath, "r", encoding="utf-8") as file:
            content = file.read()

            # STEP 1: better chunking (controlled)
            chunks = simple_chunk(content)

            embedded_chunks = []

            for chunk in chunks:
                embedding = create_embedding(chunk)

                embedded_chunks.append({
                    "text": chunk,
                    "embedding": embedding
                })

            documents.append({
                "filename": filename,
                "chunks": embedded_chunks
            })

    return documents