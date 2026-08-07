---
type: entity
date_created: 2026-08-07
date_updated: 2026-08-07
tags:
  - wiki/entity
  - project/ai-llm
  - status/active
  - tech/ollama
  - tech/fastmcp
  - philosophy/local-first
source_count: 1
---

# brAIniac

Decentralized, local-first, uncensored AI chatbot designed to run entirely on consumer hardware with a hard 8GB VRAM ceiling. No cloud dependencies, no API keys, no telemetry.

## Purpose

Prove that powerful AI doesn't require cloud infrastructure or internet connectivity. A full-featured conversational AI that respects privacy by design.

## Core Philosophy

**Local-First Everything:**
- All inference on-device (Ollama Docker container)
- No external API calls (except optional tools)
- No telemetry, no usage tracking
- Your hardware, your data, your model weights

**Uncensored by Design:**
- Open-weight models via Ollama (llama3.1:8b-instruct-q4_K_M default)
- 4-bit GGUF quantization for VRAM efficiency
- No upstream content filters
- User controls output

**VRAM Discipline:**
- Hard 8GB VRAM ceiling enforced at every layer
- Rolling context window (don't keep infinite history)
- Phase-based roadmap respects hardware constraints
- RTX 2070 SUPER is target hardware (mid-range consumer GPU)

## Key Features

- **Rich CLI Interface** — Terminal-based interaction with formatting
- **Gradio Web UI** — Browser-based chat interface
- **Modular FastMCP Tools** — Extensible tool servers (time, web search)
- **Personality Vectors** — Customize tone without code changes (snark, verbosity, empathy)
- **Rolling Memory** — Context management prevents VRAM bloat
- **Docker Compose** — Reproducible local deployment

## Tech Stack

- **Language:** Python 3.12+
- **Package Manager:** Poetry (single root `pyproject.toml`)
- **LLM Runtime:** Ollama (Docker container)
- **Default Model:** `llama3.1:8b-instruct-q4_K_M` (4-bit GGUF, ~5GB VRAM)
- **Tool Protocol:** Model Context Protocol (FastMCP v2)
- **Web UI:** Gradio 6
- **CLI:** Rich library (colored output, formatting)
- **Containers:** Docker Compose orchestration
- **Testing:** pytest, pytest-asyncio, pytest-mock, pytest-cov
- **Code Quality:** Black, mypy, ruff, isort

## Architecture

**Core Components:**
- **ChatEngine** (`core/chat.py`) — Main orchestrator connecting CLI/web to Ollama, managing memory, coordinating tool calls
- **Memory System** (`core/memory.py`) — RollingMemory and DiskMemory backends for context windowing
- **Personality Manager** (`core/personality.py`) — PersonalityManager with customizable vectors
- **Intent Classifier** (`core/intent_classifier.py`) — Route queries to tools vs. Ollama
- **Tool Servers** (`servers/base_tools/server.py`) — FastMCP servers exposing tools (time, DuckDuckGo search)

**Data Flow:**
```
User Input (CLI/Web)
    ↓ (Rich/Gradio parsing)
ChatEngine
    ↓ (Intent classification)
    Route to: Tool Server OR Ollama
    ↓
Tool Server (FastMCP) OR Ollama Inference
    ↓ (Response generation)
ChatEngine + Memory Management
    ↓
Output (formatted terminal OR web)
```

**Deployment Model:**
- Docker Compose with two services:
  1. `ollama` — Ollama LLM runtime + models
  2. `brainiac-web` — Gradio web interface
- Local file system for memory persistence

## Phase-Based Roadmap

**Phase 1: The Foundation (CURRENT - MVP)**
- Core chat loop with FastMCP tools
- VRAM management
- Simple rolling context window
- Status: ✓ Complete (MVP)

**Phase 2: Advanced Context & Research**
- Letta (MemGPT) for OS-level memory/context paging
- brainiac-research-server with SearXNG + IterDRAG
- Virtual memory to break 8GB ceiling (for specific tasks)
- Status: Planned

**Phase 3: Voice & Multi-Agent Routing**
- STT (Canary Qwen 2.5B or Parakeet V3) for speech input
- TTS (Kokoro-82M) for audio output
- Agent Squad or Observer framework for intent routing
- Status: Planned

**Phase 4: Autonomous Self-Learning**
- Nightly fine-tuning loop
- Curate successful chat histories
- Unsloth QLoRA fine-tuning
- Hot-swappable LoRA adapters
- Status: Planned

## Relationships

**Contrasts With:**
- [[GenerateIdeas]] — Cloud API (Gemini) vs. local-first philosophy
- [[TTRPG-AI-RAG-Assistant]] — Query interface vs. conversational AI
- [[Arcane-Scribe]] — Enterprise serverless vs. privacy-first consumer

**Complements:**
- [[my-cache-augmented-generation]] — Could integrate CAG as Phase 2 knowledge layer
- [[TTRPG Ecosystem]] — Could extend with game-specific FastMCP tools

**Shares Philosophy With:**
- [[Homelab-Ansible]] — On-device, self-hosted infrastructure

## Design Patterns

**FastMCP Tool Pattern:**
Every tool is a separate microservice implementing Model Context Protocol:
```python
# Tool server example
from fastmcp import FastMCP
app = FastMCP("brainiac-tools")

@app.tool()
def current_time():
    """Get current time"""
    return datetime.now().isoformat()
```

**Personality Vector System:**
Separate personality from core logic:
```python
personality = {
    "snark": 0.7,      # Higher = more sarcastic
    "verbosity": 0.5,  # Higher = longer responses
    "empathy": 0.8     # Higher = more caring tone
}
```

## Key Insights for Context-Switching

**When to use:**
- Building conversational AI without cloud dependency
- Privacy is critical (offline-capable)
- Exploring uncensored AI models
- Prototyping new FastMCP tools
- VRAM-constrained hardware

**Quick facts:**
- **VRAM:** Hard 8GB ceiling (non-negotiable design constraint)
- **Speed:** ~200-500ms per token generation (depends on GPU)
- **Privacy:** 100% on-device (no external calls by default)
- **Extensibility:** Add tools by creating new FastMCP servers
- **Cost:** Hardware only (no API costs)

## Getting Started

```bash
# 1. Clone and setup
cd brAIniac
poetry install

# 2. Start Ollama + services
docker-compose up -d

# 3. Run CLI
poetry run python main.py

# 4. Or access web UI at http://localhost:7860
```

## Open Questions

- [Phase 2: Which memory paging strategy (Letta vs. custom)?]
- [Phase 3: Which STT model is most efficient (Qwen vs. Parakeet)?]
- [Should GenerateIdeas ideas feed into brAIniac as tools?]
- [Multi-GPU support to bypass 8GB ceiling?]

## Related Concepts

- [[Local-First AI Architecture]] — Philosophy behind brAIniac
- [[FastMCP Protocol]] — Tool integration mechanism
- [[VRAM-Constrained Inference]] — Hardware efficiency techniques
- [[AI/LLM Ecosystem]] — How this fits in your AI projects

## Tech Patterns Used

- **Modular Microservices:** Each tool is a separate FastMCP server
- **Personality Vectors:** Decouple behavior from core logic
- **Rolling Context Window:** Maintain bounded memory
- **Docker Compose:** Reproducible multi-service setup
- **SOLID Principles:** Extensible, testable, maintainable

## Sources

- Wiki source: Project repository scan on 2026-08-07
- README analysis from `/mnt/c/Users/Chaddle/PycharmProjects/brAIniac`
- pyproject.toml dependency analysis
- Architecture extracted from `main.py`, `core/`, `servers/` structure
