import os

from fastapi import APIRouter, File, Form, Request, UploadFile
from rate_limiter import limiter
from services.document_service import DocumentService
from services.ingestion_service import IngestionService

router = APIRouter()

service = DocumentService()
ingestion_service = IngestionService()

UPLOAD_RATE_LIMIT = os.getenv("UPLOAD_RATE_LIMIT", "3/hour")


@router.get("/documents")
def get_documents():
    return service.get_all()


@router.get("/documents/{doc_id}")
def get_document(doc_id: str):
    return service.get_one(doc_id)


@router.get("/documents/{doc_id}/download")
def download_document(doc_id: str):
    return service.download(doc_id)


@router.post("/documents/upload")
@limiter.limit(UPLOAD_RATE_LIMIT)
async def upload_document(
    request: Request,
    file: UploadFile = File(...),
    name: str = Form(...),
    category: str = Form(""),
):
    """Uploads a PDF, registers it in the catalog, and ingests it into
    the FAISS index immediately — no separate ingestion step required."""
    return await ingestion_service.upload_and_ingest(file, name, category)
