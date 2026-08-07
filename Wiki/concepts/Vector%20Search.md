---
type: concept
date_created: 2026-08-07
date_updated: 2026-08-07
tags:
  - wiki/concept
source_count: 1
confidence: high
---

# Vector Search

Search method that finds semantically similar documents by comparing numerical embeddings rather than matching keywords.

## Definition

Vector search converts text to numerical vectors in high-dimensional space. Semantically similar texts land near each other, enabling search based on meaning rather than exact word matches.

**Process:**
1. Index phase: Convert all documents to embeddings, store them
2. Query phase: Convert user query to embedding
3. Search phase: Find vectors nearest to query vector
4. Return phase: Return documents in order of similarity

## Advantages Over Keyword Search

| Problem | Keyword (BM25) | Vector Search |
|---------|---|---|
| Synonyms | "memory" doesn't match "context" | ✓ Both match same semantic space |
| Paraphrase | "How do I keep state?" doesn't match "maintaining session information" | ✓ Same meaning matches |
| Typos | "meory" matches nothing | Often still works (depends on model) |
| Multilingual | Requires translation | Can work cross-language |

## Disadvantages

- Slower than keyword search (but still fast with modern tools)
- Requires embedding model (adds complexity)
- Less explainable (why did this document match?)
- Requires infrastructure (vector database)

## When to Use

- Synonyms and paraphrasing matter
- Multilingual documents
- Semantic understanding required
- Can tolerate slightly slower search

## Related Concepts

- [[Vector Embeddings]] — The numerical representation vectors use
- [[Hybrid Search]] — Combines vector search with keyword matching
- [[Cosine Similarity]] — Metric for measuring vector distance
- [[LLM Re-ranking]] — Ordering vector results by relevance

## Key Entities

- [[FAISS]] — Large-scale vector database
- [[qmd]] — Vector search for wikis
- [[Sentence-BERT]] — Embedding model

## Confidence Level

**High** — Vector search is well-established technology with proven effectiveness.

## Sources

- [[Wiki/sources/vector-search-knowledge-systems]] — Comprehensive technical explanation
- [[Wiki/sources/karpathy-llm-wiki-pattern]] — Mentions vector search as tool for mature wikis
