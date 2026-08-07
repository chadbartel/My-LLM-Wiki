---
type: concept
date_created: 2026-08-07
date_updated: 2026-08-07
tags:
  - wiki/concept
  - architecture
  - ai-pattern
confidence: high
source_count: 3
---

# RAG Pattern for TTRPG

Retrieval Augmented Generation (RAG) approach to TTRPG queries: ingest rulebooks as documents, generate embeddings, enable semantic search, and provide AI-powered answers grounded in source material.

## Definition

RAG = Document Storage + Semantic Search + LLM Generation

Take TTRPG rulebooks (PDFs), convert to machine-readable embeddings, store in vector database, then answer player/GM questions by:
1. Finding semantically similar rules via vector search
2. Passing those rules to LLM for answer generation
3. Grounding response in actual rulebook text

## Why RAG for TTRPG?

**Problem:**
- TTRPG rulebooks are hundreds of pages
- Players/GMs need fast rule clarification mid-session
- Manual PDF search is slow and error-prone

**Solution:**
- Vector embeddings capture semantic meaning ("Can you cast fireball in sunlight?" matches spell description even without exact keywords)
- LLM synthesizes answer from multiple rule sections
- Fast lookup (milliseconds with vector search)

## Architecture

```
                INGESTION PIPELINE
                        
PDF Rulebook (e.g., D&D 5e)
    ↓ (PyMuPDF4LLM)
Raw Text Chunks (~1000-word chunks)
    ↓ (Tokenize & Clean)
Processed Chunks
    ↓ (Embedding API: Gemini or Bedrock)
Dense Vectors (384-4096 dimensions)
    ↓ (Store)
Vector Database (Chromadb or FAISS)


                QUERY PIPELINE
                
User Question: "Can I use fireball on 3 kobolds?"
    ↓ (Embed question with same model)
Question Vector
    ↓ (Semantic Search)
Top K Similar Chunks (e.g., spell descriptions, area effects)
    ↓ (Retrieve Context)
Context + Question
    ↓ (LLM Pass)
Response: "Yes, fireball affects 20-foot radius sphere,
          dealing 8d6 fire damage to each creature..."
```

## The Three Layers

### Layer 1: Document Processing (Ingestion)
- **Input:** TTRPG PDF (e.g., D&D 5e Player's Handbook)
- **Tool:** PyMuPDF4LLM (clean text extraction, no OCR needed)
- **Output:** Text chunks ready for embedding
- **Used By:** All 3 RAG projects ([[TTRPG-AI-RAG-Assistant]], [[AIO Generative AI Solution]], [[Arcane-Scribe]])

**Example:**
```
Input PDF: "Fireball (6th level evocation spell)..."
Output Chunks:
  - "Fireball affects a 20-foot-radius sphere..."
  - "Each creature in that area must make a Dexterity save..."
  - "Casting time: 1 action. Range: 150 feet..."
```

### Layer 2: Embedding & Storage (Vector Database)
- **Input:** Text chunks from Layer 1
- **Tool:** Embedding API (Google Gemini or AWS Bedrock)
- **Storage:** Vector database (Chromadb for local, FAISS for serverless)
- **Output:** Searchable vectors with semantic meaning

**Example:**
```
Text: "Fireball affects a 20-foot-radius sphere"
Embedding: [0.123, -0.456, 0.789, ...] (384+ dimensions)
  ↓ (Stored in vector database)
Can be searched by semantic similarity
```

**Vector Databases:**
- **Chromadb** — Local file-based (used by [[TTRPG-AI-RAG-Assistant]], [[AIO Generative AI Solution]])
- **FAISS** — CPU-based indexing (used by [[Arcane-Scribe]] in Lambda)
- **Pinecone** — Managed cloud (alternative, not currently used)

### Layer 3: Query & Generation (LLM)
- **Input:** User question + retrieved rulebook chunks
- **LLM:** Google Gemini or AWS Bedrock (same service that did embeddings)
- **Output:** Natural language answer grounded in source material

**Example:**
```
Question: "Can I cast fireball on the ground?"
Retrieved Context: [spell descriptions, area effect rules, ...]
LLM Prompt: "Based on these D&D 5e rules, answer: Can I cast fireball on the ground?"
Response: "Yes. Fireball affects all creatures in a 20-foot-radius
          sphere. You can target any point you can see within range..."
```

## Why Three Projects Use This Pattern

| Project | Reason | Differences |
|---------|--------|-------------|
| [[TTRPG-AI-RAG-Assistant]] | Query over rulebooks | Local Docker, Gemini, Chromadb |
| [[AIO Generative AI Solution]] | Query over rulebooks | Local Docker, Gemini, Chromadb (similar to above) |
| [[Arcane-Scribe]] | Enterprise query service | AWS Lambda, Bedrock, FAISS |

**Key Insight:** All three use the same RAG pattern but differ in deployment and LLM provider.

## Comparison: Gemini-Based vs. Bedrock-Based

| Aspect | Gemini (Local RAG) | Bedrock (Arcane-Scribe) |
|--------|-------------------|------------------------|
| **Embeddings API** | Google Gemini | Amazon Titan |
| **LLM** | Gemini 1.5, 1.0, Flash | Claude 3.5 Haiku |
| **Storage** | Chromadb (local) | S3 + FAISS (Lambda) |
| **Deployment** | Docker container | AWS Lambda |
| **Cost** | Gemini API pricing | Bedrock + Lambda pricing |
| **Scalability** | Single-instance local | Auto-scaling serverless |
| **Latency** | ~500ms warm start | ~100ms (Lambda warm) |

## Embedding Quality Matters

Different embedding models capture semantic meaning differently:

```
Question: "Can I cast fireball in water?"
Good embeddings will match:
  ✓ Spell descriptions mentioning "fire" or "water"
  ✓ Rules about elemental interactions
  ✓ Component requirements (verbal, somatic, material)

Poor embeddings might miss context:
  ✗ Only keyword matching ("fireball" + "water")
  ✗ Ignoring semantic relationships
```

## Chunk Size Trade-offs

```
Chunk Size    | Pros                      | Cons
─────────────────────────────────────────────────
Small (100 words) | Precise context     | May need more chunks
Medium (500 words) | Good balance       | Standard choice
Large (2000 words) | Less API calls     | May retrieve irrelevant text
```

All three RAG projects use ~1000-word chunks as default.

## Vector Search Mechanics

When you ask "Can wizards use fireball?", the system:

1. **Embeds your question** into same vector space as rulebook chunks
2. **Searches for similar vectors** using cosine similarity (or Euclidean distance)
3. **Returns top K results** (usually top 3-5 most similar chunks)
4. **Passes to LLM** along with your question
5. **LLM synthesizes answer** using the retrieved context

**Why this works:**
- "Can a wizard cast fireball?" embeds similarly to "Wizards can cast fireball spells"
- Vector search finds that chunk despite different wording
- No exact keyword matching needed

## When RAG Shines vs. When It Struggles

✓ **Works Well:**
- Rule clarifications ("What does X spell do?")
- Class ability lookups ("Can rogues do sneak attack?")
- Equipment descriptions ("How much does plate armor weigh?")

✗ **Struggles:**
- Multi-step logical reasoning ("If I'm paralyzed, can I cast concentration spells?")
- Edge cases ("What happens if...")
- Homebrew rules integration (RAG needs documents)

**Workaround:** [[Automated-Taskmaster]] can generate content that [[TTRPG-AI-RAG-Assistant]] can then refine via RAG.

## Maintenance & Updates

**When you add a new rulebook:**
1. Upload PDF to project (e.g., new sourcebook, module)
2. System extracts text and generates embeddings
3. Vectors added to database
4. Queries now search expanded knowledge base

**Example:** Add Xanathar's Guide to Everything
```
New rulebook uploaded
  → Text chunks extracted
  → Embeddings generated via Gemini/Bedrock
  → Added to Chromadb/FAISS
  → Now queries can reference new rules
```

## Advanced: Reranking & Filtering

Production RAG systems (like [[Arcane-Scribe]]) often add:
1. **Semantic Reranking:** Re-rank retrieved chunks by relevance before LLM
2. **Metadata Filtering:** Filter by book name, page number, rule type
3. **Query Expansion:** "Can I cast fireball?" → expanded to multiple search queries

These improve accuracy but add complexity.

## Cost & Performance

| Aspect | Local (Gemini) | Serverless (Bedrock) |
|--------|---|---|
| **API Calls** | Pay per embedding + generation | Same |
| **Storage** | Free (local disk) | S3 charges (~$1/month) |
| **Compute** | Docker container (your hardware) | Lambda ($0.20/million invocations) |
| **Total for Low Usage** | ~$5-10/month | ~$5-10/month |
| **Total for High Usage** | ~$50-100/month | ~$50-500/month (scales) |

## Related Concepts

- [[TTRPG Ecosystem]] — Overview of your 5 TTRPG projects
- [[Multi-Provider LLM Integration]] — Gemini vs. Bedrock comparison
- [[Serverless TTRPG Services]] — Bedrock architecture in Lambda
- [[Vector Embeddings]] — How text becomes vectors

## Key Takeaways

1. **RAG is the pattern:** Document → Embedding → Vector Search → LLM
2. **Three implementations:** All use RAG; differ in deployment/LLM
3. **Fast & accurate:** Semantic search finds relevant rules quickly
4. **Grounded:** Answers cite actual rulebook text
5. **Extensible:** Add new books without retraining

## Open Questions

- [Should embed [[UnnamedRPG]] rules automatically?]
- [Reranking layer worth adding to [[TTRPG-AI-RAG-Assistant]]?]
- [Multi-language support (French D&D books)?]
- [Fine-tuned embeddings for TTRPG domain?]

## Sources

- [[Wiki/entities/TTRPG-AI-RAG-Assistant]]
- [[Wiki/entities/AIO Generative AI Solution]]
- [[Wiki/entities/Arcane-Scribe]]
- RAG architecture analysis from pyproject.toml + app.py patterns
