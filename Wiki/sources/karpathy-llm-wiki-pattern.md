---
type: source-summary
date_ingested: 2026-08-07
tags:
  - wiki/source
---

# Source: The LLM Wiki Pattern — Building Knowledge Incrementally

## Source Metadata

- **Author:** Andrej Karpathy
- **Date Published:** 2023-03-15
- **URL:** https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
- **Relevance:** Foundational pattern for building persistent knowledge bases with LLMs. Directly inspired this wiki setup.

---

## Summary

The LLM Wiki pattern proposes that instead of treating each query as an isolated prediction problem, you should incrementally build a persistent knowledge base that the LLM queries and updates. The architecture consists of three layers: immutable raw sources, a structured knowledge base (KB) maintained by the LLM, and a schema document that defines how to maintain the KB consistently.

---

## Key Points

- **Three-Layer Architecture**: Raw sources (immutable ground truth) → Knowledge base (LLM-generated summaries, entities, concepts, relationships) → Schema (rules for maintaining the KB)
  
- **Why it matters**: Knowledge is cumulative. Instead of re-deriving everything on each query, the KB compounds over time. Each ingested source makes future queries more powerful.

- **Source Summaries**: Factual extracts only (no interpretation). Extract key entities and concepts from each source.

- **Entity Pages**: One page per person, tool, organization, or concept. Links back to sources that mention it.

- **Concept Pages**: One page per idea or pattern. Includes definition, examples, related concepts, confidence level (high/medium/low based on source evidence).

- **Schema Document**: Rules for page structure (frontmatter, wikilinks, inline metadata), operations (ingest, query, lint), and critical rules (immutability, contradiction handling).

- **Operations**:
  - **Ingest**: Read raw source → create source summary → create/update entity pages → create/update concept pages → update index/log
  - **Query**: Read index → read relevant pages → synthesize answer → file back as synthesis page
  - **Lint**: Health-check for orphans, broken links, stale pages, contradictions, missing cross-references

- **Avoid Drift**: Without an explicit schema, the KB degrades as different people change folder layouts, frontmatter formats, or indexing rules. Solution: encode all rules in a CLAUDE.md or schema document.

- **Calibrate First**: Ingest 2-3 rich sources manually to calibrate templates before batching the rest.

- **Let the LLM Write**: The human reviews; the LLM writes all KB pages. This ensures consistency and reduces manual overhead.

- **Contradiction Handling**: When sources conflict, note it explicitly (don't silently overwrite). Flag for human review.

---

## Entities Mentioned

- [[Andrej Karpathy]] — Author of the LLM Wiki pattern
- [[Obsidian]] — Recommended KB client (wikilinks, graph view, plugins)
- [[qmd]] — Hybrid BM25/vector search tool for wikis
- [[Obsidian CLI]] — Programmatic access to read/create/update notes
- [[Obsidian Web Clipper]] — Tool for capturing web articles as markdown

---

## Concepts Introduced

- [[LLM Wiki Pattern]] — Incremental knowledge base architecture with immutable sources and LLM-maintained summaries
- [[Three-Layer Architecture]] — Raw sources → KB → Schema (the fundamental structure)
- [[Schema Document]] — CLAUDE.md or equivalent; defines page templates, operations, and critical rules
- [[Compound Learning]] — Each source makes the KB slightly better; knowledge compounds over time
- [[KB Drift]] — Common problem where inconsistent rules degrade KB quality over time
- [[Contradiction Handling]] — Strategy for managing conflicting claims from different sources
- [[Source Immutability]] — Raw sources are never modified; wiki layer is where clarifications go
- [[LLM as Librarian]] — Framing the LLM not as a chatbot but as a disciplined knowledge maintainer

---

## Direct Quotes

> "Instead of asking the LLM to re-derive everything on every query, you're asking it to be a disciplined librarian: reading sources carefully, extracting facts, connecting ideas, and maintaining the KB according to a consistent schema."

> "Most LLM workflows treat every query as fresh reasoning from first principles. But knowledge is cumulative. If you ask the LLM the same question twice, it should give you a better answer the second time because it's built on top of all the sources it's already processed."

> "Start small. Ingest 2-3 rich sources manually to calibrate templates before automating the rest."

---

## Related Sources

- [[Wiki/sources/obsidian-second-brain]] — Complements this source by explaining Obsidian as the KB client

---

## Ingestion Notes

This is a foundational meta-source that directly describes the system being built. High value for understanding architecture. Templates were calibrated using this source and should feel familiar when re-reading.
