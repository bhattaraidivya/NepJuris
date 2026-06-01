import requests
from rag.retriever import Retriever

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5:3b"


class Generator:
    def __init__(self):
        self.retriever = Retriever()
        self.retriever.load()

    def build_prompt(self, query, contexts):
        context_text = "\n\n".join(
            [f"- {c['text']}" for c in contexts]
        )

        prompt = f"""
You are NyayaAI, a legal assistant for Nepal.

Use ONLY the provided context to answer the question.

If the answer is not in the context, say:
"I don't have enough information in the provided legal documents."

---

Context:
{context_text}

---

Question:
{query}

---

Answer clearly and legally:
"""
        return prompt

    def generate(self, query):
        # Step 1: Retrieve relevant chunks
        contexts = self.retriever.retrieve(query)

        # Step 2: Build prompt
        prompt = self.build_prompt(query, contexts)

        # Step 3: Call Ollama
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False
            }
        )

        return response.json()["response"]