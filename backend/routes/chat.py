import logging
import os
from typing import Literal

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field

from rag.generator import GenerationError
from rag.retriever import RetrieverNotReadyError
from rate_limiter import limiter
from services.chat_service import ChatService

logger = logging.getLogger(__name__)

router = APIRouter()

chat_service = ChatService()

CHAT_RATE_LIMIT = os.getenv("CHAT_RATE_LIMIT", "10/minute")


class ChatTurn(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(..., min_length=1, max_length=2000)


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)
    # Client-held conversation history — the backend has no session store,
    # so the frontend resends recent turns with each request.
    history: list[ChatTurn] = Field(default_factory=list, max_length=20)


@router.post("/chat")
@limiter.limit(CHAT_RATE_LIMIT)
def chat(request: Request, payload: ChatRequest):
    message = payload.message.strip()
    if not message:
        raise HTTPException(status_code=400, detail="Message cannot be empty.")

    history = [turn.model_dump() for turn in payload.history]

    try:
        return chat_service.generate_response(message, history)

    except RetrieverNotReadyError as e:
        logger.error("Retriever not ready: %s", e)
        raise HTTPException(
            status_code=503,
            detail="The document index isn't loaded yet. Try again shortly, or ingest documents first.",
        ) from e

    except GenerationError as e:
        logger.error("Generation failed: %s", e)
        raise HTTPException(
            status_code=502,
            detail="The AI model couldn't generate a response. Please try again.",
        ) from e

    except Exception:
        logger.exception("Unexpected error handling chat request")
        raise HTTPException(status_code=500, detail="Something went wrong processing your request.")
