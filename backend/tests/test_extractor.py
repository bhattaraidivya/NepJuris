from pipeline.extractor import (
    _clean_page_text,
    _detect_repeated_header_footer_lines,
    _is_lone_number_line,
)


def test_is_lone_number_line_detects_stray_page_numbers():
    assert _is_lone_number_line("43") is True
    assert _is_lone_number_line("  44  ") is True


def test_is_lone_number_line_ignores_real_text():
    assert _is_lone_number_line("Article 43") is False
    assert _is_lone_number_line("43.") is False
    assert _is_lone_number_line("") is False


def test_detect_repeated_header_footer_lines_flags_frequent_lines():
    pages = [
        "THE CONSTITUTION OF NEPAL\nSome body text on page one.\nFooter text",
        "THE CONSTITUTION OF NEPAL\nSome body text on page two.\nFooter text",
        "THE CONSTITUTION OF NEPAL\nSome body text on page three.\nFooter text",
    ]

    junk = _detect_repeated_header_footer_lines(pages, edge_lines=1, threshold=0.3)

    assert "THE CONSTITUTION OF NEPAL" in junk
    assert "Footer text" in junk
    # unique body lines must never be flagged as running headers/footers
    assert "Some body text on page one." not in junk


def test_detect_repeated_header_footer_lines_ignores_rare_lines():
    # 10 pages, each with a distinct case name (1/10 = 0.1 frequency) —
    # well below the 0.3 threshold, so none should be flagged as junk.
    pages = [
        f"Unique case name {i}\nBody text {i}" for i in range(10)
    ]

    junk = _detect_repeated_header_footer_lines(pages, edge_lines=1, threshold=0.3)

    assert junk == set()


def test_clean_page_text_strips_junk_and_blank_lines():
    page_text = "HEADER\n\nReal content line.\n43\nFOOTER"
    junk_lines = {"HEADER", "FOOTER"}

    cleaned = _clean_page_text(page_text, junk_lines)

    assert cleaned == "Real content line."
