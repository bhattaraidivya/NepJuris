import json
import logging
import os

import requests

from rag.context_formatter import format_context

logger = logging.getLogger(__name__)

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://ollama:11434/api/generate")
MODEL_NAME = os.getenv("MODEL_NAME", "qwen2.5:3b").strip()

REQUEST_TIMEOUT = 60

SYSTEM_PROMPT = """You are NepJuris, a retrieval-based legal assistant for Nepal.

You DO NOT use external knowledge.
You ONLY use the provided context.

---

# STEP 1: CLASSIFY THE QUERY
Decide exactly one:
A) GREETING - small talk, no legal content
B) IN_SCOPE - a question about Nepali law, answerable (even partially) from the provided context
C) OUT_OF_SCOPE - a legal question about a jurisdiction other than Nepal, or anything requiring live/external information the context can't provide

---

# RULES

## If A (greeting):
- Respond naturally in 1-2 lines
- DO NOT use legal format, DO NOT mention legal basis, DO NOT reference context

## If B (in_scope):
- Use ONLY the provided context
- If the context does not contain the answer, say so honestly:
  -> "I don't have enough information in the provided legal documents."
- NEVER invent laws or acts, NEVER use outside knowledge

## If C (out_of_scope):
- Say: "I'm scoped to Nepali law and can't answer questions about other jurisdictions."
- Do NOT attempt to answer using outside knowledge, even if you know the answer

---

# OUTPUT FORMAT (IMPORTANT)
Respond with ONLY a single JSON object. No markdown fences, no text outside the JSON.
{"scope": "greeting" | "in_scope" | "out_of_scope", "answer": "<your response text>"}
"""

USER_PROMPT_TEMPLATE = """
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
        # SYSTEM_PROMPT contains a literal JSON example with braces, so it's
        # kept out of the .format() call to avoid it being parsed as a field.
        return SYSTEM_PROMPT + USER_PROMPT_TEMPLATE.format(context=context_text, question=query)

    def generate(self, query, contexts):
        """Returns {"answer": str, "scope": "greeting"|"in_scope"|"out_of_scope"}."""
        prompt = self.build_prompt(query, contexts)

        try:
            response = requests.post(
                OLLAMA_URL,
                json={
                    "model": MODEL_NAME,
                    "prompt": prompt,
                    "stream": False,
                    "format": "json",
                },
                timeout=REQUEST_TIMEOUT,
            )

            if response.status_code != 200:
                logger.error("Ollama returned status %s: %s", response.status_code, response.text[:500])
                raise GenerationError(f"LLM backend returned status {response.status_code}")

            data = response.json()

            if isinstance(data, dict) and "response" in data:
                return self._parse_response(data["response"])

            logger.error("Unexpected Ollama response shape: %s", data)
            raise GenerationError("LLM backend returned an unexpected response shape")

        except requests.exceptions.Timeout as e:
            logger.error("Request to Ollama timed out")
            raise GenerationError("The LLM backend timed out") from e
        except requests.exceptions.RequestException as e:
            logger.error("Request to Ollama failed: %s", e)
            raise GenerationError("Could not reach the LLM backend") from e

    @staticmethod
    def _parse_response(raw_text):
        text = raw_text.strip()
        if text.startswith("```"):
            text = text.strip("`").strip()
            if text.lower().startswith("json"):
                text = text[4:].strip()

        try:
            data = json.loads(text)
            return {
                "answer": str(data.get("answer", "")).strip(),
                "scope": data.get("scope", "in_scope"),
            }
        except (json.JSONDecodeError, AttributeError):
            logger.warning("LLM did not return valid JSON, using raw text as answer: %r", raw_text[:200])
            return {"answer": raw_text.strip(), "scope": "in_scope"}
