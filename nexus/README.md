# 🇳🇵 NyayaAI — AI Legal Assistant for Nepal

NyayaAI is a full-stack AI-powered legal assistant designed to help users understand Nepali laws in simple language using a Retrieval-Augmented Generation (RAG) system.

---

## 🚀 Live Features

### 🧠 AI Chat System
- Ask legal questions in natural language
- AI responds using relevant legal document chunks
- Context-aware responses using RAG pipeline

### 💬 Chat UI (React)
- ChatGPT-style interface
- User / AI message bubbles
- Sidebar with chat history
- Create, switch, rename, and delete conversations
- Persistent chat storage (localStorage)

### ⚙️ Backend (FastAPI)
- `/chat` endpoint for AI responses
- Document loader system
- Text chunking + embedding generation
- Cosine similarity-based retrieval system
- Context-based response generation

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
- NumPy

### AI System
- Retrieval-Augmented Generation (RAG)
- Vector similarity search
- Embedding-based document retrieval

---

## 🔄 System Architecture

User Query  
→ React Chat UI  
→ FastAPI `/chat`  
→ Embedding Generation  
→ Vector Similarity Search  
→ Top Legal Chunks Retrieved  
→ AI Response Generation  
→ Returned to Frontend  

---


