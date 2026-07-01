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
| Citation Metadata (page numbers) | ✅ Operational | Page-level citation added June 2026; article/section detection still deferred |
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
  PDF → PyMuPDF extraction (page-aware, header/footer stripped) →
  sentence-aware chunker (page-aware) → SentenceTransformer embedding →
  FAISS index

Query:
  User input → embedding → FAISS top-k retrieval → context formatter
  (with page citation) → prompt builder (with legal grounding constraints) →
  Ollama /api/generate → structured response
```

**Grounding enforcement:** The system prompt instructs the model to answer only from retrieved context and to explicitly decline when context is insufficient. This is enforced at the prompt level, not the model level — it is strong but not absolute.

**Model:** qwen 2.5:3b via Ollama. Chosen for its balance of instruction-following quality and hardware accessibility (runs on consumer GPU or CPU-only).

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

## Citation Pipeline Fix (June 2026)

**Problem found:** Despite `format_context` supporting `page`, `section`, and `article`
citation fields, every chunk's metadata had these fields hardcoded to `None`. Root cause
traced through three layers:

1. `extractor.py` flattened all PDF pages into a single string with no page markers,
   discarding page boundaries immediately after `fitz` extraction.
2. `chunker.py` did pure character-offset sliding-window chunking with no page awareness.
3. `ingest.py` read `page`/`section`/`article` from the document-level catalog entry
   (`doc.get("page")`) instead of per-chunk data — which doesn't exist at the document
   level in the first place.

**Fix:** `extractor.py` now embeds `<<<PAGE:N>>>` markers between pages before joining.
`chunker.py` parses these markers to compute `page_start`/`page_end` per chunk, then
strips them before returning chunk text. `ingest.py` now builds a `page` label
(`"12"` or `"12-13"` for chunks spanning multiple pages) from this data.

**Result:** Citations now show real page numbers per chunk. Verified via manual spot
checks across Criminal Law and Supreme Court documents — correct, plausible pages
returned consistently.

**Still deferred:** `article` and `section` remain `None`. Populating these requires
parsing legal structure (e.g. detecting "Article 12" as a heading) from raw extracted
text — a separate, larger task, not yet started.

**Side finding — retrieval, not a bug:** Query expansion (`_expand_query`) was removed
from `Retriever`. It used exact-match lookup against ~8 hardcoded keywords, which meant
it only fired when a query was *exactly* one keyword (e.g. literally `"citizenship"`)
and silently did nothing for any real natural-language question. Replaced with raw
query embedding — SentenceTransformer models handle full sentences natively. No
measured retrieval-quality regression found in manual spot checks; formal comparison
deferred to the eval set (below).

**Open product question (not yet resolved):** A spot check on "What are the fundamental
rights in the constitution?" returned all top-5 chunks from *Supreme Court Landmark
Decision*, none from *Constitution of Nepal* — because the court ruling discusses and
quotes constitutional rights articles extensively (Art. 12, 13, 28, 32). Retrieval is
semantically correct, but a user naming "the constitution" explicitly may expect
primary-source text over case-law commentary. Whether to bias retrieval toward
named/primary sources is an open design question, to be informed by eval results
rather than decided ad hoc.

---

## Chunking Quality Fix (June 2026)

**Problem found:** Manual inspection of retrieved chunks during eval testing surfaced
badly degraded chunk text — mid-word cuts, repeated page headers and case-name lines
bleeding into body text, and stray standalone page numbers (e.g. a lone "43" then "44")
injected directly into sentences. Root cause: `chunk_text()` sliced raw extracted text
by fixed character count (`chunk_size=400`) with zero awareness of word, sentence, or
page boundaries, and `extract_text_from_pdf()` did no cleanup of PyMuPDF's per-page
output before concatenation — running headers/footers and page numbers were extracted
as if they were body text.

**Fix:**
- `extractor.py` now detects repeated header/footer lines automatically — any line
  appearing at the top/bottom of more than ~30% of pages is treated as a running
  header and stripped, along with any standalone numeric-only lines (stray page
  numbers). Detection is frequency-based per document, so it generalizes across all
  5 corpus documents without manual pattern-writing per file.
- `chunker.py` was rewritten from character-offset slicing to sentence-aware grouping:
  text is split into sentences first, then grouped up to `chunk_size=600` characters,
  never cutting a sentence in half. One sentence of overlap is carried into the next
  chunk for continuity. Page tracking (`page_start`/`page_end`) preserved via the same
  `<<<PAGE:N>>>` marker approach from the citation fix.

**Result (partially verified):** Re-running the exact query used in the original eval
batch 1 ("What is the punishment for murder under Nepal's criminal code?") before and
after this fix:
- **Before:** 5 results, ~3/5 genuinely on-topic, 2/5 off-topic noise (e.g. an
  unrelated offence against the state, a discrimination case rather than punishment
  itself). Chunk text contained visible extraction artifacts (mid-word cuts, stray
  page numbers like "45 \n 46" embedded mid-sentence).
- **After:** 5 results, ~4-5/5 on-topic and more tightly clustered around the actual
  murder/punishment provisions (pages 2-3, 33, 41-42) plus a relevant Supreme Court
  citation. Chunk text reads as clean, properly bounded sentences with no visible
  extraction noise.

**Not yet verified:** Only 1 of the 5 original eval batch-1 queries has been re-run
against the new chunking. The other 4 (right to equality, citizenship loss, cybercrime,
divorce process) have not yet been re-checked post-fix — improvement is observed on
this one query, not yet confirmed system-wide. Re-verification of the full batch is
planned before drawing broader conclusions.

**Known limitation:** Header detection is frequency-based and only catches lines that
repeat *identically* across many pages. Headers that follow a structural pattern but
differ per instance (e.g. each Supreme Court case in the Landmark Decisions document
has a different case-name header) are not caught, since no single line crosses the
repetition threshold. One such artifact was observed post-fix (a case-name fragment
embedded mid-chunk). Not yet addressed — logged as a known gap.

**Chunk size:** Changed from 400 (character-based) to 600 (sentence-grouped, so this
is now an upper bound rather than a fixed slice size). This value is a starting point,
not yet benchmarked — formal chunk-size tuning remains planned work, now to be done
against the new sentence-aware chunker rather than the old character-slicer.

---

## Known Gaps

| Gap | Priority | Notes |
|---|---|---|
| No chunking benchmarks | Medium | Chunk size (now 600, sentence-grouped) still empirical, not optimized |
| No retrieval accuracy metrics | Medium | No ground-truth eval set exists yet — in progress; only 1/5 batch-1 queries re-verified post chunking fix |
| Per-case headers not stripped | Low | Frequency-based header detection misses unique-per-case header lines (e.g. varying case names in Supreme Court doc) |
| No response latency profiling | Low | LLaMA 3 8B on CPU is slow; not yet measured |
| No auth layer | Low | Single-user local tool, auth not in scope |
| Corpus limited to English | Medium | Nepali-language documents excluded; no Nepali embedding model integrated |
| localStorage only | Low | Chat history lost on browser clear; no backend persistence |
| No article/section citation | Medium | Page-level citation works; article/section requires legal-structure parsing |

---

## Planned Work

- [x] Page-level citation metadata in retrieval pipeline (June 2026)
- [x] Sentence-aware chunking + automatic header/footer stripping (June 2026)
- [ ] Re-verify remaining 4/5 eval batch-1 queries against new chunking
- [ ] Eval set for retrieval/generation accuracy — in progress
- [ ] Chunk size / overlap benchmarking against retrieval recall (now against sentence-aware chunker)
- [ ] Response latency profiling — GPU vs CPU inference
- [ ] Citation rendering in UI — surface page-level source in frontend (backend now provides real page data; UI work remains)
- [ ] Article/section-level citation — requires legal-structure parsing of raw text, deferred as a separate task
- [ ] Per-case header stripping (Supreme Court doc) — frequency-based detection misses unique-per-case headers
- [ ] Expand corpus: add more acts and regulations
- [ ] Explore Nepali-language document support (requires multilingual embedding model)
- [ ] Backend-persisted chat history (replace localStorage with database)

---

## Design Principles (Enforced)

1. **Retrieval-first** — the model cannot answer without retrieved context
2. **Offline-first** — no outbound network calls after initial setup
3. **Privacy-preserving** — legal queries never leave the local machine
4. **Strict separation of concerns** — UI / API / inference / retrieval are independent layers
5. **Type safety where it matters** — contracts and state machines, not UI boilerplate

---

*Last updated: June 2026*
