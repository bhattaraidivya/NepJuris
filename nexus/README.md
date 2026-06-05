# 🇳🇵 NyayaAI — AI Legal Assistant for Nepal

NyayaAI is a full-stack AI-powered legal assistant designed to help users understand Nepali laws in simple language using a Retrieval-Augmented Generation (RAG) system.

It combines document embeddings, FAISS vector search, and a local LLM (Ollama) to deliver context-aware legal responses.

---

## 🚀 Live Features

### 🧠 AI Chat System (RAG-based)
- Ask legal questions in natural language
- Answers grounded in Nepali legal documents
- Retrieval-Augmented Generation (RAG) pipeline
- FAISS-based semantic search for relevant context
- Local LLM (Ollama - Qwen 2.5) for response generation

---

### 💬 Chat UI (React)
- ChatGPT-style interface
- User / AI message bubbles
- Sidebar with chat history
- Create, switch, rename, and delete conversations
- Typing indicator (AI response loading state)
- Persistent chat storage using localStorage
- Modular component-based architecture

---

### ⚙️ Backend (FastAPI + RAG Pipeline)
- `/chat` endpoint for AI responses
- Document ingestion pipeline (PDF → text extraction)
- Text chunking system for semantic segmentation
- SentenceTransformer embeddings generation
- FAISS vector database for similarity search
- Context-aware response generation using LLM

---

## 🧱 Tech Stack

### Frontend
- React (Vite)
- TailwindCSS
- JavaScript
- React Hooks (useState, useEffect, useRef)

### Backend
- FastAPI
- Python
- Sentence Transformers
- FAISS (Vector Database)
- NumPy

### AI System
- Retrieval-Augmented Generation (RAG)
- Local LLM via Ollama (Qwen 2.5 3B)
- Semantic vector search
- Embedding-based document retrieval

---

## 🔄 System Architecture

User Query  
→ React Chat UI  
→ FastAPI `/chat` endpoint  
→ Query Embedding Generation  
→ FAISS Vector Similarity Search  
→ Relevant Legal Chunks Retrieved  
→ Context + Query sent to LLM (Ollama)  
→ AI Response Generated  
→ Returned to Frontend  
→ UI updates chat window  

---

