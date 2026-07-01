from rag.generator import Generator
from rag.retriever import get_retriever


class ChatService:
    def __init__(self):
        self.retriever = get_retriever()
        self.generator = Generator()

    def generate_response(self, message: str) -> dict:
        # 1. retrieve context
        contexts = self.retriever.retrieve(message)

        # 2. generate answer using context
        response = self.generator.generate(message, contexts)

        # 3. surface citations alongside the answer
        sources = self._build_sources(contexts)

        return {"response": response, "sources": sources}

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
