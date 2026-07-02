import json
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

# Number of prior turns (user + assistant messages combined) sent with each
# request. The frontend keeps full history client-side; the backend stays
# stateless and just trusts the last N turns it's handed each call.
MAX_HISTORY_MESSAGES = int(os.getenv("MAX_HISTORY_MESSAGES", "6"))

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

    def generate(self, query, contexts, history=None):
        """Returns {"answer": str, "scope": "greeting"|"in_scope"|"out_of_scope"}.

        history is an ordered list of {"role": "user"|"assistant", "content": str}
        prior turns, oldest first; only the most recent MAX_HISTORY_MESSAGES are used.
        """
        user_prompt = self.build_prompt(query, contexts)
        history = (history or [])[-MAX_HISTORY_MESSAGES:]

        try:
            raw = self._call_groq(user_prompt, history)
        except Exception as groq_error:
            logger.warning("Groq generation failed, falling back to Gemini: %s", groq_error)

            try:
                raw = self._call_gemini(user_prompt, history)
            except Exception as gemini_error:
                logger.error("Gemini fallback also failed: %s", gemini_error)
                raise GenerationError("Could not reach any configured LLM backend") from gemini_error

        return self._parse_response(raw)

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

    def _call_groq(self, user_prompt, history):
        if not GROQ_API_KEY:
            raise GenerationError("GROQ_API_KEY is not configured")

        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        for turn in history:
            role = "assistant" if turn.get("role") == "assistant" else "user"
            messages.append({"role": role, "content": turn.get("content", "")})
        messages.append({"role": "user", "content": user_prompt})

        response = requests.post(
            GROQ_URL,
            headers={"Authorization": f"Bearer {GROQ_API_KEY}"},
            json={
                "model": GROQ_MODEL,
                "messages": messages,
                "temperature": 0.3,
                "response_format": {"type": "json_object"},
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

    def _call_gemini(self, user_prompt, history):
        if not GEMINI_API_KEY:
            raise GenerationError("GEMINI_API_KEY is not configured")

        contents = []
        for turn in history:
            role = "model" if turn.get("role") == "assistant" else "user"
            contents.append({"role": role, "parts": [{"text": turn.get("content", "")}]})
        contents.append({"role": "user", "parts": [{"text": user_prompt}]})

        url = GEMINI_URL.format(model=GEMINI_MODEL)
        response = requests.post(
            url,
            params={"key": GEMINI_API_KEY},
            json={
                "systemInstruction": {"parts": [{"text": SYSTEM_PROMPT}]},
                "contents": contents,
                "generationConfig": {"temperature": 0.3, "responseMimeType": "application/json"},
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
