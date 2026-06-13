# NepJuris — Project State

> Internal engineering reference. Tracks what is built, what works, what is intentionally deferred, and what comes next.

---

## Current Status: Fully Operational

All core systems are containerized and running end-to-end. A single `docker compose up --build` provisions the full stack.

| Layer | Status | Notes |
|---|---|---|
| React Frontend (Vite) | ✅ Operational | Served via Nginx container |
| FastAPI Backend | ✅ Operational | Dockerized, all routes responding |
| RAG Pipeline | ✅ Operational | Retrieval → context → generation working |
| FAISS Vector Store | ✅ Operational | Indexed, stable retrieval |
| Ollama (LLaMA 3 8B) | ✅ Operational | Local inference via Docker network |
| Nginx Reverse Proxy | ✅ Configured | `/api/*` → backend, `/` → SPA |
| Multi-workspace Chat | ✅ Operational | Persistent state via localStorage |
| Document Browser | ✅ Operational | Corpus browsable, doc-to-chat linked |
| TypeScript Migration | 🔄 Partial | Core domain complete, UI pages intentionally deferred |
| Performance Metrics | ⏳ Not yet measured | Benchmarking planned |

---

## Corpus

**Indexed documents (English PDFs):**

- Constitution of Nepal 2015
- Civil Code of Nepal
- Criminal Code of Nepal
- Cyber Law of Nepal
- Supreme Court Landmark Decisions

All five documents are chunked, embedded via SentenceTransformers, and indexed in the FAISS vector store.

**Chunking strategy:** Chunk size and overlap not yet formally benchmarked. Current values are functional but unoptimized — this is a known gap.

---

## RAG Pipeline — Implementation Detail

```
Ingest:
  PDF → PyMuPDF extraction → text chunker → SentenceTransformer embedding → FAISS index

Query:
  User input → embedding → FAISS top-k retrieval → context formatter →
  prompt builder (with legal grounding constraints) → Ollama /api/generate →
  structured response
```

**Grounding enforcement:** The system prompt instructs the model to answer only from retrieved context and to explicitly decline when context is insufficient. This is enforced at the prompt level, not the model level — it is strong but not absolute.

**Model:** LLaMA 3 8B via Ollama. Chosen for its balance of instruction-following quality and hardware accessibility (runs on consumer GPU or CPU-only).

---

## Docker Architecture

**Services:**

| Service | Image | Role |
|---|---|---|
| `frontend` | Custom (Node + Nginx) | Builds React SPA, serves via Nginx |
| `backend` | Custom (Python 3.11) | FastAPI + RAG pipeline |
| `ollama` | `ollama/ollama` | Local LLM inference runtime |
| `nginx` | `nginx:alpine` | Reverse proxy, unified routing |

**Networking:** All services communicate over an internal Docker bridge network. The backend reaches Ollama at `http://ollama:11434` — not `localhost`, which was a resolved integration issue (see Engineering Challenges below).

---

## TypeScript Migration State

**Philosophy:** Type safety applied where it prevents real bugs — data contracts, state machines, API boundaries. Not applied to pure rendering components where types add ceremony without benefit.

**Fully typed:**
- `api.ts` — all backend communication
- `chat.types.ts` — message, workspace, and session types
- `contracts.ts` — single source of truth for shared data shapes
- `useChat.ts` — chat state hook
- `Chat.tsx` — main chat page

**Intentionally deferred:**
- `Home.jsx` — static marketing page, no state
- `Docs.jsx` — document browser, lightweight interaction
- Pure UI components — buttons, layout wrappers, animations

---

## Engineering Challenges Resolved

**Ollama container networking**
The backend initially called `http://localhost:11434` which resolves to the backend container itself, not Ollama. Fixed by using the Docker service name: `http://ollama:11434`. A subtle but critical Docker networking issue.

**Nginx 502/504 gateway errors**
Initial proxy configuration did not correctly route `/api/` prefixed requests to the FastAPI backend. Resolved by correcting `proxy_pass` directives and ensuring upstream service names matched Docker Compose service definitions.

**`import.meta.env` in Vite + TypeScript**
Environment variable access broke during TypeScript migration. Fixed by adding proper `vite-env.d.ts` type declarations and aligning variable naming to Vite's `VITE_` prefix convention.

**`python-dotenv` dependency**
Backend container failed on startup due to missing `python-dotenv`. Resolved by adding it to `requirements.txt` and rebuilding the image.

---

## Known Gaps

| Gap | Priority | Notes |
|---|---|---|
| No chunking benchmarks | Medium | Chunk size/overlap chosen empirically, not optimized |
| No retrieval accuracy metrics | Medium | No ground-truth eval set exists yet |
| No response latency profiling | Low | LLaMA 3 8B on CPU is slow; not yet measured |
| No auth layer | Low | Single-user local tool, auth not in scope |
| Corpus limited to English | Medium | Nepali-language documents excluded; no Nepali embedding model integrated |
| localStorage only | Low | Chat history lost on browser clear; no backend persistence |

---

## Planned Work

- [ ] Chunk size / overlap benchmarking against retrieval recall
- [ ] Build a small eval set of legal Q&A pairs for retrieval accuracy measurement
- [ ] Response latency profiling — GPU vs CPU inference
- [ ] Expand corpus: add more acts and regulations
- [ ] Explore Nepali-language document support (requires multilingual embedding model)
- [ ] Backend-persisted chat history (replace localStorage with database)
- [ ] Citation rendering in UI — surface which document chunk grounded each response

---

## Design Principles (Enforced)

1. **Retrieval-first** — the model cannot answer without retrieved context
2. **Offline-first** — no outbound network calls after initial setup
3. **Privacy-preserving** — legal queries never leave the local machine
4. **Strict separation of concerns** — UI / API / inference / retrieval are independent layers
5. **Type safety where it matters** — contracts and state machines, not UI boilerplate

---

*Last updated: June 2025*
