from fastapi import APIRouter
from services.document_service import DocumentService

router = APIRouter()

service = DocumentService()


@router.get("/documents")
def get_documents():
    return service.get_all()


@router.get("/documents/{doc_id}")
def get_document(doc_id: str):
    return service.get_one(doc_id)


@router.get("/documents/{doc_id}/download")
def download_document(doc_id: str):
    return service.download(doc_id)