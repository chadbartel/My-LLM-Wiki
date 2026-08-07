---
type: concept
date_created: 2026-08-07
date_updated: 2026-08-07
tags:
  - wiki/concept
source_count: 1
confidence: high
---

# Hybrid Search

Search strategy combining keyword matching (BM25) with vector search and LLM re-ranking.

## Definition

Hybrid search runs multiple search methods in parallel and combines results:

1. **BM25** (keyword search) — Find exact and partial word matches
2. **Vector Search** (semantic search) — Find semantically similar documents
3. **LLM Re-ranking** (relevance ordering) — Order results by relevance to actual user intent

## Why Hybrid Works Better

Each method catches what others miss:

- **BM25** catches exact-word queries ("Obsidian" or "FAISS")
- **Vector** catches semantic queries ("tools for maintaining state")
- **LLM re-ranking** orders results by what the user actually meant

## Example

Query: "How do I keep a chatbot's memory fresh?"

**BM25 results:**
- Note with "memory"
- Note with "cache"
- Note with "conversation"

**Vector results:**
- Note about "context window management"
- Note about "session state"
- Note about "prompt engineering"

**Combined + LLM re-ranked:**
1. Note about "prompt engineering for memory management" (combines BM25 keyword + vector semantic)
2. Note about "context window management"
3. Note with "memory"
4. ...

## Scaling Strategy

- **< 50 sources:** Keyword search (manual indexing)
- **50-200 sources:** Add hybrid search (qmd)
- **200+ sources:** Add LLM re-ranking
- **500+ sources:** Consider knowledge graph DB

## Implementation

Most tools implement this automatically:

```bash
qmd query "How do I keep a chatbot's memory fresh?"
# Automatically runs BM25 + vector + LLM re-ranking
```

## Related Concepts

- [[Vector Search]] — The semantic component
- [[LLM Re-ranking]] — The ranking component
- [[Cosine Similarity]] — How vectors are compared
- [[Query Expansion]] — Future direction for hybrid search

## Key Entities

- [[qmd]] — Tool that implements hybrid search for wikis
- [[FAISS]] — Vector database (one component)

## Confidence Level

**High** — Hybrid search is the current best practice for knowledge base search.

## Sources

- [[Wiki/sources/vector-search-knowledge-systems]] — Explains hybrid search as pragmatic approach
