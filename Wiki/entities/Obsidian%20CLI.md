---
type: entity
date_created: 2026-08-07
date_updated: 2026-08-07
tags:
  - wiki/entity
source_count: 1
---

# Obsidian CLI

Command-line interface for Obsidian that enables programmatic access to vault operations.

## Role/Context

The CLI allows scripts and LLM agents to read, create, update, and search notes without opening the Obsidian GUI.

## Key Attributes

- **Availability:** Built into Obsidian 1.12+
- **Setup:** Must be registered in Obsidian settings, then symlinked into PATH
- **Platform:** macOS, Linux, Windows
- **Use Cases:** Automation, LLM integration, scripting

## Common Commands

```bash
obsidian read file="My Note"                    # read a note
obsidian create name="New Note" content="# Hello" silent
obsidian append file="My Note" content="New line"
obsidian search query="search term" limit=10
obsidian tasks todo                             # list open tasks
obsidian property:set name="status" value="done" file="My Note"
```

## Key Relationships

- [[LLM Wiki Pattern]] — CLI enables automated wiki maintenance
- [[Obsidian]] — CLI is the programmatic interface to Obsidian

## Sources

- [[Wiki/sources/karpathy-llm-wiki-pattern]] — Lists CLI as a tool for the wiki pattern
