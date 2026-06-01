# 🇳🇵 NyayaAI — AI Legal Assistant

## Project Overview

NyayaAI is an AI-powered legal assistant designed for Nepal. The goal is to provide legal information and guidance through Retrieval-Augmented Generation (RAG) using Nepalese legal documents such as the Constitution, Civil Code, Criminal Code, Acts, Regulations, and Court Decisions.

The project is being developed as a portfolio-grade AI + Full Stack application demonstrating:

* Modern React Frontend Architecture
* FastAPI Backend Development
* Retrieval-Augmented Generation (RAG)
* Vector Databases (FAISS)
* Local LLM Integration
* AI System Design
* Scalable Software Architecture

---

# Current Development Stage

## Completed

### Frontend MVP

* React + Vite setup
* Chat interface
* Sidebar conversation management
* Chat history persistence (localStorage)
* Rename conversations
* Delete conversations
* Typing indicator
* Auto-scroll
* API integration layer

### Data Engine

* PDF document collection
* Metadata catalog system
* PDF text extraction (PyMuPDF)
* Text chunking pipeline
* Multi-document ingestion
* Document categorization

### Embedding Pipeline

* SentenceTransformer integration
* Chunk embedding generation
* Multi-document processing

### Vector Database

* FAISS integration
* Vector indexing
* Metadata storage
* Persistent vector database

### Retrieval Engine

* Query embedding generation
* Semantic similarity search
* Top-k chunk retrieval
* Multi-document retrieval

---

# In Progress

### Generation Layer

Planned architecture:

User Query
→ Retriever
→ Top Relevant Chunks
→ Context Builder
→ Local LLM (Qwen)
→ Final Answer

---

# Planned Features

## AI Features

### Version 1

* Local LLM integration
* RAG answer generation
* Source-grounded responses

### Version 2

* Conversational memory
* Follow-up question support
* Context-aware conversations

### Version 3

* Nepali language support
* English ↔ Nepali legal understanding
* Multilingual retrieval

### Version 4

* Fine-tuned legal model
* Nepal-specific legal reasoning
* Legal summarization

---

# Backend Architecture

backend/

├── main.py

├── pipeline/
│   ├── extractor.py
│   ├── chunker.py
│   └── ingest.py

├── rag/
│   ├── embedder.py
│   ├── vector_store.py
│   └── retriever.py

├── data/
│   ├── raw/
│   ├── embeddings/
│   └── data_catalog.json

└── documents/

---

# Frontend Architecture

frontend/

├── src/
│
├── pages/
│   ├── Home.jsx
│   └── Chat.jsx
│
├── components/
│   ├── Sidebar.jsx
│   ├── ChatBox.jsx
│   ├── Message.jsx
│   ├── InputBox.jsx
│   ├── Navbar.jsx
│   └── Features.jsx
│
├── services/
│   └── api.js
│
├── hooks/
│   └── useChat.js 
│
└── core/
├── contracts.js
└── apicontract.js

---

# Current RAG Pipeline

PDF Documents
→ Extraction
→ Chunking
→ SentenceTransformer Embeddings
→ FAISS Index

User Query
→ Query Embedding
→ FAISS Retrieval
→ Top-k Relevant Chunks

(Generation Layer In Progress)

---

# Target Architecture

User
↓
React Frontend
↓
FastAPI API
↓
Retriever
↓
FAISS Vector Database
↓
Relevant Legal Chunks
↓
Context Builder
↓
Local LLM (Qwen)
↓
AI Response
↓
Frontend Chat Interface

---

# Future Modules

* Legal Document Explorer
* Admin Dashboard
* News Section
* OCR Pipeline
* Case Law Search
* Legal Citation System
* User Accounts
* Document Upload System

---

# Technology Stack

Frontend

* React
* Vite
* TailwindCSS

Backend

* FastAPI
* Python

AI

* SentenceTransformers
* FAISS
* Retrieval-Augmented Generation
* Local LLM (Planned)

Database

* FAISS Vector Store
* Metadata Storage

Deployment (Planned)

* Docker
* Cloud Deployment
* CI/CD Pipeline
