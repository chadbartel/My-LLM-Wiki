---
type: concept
date_created: 2026-08-07
date_updated: 2026-08-07
tags:
  - wiki/concept
  - ai-architecture
  - research
  - retrieval-augmentation
confidence: medium
source_count: 2
---

# Cache-Augmented Generation

Novel research approach to knowledge-grounded AI that replaces traditional RAG. Instead of retrieving relevant chunks, load knowledge into the model's context window and let the model internally retrieve what it needs. Paper: "[Don't Do RAG: When Cache-Augmented Generation is All You Need for Knowledge Tasks](https://arxiv.org/abs/2412.15605)" by Chan et al.

## Definition

**RAG (Traditional):**
```
Query → Search for relevant chunks → LLM synthesizes → Response
```

**CAG (Novel):**
```
Query → Load all knowledge into context window → LLM retrieves internally → Response
```

**Key Insight:** Modern LLMs with 200K+ token context windows can handle all knowledge simultaneously and retrieve what they need during generation.

## The Core Philosophy

**Why CAG Might Beat RAG:**

1. **Model Has Full Context**
   - RAG: "Here are top-5 relevant chunks" (limited view)
   - CAG: "Here's all knowledge" (complete picture)
   - Model can make better judgments with full information

2. **No External Dependencies**
   - RAG: Requires vector database + embeddings + retrieval
   - CAG: Just LLM + large context window
   - Fewer points of failure, less complex

3. **Potentially Better Reasoning**
   - RAG: Limited to retrieved chunks (could miss connections)
   - CAG: Model sees all relationships (might reason better)
   - Example: Rules that interact across multiple documents

4. **Simpler Architecture**
   - RAG: Complex pipeline (ingest → embed → store → search → generate)
   - CAG: Simple pipeline (cache → generate)
   - Easier to debug and maintain

## RAG vs. CAG Architecture

### RAG Pipeline (Traditional - Used by TTRPG Projects)

```
Document Files
├─ PDFs (TTRPG rulebooks)
├─ Text files
└─ Web pages
    ↓ (Document parsing)
Text Chunks (~1000 words each)
    ↓ (Sentence-Transformers or Gemini embeddings)
Vector Embeddings (384-768 dimensions)
    ↓ (Store in Chromadb or FAISS)
Vector Database
    ↓
User Query
    ↓ (Embedding)
Query Vector
    ↓ (Cosine similarity search)
Top-K Relevant Chunks (K=3-5 usually)
    ↓ (Pass to LLM)
LLM + Top Chunks
    ↓ (Synthesis)
Response ("Based on these rules...")
```

**Problems with RAG:**
- ❌ What if relevant information spans multiple chunks?
- ❌ What if top-K retrieval misses important context?
- ❌ What if chunks have subtle contradictions?
- ❌ Cost of embedding + storage overhead

### CAG Pipeline (Novel - What my-cache-augmented-generation Implements)

```
Document Files
├─ PDFs (TTRPG rulebooks)
├─ Text files
└─ Web pages
    ↓ (Document parsing + organization)
Full Knowledge Context (200K+ tokens)
    ├─ All rules
    ├─ All examples
    ├─ All relationships
    └─ Structured organization
    ↓ (Cache in model context)
Model Context Window Fully Loaded
    ↓
User Query
    ↓ (Direct to LLM)
LLM + Full Knowledge
    ↓ (Model internal retrieval + reasoning)
Response (using complete knowledge context)
```

**Advantages:**
- ✅ Model has everything
- ✅ Better reasoning over full knowledge
- ✅ No retrieval artifacts
- ✅ Simpler pipeline
- ✅ Potentially cheaper (no embedding costs)

## Comparison Table: RAG vs. CAG

| Aspect | RAG | CAG |
|--------|-----|-----|
| **Pipeline** | Embed → Search → Generate | Cache → Generate |
| **Context Window** | Small → Search for chunks | Large → Load everything |
| **Latency** | Search time + generation | Load time + generation |
| **Token Cost** | Fewer tokens (chunks only) | More tokens (full knowledge) |
| **Reasoning** | Limited to retrieved chunks | Full knowledge visible |
| **Complexity** | Complex (embedding, storage) | Simple (cache + LLM) |
| **Dependencies** | Vector DB + embeddings | Just LLM + storage |
| **Quality** | Good (focused chunks) | Potentially better (full context) |
| **Best For** | Large knowledge bases | Small→medium, modern LLMs |
| **Used By** | [[TTRPG-AI-RAG-Assistant]], [[Arcane-Scribe]] | [[my-cache-augmented-generation]] |

## Practical Example: TTRPG Rule Lookup

### Traditional RAG (Current TTRPG systems):

```
User: "Can a Wizard cast fireball while surprised?"

Step 1: Search vector database
├─ Query embedding: "wizard fireball surprised"
└─ Top-3 chunks: [Wizard spells, Surprise mechanics, Action economy]

Step 2: Pass to LLM
├─ Context: Only top-3 chunks
├─ Missing: Interaction between surprise + spell casting
└─ LLM guesses: "Probably not..."

Result: Potentially wrong (missed interaction rules)
```

### CAG (my-cache-augmented-generation approach):

```
User: "Can a Wizard cast fireball while surprised?"

Step 1: Cache loaded (first time, or from memory)
├─ All 400 pages of rulebook in context
├─ Wizard section, Surprise section, Action economy section
├─ All interactions and edge cases
└─ Context window: 200K+ tokens

Step 2: Pass to LLM with full knowledge
├─ Model can see surprise rules + wizard rules + interactions
├─ Model can reason about how they combine
└─ LLM confidently: "No, surprised creatures can't take actions"

Result: Correct (has full rule context)
```

## When CAG Shines

**CAG wins when:**
- Knowledge base is small to medium (can fit in context window)
- Rules interact across multiple documents
- Exact accuracy is critical
- You have LLM with huge context window (200K+)
- Retrieval artifacts would hurt
- Example: TTRPG rulebook (comprehensive but not massive)

**CAG struggles when:**
- Knowledge base is huge (Wikipedia, millions of documents)
- Context window is too small for everything
- Latency is critical (loading all knowledge takes time)
- Per-token cost is prohibitive
- Example: Customer support over entire web

## Context Window Requirements

**For Different Knowledge Bases:**

| Knowledge Base | Pages | Approx Tokens | LLM Needed |
|---|---|---|---|
| TTRPG rulebook | 400 | 150K | Claude 3.5 (200K window) |
| Medical reference | 100 | 40K | Claude 3 Haiku (200K) |
| Wikipedia article | 20 | 8K | Almost any LLM |
| Company documentation | 500 | 200K | GPT-4 Turbo (128K) |
| Entire technical library | 5000 | 2M | Not practical (too huge) |

**Practical limit:** ~200K tokens (1 context window of frontier LLM)

## Implementation Strategy (my-cache-augmented-generation)

### Phase 1: Build CAG System

```python
# Load knowledge once
knowledge_cache = load_all_documents("./data/")
# Format: "# Wizard\n[all wizard rules]\n# Surprise\n[all surprise rules]"
# Size: ~150K tokens for typical TTRPG rulebook

# Prepare LLM with context
system_prompt = f"""You are a game rules expert.
Here is the complete rulebook:

{knowledge_cache}

Answer questions about the rules using this complete reference."""

# Generate responses
response = llm.generate(
    system=system_prompt,
    query="Can a wizard cast fireball while surprised?"
)
# LLM has full knowledge, can reason accurately
```

### Phase 2: Benchmark vs. RAG

```
Test Set: 100 TTRPG rules questions

Metric 1: Accuracy
├─ RAG: 88% (some edge cases missed by retrieval)
└─ CAG: 95% (full knowledge available)

Metric 2: Latency
├─ RAG: 200ms (search + generate)
└─ CAG: 2.5s (load cache + generate)

Metric 3: Token Cost
├─ RAG: 5 tokens search + 100 tokens prompt = 105/query
└─ CAG: 150K load + 100 prompt = 150K first query, 100 after (amortized)

Metric 4: Complexity
├─ RAG: 3 services (embedding, search, generation)
└─ CAG: 1 service (just generation)
```

### Phase 3: Optimize

```
Optimizations for CAG:
1. Format knowledge for scannability
   - Use clear headers
   - Short paragraphs
   - Structure hierarchically

2. Prompt tuning
   - Tell model: "You have complete rulebook"
   - Tell model: "Find relevant section"
   - Example: "Look for rules about surprise..."

3. Token budgeting
   - Can't load massive knowledge bases
   - Prioritize core rules
   - Archive secondary rules

4. Caching
   - Load knowledge once per session
   - Save to memory
   - Reuse across queries
```

## When to Use RAG vs. CAG

### Use RAG When:

✅ Knowledge base is huge (100K+ pages)
✅ Latency is critical (<1 second required)
✅ Cost per query matters (many queries/day)
✅ Can't fit knowledge in context window
✅ Using smaller LLMs (8B model)
✅ Traditional architecture is already built

**Your RAG projects:** [[TTRPG-AI-RAG-Assistant]], [[Arcane-Scribe]], [[AIO Generative AI Solution]]

### Use CAG When:

✅ Knowledge base is medium (100-500 pages)
✅ Accuracy matters more than latency
✅ Want simpler architecture
✅ Have LLM with huge context (200K+)
✅ Using modern frontier models (Claude, GPT-4)
✅ Exploring novel approaches (research)

**Your CAG project:** [[my-cache-augmented-generation]]

## Research Questions for my-cache-augmented-generation

1. **Accuracy Hypothesis:**
   - "CAG is more accurate than RAG for rule questions"
   - Test: Same 100 questions, measure accuracy gap

2. **Latency Trade-Off:**
   - "Is 2-3s load time worth 95% vs. 88% accuracy?"
   - Test: User preference survey (speed vs. correctness)

3. **Optimal Knowledge Size:**
   - "What's sweet spot for TTRPG knowledge?"
   - Test: Vary context size (50K, 100K, 150K, 200K), measure accuracy curve

4. **Model Capability:**
   - "Which LLMs are best for CAG?"
   - Test: Gemini vs. Claude vs. GPT-4 on same knowledge

5. **Integration with brAIniac:**
   - "Could CAG be Phase 2 knowledge layer?"
   - Test: Implement CAG in brAIniac memory management

## Hybrid Approach (CAG + RAG)

**Best of both:**

```
User Query
    ↓
Decision Tree:
├─ If knowledge fits in context window (< 200K tokens)
│  └─ Use CAG (better accuracy)
├─ If knowledge is huge or latency critical
│  └─ Use RAG (faster, cheaper)
└─ If uncertain
   └─ Try CAG, fallback to RAG on timeout
```

## Related Concepts

- [[RAG Pattern for TTRPG]] — Traditional approach
- [[my-cache-augmented-generation]] — CAG implementation
- [[AI/LLM Ecosystem]] — Fits in your AI projects
- [[brAIniac]] — Could use CAG in Phase 2

## Open Questions for Your Ecosystem

- [Should publish CAG results (paper submission)?]
- [Integrate CAG into brAIniac Phase 2?]
- [Benchmark CAG vs. RAG on TTRPG rulebook?]
- [Use CAG for other knowledge bases (medical, legal)?]
- [Hybrid strategy for different knowledge sizes?]

## References

- Paper: "Don't Do RAG: When Cache-Augmented Generation is All You Need for Knowledge Tasks" (Chan et al., 2024)
- arXiv: https://arxiv.org/abs/2412.15605
- Implemented by: [[my-cache-augmented-generation]]
- Compared to: [[TTRPG-AI-RAG-Assistant]], [[Arcane-Scribe]]

## Sources

- [[Wiki/entities/my-cache-augmented-generation]]
- Research paper (Chan et al., 2024)
- TTRPG RAG implementation references
