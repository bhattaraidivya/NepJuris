import logging
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

from routes.chat import router as chat_router  # noqa: E402
from routes.documents import router as docs_router  # noqa: E402

app = FastAPI(title="NepJuris API")

DEFAULT_ORIGINS = "http://localhost:5173,http://localhost"
allowed_origins = [
    origin.strip()
    for origin in os.getenv("ALLOWED_ORIGINS", DEFAULT_ORIGINS).split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# register routes
app.include_router(chat_router)
app.include_router(docs_router)


@app.get("/health")
def health():
    """Liveness probe used by the Docker healthcheck."""
    return {"status": "ok"}