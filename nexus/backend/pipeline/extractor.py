import fitz
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def extract_text_from_pdf(file_path: str) -> str:
    full_path = os.path.join(BASE_DIR, file_path)

    doc = fitz.open(full_path)

    text_pages = []

    for page in doc:
        text_pages.append(page.get_text())

    return "\n".join(text_pages)


def extract_document(doc: dict) -> str:
    file_path = doc["file_path"]
    extraction_type = doc.get("extraction_type", "text")

    if extraction_type == "text":
        return extract_text_from_pdf(file_path)

    raise ValueError("Unsupported extraction type")