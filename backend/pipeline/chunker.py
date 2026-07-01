import re

PAGE_MARKER_PATTERN = re.compile(r"<<<PAGE:(\d+)>>>")
SENTENCE_SPLIT_PATTERN = re.compile(r"(?<=[.!?])\s+")


def _split_into_sentences(text: str) -> list:
    """Simple sentence splitter. Not perfect for legal abbreviations
    (e.g. 'No.', 'Art.') but good enough as a first pass."""
    sentences = SENTENCE_SPLIT_PATTERN.split(text)
    return [s.strip() for s in sentences if s.strip()]


def chunk_text(text: str, chunk_size: int = 600, overlap_sentences: int = 1):
    """
    Sentence-aware chunker for RAG. Groups whole sentences together
    until adding the next sentence would exceed chunk_size, then starts
    a new chunk carrying over the last `overlap_sentences` for continuity.
    Tracks page_start/page_end per chunk using <<<PAGE:N>>> markers.
    """
    chunks = []
    if not text:
        return chunks

    clean_text = PAGE_MARKER_PATTERN.sub("", text)

    # Locate page marker positions relative to clean_text (i.e. after
    # stripping), so sentence offsets computed against clean_text later
    # can be mapped back to the correct page.
    cleaned_boundaries = []
    removed_so_far = 0
    for match in PAGE_MARKER_PATTERN.finditer(text):
        marker_len = match.end() - match.start()
        clean_pos = match.start() - removed_so_far
        cleaned_boundaries.append((clean_pos, int(match.group(1))))
        removed_so_far += marker_len

    def page_for_position(pos: int) -> int:
        page = cleaned_boundaries[0][1] if cleaned_boundaries else 1
        for boundary_pos, page_num in cleaned_boundaries:
            if boundary_pos <= pos:
                page = page_num
            else:
                break
        return page

    sentences = _split_into_sentences(clean_text)

    # Track each sentence's approximate character offset in clean_text
    # so we can determine page numbers per chunk.
    sentence_positions = []
    cursor = 0
    for sentence in sentences:
        pos = clean_text.find(sentence, cursor)
        if pos == -1:
            pos = cursor
        sentence_positions.append(pos)
        cursor = pos + len(sentence)

    current_chunk_sentences = []
    current_length = 0
    i = 0

    while i < len(sentences):
        sentence = sentences[i]
        sentence_len = len(sentence)

        if current_length + sentence_len > chunk_size and current_chunk_sentences:
            chunk_str = " ".join(current_chunk_sentences)
            first_idx = i - len(current_chunk_sentences)
            page_start = page_for_position(sentence_positions[first_idx])
            page_end = page_for_position(sentence_positions[i - 1])

            chunks.append({
                "text": chunk_str,
                "page_start": page_start,
                "page_end": page_end,
            })

            # Carry over last N sentences for overlap/continuity
            current_chunk_sentences = current_chunk_sentences[-overlap_sentences:] if overlap_sentences else []
            current_length = sum(len(s) for s in current_chunk_sentences)

        current_chunk_sentences.append(sentence)
        current_length += sentence_len
        i += 1

    if current_chunk_sentences:
        chunk_str = " ".join(current_chunk_sentences)
        first_idx = len(sentences) - len(current_chunk_sentences)
        page_start = page_for_position(sentence_positions[first_idx])
        page_end = page_for_position(sentence_positions[-1])
        chunks.append({
            "text": chunk_str,
            "page_start": page_start,
            "page_end": page_end,
        })

    return chunks