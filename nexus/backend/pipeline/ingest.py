import json
import os

from pipeline.extractor import extract_document
from pipeline.chunker import chunk_text
from rag.embedder import create_embedding
from rag.vector_store import VectorStore


# =========================
# BASE PATH SETUP
# =========================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# =========================
# LOAD CATALOG
# =========================
def load_catalog():
    catalog_path = os.path.join(
        BASE_DIR,
        "data",
        "data_catalog.json"
    )

    with open(catalog_path, "r", encoding="utf-8") as f:
        return json.load(f)


# =========================
# BUILD FAISS KNOWLEDGE BASE
# =========================
def build_knowledge_base():
    catalog = load_catalog()

    # FAISS VECTOR STORE INIT (384 = MiniLM dimension)
    store = VectorStore(dim=384)

    total_chunks = 0

    for doc in catalog:
        print("\n==============================")
        print(f"📄 Processing: {doc['name']}")

        # STEP 1: Extract text
        text = extract_document(doc)

        if not text or len(text.strip()) == 0:
            print("⚠️ No text extracted, skipping document")
            continue

        # STEP 2: Chunk text
        chunks = chunk_text(text)

        print(f"   🔹 Chunks: {len(chunks)}")

        # STEP 3: Embed + store in FAISS
        for i, chunk in enumerate(chunks):
            embedding = create_embedding(chunk)

            metadata = {
                "doc_id": doc["id"],
                "chunk_id": f"{doc['id']}_{i}",
                "category": doc["category"],
                "language": doc["language"],
                "text": chunk
            }

            store.add(embedding, metadata)
            total_chunks += 1

    # =========================
    # SAVE FAISS INDEX
    # =========================
    output_dir = os.path.join(BASE_DIR, "data", "embeddings")
    os.makedirs(output_dir, exist_ok=True)

    store_path = os.path.join(output_dir, "faiss_index")
    store.save(store_path)

    print("\n==============================")
    print("✅ FAISS KNOWLEDGE BASE CREATED")
    print(f"📦 Total chunks indexed: {total_chunks}")
    print(f"💾 Saved to: {store_path}.index + _meta.json")


# =========================
# RUN PIPELINE
# =========================
if __name__ == "__main__":
    build_knowledge_base()