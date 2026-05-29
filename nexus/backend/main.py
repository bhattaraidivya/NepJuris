from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from rag.loader import load_documents
from rag.embedder import create_embedding
from rag.retriever import retrieve_top_chunks
from rag.responder import generate_response

def generate_title(message: str):
    words = message.split()

    stopwords = {
        "what", "is", "the", "a", "an", "how", "to", "in", "of", "about", "explain"
    }

    filtered = [w for w in words if w.lower() not in stopwords]

    title = " ".join(filtered[:6])

    return title.title() if title else "New Chat"

# -------------------------
# APP INIT
# -------------------------
app = FastAPI()

# -------------------------
# CORS SETUP
# -------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# LOAD DOCUMENTS ON START
# -------------------------
documents = load_documents()

# -------------------------
# REQUEST MODEL
# -------------------------
class ChatRequest(BaseModel):
    message: str

# -------------------------
# ROUTES
# -------------------------
@app.get("/")
def home():
    return {"message": "NyayaAI backend is running 🚀"}

@app.get("/documents")
def get_documents():
    return documents

@app.post("/chat")
def chat(req: ChatRequest):

    user_msg = req.message
    chat_title = generate_title(user_msg)

    # 1. Convert query to embedding
    query_embedding = create_embedding(user_msg)

    # 2. Retrieve top matching chunks
    results = retrieve_top_chunks(query_embedding, documents)

    # Safety check
    if not results:
        return {
            "response": "No relevant legal information found."
        }

    # 3. Combine top chunks
    top_chunks = [item["text"] for item in results]
    combined_text = "\n\n".join(top_chunks)

    # 4. Best score for confidence
    score = results[0]["score"]

    # 5. Generate final response
    response = generate_response(
        user_msg,
        combined_text,
        score
    )
  
   

    return {
        "response": response,
        "title": chat_title
       
    }