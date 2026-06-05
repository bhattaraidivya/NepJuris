# 🇳🇵 NepJuris — AI Legal Intelligence Platform

> A production-grade, full-stack AI legal reasoning system for Nepal.
> Built with RAG, FAISS, local LLM inference, and a premium React frontend.

---

## 🟢 Project Status: Complete

| Layer | Status |
|---|---|
| Frontend | ✅ Complete |
| Backend | ✅ Complete |
| RAG Pipeline | ✅ Active |
| AI System | ✅ Functional |
| Design System | ✅ Finalized |

---

## 🧠 What NepJuris Is

NepJuris is a full-stack AI-powered legal intelligence platform for Nepal, built on Retrieval-Augmented Generation (RAG).

It transforms Nepalese legal documents — constitutions, civil codes, criminal procedure acts — into a searchable, explainable, and conversational legal intelligence system using semantic retrieval, vector databases, and local LLM reasoning.

It is not a chatbot. It is a legal reasoning platform.

---

## 🏗 System Architecture

### Frontend — React + Vite

```
src/
├── pages/
│   ├── Home.jsx
│   ├── Chat.jsx
│   └── Docs.jsx
│
├── components/
│   ├── chat/
│   │   ├── Sidebar.jsx
│   │   ├── ChatArea.jsx
│   │   ├── ChatBox.jsx
│   │   ├── Message.jsx
│   │   └── InputBox.jsx
│   │
│   ├── home/
│   │   ├── Hero.jsx
│   │   ├── Workflow.jsx
│   │   ├── Features.jsx
│   │   └── CorpusPreview.jsx
│   │
│   ├── docs/
│   │   └── DocumentCard.jsx
│   │
│   ├── layout/
│   │   ├── Navbar.jsx
│   │   └── Footer.jsx
│   │
│   └── ui/
│       ├── Button.jsx
│       ├── Card.jsx
│       ├── Badge.jsx
│       ├── Input.jsx
│       ├── Section.jsx
│       └── Container.jsx
│
├── hooks/
│   └── useChat.js
│
├── services/
│   └── api.js
│
├── design/
│   ├── colors.js
│   ├── typography.js
│   ├── spacing.js
│   └── layout.js
│
└── core/
    ├── contracts.js
    └── apiContract.js
```

### Backend — FastAPI

```
backend/
├── main.py
│
├── routes/
│   ├── chat.py
│   └── documents.py
│
├── services/
│   ├── chat_service.py
│   └── document_service.py
│
├── pipeline/
│   ├── extractor.py
│   ├── chunker.py
│   └── ingest.py
│
├── rag/
│   ├── embedder.py
│   ├── vector_store.py
│   ├── retriever.py
│   └── generator.py
│
└── data/
    ├── raw/
    ├── processed/
    ├── chunks/
    ├── embeddings/
    └── data_catalog.json
```

---

## ⚙ Backend — 3-Layer Architecture

### 1. Routes Layer
HTTP endpoints, request handling, response serialization. Zero business logic.

### 2. Services Layer
Chat orchestration, document operations, business workflows, file resolution.

### 3. RAG Layer
Embedding generation, FAISS retrieval, context construction, LLM generation.

---

## 🧠 RAG Pipeline

```
User Query
    ↓
SentenceTransformer Embedding
    ↓
FAISS Vector Search
    ↓
Top-K Legal Chunks Retrieved
    ↓
Context Builder
    ↓
Qwen via Ollama (Local LLM)
    ↓
Retrieval-Grounded Legal Response
```

---

## 🎨 Frontend Design System

A fully centralized, reusable UI architecture built with design tokens and shared primitives — consistent across all pages.

**Design Tokens:** Typography scale, color system, spacing system, layout containers

**UI Primitives:** Button, Card, Badge, Input, Section, Container

**Visual Identity:** Dark cinematic legal-tech aesthetic inspired by Harvey AI — premium, minimal, purposeful.

---

## 🖥 Completed Pages

### Home
Full-screen immersive hero with animated legal-tech marquee, AI workflow visualization with Framer Motion, feature showcase, legal corpus preview stream, and premium Harvey-style footer.

### Chat
Multi-conversation sidebar, LocalStorage-persisted chat history, centered message layout, real-time RAG query interface, loading states.

### Docs
Legal document browser with document cards, corpus catalog integration, document metadata display.

---

## ✅ Completed Features

### Frontend
- Modular component architecture with separation of concerns
- Multi-chat system with sidebar conversation management
- LocalStorage persistence across sessions
- Reusable design token system
- Framer Motion animations throughout
- Premium dark UI — cinematic legal-tech aesthetic
- Animated marquee with seamless infinite loop
- Responsive layout system
- Document browsing and catalog interface

### Backend
- FastAPI modular 3-layer architecture
- PDF ingestion pipeline via PyMuPDF
- Intelligent text chunking system
- SentenceTransformer semantic embeddings
- FAISS vector index with metadata
- Document catalog system (data_catalog.json)
- Ollama integration with local Qwen inference
- Retrieval-grounded response generation

### AI System
- Fully functional end-to-end RAG pipeline
- Semantic legal document retrieval
- Context-aware legal reasoning
- Local inference — no external API dependency
- Nepal legal corpus indexed and searchable

---

## 🚀 Future Roadmap

### AI Enhancements
- Multi-turn conversation memory
- Citation-aware generation with source linking
- Nepali + English bilingual reasoning
- Legal summarization system
- Context-aware follow-up handling

### Product Features
- Ask AI directly from Docs page
- Advanced legal explorer
- Case law search engine
- OCR ingestion for scanned documents
- Admin upload dashboard
- Citation graph and legal knowledge relationships

### Infrastructure
- Dockerized deployment
- Cloud infrastructure (AWS / GCP)
- CI/CD pipeline
- Authentication system
- SaaS-ready multi-tenant architecture

---

## 🎯 What This Project Demonstrates

NepJuris was built to demonstrate production-grade AI engineering — not tutorial-level knowledge.

| Capability | Evidence |
|---|---|
| RAG system design | End-to-end pipeline from PDF to response |
| NLP for low-resource languages | Nepali legal corpus, multilingual reasoning |
| Full-stack AI development | React frontend + FastAPI backend + local LLM |
| Software architecture | 3-layer backend, modular frontend, design system |
| Product thinking | Harvey AI-inspired UX, complete user flows |
| Real-world application | Solves an actual problem in the Nepali legal space |

---

> NepJuris evolved from an AI chatbot project into a complete legal intelligence platform —
> a retrieval-first reasoning system built for production, designed for impact.
