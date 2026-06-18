import os

import requests
from rag.retriever import Retriever
from rag.context_formatter import format_context

OLLAMA_URL = os.getenv(
    "OLLAMA_URL",
    "http://ollama:11434/api/generate"
)
MODEL_NAME = "llama3"


class Generator:
    def build_prompt(self, query, contexts):

        context_text = format_context(contexts)

        prompt = f"""
You are NepJuris, a professional AI legal assistant for Nepal.

You must answer ONLY using the provided legal context.

If the answer is not present in the context, say:
"I don't have enough information in the provided legal documents."

---

# LEGAL CONTEXT
{context_text}

---

# USER QUESTION
{query}

---

# RESPONSE FORMAT

📌 Answer:
- Give a short direct answer first

📖 Legal Basis:
- MUST cite the provided source and reference 
- Use this format: (Source Name, Reference)

⚖️ Explanation:
- Explain briefly using only retrieved legal context
- Keep explanation concise and structured



Rules:
- NEVER use outside knowledge 
- NEVER hallucinate laws
- NEVER invent sections or articles 
- NEVER write long paragraphs
- NEVER repeat the entire context 
- Every factual statement must be grounded in retrieved context 
- Always include citations when possible 
- Keep total response under 12 lines
---

Answer:
"""
        return prompt

    def generate(self, query, contexts):

        prompt = self.build_prompt(query, contexts)

        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False
            }
        )

        data = response.json()
        return data.get("response", "Error generating response")