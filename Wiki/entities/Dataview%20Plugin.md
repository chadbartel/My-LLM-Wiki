---
type: entity
date_created: 2026-08-07
date_updated: 2026-08-07
tags:
  - wiki/entity
source_count: 1
---

# Dataview Plugin

Obsidian plugin that provides SQL-like query capabilities over vault metadata and frontmatter.

## Role/Context

Dataview enables querying your vault as if it were a database. Perfect for the LLM wiki pattern because every wiki page has structured frontmatter (type, date_updated, source_count, confidence, tags).

## Key Attributes

- **Query Language:** SQL-like syntax
- **Data Source:** YAML frontmatter + inline metadata
- **Output:** Dynamic tables, lists, task views
- **Use Cases:** 
  - "Show all concepts tagged wiki/concept created in 2024"
  - "List all entities mentioned in more than 3 sources"
  - "Find stale pages (not updated in 30 days)"

## Example Query

```
table source_count, confidence, date_updated
from "Wiki/concepts"
where type = "concept" and confidence = "high"
sort date_updated desc
```

This shows all high-confidence concepts, sorted by most recently updated.

## Key Relationships

- [[Obsidian]] — The plugin that hosts Dataview
- [[LLM Wiki Pattern]] — Dataview enables health checks and querying

## Sources

- [[Wiki/sources/obsidian-second-brain]] — Recommends Dataview for querying vault metadata
