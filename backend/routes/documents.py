from fastapi import APIRouter, File, Form, UploadFile
from services.document_service import DocumentService
from services.ingestion_service import IngestionService

router = APIRouter()

service = DocumentService()
ingestion_service = IngestionService()


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
async def upload_document(
    file: UploadFile = File(...),
    name: str = Form(...),
    category: str = Form(""),
):
    """Uploads a PDF, registers it in the catalog, and ingests it into
    the FAISS index immediately — no separate ingestion step required."""
    return await ingestion_service.upload_and_ingest(file, name, category)
