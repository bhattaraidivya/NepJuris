from fastapi import APIRouter
from pydantic import BaseModel
from services.chat_service import ChatService

router = APIRouter()

chat_service = ChatService()



class ChatRequest(BaseModel):
    message: str


@router.post("/chat")
def chat(request: ChatRequest):
    try:
        response = chat_service.generate_response(request.message)
        return {"response": response}

    except Exception as e:
        return {"error": str(e)}