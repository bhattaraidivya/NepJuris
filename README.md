# NepJuris

**An offline-first, retrieval-grounded AI legal intelligence system for Nepali law.**

NepJuris is not a chatbot. It is a RAG-powered legal reasoning engine that retrieves context from a structured corpus of Nepali legal documents and generates responses grounded strictly in that retrieved content — no hallucinated statutes, no invented case law.

Built entirely with local infrastructure. No external APIs. No cloud dependency. Runs on a single `docker compose up`.

---

## The Problem

Nepal's legal system is inaccessible in practice. Primary legal documents — the Constitution, Civil Code, Criminal Code, Cyber Law, and Supreme Court decisions — exist as dense English PDFs scattered across government portals. For a law student, independent researcher, or citizen trying to understand their rights, there is no reliable way to query this corpus and get a grounded, citable answer.

General-purpose AI tools make this worse: they hallucinate statute numbers, invent provisions, and cite cases that don't exist. The problem isn't lack of AI — it's lack of *retrieval-grounded* AI trained on the actual documents.

NepJuris solves this by combining semantic retrieval over the real legal corpus with local LLM inference, enforcing a strict no-hallucination constraint at the prompt level.

---

## Corpus

NepJuris currently indexes the following documents (English PDFs):

| Document | Type |
|---|---|
| Constitution of Nepal 2015 | Constitutional Law |
| Civil Code of Nepal | Substantive Civil Law |
| Criminal Code of Nepal | Substantive Criminal Law |
| Cyber Law of Nepal | Regulatory / Digital Law |
| Supreme Court Landmark Decisions | Case Law / Precedent |

All documents are chunked, embedded, and indexed into a FAISS vector store at ingestion time.

---

## Architecture

```
User Query (Browser)
      ↓
React SPA — Nginx Container
      ↓
FastAPI Backend — RAG Engine
      ↓
FAISS Vector Store (local)
      ↓
SentenceTransformer Embeddings
      ↓
Context Formatter + Prompt Builder
      ↓
Ollama — LLaMA 3 8B (local inference)
      ↓
Retrieval-Grounded Legal Response
```

Every response is sourced from retrieved document chunks. The prompt explicitly prohibits the model from drawing on outside knowledge or fabricating legal references.

---

## Stack

**Frontend**
- React + Vite (SPA, served via Nginx)
- TypeScript — core chat domain, API contracts, state types
- Tailwind CSS + Framer Motion
- Multi-workspace chat system with persistent localStorage state

**Backend**
- FastAPI — REST API + RAG pipeline orchestration
- PyMuPDF — PDF ingestion and text extraction
- SentenceTransformers — document and query embedding
- FAISS — vector similarity search
- Prompt engineering layer — strict legal grounding constraints

**Inference**
- Ollama running LLaMA 3 8B — fully local, no external API calls

**Infrastructure**
- Docker Compose — four-service orchestration (frontend, backend, ollama, nginx)
- Nginx — reverse proxy, `/api/*` → FastAPI, `/` → React SPA
- Internal Docker network — all inter-service communication contained

---

## Key Engineering Decisions

**Why FAISS over a managed vector DB?**
NepJuris is designed to run entirely offline. A managed vector store (Pinecone, Weaviate) would require outbound network access, breaking the offline-first constraint. FAISS runs in-process with the FastAPI backend.

**Why local LLM (Ollama) over OpenAI/Anthropic API?**
Legal documents contain sensitive queries. Sending them to an external API violates the privacy-first design principle. Ollama runs LLaMA 3 8B entirely inside the Docker network — no query ever leaves the machine.

**Why strict retrieval grounding?**
Legal AI that hallucinates is worse than no legal AI. The system prompt explicitly instructs the model to refuse to answer if retrieved context is insufficient, rather than generate a plausible-sounding but unsupported response.

**TypeScript migration strategy**
TypeScript is applied selectively to data integrity layers: API contracts (`api.ts`), chat state (`chat.types.ts`), and the single source of truth (`contracts.ts`). Pure UI rendering components remain in JSX — typed where it prevents bugs, not for coverage metrics.

---

## Project Structure

```
nepjuris/
├── docker-compose.yml
├── nginx.conf
├── frontend/
│   ├── Dockerfile
│   ├── .env
│   ├── dist/                   # production build (Vite output, served by Nginx)
│   └── src/
│       ├── pages/          # Home.jsx · Chat.tsx · Docs.jsx
│       ├── components/
│       │   ├── chat/       # TypeScript-migrated core system
│       │   ├── home/
│       │   ├── docs/
│       │   ├── layout/
│       │   └── ui/
│       ├── hooks/
│       │   └── useChat.ts
│       ├── services/
│       │   └── api.ts
│       ├── core/
│       │   └── contracts.ts
│       └── types/
│           └── chat.types.ts
│
└── backend/
    ├── routes/
    │   ├── chat.py
    │   └── documents.py
    ├── services/
    │   └── chat_service.py
    ├── rag/
    │   ├── retriever.py
    │   ├── generator.py
    │   ├── context_formatter.py
    │   ├── embedder.py
    │   └── vector_store.py
    ├── pipeline/
    │   ├── extractor.py
    │   ├── chunker.py
    │   └── ingest.py
    └── main.py
    ├── Dockerfile
    ├── .env
```

---

## Running Locally

**Prerequisites:** Docker + Docker Compose

```bash
git clone https://github.com/bhattaridivya/nepjuris
cd nepjuris
docker compose up --build
```

The system automatically provisions all four containers and wires them over an internal Docker network. Open `http://localhost` when startup completes.

To ingest documents, place PDFs in the designated corpus directory and trigger the ingestion pipeline via the `/api/ingest` endpoint or the document management UI.

---

## Features

- **Multi-workspace chat** — independent sessions, each with persistent history
- **Retrieval-grounded responses** — every answer sourced from actual document chunks
- **Document browser** — metadata-aware corpus explorer with direct doc-to-chat interaction
- **No-hallucination enforcement** — prompt-level constraint refusing unsupported answers
- **Fully offline** — zero outbound network dependency after initial model pull

---

## What This Is (and Isn't)

NepJuris is a demonstration of production-grade RAG system design applied to a real-world legal accessibility problem in Nepal. It is not a substitute for legal counsel. It is a research and reference tool that grounds AI responses in primary legal sources.

---

*Built by [Divya Bhattarai]*
