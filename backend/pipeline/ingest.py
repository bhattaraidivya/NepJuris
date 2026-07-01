import json
import logging
import os

from pipeline.extractor import extract_document
from pipeline.chunker import chunk_text
from rag.embedder import create_embedding
from rag.vector_store import VectorStore

logger = logging.getLogger(__name__)


# =========================
# BASE PATH SETUP
# =========================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATALOG_PATH = os.path.join(BASE_DIR, "data", "data_catalog.json")
INDEX_PATH = os.path.join(BASE_DIR, "data", "embeddings", "faiss_index")


# =========================
# LOAD CATALOG
# =========================
def load_catalog():
    with open(CATALOG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


# =========================
# UPDATE DOCUMENT STATUS
# =========================
def update_doc_status(doc_id: str, new_status: str):
    with open(CATALOG_PATH, "r", encoding="utf-8") as f:
        docs = json.load(f)

    for doc in docs:
        if doc["id"] == doc_id:
            doc["status"] = new_status
            break

    with open(CATALOG_PATH, "w", encoding="utf-8") as f:
        json.dump(docs, f, indent=2)


# =========================
# PROCESS A SINGLE DOCUMENT
# =========================
def ingest_document_into_store(doc: dict, store: VectorStore) -> int:
    """Extracts, chunks, embeds, and adds one catalog document to `store`.

    Shared by the bulk CLI build and the single-document upload flow so
    both paths produce identically-shaped chunk metadata.
    """
    text = extract_document(doc)

    if not text or len(text.strip()) == 0:
        raise ValueError(f"No text extracted from {doc['name']}")

    chunks = chunk_text(text)

    for i, chunk in enumerate(chunks):
        embedding = create_embedding(chunk["text"])

        page_label = (
            str(chunk["page_start"])
            if chunk["page_start"] == chunk["page_end"]
            else f"{chunk['page_start']}-{chunk['page_end']}"
        )

        metadata = {
            "doc_id": doc["id"],
            "doc_name": doc["name"],
            "source": doc["name"],
            "page": page_label,
            "section": doc.get("section", None),
            "article": doc.get("article", None),
            "chunk_id": f"{doc['id']}_{i}",
            "text": chunk["text"],
        }

        store.add(embedding, metadata)

    return len(chunks)


def save_store(store: VectorStore):
    output_dir = os.path.dirname(INDEX_PATH)
    os.makedirs(output_dir, exist_ok=True)
    store.save(INDEX_PATH)


def load_or_create_store() -> VectorStore:
    store = VectorStore(dim=384)
    if os.path.exists(INDEX_PATH + ".index") and os.path.exists(INDEX_PATH + "_meta.json"):
        store.load(INDEX_PATH)
    return store


# =========================
# BUILD FAISS KNOWLEDGE BASE (bulk, from scratch)
# =========================
def build_knowledge_base():
    catalog = load_catalog()

    # FAISS VECTOR STORE INIT (384 = MiniLM dimension)
    store = VectorStore(dim=384)

    total_chunks = 0

    for doc in catalog:
        print("\n==============================")
        print(f"📄 Processing: {doc['name']}")

        try:
            chunk_count = ingest_document_into_store(doc, store)
            total_chunks += chunk_count

            update_doc_status(doc["id"], "indexed")
            print(f"   🔹 Chunks: {chunk_count}")
            print(f"   ✅ {doc['name']} indexed")

        except Exception as e:
            print(f"❌ Error processing {doc['name']}: {str(e)}")
            update_doc_status(doc["id"], "failed")

    save_store(store)

    print("\n==============================")
    print("✅ FAISS KNOWLEDGE BASE CREATED")
    print(f"📦 Total chunks indexed: {total_chunks}")
    print(f"💾 Saved to: {INDEX_PATH}.index + _meta.json")


# =========================
# RUN PIPELINE
# =========================
if __name__ == "__main__":
    build_knowledge_base()
