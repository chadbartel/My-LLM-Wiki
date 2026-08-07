---
type: entity
date_created: 2026-08-07
date_updated: 2026-08-07
tags:
  - wiki/entity
source_count: 1
---

# Obsidian

A local-first, privacy-focused note-taking and knowledge management system built on Markdown.

## Role/Context

Obsidian is the recommended client for implementing the LLM Wiki pattern. It provides:
- **Wikilinks** (bidirectional links between notes)
- **Graph view** (visual representation of note relationships)
- **Plugin ecosystem** (extensions for dataview, daily notes, etc.)
- **Local data ownership** (vault stored as plain markdown files)

## Key Attributes

- **Data Format:** Plain text Markdown files in a local vault folder
- **License:** Proprietary (free core, paid plugins/sync)
- **Platform:** Desktop (Windows, macOS, Linux) + Mobile (iOS, Android)
- **Key Feature:** Wikilinks (`[[Note Name]]`) enable bidirectional linking and graph view
- **Sync:** Optional (Obsidian Sync, Git, Dropbox, iCloud)

## Key Relationships

- [[LLM Wiki Pattern]] — Obsidian is the recommended client for implementing this pattern
- [[Obsidian CLI]] — Programmatic interface to Obsidian vaults
- [[Obsidian Web Clipper]] — Browser extension that works with Obsidian
- [[Dataview Plugin]] — Popular plugin for querying vault metadata
- [[qmd]] — Alternative search tool that can index Obsidian vaults

## Why It Fits the Wiki Pattern

1. **Wikilinks** make it easy to build dense relationship graphs
2. **Graph view** visualizes emergent structure (hubs, clusters, orphans)
3. **Plain text** ensures data portability and longevity
4. **Local-first** respects privacy and data ownership
5. **Plugin ecosystem** enables customization without vendor lock-in

## Sources

- [[Wiki/sources/karpathy-llm-wiki-pattern]] — Recommends Obsidian as KB client
- [[Wiki/sources/obsidian-second-brain]] — Deep dive into Obsidian features and methodology
