---
type: concept
date_created: 2026-08-07
date_updated: 2026-08-07
tags:
  - wiki/concept
source_count: 1
confidence: high
---

# Compound Learning

The principle that a knowledge base improves over time as each new source is ingested, with each addition making future queries more powerful.

## Definition

Instead of treating each query as an isolated problem (where the LLM starts from scratch), compound learning recognizes that:

1. Each source adds entities, concepts, and relationships to the KB
2. Future queries benefit from the accumulated context
3. The KB becomes a more powerful reasoning tool with each update
4. The LLM can synthesize across multiple sources, not just within one

## Why It Matters

- **Efficiency**: You don't re-read the same source twice
- **Depth**: Queries can connect insights from multiple sources
- **Evolution**: The KB's understanding of a topic deepens as you ingest more sources on that topic
- **Serendipity**: You discover unexpected connections between sources

## Key Examples

- **After 1 source**: You have a definition of "LLM Wiki Pattern"
- **After 3 sources**: You see how pattern relates to Obsidian, vector search, and knowledge management
- **After 20 sources**: You have a rich, interconnected view of how different tools and techniques complement each other

## Contrast

**Without compound learning** (traditional LLM workflow):
- User asks "How do I build a wiki?"
- LLM re-reads all documents from scratch
- LLM generates an answer
- Knowledge is thrown away after the query

**With compound learning** (LLM wiki pattern):
- Ingest sources once (create KB pages once)
- User asks "How do I build a wiki?"
- LLM reads the KB (not raw sources)
- LLM synthesizes across pre-organized entity and concept pages
- Answer gets filed back into KB for future reference

## Related Concepts

- [[LLM Wiki Pattern]] — The framework that enables compound learning
- [[KB Drift]] — Risk when compound learning isn't managed consistently
- [[Source Immutability]] — Enables compound learning by providing stable ground truth

## Confidence Level

**High** — This is a core principle validated by implementations of the LLM wiki pattern.

## Sources

- [[Wiki/sources/karpathy-llm-wiki-pattern]] — Explains compound learning as a benefit of the pattern
