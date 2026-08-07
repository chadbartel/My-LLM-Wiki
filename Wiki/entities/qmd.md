---
type: entity
date_created: 2026-08-07
date_updated: 2026-08-07
tags:
  - wiki/entity
source_count: 1
---

# qmd (Query Model Database)

A hybrid BM25/vector search tool designed for knowledge bases and wikis.

## Role/Context

`qmd` provides search capabilities beyond simple keyword matching. It combines:
- **BM25** (traditional keyword search)
- **Vector search** (semantic similarity)
- **LLM re-ranking** (relevance ordering)

Useful when an LLM wiki grows beyond 50-100 sources and manual indexing becomes insufficient.

## Key Attributes

- **Language:** Go
- **Architecture:** Hybrid search (keyword + semantic + LLM)
- **Data Source:** Indexes Markdown files locally
- **Interface:** CLI + MCP server (for LLM agents)
- **Cost:** Open source, runs locally (no cloud dependency)

## Use Cases

- Search 100+ note vault for semantically related concepts
- Find notes using different terminology for the same idea
- LLM agents can use qmd as a native tool via MCP server

## Key Relationships

- [[LLM Wiki Pattern]] — Recommended search tool for mature wikis (200+ sources)
- [[Vector Search]] — Core technology that qmd uses
- [[Obsidian]] — qmd can index Obsidian vaults

## Installation Path

```bash
go install github.com/tobi/qmd@latest
qmd collection add my-vault /path/to/vault "**/*.md"
qmd update && qmd embed
qmd query "your search query"
```

## When to Use

- **< 50 sources:** Skip qmd, use manual wikilinks + `index.md`
- **50-200 sources:** Add qmd for semantic search
- **200+ sources:** Full hybrid search + LLM re-ranking

## Sources

- [[Wiki/sources/karpathy-llm-wiki-pattern]] — Recommends qmd as search tool
- [[Wiki/sources/vector-search-knowledge-systems]] — Technical background on how qmd works
