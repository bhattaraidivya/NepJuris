from fastapi import FastAPI
from pydantic import BaseModel

from rag.generator import Generator
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize generator ONCE (important)
generator = Generator()
generator.retriever.load()


# Request schema
class ChatRequest(BaseModel):
    message: str


@app.post("/chat")
def chat(request: ChatRequest):
    query = request.message

    try:
        response = generator.generate(query)
        return {
            "response": response
        }

    except Exception as e:
        return {
            "error": str(e)
        }