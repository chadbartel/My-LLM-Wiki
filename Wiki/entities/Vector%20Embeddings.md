---
type: entity
date_created: 2026-08-07
date_updated: 2026-08-07
tags:
  - wiki/entity
source_count: 1
---

# Vector Embeddings

Numerical representation of text as points in high-dimensional space.

## Role/Context

Vector embeddings enable semantic search by converting text into vectors such that semantically similar texts are located near each other in vector space.

## Key Attributes

- **Dimensionality**: Typically 768-4096 dimensions (depending on model)
- **Metric**: Compared using cosine similarity, Euclidean distance, or similar
- **Model-dependent**: Different embedding models (BERT, Sentence-BERT, Word2Vec) produce different quality embeddings
- **Static**: Same text always produces same embedding (deterministic)

## Types

- **Word Embeddings** (Word2Vec, GloVe) — Individual words as vectors
- **Sentence Embeddings** (Sentence-BERT) — Entire sentences as vectors
- **Document Embeddings** (BERT) — Full documents as vectors

## Use in Knowledge Bases

- Convert user query to embedding
- Compare against all document embeddings
- Return documents with highest cosine similarity
- More effective than keyword matching for synonyms and semantic equivalents

## Key Relationships

- [[Vector Search]] — Uses embeddings to find similar documents
- [[Hybrid Search]] — Combines embeddings with keyword search
- [[qmd]] — Tool that implements vector search for wikis

## Sources

- [[Wiki/sources/vector-search-knowledge-systems]] — Technical explanation of embeddings
