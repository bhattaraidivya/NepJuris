# 🇳🇵 NyayaAI — Project State

## 📌 Overview
NyayaAI is an AI-powered legal assistant platform designed for Nepal.  
It combines a modern web frontend with a Retrieval-Augmented Generation (RAG) backend to provide legal explanations in English and Nepali.

---

## 🚀 Current Stage: MVP (v0.1)

The system is currently a **working minimum viable product** with core AI chat functionality fully functional.

---

## 🧠 Core Features Implemented

### 🟢 Backend (FastAPI + RAG)
- FastAPI server running successfully
- `/chat` endpoint implemented
- Document loading system
- Text chunking + embedding generation
- Cosine similarity-based retrieval system
- Returns relevant legal context with confidence score

---

### 🟢 Frontend (React + Vite)
- React application initialized with routing
- Clean page-based architecture:
  - Home page
  - Chat page
- Chat UI implemented with:
  - Message bubbles (user + AI)
  - Input box
  - Message history state management
- API integration with backend via fetch

---

### 🟢 AI System (RAG Pipeline)
- User query converted to embeddings
- Similarity search against document chunks
- Top relevant legal chunk retrieved
- Response generated using retrieved context

---

## 🧪 Working Flow

User Input → React Chat UI → FastAPI `/chat`  
→ Embedding generation → Vector similarity search  
→ Best legal chunk retrieved → AI response returned  
→ Rendered in chat interface

---

## ⚙️ Tech Stack

### Frontend
- React (Vite)
- React Router
- TailwindCSS (UI styling)

### Backend
- FastAPI
- Python
- NumPy
- Embedding model (custom or API-based)

### AI Layer
- RAG (Retrieval Augmented Generation)
- Cosine similarity search
- Document chunking system

---

## 📂 Current Pages

- `/` → Landing page (Home)
- `/chat` → AI Legal Assistant

---

## 🧱 Current Limitations

- No news system yet
- No documents UI page yet
- No multilingual support implemented
- UI is functional but not fully polished
- No persistent chat history

---

## 🎯 Next Development Phase

### Phase 2 (Frontend Expansion)
- Improve Home page (SaaS-level UI)
- Add Legal News page
- Add Documents/Resources page
- Improve navigation system

### Phase 3 (AI Enhancements)
- Nepali language support
- Better retrieval ranking
- Citation-based responses
- Memory for chat sessions

---

## 🧭 Vision

To build a **Nepal-focused AI legal-tech platform** that:
- explains laws in simple language
- supports English + Nepali
- provides structured legal knowledge access
- demonstrates real-world AI + full-stack engineering

---

## 📌 Current Status Summary

✔ Chat system working  
✔ Backend + frontend connected  
✔ RAG pipeline functional  
⚠ UI needs refinement  
⚠ Product pages not built yet  

---

## 🏁 Milestone Tag

v0.1-mvp — Working AI Chat System