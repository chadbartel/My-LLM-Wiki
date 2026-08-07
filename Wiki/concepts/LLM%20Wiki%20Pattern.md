---
type: concept
date_created: 2026-08-07
date_updated: 2026-08-07
tags:
  - wiki/concept
source_count: 1
confidence: high
---

# LLM Wiki Pattern

A methodology for using LLMs to incrementally build and maintain a persistent, interlinked knowledge base rather than re-deriving knowledge on every query.

## Definition

The LLM Wiki pattern proposes a three-layer architecture:

1. **Raw Sources** — Immutable inputs (articles, papers, clippings). Never modified by the LLM.
2. **Knowledge Base** — LLM-maintained summaries, entity pages, concept pages, relationships. Updated incrementally.
3. **Schema** — Rules document (e.g., CLAUDE.md) that defines page structure, operations, and critical rules.

The LLM's job is to be a disciplined librarian: reading sources carefully, extracting facts, connecting ideas, and maintaining the KB according to the schema.

## Why It Matters

Most LLM workflows treat each query as an isolated prediction problem. But knowledge is cumulative. The wiki pattern makes this explicit:

- **Compound Learning**: Each source makes the KB better. Future queries benefit from all previous ingestions.
- **Consistency**: The schema ensures the KB stays coherent as it grows.
- **Explainability**: You can trace any claim back to its source.
- **Efficiency**: You don't re-read sources for every query; you query the KB.

## Key Examples

- **Early stage (2-3 sources):** Manual ingestion to calibrate templates. [[Wiki/sources/karpathy-llm-wiki-pattern]] and [[Wiki/sources/obsidian-second-brain]] establish the foundation.
  
- **Growing stage (50+ sources):** Add hybrid search (qmd) as manual indexing becomes insufficient.

- **Mature stage (200+ sources):** Vector search + LLM re-ranking for sophisticated semantic queries.

## Related Concepts

- [[Three-Layer Architecture]] — The structural foundation of the pattern
- [[Schema Document]] — Rules that enforce consistency
- [[Source Immutability]] — Why raw sources never change
- [[Compound Learning]] — How knowledge compounds over time
- [[KB Drift]] — Common problem this pattern prevents

## Key Entities

- [[Andrej Karpathy]] — Originated the pattern
- [[Obsidian]] — Recommended KB client
- [[qmd]] — Search tool for mature wikis

## Confidence Level

**High** — The pattern is well-documented, widely adopted, and proven effective across multiple implementations.

## Sources

- [[Wiki/sources/karpathy-llm-wiki-pattern]] — Primary source defining the pattern
