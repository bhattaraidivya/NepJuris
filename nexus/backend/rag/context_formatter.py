def format_context(contexts):
    formatted = []

    for c in contexts:
        doc = c.get("source", "Unknown Document")
        page = c.get("page")
        section = c.get("section")
        article = c.get("article")

        citation = doc

        if article:
            citation += f", Article {article}"
        if section:
            citation += f", Section {section}"
        if page:
            citation += f", Page {page}"

        formatted.append(
            f"[SOURCE]\n{citation}\n\n{c['text']}"
        )

    return "\n\n".join(formatted)