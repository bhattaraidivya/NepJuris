def chunk_text(text: str, chunk_size: int = 400, overlap: int = 80):
    """
    Simple sliding window chunker for RAG
    """
    chunks = []

    if not text:
        return chunks

    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks