import fitz
import os
import re
from collections import Counter


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PAGE_MARKER_PATTERN = re.compile(r"<<<PAGE:(\d+)>>>")


def _is_lone_number_line(line: str) -> bool:
    """Catches stray page-number-only lines like '43' or '44'."""
    stripped = line.strip()
    return stripped.isdigit() and len(stripped) <= 4


def _detect_repeated_header_footer_lines(pages_text: list, edge_lines: int = 2, threshold: float = 0.3) -> set:
    """
    Looks at the first/last N lines of every page. Any exact line that
    repeats across more than `threshold` fraction of pages is treated
    as a running header/footer and flagged for removal.
    """
    line_counts = Counter()
    total_pages = len(pages_text)

    for page_text in pages_text:
        lines = page_text.split("\n")
        candidate_lines = lines[:edge_lines] + lines[-edge_lines:]
        for line in candidate_lines:
            cleaned = line.strip()
            if cleaned and not _is_lone_number_line(cleaned):
                line_counts[cleaned] += 1

    junk_lines = {
        line for line, count in line_counts.items()
        if count / total_pages >= threshold
    }
    return junk_lines


def _clean_page_text(page_text: str, junk_lines: set) -> str:
    cleaned_lines = []
    for line in page_text.split("\n"):
        stripped = line.strip()
        if not stripped:
            continue  # drop blank lines
        if stripped in junk_lines:
            continue  # drop detected running header/footer
        if _is_lone_number_line(stripped):
            continue  # drop stray page numbers
        cleaned_lines.append(stripped)
    return "\n".join(cleaned_lines)


def extract_text_from_pdf(file_path: str) -> str:
    full_path = os.path.join(BASE_DIR, file_path)
    doc = fitz.open(full_path)

    raw_pages = [page.get_text() for page in doc]

    junk_lines = _detect_repeated_header_footer_lines(raw_pages)

    text_pages = []
    for page_index, page_text in enumerate(raw_pages):
        page_number = page_index + 1
        cleaned = _clean_page_text(page_text, junk_lines)
        text_pages.append(f"<<<PAGE:{page_number}>>>\n{cleaned}")

    return "\n".join(text_pages)


def extract_document(doc: dict) -> str:
    file_path = doc["file_path"]
    extraction_type = doc.get("extraction_type", "text")

    if extraction_type == "text":
        return extract_text_from_pdf(file_path)

    raise ValueError("Unsupported extraction type")