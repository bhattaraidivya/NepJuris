from rag.context_formatter import format_context


def test_format_context_includes_full_citation():
    contexts = [{
        "source": "Constitution of Nepal",
        "page": "12",
        "section": "3",
        "article": "13",
        "text": "Equality before the law.",
    }]

    formatted = format_context(contexts)

    assert "Constitution of Nepal" in formatted
    assert "Article 13" in formatted
    assert "Section 3" in formatted
    assert "Page 12" in formatted
    assert "Equality before the law." in formatted


def test_format_context_omits_missing_citation_fields():
    contexts = [{
        "source": "Civil Code of Nepal",
        "page": None,
        "section": None,
        "article": None,
        "text": "Some provision text.",
    }]

    formatted = format_context(contexts)

    assert formatted.startswith("[SOURCE]\nCivil Code of Nepal\n")
    assert "Article" not in formatted
    assert "Section" not in formatted
    assert "Page" not in formatted


def test_format_context_joins_multiple_chunks():
    contexts = [
        {"source": "Doc A", "page": "1", "text": "First chunk."},
        {"source": "Doc B", "page": "2", "text": "Second chunk."},
    ]

    formatted = format_context(contexts)

    assert formatted.count("[SOURCE]") == 2
    assert "First chunk." in formatted
    assert "Second chunk." in formatted
