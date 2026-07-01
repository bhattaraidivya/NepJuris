# Deploying the `hosted` branch (Vercel + Render)

This branch swaps local Ollama inference for hosted LLM APIs (Groq primary,
Gemini fallback) so the app can run on free hosting tiers. The `main`
branch (Docker Compose + Ollama, fully offline) is the one to run locally
for the full local-first experience — this branch exists specifically for
a public, always-reachable demo link.

Topology: Vercel serves the static frontend directly; it calls the Render
backend's own domain directly over CORS. There's no nginx reverse proxy in
this setup (unlike the `main` branch's docker-compose stack).

## Backend (Render)

1. New Web Service → connect this repo → branch `hosted`.
2. Runtime: Docker. Root directory: `backend`.
3. Environment variables (Render dashboard → Environment, never commit these):
   - `GROQ_API_KEY` — from https://console.groq.com
   - `GEMINI_API_KEY` — from https://aistudio.google.com/app/apikey
   - `GROQ_MODEL` (optional, defaults to `llama-3.1-8b-instant`)
   - `GEMINI_MODEL` (optional, defaults to `gemini-1.5-flash`)
   - `ALLOWED_ORIGINS` — your Vercel deployment URL, e.g. `https://nepjuris.vercel.app`
   - `CHAT_RATE_LIMIT` (optional, defaults to `10/minute`)
   - `UPLOAD_RATE_LIMIT` (optional, defaults to `3/hour`)
4. Render injects `PORT` automatically; the Dockerfile already binds to it.

**If the deploy OOMs again** (Render's free tier caps instances at 512MB,
and PyTorch + sentence-transformers is genuinely borderline at that size
even with the CPU-only wheel already in use): the next lever is replacing
`sentence-transformers` with `fastembed` (ONNX Runtime, no torch dependency,
typically <150MB) in `rag/embedder.py`. Not done preemptively since it
needs re-verifying retrieval quality — only worth it if the current setup
actually OOMs on Render.

## Frontend (Vercel)

1. New Project → connect this repo → branch `hosted`.
2. Root directory: `frontend`. Framework preset: Vite.
3. Environment variables:
   - `VITE_API_BASE_URL` — the Render backend's URL, **no** `/api` suffix
     (e.g. `https://nepjuris-backend.onrender.com`)
   - `VITE_DEMO_MODE=true` — shows the "uploads are temporary" banner on
     the Docs page (Render's free tier has no persistent disk)
4. `vercel.json` (already in the repo) handles the SPA rewrite so refreshing
   on `/chat` or `/docs` doesn't 404.

## Notes

- The document corpus (FAISS index, catalog, raw PDFs) ships inside the
  backend Docker image exactly as on `main` — nothing about retrieval
  changes when swapping the generation backend.
- Uploaded documents on the hosted backend only persist for the life of
  that Render instance; a restart/redeploy reverts to the baked-in corpus.
- Free-tier instances on Render spin down after inactivity — the first
  request after idling will be slow (cold start + model load).
