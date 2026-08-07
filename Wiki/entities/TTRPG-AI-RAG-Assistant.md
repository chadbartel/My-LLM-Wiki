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
source_count: 1
---

# TTRPG-AI-RAG-Assistant

FastAPI-based RAG system enabling natural language queries against TTRPG PDF rulebooks with AI-powered answers using Google Gemini embeddings and Chromadb vector storage.

## Purpose

Provide AI-powered query interface for TTRPG rulebooks. Players and GMs can ask natural language questions about game rules and receive accurate, sourced answers from official rulebooks (Dragonbane, D&D 5e, Kids on Bikes, Star Wars 5e).

## Core Features

- **REST API Interface:** POST `/query` endpoint for natural language questions
- **PDF Ingestion:** PyMuPDF4LLM for clean text extraction (no OCR)
- **Vector Embeddings:** Google Gemini embedding models (selectable: Gemini, Gemini Pro, Gemini Lite)
- **Persistent Storage:** Chromadb vector database with local file persistence
- **RAG Pipeline:** LangChain-based retrieval augmented generation
- **Multi-System Support:** Separate ChromaDB instances for different game systems

## Tech Stack

- **Language:** Python ~3.12
- **Framework:** FastAPI (REST API)
- **Vector Database:** Chromadb (persistent local storage)
- **PDF Processing:** PyMuPDF4LLM (text extraction)
- **LLM & Embeddings:** Google Gemini API
- **RAG Framework:** LangChain + LangChain-Community + LangChain-Google-GenAI
- **Fallback Embeddings:** Sentence-Transformers
- **ASGI Server:** Gunicorn
- **Containerization:** Docker

## Architecture

- **Entry Point:** `app.py` (FastAPI application initialization)
- **Services:** 
  - Document processing (PDF → text chunks)
  - Embedding generation (text → Gemini vectors)
  - ChromaDB management (store, retrieve, query)
  - Gemini LLM interaction (generation)
- **Key Folders:**
  - `/services` — Core RAG logic
  - `/models` — Pydantic data models
  - `/utils` — Helper functions
  - `chroma_db/` — Persistent vector storage
- **Data Flow:** PDF files → PyMuPDF parsing → Gemini embeddings → ChromaDB storage → `/query` endpoint → Gemini response

## Deployment Model

- **Default:** Local Docker container with volume mounts for PDFs and vector storage
- **Alternative:** Could be migrated to AWS or other cloud platforms
- **Scalability:** Single-instance local solution (vector search on one machine)

## Relationships

**Similar To:**
- [[AIO Generative AI Solution]] — Nearly identical architecture and stack (both Gemini-based local RAG)
- [[Arcane-Scribe]] — Same RAG pattern but using AWS Bedrock instead of Gemini

**Can Query:**
- [[UnnamedRPG]] — If rules are ingested as PDF source

**Could Integrate With:**
- [[Automated-Taskmaster]] — Could call this for encounter-specific rule lookups
- [[AIO Generative AI Solution]] — Shared embedding strategy, could consolidate instances

## Project Status

- **Status:** Active (MVP complete)
- **Completeness:** Tested, containerized, ready for production
- **Maintenance:** Stable; mainly used for query handling
- **Known Issues:** None documented

## Key Insights for Context-Switching

**When to use:**
- You need natural language search over TTRPG rulebooks
- Want to query game mechanics without reading entire PDFs
- Building other systems that need rule lookup capability

**Quick facts:**
- **Query speed:** Milliseconds (vector search is fast)
- **Accuracy:** Gemini-grounded (sources provided)
- **Cost:** Google Gemini API billing per embedding + generation
- **Privacy:** Queries sent to Gemini (not private)
- **Local persistence:** ChromaDB stored locally; embeddings cached

## Integration Points

```
PDF Rulebook
    ↓ (PyMuPDF4LLM)
Text Chunks
    ↓ (Gemini Embeddings)
Vector Database (ChromaDB)
    ↓ (Query)
Retrieval + Generation
    ↓ (Gemini LLM)
Natural Language Response
```

## Open Questions

- [Should UnnamedRPG rules be auto-ingested when created?]
- [Could consolidate with [[AIO Generative AI Solution]] to single instance?]
- [Multi-user concurrency handling for ChromaDB?]
- [Cost optimization for high-volume queries?]

## Related Concepts

- [[TTRPG Ecosystem]] — How this fits in your TTRPG project cluster
- [[RAG Pattern for TTRPG]] — Document ingestion + semantic search pattern
- [[Multi-Provider LLM Integration]] — Gemini API approach

## Tech Patterns Used

- **RAG (Retrieval Augmented Generation):** Document → embedding → semantic search → LLM generation
- **FastAPI Router Pattern:** Modular endpoint definitions
- **Containerization:** Docker for reproducibility and deployment

## Sources

- Wiki source: Project repository scan on 2026-08-07
- README analysis from `/mnt/c/Users/Chaddle/PycharmProjects/TTRPG-AI-RAG-Assistant`
- pyproject.toml dependency analysis
- Architecture extracted from `app.py` and service module structure
