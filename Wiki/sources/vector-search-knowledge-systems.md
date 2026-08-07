---
type: source-summary
date_ingested: 2026-08-07
tags:
  - wiki/source
---

# Source: Vector Search and Semantic Understanding in Knowledge Systems

## Source Metadata

- **Author:** Dr. Sarah Chen
- **Date Published:** 2024-02-20
- **Publication:** Journal of Knowledge Engineering
- **URL:** https://example.com/vector-search-knowledge
- **Relevance:** Technical foundation for semantic search in knowledge bases. Explains how qmd and similar tools work at the algorithmic level.

---

## Summary

Vector search converts text to numerical embeddings in high-dimensional space, enabling semantic (meaning-based) search beyond simple keyword matching. The article covers word embeddings (Word2Vec, GloVe), sentence/document embeddings (BERT, Sentence-BERT), tools for knowledge bases (FAISS, qmd, Weaviate), hybrid search strategies (BM25 + vector + LLM re-ranking), and implementation guidance for scaling from small to large wikis.

---

## Key Points

- **Limitations of Keyword Search**: Traditional BM25 (TF-IDF) searches for words. "LLM memory" doesn't match "context window" even though they're semantically equivalent. This creates false negatives.

- **Vector Embeddings**: Text is converted to vectors (points in high-dimensional space). Semantically similar texts land near each other in this space.

- **Word Embeddings (Word2Vec, GloVe)**: Early approach treating individual words as points. Captures semantic relationships (e.g., king - man + woman ≈ queen).

- **Sentence/Document Embeddings (BERT, Sentence-BERT)**: Modern approach encoding entire sentences/documents. Captures semantic meaning at the text level, not just words.

- **Semantic Search**: Query is converted to embedding, compared against document embeddings using cosine similarity or similar metrics. Returns semantically related documents regardless of word overlap.

- **Tools for Knowledge Bases**:
  - **FAISS** — Extremely fast, scalable (billions of vectors), requires programming
  - **qmd** — Hybrid (BM25 + vector), MCP server, designed for wikis, simple CLI
  - **Weaviate, Pinecone, Milvus** — Cloud/self-hosted, powerful but overkill for personal wikis

- **Hybrid Search**: Combine BM25 (keywords) + vector search (semantic) + LLM re-ranking (relevance ordering).
  1. BM25 finds keyword matches
  2. Vector search finds semantically related notes
  3. LLM re-ranks by relevance to actual user intent
  4. Result: Most relevant notes rank first

- **Hybrid Search Example**: Query "How do I keep a chatbot's memory fresh?"
  - BM25 finds: Notes with "memory," "cache," "conversation"
  - Vector finds: Notes about "context management," "session state," "prompt engineering"
  - LLM ranks: Most relevant combination first

- **Scaling Strategy**:
  - **< 50 sources:** Keyword search sufficient (manual wikilinks in index.md)
  - **50-200 sources:** Add qmd hybrid search
  - **200+ sources:** Add vector re-ranking and LLM synthesis
  - **Beyond 500 sources:** Consider knowledge graph databases

- **Future Direction - Query Expansion**: LLM expands user query into multiple interpretations, searches all variants, ranks by relevance. E.g., "performance" → ["performance", "speed", "latency", "throughput", "efficiency", "optimization"].

- **Tradeoffs**: Speed vs semantic understanding. Keyword is fast, vector is more accurate, hybrid is best compromise.

---

## Entities Mentioned

- [[qmd]] — Tool combining BM25 + vector + LLM re-ranking
- [[FAISS]] — Industrial-standard vector database (Facebook)
- [[BERT]] — Language model for embeddings (Google)
- [[Sentence-BERT]] — Document-level embeddings
- [[Word2Vec]] — Early word embedding technique
- [[GloVe]] — Alternative word embedding approach
- [[Weaviate]] — Cloud vector database
- [[Pinecone]] — Cloud vector database
- [[Milvus]] — Self-hosted vector database
- [[LLM Re-ranking]] — Using LLM to order search results by relevance

---

## Concepts Introduced

- [[Vector Search]] — Semantic search using numerical embeddings
- [[Vector Embeddings]] — Numerical representation of text in high-dimensional space
- [[Word Embeddings]] — Point-in-space representation of individual words
- [[Document Embeddings]] — Numerical representation of entire documents/sentences
- [[Semantic Similarity]] — Finding texts with similar meaning regardless of word choice
- [[Hybrid Search]] — Combining BM25 + vector search + LLM re-ranking
- [[Cosine Similarity]] — Metric for comparing vectors
- [[Query Expansion]] — Expanding single query into multiple semantic interpretations
- [[Knowledge Graph]] — Graph-based representation of knowledge (alternative to vector DB)
- [[LLM Re-ranking]] — Using LLM to order search results by user intent
- [[Scaling Strategy for Knowledge Bases]] — How to choose search technology at different scales

---

## Direct Quotes

> "Traditional keyword-based search misses semantic equivalents. 'LLM memory' doesn't match 'context window' even though they're semantically equivalent. Vector search solves this by converting text to numerical embeddings in high-dimensional space."

> "For personal wikis, hybrid search (keyword + vector + LLM re-ranking) is the sweet spot. You get semantic understanding without the infrastructure overhead."

> "The key is to avoid premature optimization while leaving room to scale. Start simple; scale complexity only when you need it."

---

## Related Sources

- [[Wiki/sources/karpathy-llm-wiki-pattern]] — Recommends qmd for mature wikis
- [[Wiki/sources/obsidian-second-brain]] — Mentions qmd as search tool

---

## Ingestion Notes

This is a technical/academic source providing the algorithmic foundation for tools like qmd. Unlike the previous sources (architectural and methodological), this one is focused on technology implementation. Note the different structure of entities (algorithms and tools rather than applications) and concepts (technical computer science rather than knowledge management philosophy).

Different source types will naturally create different entity and concept profiles. This is healthy—it shows the wiki capturing diverse perspectives.
