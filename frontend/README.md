# 📘 NepJuris

AI Legal Workspace for Nepali Law powered by RAG + Local LLM

---

# ⚙️ Overview

NepJuris is a full-stack AI legal workspace, not a chatbot.

It enables users to:
- Query Nepali legal documents
- Interact with a RAG-based AI system
- Browse a structured legal knowledge base
- Manage multiple conversation workspaces
- Get AI responses grounded in real legal corpus

---

# 🧠 Core System

## Backend (FastAPI)
- REST API server
- PDF ingestion using PyMuPDF
- Text chunking pipeline
- SentenceTransformer embeddings
- FAISS vector database
- RAG-based retrieval system
- Local LLM integration via Ollama (Qwen 2.5)

---

## Frontend (React + Vite)
- Workspace-based chat system (not single chatbot)
- Multi-chat sidebar (create / rename / delete)
- Persistent chat storage (localStorage)
- Floating ChatGPT-style input UI
- Document browsing interface
- Modular component architecture

---

# 📂 Features

## 🧩 Workspace System
- Multiple independent chats
- Persistent chat history
- Rename / delete workspaces
- Auto-save state

## ⚖️ Legal Intelligence
- Nepal Constitution chunked & embedded
- RAG-based context retrieval
- Legal-grounded AI responses

## 📚 Document System
- Browse legal document corpus
- Download original PDFs
- Ask AI directly from document context

---

# 🧱 Architecture

User (React UI)
   ↓
FastAPI Backend
   ↓
FAISS Vector Store
   ↓
SentenceTransformer Embeddings
   ↓
Ollama (Qwen 2.5 Local LLM)
   ↓
RAG Response Engine

---

# 💻 Tech Stack

## Frontend
- React (Vite)
- Tailwind CSS
- React Router
- Custom Hooks (useChat)

## Backend
- FastAPI
- PyMuPDF
- FAISS
- SentenceTransformers
- Ollama

---

# Backend Setup
cd backend
python -m venv .venv
.\.venv\Scripts\activate   # Windows
pip install -r requirements.txt
uvicorn main:app --reload

---

# Frontend Setup
cd frontend
npm install
npm run dev

---

# Local LLM Setup
Install Ollama: https://ollama.ai
ollama pull qwen2.5
ollama run qwen2.5

---

# Current Status
- RAG pipeline working
- FAISS vector search integrated
- Chat workspace system complete
- Document ingestion complete
- UI refactored

---

# Future Improvements
- Docker support
- Authentication system
- Cloud vector DB option
- Better legal citation         formatting
- Multi-model switching support

---

# Requirements
- Python 3.10+
- Node.js
- Ollama (for local LLM)