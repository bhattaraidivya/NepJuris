import logging
from typing import Literal

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from rag.generator import GenerationError
from rag.retriever import RetrieverNotReadyError
from services.chat_service import ChatService

logger = logging.getLogger(__name__)

router = APIRouter()

chat_service = ChatService()


class ChatTurn(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(..., min_length=1, max_length=2000)


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)
    # Client-held conversation history — the backend has no session store,
    # so the frontend resends recent turns with each request.
    history: list[ChatTurn] = Field(default_factory=list, max_length=20)


@router.post("/chat")
def chat(request: ChatRequest):
    message = request.message.strip()
    if not message:
        raise HTTPException(status_code=400, detail="Message cannot be empty.")

    history = [turn.model_dump() for turn in request.history]

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
