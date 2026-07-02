from rag.generator import Generator
from rag.retriever import get_retriever


class ChatService:
    def __init__(self):
        self.retriever = get_retriever()
        self.generator = Generator()

    def generate_response(self, message: str, history: list[dict] | None = None) -> dict:
        # 1. retrieve context (retrieval is based on the current message only —
        # no query rewriting from history, so follow-ups that rely heavily on
        # prior context may retrieve weaker matches even though the LLM still
        # has the conversation to reason over)
        contexts = self.retriever.retrieve(message)

        # 2. generate answer + scope classification using context and history
        result = self.generator.generate(message, contexts, history)

        # 3. only cite sources when the answer is actually grounded in the
        # corpus — a greeting or an out-of-scope refusal shouldn't carry
        # citations just because retrieval happened to score some chunks
        # above threshold.
        sources = self._build_sources(contexts) if result["scope"] == "in_scope" else []

        return {"response": result["answer"], "sources": sources}

    @staticmethod
    def _build_sources(contexts: list) -> list:
        """Dedupes retrieved chunks into a citation list, preserving
        relevance order (contexts already come back ranked by FAISS)."""
        seen = set()
        sources = []

        for c in contexts:
            key = (c.get("source"), c.get("page"))
            if key in seen:
                continue
            seen.add(key)

            sources.append({
                "source": c.get("source", "Unknown Document"),
                "page": c.get("page"),
                "section": c.get("section"),
                "article": c.get("article"),
            })

        return sources
