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
# UPDATE DOCUMENT STATUS
# =========================
def update_doc_status(doc_id: str, new_status: str):
    catalog_path = os.path.join(BASE_DIR, "data", "data_catalog.json")

    with open(catalog_path, "r", encoding="utf-8") as f:
        docs = json.load(f)

    for doc in docs:
        if doc["id"] == doc_id:
            doc["status"] = new_status
            break

    with open(catalog_path, "w", encoding="utf-8") as f:
        json.dump(docs, f, indent=2)


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

        try:
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
                    "doc_name": doc["name"],

                    # 🔥 REAL CITATION FIELDS
                    "source": doc["name"],

                    # If available from PDF processing later
                    "page": doc.get("page", None),
                    "section": doc.get("section", None),
                    "article": doc.get("article", None),

                    "chunk_id": f"{doc['id']}_{i}",

                    "text": chunk
                }




                store.add(embedding, metadata)
                total_chunks += 1

            # STEP 4: UPDATE STATUS (NEW ADDITION)
            update_doc_status(doc["id"], "indexed")
            print(f"   ✅ {doc['name']} indexed")

        except Exception as e:
            print(f"❌ Error processing {doc['name']}: {str(e)}")
            update_doc_status(doc["id"], "failed")

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