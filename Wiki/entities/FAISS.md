---
type: entity
date_created: 2026-08-07
date_updated: 2026-08-07
tags:
  - wiki/entity
source_count: 1
---

# FAISS (Facebook AI Similarity Search)

Industry-standard vector database for similarity search at scale.

## Role/Context

FAISS is the de-facto standard for efficient vector search in large datasets (billions of vectors). Used by researchers, companies, and production systems.

## Key Attributes

- **Creator**: Facebook (Meta) Research
- **Language**: C++ with Python bindings
- **Scalability**: Can handle billions of vectors
- **Speed**: Extremely fast nearest-neighbor search
- **Algorithms**: Multiple indexing strategies (IVF, HNSW, etc.) for different tradeoffs

## Advantages

- Proven in production at massive scale
- Active research community
- Highly optimized
- Supports GPUs

## Disadvantages

- Requires programming (C++/Python)
- Steeper learning curve
- Less beginner-friendly than qmd

## Key Relationships

- [[Vector Search]] — FAISS is one implementation
- [[qmd]] — Simpler alternative for wikis/knowledge bases

## When to Use

- Research and development
- Production systems with billions of vectors
- When raw speed is paramount

## Sources

- [[Wiki/sources/vector-search-knowledge-systems]] — Recommends FAISS for large-scale applications
