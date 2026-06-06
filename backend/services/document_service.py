import os
import json
from fastapi import HTTPException
from fastapi.responses import FileResponse


class DocumentService:

    def __init__(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.catalog_path = os.path.join(self.base_dir, "data", "data_catalog.json")

    def _load_docs(self):
        with open(self.catalog_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def get_all(self):
        docs = self._load_docs()
        return {
            "count": len(docs),
            "documents": docs
        }

    def get_one(self, doc_id: str):
        docs = self._load_docs()

        for doc in docs:
            if doc.get("id") == doc_id:
                return doc

        raise HTTPException(status_code=404, detail="Document not found")

    def download(self, doc_id: str):
            docs = self._load_docs()

            for doc in docs:
                if doc.get("id") == doc_id:
                    file_path = os.path.join(self.base_dir, doc["file_path"])

                    return FileResponse(
                        path=file_path,
                        filename=doc["name"] + ".pdf",
                        media_type="application/pdf",
                        headers={
                            "Content-Disposition": "inline"
                        }
                    )

            raise HTTPException(status_code=404, detail="File not found")