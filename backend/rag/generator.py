import logging
import os

import requests

from rag.context_formatter import format_context

logger = logging.getLogger(__name__)

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant").strip()
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash").strip()
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"

REQUEST_TIMEOUT = 30

SYSTEM_PROMPT = """You are NepJuris, a retrieval-based legal assistant for Nepal.

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
"""

USER_PROMPT_TEMPLATE = """# CONTEXT
{context}

---

# QUESTION
{question}

---

# RESPONSE:
"""


class GenerationError(Exception):
    """Raised when no configured LLM backend can produce a response."""


class Generator:
    """Builds prompts from retrieved context and calls a hosted LLM API
    (Groq primary, Gemini fallback) to generate answers."""

    def build_prompt(self, query, contexts):
        context_text = format_context(contexts)
        return USER_PROMPT_TEMPLATE.format(context=context_text, question=query)

    def generate(self, query, contexts):
        user_prompt = self.build_prompt(query, contexts)

        try:
            return self._call_groq(user_prompt)
        except Exception as groq_error:
            logger.warning("Groq generation failed, falling back to Gemini: %s", groq_error)

        try:
            return self._call_gemini(user_prompt)
        except Exception as gemini_error:
            logger.error("Gemini fallback also failed: %s", gemini_error)
            raise GenerationError("Could not reach any configured LLM backend") from gemini_error

    def _call_groq(self, user_prompt):
        if not GROQ_API_KEY:
            raise GenerationError("GROQ_API_KEY is not configured")

        response = requests.post(
            GROQ_URL,
            headers={"Authorization": f"Bearer {GROQ_API_KEY}"},
            json={
                "model": GROQ_MODEL,
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt},
                ],
                "temperature": 0.3,
            },
            timeout=REQUEST_TIMEOUT,
        )

        if response.status_code != 200:
            raise GenerationError(f"Groq returned status {response.status_code}: {response.text[:300]}")

        data = response.json()
        try:
            return data["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as e:
            raise GenerationError(f"Unexpected Groq response shape: {data}") from e

    def _call_gemini(self, user_prompt):
        if not GEMINI_API_KEY:
            raise GenerationError("GEMINI_API_KEY is not configured")

        url = GEMINI_URL.format(model=GEMINI_MODEL)
        response = requests.post(
            url,
            params={"key": GEMINI_API_KEY},
            json={
                "contents": [{"parts": [{"text": f"{SYSTEM_PROMPT}\n\n{user_prompt}"}]}],
                "generationConfig": {"temperature": 0.3},
            },
            timeout=REQUEST_TIMEOUT,
        )

        if response.status_code != 200:
            raise GenerationError(f"Gemini returned status {response.status_code}: {response.text[:300]}")

        data = response.json()
        try:
            return data["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError, TypeError) as e:
            raise GenerationError(f"Unexpected Gemini response shape: {data}") from e
