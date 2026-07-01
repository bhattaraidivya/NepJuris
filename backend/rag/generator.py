import logging
import os

import requests

from rag.context_formatter import format_context

logger = logging.getLogger(__name__)

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://ollama:11434/api/generate")
MODEL_NAME = os.getenv("MODEL_NAME", "qwen2.5:3b").strip()

REQUEST_TIMEOUT = 60

PROMPT_TEMPLATE = """
You are NepJuris, a retrieval-based legal assistant for Nepal.

You DO NOT use external knowledge.
You ONLY use the provided context.

---

# STEP 1: CLASSIFY QUERY
Decide:
A) GREETING / CASUAL
B) LEGAL QUESTION

---

# RULES

## If A (Greeting/Casual):
- Respond naturally in 1-2 lines
- DO NOT use legal format
- DO NOT mention legal basis
- DO NOT reference context

## If B (Legal Question):
- Use ONLY provided context
- If context does not contain answer:
  -> say: "I don't have enough information in the provided legal documents."
- NEVER invent laws or acts
- NEVER use outside knowledge

---

# OUTPUT RULES (IMPORTANT)

- Do NOT output tool calls
- Do NOT output internal reasoning
- Do NOT output markdown headings
- Keep response clean and human readable

---

# CONTEXT
{context}

---

# QUESTION
{question}

---

# RESPONSE:
"""


class GenerationError(Exception):
    """Raised when the LLM backend fails to produce a response."""


class Generator:
    """Builds prompts from retrieved context and calls Ollama to generate answers."""

    def build_prompt(self, query, contexts):
        context_text = format_context(contexts)
        return PROMPT_TEMPLATE.format(context=context_text, question=query)

    def generate(self, query, contexts):
        prompt = self.build_prompt(query, contexts)

        try:
            response = requests.post(
                OLLAMA_URL,
                json={
                    "model": MODEL_NAME,
                    "prompt": prompt,
                    "stream": False,
                },
                timeout=REQUEST_TIMEOUT,
            )

            if response.status_code != 200:
                logger.error("Ollama returned status %s: %s", response.status_code, response.text[:500])
                raise GenerationError(f"LLM backend returned status {response.status_code}")

            data = response.json()

            if isinstance(data, dict) and "response" in data:
                return data["response"]

            logger.error("Unexpected Ollama response shape: %s", data)
            raise GenerationError("LLM backend returned an unexpected response shape")

        except requests.exceptions.Timeout as e:
            logger.error("Request to Ollama timed out")
            raise GenerationError("The LLM backend timed out") from e
        except requests.exceptions.RequestException as e:
            logger.error("Request to Ollama failed: %s", e)
            raise GenerationError("Could not reach the LLM backend") from e
