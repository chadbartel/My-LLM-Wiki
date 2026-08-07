---
type: concept
date_created: 2026-08-07
date_updated: 2026-08-07
tags:
  - wiki/concept
  - architecture
  - philosophy
  - privacy
confidence: high
source_count: 1
---

# Local-First AI Architecture

Design philosophy where all AI computation happens on your hardware, with no external API dependencies or cloud connections. Everything stays on-device: models, inference, memory, tools.

## Definition

**Local-First AI** means:
- All LLM inference runs on local hardware (GPU or CPU)
- Models are stored locally (downloaded once, run many times)
- No internet required for core operation
- No API keys, no rate limits, no telemetry
- Full control over model weights and output

**Contrast:**
- **Cloud API:** Send query to external service (Gemini, OpenAI, Bedrock)
- **Hybrid:** Local + occasional cloud calls
- **Local-First:** Everything local with optional external tools

## Philosophy

**Privacy First:**
- Your data never leaves your computer
- No logs on external servers
- No usage tracking
- No marketing analysis
- Your model weights stay yours

**Control & Customization:**
- Modify model behavior freely
- No content filters or guardrails (unless you add them)
- Customize system prompts and personality
- Add tools specific to your workflow
- No artificial limitations

**Cost Efficiency:**
- No per-token billing
- One-time hardware investment
- No subscription fees
- No usage-based limits
- Pay once, use forever

**Resilience:**
- Works offline (no internet required)
- No external service outages affect you
- Reproducible results (same model, same hardware)
- No API deprecation risk
- Can archive and version models

## Implementation Patterns

### Model Management

**Option 1: Ollama (recommended for beginners)**
```bash
# Download and run 7B model
ollama run llama3.1:8b-instruct-q4_K_M

# Same model every time
# ~5GB VRAM for 8B model
```

**Option 2: Direct Transformers (for advanced users)**
```python
from transformers import AutoModelForCausalLM, AutoTokenizer

model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-2-7b-hf",
    torch_dtype=torch.float16,
    device_map="auto"
)
```

**Option 3: GGML Format (CPU-friendly)**
```bash
# Run on CPU or GPU efficiently
./main -m model.gguf -p "Hello" -n 128
```

### Architecture Layers

```
User Interface
├─ CLI (Rich, colorama)
├─ Web UI (Gradio, Streamlit)
└─ Direct API (FastAPI)
    ↓
Application Logic
├─ Memory management (rolling context)
├─ Intent classification
└─ Tool coordination (FastMCP)
    ↓
Local LLM Runtime
├─ Ollama (recommended)
├─ vLLM (high-throughput)
├─ Text Generation WebUI
└─ Direct transformers
    ↓
Model File Storage
└─ ~5-30GB SSD space for models
```

### VRAM Management (Critical for Consumer Hardware)

**8GB VRAM GPU Constraints:**

| Model Size | Quantization | VRAM Needed | Quality Loss |
|------------|--------------|-------------|--------------|
| 70B params | Q4_K_M | 28GB | ~5% |
| 70B params | Q3_K_S | 18GB | ~10% |
| 13B params | Q4_K_M | 6.5GB | ~5% |
| 8B params | Q4_K_M | 5GB | ~5% |
| 7B params | Q5_K_M | 4.5GB | ~2% |
| 3.8B params | Q4_K_M | 2.5GB | ~5% |

**brAIniac's Strategy:**
- Hard 8GB ceiling enforced
- Uses 8B model (llama3.1:8b-instruct-q4_K_M)
- Rolling context window to prevent memory bloat
- Leaves room for tools and UI (never use all 8GB)

### Tool Integration Pattern (FastMCP)

Local-first AI benefits from local tools:

```python
# Tool server (separate process)
from fastmcp import FastMCP
app = FastMCP("brainiac-tools")

@app.tool()
def search_local_files(query: str) -> str:
    """Search local filesystem, not the internet"""
    return search_my_documents(query)

@app.tool()
def run_local_code(code: str) -> str:
    """Execute Python locally"""
    return execute_sandbox(code)

# Tools stay local, same as LLM
```

## Trade-Offs

### Advantages

✅ **Privacy:** 100% on-device, no external data flows
✅ **Cost:** No per-token billing (hardware is one-time)
✅ **Offline:** Works without internet
✅ **Control:** Modify models and behavior freely
✅ **Latency:** No network latency (only inference latency)
✅ **Reproducibility:** Same hardware = same results
✅ **Resilience:** No external service dependencies

### Disadvantages

❌ **Capability:** Smaller quantized models vs. GPT-4/Claude
❌ **Latency:** ~200-500ms per token on consumer GPU (vs. 50ms cloud)
❌ **Effort:** Setup, tuning, maintenance required
❌ **Hardware:** Need GPU (or very slow on CPU)
❌ **VRAM Ceiling:** Limited by GPU memory
❌ **Knowledge Currency:** Offline → outdated information
❌ **Updates:** Need to manually manage model updates

## Comparison: Local vs. Cloud

| Aspect | Local-First | Cloud API |
|--------|------------|-----------|
| **Privacy** | ✅ On-device | ❌ External servers |
| **Cost** | ✅ One-time (hardware) | ❌ Per-token billing |
| **Offline** | ✅ Works offline | ❌ Requires internet |
| **Capability** | ⚠️ 8B model vs. 400B | ✅ Frontier models |
| **Latency** | ⚠️ 200-500ms/token | ✅ 50-100ms/token |
| **Setup** | ❌ Complex | ✅ Simple |
| **Control** | ✅ Full control | ❌ Provider decides |
| **Censorship** | ✅ You decide | ❌ Filters applied |

## When Local-First Wins

**Use local-first AI when:**
- Privacy is critical (healthcare, legal, finance)
- Offline capability is required (no connectivity)
- You need uncensored models
- Long-term cost matters (high usage volume)
- You want full customization
- Running in restricted networks
- ADHD context-switching (instant access, no API calls)

**Example scenarios:**
- Personal assistant (sensitive data)
- Research tool (proprietary documents)
- Creative writing (no censorship)
- System automation (always available)
- Exploratory learning (customize for your style)

## When Cloud-First Wins

**Use cloud API when:**
- You need frontier capability (GPT-4, Claude)
- Privacy isn't critical
- Occasional use (no infrastructure burden)
- Fast time-to-market
- No internet connectivity concerns
- Prefer not to manage infrastructure

**Example scenarios:**
- One-off brainstorming (GenerateIdeas)
- Enterprise application (dedicated support)
- Rapid prototyping
- No hardware investment possible

## Hybrid Approach (Recommended)

**Best of both worlds:**

```
Local-First + Cloud Fallback
|
User Query
├─→ Try local inference first
│   ├─→ If successful, return result
│   └─→ If VRAM exhausted or timeout, fallback
├─→ Call cloud API as fallback
│   └─→ Higher capability for complex queries
└─→ Cache results for next time
```

**Your Ecosystem:**
- [[brAIniac]] — Local-first conversational AI
- [[GenerateIdeas]] — Cloud-first brainstorming
- [[my-cache-augmented-generation]] — Research exploring alternatives

## Practical Implementation: brAIniac

**How brAIniac implements local-first:**

```
1. Model Management
   - Ollama pulls llama3.1:8b-instruct-q4_K_M once
   - Stored in Ollama cache (~5GB)
   - Reused across all invocations

2. Memory Management
   - Rolling context window (don't keep all history)
   - RollingMemory class pops oldest messages
   - DiskMemory persists to SQLite
   - Prevents VRAM bloat

3. Tool Integration
   - FastMCP servers run locally
   - Time tool (local)
   - Web search (optional, via DuckDuckGo)
   - Future: Local search, local code execution

4. Interface
   - CLI: Rich library for formatting
   - Web: Gradio UI (runs locally)
   - Both interfaces stay on-device
```

## Setting Up Local-First AI

### Minimal Setup

```bash
# 1. Install Ollama (https://ollama.ai)
brew install ollama  # or download

# 2. Pull a model
ollama pull llama3.1:8b-instruct-q4_K_M

# 3. Start Ollama service
ollama serve

# 4. Test in another terminal
curl http://localhost:11434/api/generate \
  -d '{"model": "llama3.1", "prompt": "Hello"}'
```

### For ADHD Context-Switching

Local-first is ideal because:
- **Instant Access:** No API keys, no waiting for cloud
- **Offline:** No internet means no distractions
- **Reproducibility:** Same model every time
- **Customization:** Adjust personality vectors
- **No Rate Limits:** Generate ideas continuously

## Maintenance & Scaling

**Phase 1 (Current):**
- Single 8B model
- Enough for conversational AI
- ~200-300ms per token generation

**Phase 2 (Planned for brAIniac):**
- Virtual memory via Letta (memory paging to disk)
- Could use larger models (30B with aggressive caching)
- Multiple tool servers

**Phase 3+ (Future):**
- Multi-GPU support (escape 8GB ceiling)
- Model quantization tuning (find optimal quality/speed)
- Custom fine-tuning (QLoRA, LoRA adapters)
- Speculative decoding (faster generation)

## Related Concepts

- [[brAIniac]] — Primary implementation
- [[Cloud vs. On-Device LLM Strategy]] — Philosophical comparison
- [[VRAM-Constrained Inference]] — Hardware optimization
- [[FastMCP Protocol]] — Local tool integration

## Open Questions

- [Multi-GPU setup for larger models?]
- [Optimal VRAM budget for different tasks?]
- [Should integrate CAG for knowledge layer?]
- [Fine-tuning strategy for ADHD assistant persona?]

## Resources

- Ollama documentation: https://ollama.ai
- GGUF format: https://github.com/ggerganov/llama.cpp
- FastMCP protocol: Model Context Protocol (MCP)
- Quantization guide: https://huggingface.co/docs/optimum/quantization

## Sources

- [[Wiki/entities/brAIniac]]
- Ollama documentation
- Transformer models documentation
- GGML/GGUF specifications
