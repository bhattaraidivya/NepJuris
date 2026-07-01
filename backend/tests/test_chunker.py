from pipeline.chunker import chunk_text


def test_empty_text_returns_no_chunks():
    assert chunk_text("") == []


def test_single_short_sentence_is_one_chunk():
    text = "<<<PAGE:1>>>\nThis is a short sentence."
    chunks = chunk_text(text, chunk_size=600)

    assert len(chunks) == 1
    assert chunks[0]["text"] == "This is a short sentence."
    assert chunks[0]["page_start"] == 1
    assert chunks[0]["page_end"] == 1


def test_never_splits_a_sentence_in_half():
    long_sentence = "Word " * 200 + "."
    text = f"<<<PAGE:1>>>\n{long_sentence.strip()} Second sentence here."

    chunks = chunk_text(text, chunk_size=50)

    for chunk in chunks:
        # Every chunk should be made of whole sentences we recognize,
        # never a mid-word/mid-sentence fragment introduced by slicing.
        assert chunk["text"].strip().endswith((".", "!", "?"))


def test_tracks_page_span_across_page_marker():
    text = (
        "<<<PAGE:1>>>\nFirst page sentence one. First page sentence two.\n"
        "<<<PAGE:2>>>\nSecond page sentence one."
    )

    chunks = chunk_text(text, chunk_size=1000, overlap_sentences=0)

    assert len(chunks) == 1
    assert chunks[0]["page_start"] == 1
    assert chunks[0]["page_end"] == 2


def test_overlap_carries_last_sentence_into_next_chunk():
    text = "<<<PAGE:1>>>\n" + " ".join(f"Sentence number {i}." for i in range(20))

    chunks = chunk_text(text, chunk_size=40, overlap_sentences=1)

    assert len(chunks) > 1
    # the last sentence of a chunk should reappear as the first sentence
    # of the following chunk (continuity for the reader/retriever).
    first_chunk_sentences = chunks[0]["text"].split(". ")
    second_chunk_sentences = chunks[1]["text"].split(". ")
    assert first_chunk_sentences[-1].rstrip(".") in second_chunk_sentences[0]
