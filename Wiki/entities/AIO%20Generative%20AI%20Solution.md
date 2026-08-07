---
type: entity
date_created: 2026-08-07
date_updated: 2026-08-07
tags:
  - wiki/entity
  - project/ttrpg
  - status/active
  - tech/fastapi
  - tech/chromadb
  - tech/gemini
  - deployment/docker
source_count: 1
---

# AIO Generative AI Solution

Docker-based MVP for TTRPG PDF analysis and Q&A, enabling users to query specific TTRPG rulebooks with AI-powered answers using Google Gemini and Chromadb. Focus on deterministic, accurate responses for TTRPG mechanics lookup.

## Purpose

Practical TTRPG companion for players and GMs. Query rulebooks (D&D 5e, Dragonbane, Kids on Bikes, Star Wars 5e) without manually searching PDFs. Built for local deployment with persistent vector storage.

## Core Features

- **FastAPI REST API:** `/query`, `/add_document`, `/update_document` endpoints
- **PDF Text Extraction:** PyMuPDF (no OCR—assumes clean, copy-paste-able text)
- **Google Gemini Embeddings:** Selectable models (Gemini, Gemini Pro, Gemini Lite)
- **Chromadb Vector Database:** Persistent local storage with volume mounts
- **LangChain RAG Pipeline:** Deterministic retrieval + generation
- **TTRPG Organization:** Separate folders for Dragonbane, D&D 5e, Kids on Bikes, Star Wars 5e
- **Docker Ready:** Local deployment with mounted volumes for PDFs and database

## Tech Stack

- **Language:** Python ~3.12
- **Framework:** FastAPI (REST API)
- **Vector Database:** Chromadb (persistent local storage)
- **PDF Processing:** PyMuPDF4LLM (text extraction)
- **LLM & Embeddings:** Google Gemini API (configurable model)
- **RAG Framework:** LangChain + LangChain-Community + LangChain-Google-GenAI
- **Embeddings Fallback:** Sentence-Transformers (local alternative to Gemini)
- **ASGI Server:** Gunicorn (production-ready)
- **Containerization:** Docker (volume mounts for data persistence)

## Architecture

- **Entry Point:** `app.py` (FastAPI app initialization and routing)
- **Configuration:** `config.py` (API keys, model selection, paths)
- **Services:**
  - Document processor (PDF extraction, chunking)
  - Embedding generator (Gemini API calls)
  - ChromaDB interface (store, retrieve, query)
  - Gemini LLM client (generation)
- **Key Folders:**
  - `/models` — Pydantic data models (Query, Response schemas)
  - `/services` — Core RAG pipeline logic
  - `/utils` — Utility functions and helpers
  - `chroma_db/` — Persistent vector database directory
- **Data Flow:** Local PDF folder → PyMuPDF extraction → Gemini embedding → ChromaDB storage → Query endpoint → Gemini generation → Response

## Deployment Model

- **Default:** Local Docker container
- **Data Persistence:** Volume mounts for `/chroma_db/` (embeddings) and `/models/` (PDFs)
- **API Access:** HTTP (localhost:8000 or proxied)
- **Scalability:** Single-instance local solution (suitable for small teams)

## Relationships

**Nearly Identical To:**
- [[TTRPG-AI-RAG-Assistant]] — Same stack, architecture, and purpose (Gemini-based local RAG)
- Could consolidate into single service to reduce maintenance

**Differs From:**
- [[Arcane-Scribe]] — Local/Gemini vs. AWS/Bedrock (production vs. enterprise)
- [[Automated-Taskmaster]] — Document query vs. stateless generation

**Supports:**
- [[UnnamedRPG]] — Could ingest rulebook as source material

## Project Status

- **Status:** Active (MVP deployed locally)
- **Completeness:** Ready for AWS migration or continued local use
- **Deployment:** Currently local Docker; AWS version planned
- **Maintenance:** Stable, tested

## Key Insights for Context-Switching

**When to use:**
- You're writing a campaign and need quick rule lookups
- Testing new TTRPG mechanics
- Building AI features for other TTRPG projects
- Need fast, local query interface without cloud latency

**Quick facts:**
- **Performance:** Vector search responses in <1 second
- **Cost:** Gemini API billing (cheaper than Bedrock alternatives)
- **Privacy:** Local storage, Gemini API calls only for embeddings/generation
- **Setup:** Docker pull + volume mount for PDFs
- **Scalability:** Single-instance; suitable for 1-10 users

## Integration Points

```
TTRPG Rulebook (PDF)
    ↓ (PyMuPDF4LLM)
Clean Text Chunks
    ↓ (Gemini Embeddings)
Vector Store (ChromaDB)
    ↓ (Semantic Search)
Retrieved Context + Query
    ↓ (Gemini LLM)
Accurate Rule Response
```

## Deployment Considerations

- **Local option:** Docker Compose for quick local setup
- **AWS option:** Pending migration (Lambda + RDS replacement planned)
- **Volume management:** Persistent `/chroma_db/` must survive container restarts
- **API Gateway:** Would be fronted by reverse proxy in production

## Open Questions

- [Consolidate with [[TTRPG-AI-RAG-Assistant]]—keep both instances?]
- [AWS Lambda deployment planned—timeline?]
- [Multi-user concurrency support in ChromaDB?]
- [OCR support for scanned rulebooks?]

## Related Concepts

- [[TTRPG Ecosystem]] — Role in your TTRPG project cluster
- [[RAG Pattern for TTRPG]] — Document ingestion + semantic search architecture
- [[Multi-Provider LLM Integration]] — Gemini API approach vs. Bedrock
- [[Local Deployment Patterns]] — Docker-based services

## Tech Patterns Used

- **RAG (Retrieval Augmented Generation):** PDF → chunks → embeddings → search → generation
- **FastAPI Routers:** Modular endpoint design
- **Dependency Injection:** Service initialization in `app.py`
- **Docker Volumes:** Persistent data across container lifecycle

## Sources

- Wiki source: Project repository scan on 2026-08-07
- README analysis from `/mnt/c/Users/Chaddle/PycharmProjects/AIO Generative AI Solution`
- pyproject.toml dependency and configuration analysis
- Architecture extracted from `app.py` and `/services` module structure
