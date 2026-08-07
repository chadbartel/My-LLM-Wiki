---
type: entity
date_created: 2026-08-07
date_updated: 2026-08-07
tags:
  - wiki/entity
  - project/ai-llm
  - status/in-progress
  - tech/fastapi
  - tech/chromadb
  - philosophy/research
source_count: 1
---

# my-cache-augmented-generation

Research implementation of the Cache-Augmented Generation (CAG) model from the paper "[Don't Do RAG: When Cache-Augmented Generation is All You Need for Knowledge Tasks](https://arxiv.org/abs/2412.15605)" by Chan et al. Explores using model context windows as a cache-based retrieval mechanism instead of traditional RAG.

## Purpose

Prove that modern LLMs with large context windows don't need traditional RAG. Instead, cache the knowledge in the model's context and let it retrieve from memory as needed.

## Core Philosophy

**CAG vs. RAG:**
- **RAG (Retrieval Augmented Generation):** Retrieve relevant chunks → pass to LLM → generate response
- **CAG (Cache-Augmented Generation):** Load knowledge into context window → model internally retrieves what it needs → generate response

**Why CAG Might Win:**
- Fewer external dependencies (no vector search)
- Model has full knowledge when generating
- Context window is the cache (no separate vector DB)
- Potentially more accurate (model sees all options)

**Trade-Off:**
- Requires LLMs with huge context windows (200K+ tokens)
- Higher latency for loading context
- Higher token costs
- But potentially better reasoning

## Key Features

- **CAG Model Implementation** — Paper-based research code
- **FastAPI Backend** — REST interface for inference
- **ChromaDB Integration** — Optional vector storage for comparison
- **Sentence-Transformers** — Embedding generation for research
- **Knowledge Base Support** — Load and cache domain knowledge
- **Docker Deployment** — Containerized research environment
- **Comprehensive Testing** — Unit + integration tests

## Tech Stack

- **Language:** Python 3.11
- **Package Manager:** Poetry
- **Framework:** FastAPI (backend), Uvicorn (ASGI server)
- **Vector DB:** ChromaDB 0.6.3 (optional, for comparison with RAG)
- **Embeddings:** Sentence-Transformers 3.4.1
- **NLP Processing:** Unstructured 0.16.21 (document parsing)
- **Transformers:** Hugging Face Transformers 4.49.0
- **Testing:** pytest, pytest-cov
- **Code Quality:** Black, isort, flake8
- **Task Runner:** poethepoet (poe)
- **Containerization:** Docker + Docker Compose

## Architecture

**Project Structure:**
```
my-cache-augmented-generation/
├── api/           # FastAPI application
├── models/        # Data models and CAG implementation
├── services/      # Core service logic
├── utils/         # Helper functions
├── data/          # Input documents
├── knowledge_base/ # Processed embeddings and cache
├── tests/
│   ├── unit/      # Unit tests
│   └── integration/ # Integration tests
├── Dockerfile     # Container definition
└── docker-compose.yml
```

**Core Modules:**
- **API Layer** (`api/main.py`) — FastAPI routes for inference
- **Models** (`models/`) — CAG model implementation + data schemas
- **Services** (`services/`) — Knowledge retrieval + caching logic
- **Utils** (`utils/`) — Embedding, parsing, text processing

**Data Flow:**
```
Raw Documents (PDF, text, etc.)
    ↓ (Unstructured library)
Parsed Text
    ↓ (Sentence-Transformers)
Embeddings
    ↓ (ChromaDB or direct cache)
Knowledge Cache
    ↓ (FastAPI endpoint)
CAG Model + Context Loading
    ↓ (LLM inference with cached knowledge)
Response (with internal model retrieval)
```

## Research Focus

**This Project Explores:**
1. **Does CAG outperform RAG?** — Accuracy comparison on knowledge tasks
2. **What's the optimal context window size?** — Token budget vs. performance
3. **How does chunking affect CAG?** — Does document structure matter?
4. **Latency trade-offs** — Context loading time vs. retrieval speed

**Compared to:**
- [[TTRPG-AI-RAG-Assistant]], [[AIO Generative AI Solution]], [[Arcane-Scribe]] — All use traditional RAG
- This research explores alternative architecture

## Deployment Model

- **Development:** Local Docker Compose with API server
- **Testing:** Comprehensive unit + integration tests (TDD approach)
- **Production Ready:** Infrastructure in place; awaiting research results
- **Scaling:** FastAPI can handle concurrent inference requests

## Relationships

**Feeds Into:**
- [[brAIniac]] — Phase 2 planned to integrate knowledge layers (could use CAG instead of Letta)
- [[TTRPG Ecosystem]] — Could benchmark CAG against Arcane-Scribe's RAG approach

**Contrasts With:**
- [[TTRPG-AI-RAG-Assistant]] — Traditional RAG approach
- [[AIO Generative AI Solution]] — Traditional RAG approach
- [[Arcane-Scribe]] — Enterprise RAG with FAISS

**Shares Philosophy With:**
- [[brAIniac]] — Research-focused, exploring novel architectures
- Academic papers — Bridging research and implementation

## Key Insights for Context-Switching

**When to use:**
- Exploring alternative LLM architectures
- Benchmarking CAG vs. RAG
- Working with LLMs that have huge context windows (Claude, GPT-4, Gemini)
- Reducing external dependencies (no vector search database)

**Quick facts:**
- **Purpose:** Research, not production (yet)
- **Context window:** Requires 200K+ token LLM
- **Token cost:** Higher than RAG (more tokens in context)
- **Accuracy:** Potentially better (model sees all options)
- **Latency:** Higher upfront (context loading), faster generation (no external search)

## Getting Started

```bash
# Setup
cd my-cache-augmented-generation
poetry install

# Run tests
poetry run poe test

# Start API server
poetry run poe dev

# Access FastAPI docs at http://localhost:8000/docs
```

## Research Workflow

```
1. Prepare Knowledge Base
   - Load documents into `data/`
   - Process with Unstructured
   - Generate embeddings (Sentence-Transformers)
   - Cache in `knowledge_base/`

2. Run CAG Model
   - Send query to `/infer` endpoint
   - Model loads cached knowledge into context
   - Generate response

3. Compare with RAG
   - Same query to Chromadb + traditional RAG
   - Measure accuracy, latency, cost

4. Iterate
   - Adjust chunk sizes, context windows, models
   - Re-run comparisons
   - Document findings
```

## Open Questions

- [CAG truly better than RAG for knowledge tasks?]
- [Which LLMs are best for CAG (context window size vs. reasoning)?]
- [Optimal knowledge base size for context caching?]
- [Should integrate with [[brAIniac]] Phase 2 as memory layer?]

## Related Concepts

- [[Cache-Augmented Generation]] — Core research approach
- [[RAG Pattern for TTRPG]] — Traditional approach (for comparison)
- [[AI/LLM Ecosystem]] — Role in your AI projects

## Tech Patterns Used

- **Separation of Concerns:** API layer, services, models, utils
- **SOLID Principles:** Extensible, testable service design
- **Test-Driven Development:** Unit + integration tests
- **Docker:** Reproducible development and deployment
- **Paper Implementation:** Research → code translation

## Testing Strategy

```bash
# Unit tests (fast, isolated)
poetry run poe test:unit

# Integration tests (slower, with services)
poetry run poe test:integration

# Coverage report
poetry run poe cov
```

## Sources

- Wiki source: Project repository scan on 2026-08-07
- README analysis from `/mnt/c/Users/Chaddle/PycharmProjects/my-cache-augmented-generation`
- Paper: "Don't Do RAG: When Cache-Augmented Generation is All You Need for Knowledge Tasks" by Chan et al.
- Architecture extracted from `api/main.py`, project structure
