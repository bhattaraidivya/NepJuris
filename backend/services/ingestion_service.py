import json
import logging
import os
import re

from fastapi import HTTPException, UploadFile

from pipeline.ingest import (
    CATALOG_PATH,
    ingest_document_into_store,
    load_or_create_store,
    save_store,
    update_doc_status,
)
from rag.retriever import get_retriever

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")

MAX_UPLOAD_BYTES = 20 * 1024 * 1024  # 20 MB


class IngestionService:
    """Handles user-uploaded PDFs: saves the file, registers it in the
    catalog, and incrementally ingests it into the existing FAISS index
    without rebuilding the whole knowledge base from scratch.
    """

    def _load_catalog(self) -> list:
        with open(CATALOG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save_catalog(self, docs: list):
        with open(CATALOG_PATH, "w", encoding="utf-8") as f:
            json.dump(docs, f, indent=2)

    def _next_doc_id(self, docs: list) -> str:
        max_n = 0
        for doc in docs:
            match = re.match(r"doc_(\d+)$", doc.get("id", ""))
            if match:
                max_n = max(max_n, int(match.group(1)))
        return f"doc_{max_n + 1:03d}"

    async def upload_and_ingest(self, file: UploadFile, name: str, category: str) -> dict:
        if not name or not name.strip():
            raise HTTPException(status_code=400, detail="Document name is required.")

        is_pdf = (file.content_type == "application/pdf") or (
            file.filename and file.filename.lower().endswith(".pdf")
        )
        if not is_pdf:
            raise HTTPException(status_code=400, detail="Only PDF files are supported.")

        contents = await file.read()
        if not contents:
            raise HTTPException(status_code=400, detail="Uploaded file is empty.")
        if len(contents) > MAX_UPLOAD_BYTES:
            raise HTTPException(status_code=400, detail="File exceeds the 20MB upload limit.")

        os.makedirs(RAW_DIR, exist_ok=True)

        docs = self._load_catalog()
        doc_id = self._next_doc_id(docs)
        relative_path = f"data/raw/{doc_id}.pdf"
        full_path = os.path.join(BASE_DIR, relative_path)

        with open(full_path, "wb") as f:
            f.write(contents)

        doc = {
            "id": doc_id,
            "name": name.strip(),
            "file_path": relative_path,
            "language": "en",
            "type": "pdf",
            "category": category.strip() if category and category.strip() else "uncategorized",
            "extraction_type": "text",
            "source": "user_upload",
            "status": "pending",
        }
        docs.append(doc)
        self._save_catalog(docs)

        try:
            store = load_or_create_store()
            chunk_count = ingest_document_into_store(doc, store)
            save_store(store)
            update_doc_status(doc_id, "indexed")
            doc["status"] = "indexed"

            # Hot-reload the shared retriever so the new document is
            # searchable immediately, with no backend restart required.
            get_retriever().load()

            logger.info("Ingested %s (%s) — %d chunks", doc_id, doc["name"], chunk_count)
            return {"document": doc, "chunks_indexed": chunk_count}

        except Exception as e:
            logger.exception("Ingestion failed for %s", doc_id)
            update_doc_status(doc_id, "failed")
            raise HTTPException(
                status_code=500,
                detail=f"Document was saved but ingestion failed: {e}",
            ) from e
