# 📘 NepJuris — AI Legal Intelligence Platform

> A full-stack AI legal reasoning system for Nepali law powered by Retrieval-Augmented Generation (RAG) and a local LLM.

---

# ⚙️ Overview

NepJuris is a full-stack AI-powered legal intelligence workspace, designed to transform Nepalese legal documents into an interactive, searchable, and conversational knowledge system.

It is not a chatbot — it is a **retrieval-grounded legal reasoning platform**.

Users can:

* Query Nepali legal documents using natural language
* Interact with a RAG-powered AI system
* Browse a structured legal corpus
* Manage multiple persistent chat workspaces
* Receive responses grounded in retrieved legal context

---

# 🧠 Core System Architecture

## Backend (FastAPI)

* RESTful API architecture
* PDF ingestion using PyMuPDF
* Text chunking pipeline for legal documents
* SentenceTransformer embeddings
* FAISS vector similarity search
* RAG-based retrieval pipeline
* Local LLM inference via Ollama (Qwen 2.5)

---

## Frontend (React + Vite + TypeScript Hybrid)

* Workspace-based multi-chat system (not single-session chatbot)
* Persistent chat state using localStorage
* Multi-chat sidebar (create / rename / delete workspaces)
* ChatGPT-style floating input interface
* Document browsing system for legal corpus
* Modular component architecture (chat / home / docs / UI separation)
* TypeScript migration for core chat system (hooks, state, contracts)

---

# 📂 Key Features

## 🧩 Workspace Chat System

* Multiple independent chat sessions
* Persistent conversation history
* Rename and delete workspaces
* Automatic state persistence across sessions

---

## ⚖️ Legal Intelligence (RAG System)

* Nepal Constitution and legal corpus chunked and embedded
* FAISS-powered semantic retrieval
* Context-aware AI responses grounded in retrieved documents
* Local LLM inference (no external API dependency)

---

## 📚 Document Intelligence System

* Structured legal document browser
* Corpus-based navigation
* Direct AI interaction with legal documents
* Metadata-aware document organization

---

## 🎨 Frontend Experience

* Dark, cinematic UI inspired by modern AI tools
* Framer Motion animations for smooth interactions
* Responsive layout system
* Reusable UI primitives (Button, Card, Input, etc.)
* Clean separation of domain logic and UI components

---

# 🧱 System Architecture

```
User (React Frontend)
        ↓
FastAPI Backend
        ↓
FAISS Vector Database
        ↓
SentenceTransformer Embeddings
        ↓
Context Retrieval Layer
        ↓
Ollama (Qwen 2.5 Local LLM)
        ↓
RAG Response Generator
        ↓
Grounded Legal Answer
```

---

# 💻 Tech Stack

## Frontend

* React (Vite)
* TypeScript (partial migration for core system)
* Tailwind CSS
* React Router
* Framer Motion
* Custom Hooks (useChat architecture)

## Backend

* FastAPI
* PyMuPDF
* FAISS
* SentenceTransformers
* Ollama (local inference)

---

# 🧠 TypeScript Architecture (Current State)

NepJuris uses a **hybrid TypeScript migration strategy**:

### ✔ Fully Typed

* Chat state management (useChat)
* API layer (sendMessage)
* Core contracts (runtime + type system separation)
* Chat domain models

### ✔ Partially Typed (Intentional)

* UI components (stateless presentational components)
* Pages (light typing only)

### ✔ Design Principle

> Type safety is applied where data integrity matters (core + API), not where UI is deterministic.

---

# 📁 Project Structure

```
src/
├── components/
│   ├── chat/
│   ├── home/
│   ├── docs/
│   ├── layout/
│   └── ui/
│
├── pages/
│   ├── Chat.tsx
│   ├── Home.jsx
│   └── Docs.jsx
│
├── hooks/
│   └── useChat.ts
│
├── services/
│   └── api.ts
│
├── core/
│   └── contracts.ts
│
├── types/
│   └── chat.types.ts
│
├── design/
└── assets/
```

---

# 🖥 Backend Architecture

```
backend/
├── routes/
├── services/
├── pipeline/
│   ├── extractor.py
│   ├── chunker.py
│   └── ingest.py
├── rag/
|   |__context_formatter.py
|   |
│   ├── embedder.py
│   ├── retriever.py
│   ├── vector_store.py
│   └── generator.py
└── main.py
```

---

# 🧪 Current Status

* RAG pipeline fully functional
* FAISS vector search integrated
* Local LLM inference working (Ollama)
* Multi-chat workspace system complete
* Document ingestion pipeline complete
* Frontend architecture modularized
* TypeScript migration completed for core system

---

# 🖼 Assets / Screenshots

> UI screenshots demonstrating the system are available in:

```
/assets
```

Includes:

* Chat interface
* Document browser
* Home UI workflow
* RAG response examples

---

# 🚀 Future Improvements

* Dockerized deployment setup
* Authentication system
* Cloud vector database support
* Improved citation visualization in UI
* Multi-model switching support
* Advanced legal reasoning pipelines

---

# 🎯 What This Project Demonstrates

NepJuris demonstrates production-level AI engineering across multiple domains:

* Full-stack AI system design
* RAG architecture implementation
* Vector database integration (FAISS)
* Local LLM inference systems
* Scalable frontend architecture
* Type-safe state management (TypeScript)
* Real-world legal domain application

---

> NepJuris represents the evolution of a chatbot into a structured legal intelligence system — combining retrieval, reasoning, and interface design into a unified AI workspace.
