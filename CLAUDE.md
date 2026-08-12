# CLAUDE.md — AI Coding Guide for LLM Wiki Maintenance

This document is the **schema layer** that makes you a disciplined LLM-guided wiki maintainer. When working with the wiki, follow these rules and procedures exactly.

## The Six Phases

The wiki building process is organized into 6 phases:

1. **Phase 1-4:** Ingestion (TTRPG, AI/LLM, AWS Infrastructure, Utilities & Learning) — ✓ COMPLETE
2. **Phase 5:** Synthesis (ADHD-optimized context-switching guides) — ✓ COMPLETE
3. **Phase 6:** Automated Monitoring (Wiki auto-sync system) — ✓ COMPLETE

### Phase 6: Automated Monitoring

**Purpose:** Keep wiki synchronized with workspace projects automatically.

**Components:**
- `scripts/sync-wiki.py` — Main sync script (700+ lines)
- `Wiki/.last-sync.json` — State tracking file
- `.github/workflows/wiki-sync.yml` — GitHub Actions automation
- `scripts/README.md` — Quick reference guide
- `Wiki/synthesis/Phase-6-Automated-Monitoring.md` — Full documentation

**How to Use:**
```bash
# Preview changes (safe)
python3.12 /mnt/c/Users/Chaddle/Documents/ObsidianVault/scripts/sync-wiki.py --verbose --dry-run

# Apply changes
python3.12 /mnt/c/Users/Chaddle/Documents/ObsidianVault/scripts/sync-wiki.py --verbose

# Runs automatically: Every Monday 9 AM UTC via GitHub Actions
```

**What It Does:**
- Scans all 20+ workspace projects
- Detects: new projects, status changes, file modifications, dependency updates
- Auto-updates entity pages, synthesis pages, log.md
- Creates new entity pages for discovered projects
- Maintains change history in `.last-sync.json`

**Key Files:**
- State: `Wiki/.last-sync.json` (DO NOT EDIT MANUALLY)
- Log: `Wiki/log.md` (append-only, auto-updated with sync entries)
- Log Entries: Format `## [YYYY-MM-DD HH:MM] AUTO-SYNC | Summary`

---

---

## LLM Wiki Architecture

### Hybrid Knowledge Lifecycle

This repo now follows a hybrid model combining the workspace portfolio strategy with the second-brain workflow:

1. **Raw sources** — immutable inputs stored in `raw/`
2. **Wiki pages** — synthesized, linked, and curated in `Wiki/`
3. **Output artifacts** — reports and exports in `output/`
4. **Git discipline** — all updates happen from a fresh `main` branch and a PR-backed review cycle

This keeps the knowledge graph useful for project context while adding a cleaner source-to-wiki pipeline.

### Purpose

The LLM Wiki is a persistent, interlinked knowledge base built incrementally from raw sources. It uses the pattern from [Karpathy's llm-wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) adapted for Obsidian.

**Key principle:** Use LLMs to *incrementally build and maintain* a wiki, not to re-derive knowledge on every query.

### Three Layers

1. **Raw Sources** — Immutable clippings and captures  
   Location: `/mnt/c/Users/Chaddle/Documents/RawSources/`  
   Rule: **NEVER modify** raw source files  
   Tool: Obsidian Web Clipper → local image download → careful storage

2. **The Wiki** — LLM-generated, interlinked markdown  
   Location: `/mnt/c/Users/Chaddle/Documents/ObsidianVault/Wiki/`  
   Structure: `sources/`, `entities/`, `concepts/`, `synthesis/`  
   Rule: **LLM owns this entirely.** Update `index.md` and `log.md` on every change.

3. **The Schema** — This file  
   Purpose: Disciplined wiki maintenance procedures  
   Evolution: Update as you discover what works for your domain

---

## Wiki Structure & Conventions

### Git workflow rule for any repo change

Before editing this project, always follow this sequence exactly:

1. `git pull --prune origin main`
2. Create a new branch from `main`
3. Make the change on that branch
4. Commit the change
5. Push the branch
6. Open a pull request against `main`
7. Include the PR link in the final response

This is mandatory for every change to My-LLM-Wiki.

### Directory Layout

```
Wiki/
├── index.md              # Content catalog (read this first)
├── log.md                # Append-only operation log
├── overview.md           # High-level synthesis
├── sources/              # Source summaries (one per ingested source)
├── entities/             # People, tools, orgs, repos (one per entity)
├── concepts/             # Ideas, patterns, techniques (one per concept)
└── synthesis/            # Query answers filed back into wiki
```

### Page Conventions

**Every wiki page must have:**

1. **YAML Frontmatter**
   ```yaml
   ---
   type: source-summary | entity | concept | synthesis
   date_created: YYYY-MM-DD
   date_updated: YYYY-MM-DD
   tags:
     - wiki/source
     - wiki/entity
     - wiki/concept
     - wiki/synthesis
   source_count: N                    # For entities and concepts
   confidence: high | medium | low    # For concepts only
   ---
   ```

2. **Heavy Wikilinks** — Use `[[name]]` and `[[file#section]]` everywhere  
   - For Obsidian graph view
   - For cross-references between pages
   - For bidirectional linking

3. **Inline Metadata** — For Dataview queries  
   Format: `[key::value]` in the prose
   ```
   This concept was developed by [researcher::Alan Turing] at [org::Princeton].
   ```

4. **Source Attribution** — Always cite which raw sources contributed  
   Format: `(from [[Wiki/sources/source-name]])`

5. **Contradiction Handling** — If new sources contradict existing content  
   **Explicit notation required:**
   ```
   CONTRADICTION [date]: Source A claims X, but Source B claims Y.
   Need more research.
   ```
   Do NOT silently overwrite existing content.

---

## Page-Specific Rules

### Source Summary Pages (`Wiki/sources/`)

**File naming:** Use slug of source title, e.g., `karpathy-llm-wiki.md`

**Structure:**
```markdown
---
type: source-summary
date_ingested: YYYY-MM-DD
tags:
  - wiki/source
---

# Source Title

[Summary in 2-3 sentences]

## Source Metadata
- **Author:** [name]
- **Date Published:** YYYY-MM-DD
- **URL/Location:** [link if applicable]
- **Relevance:** [why this source matters]

## Key Points

- Point 1: [factual summary] (don't interpret)
- Point 2: [factual summary]
- Point 3: [factual summary]

## Entities Mentioned

- [[Entity Name]] — role in this source
- [[Another Entity]] — role in this source

## Concepts Introduced

- [[Concept Name]] — explained in this source
- [[Another Concept]] — explained in this source

## Direct Quotes

> "Quote 1" — context if needed
> "Quote 2" — context if needed

## Related Sources

- [[Wiki/sources/other-source]] — similar topic
```

### Entity Pages (`Wiki/entities/`)

**File naming:** Entity name, e.g., `Alan Turing.md`, `Obsidian.md`

**Structure:**
```markdown
---
type: entity
date_created: YYYY-MM-DD
date_updated: YYYY-MM-DD
tags:
  - wiki/entity
source_count: N
---

# Entity Name

[One-sentence description]

## Role/Context

What this person/tool/org does and why it matters.

## Key Attributes

- Attribute 1: [value]
- Attribute 2: [value]

## Relationships

- [[Related Entity 1]] — how they relate
- [[Related Entity 2]] — how they relate

## Mentions in Concepts

- [[Concept A]] — relevant to this entity
- [[Concept B]] — relevant to this entity

## Sources

- [[Wiki/sources/source1]] — mentions this entity
- [[Wiki/sources/source2]] — mentions this entity
```

### Concept Pages (`Wiki/concepts/`)

**File naming:** Concept name, e.g., `Knowledge Representation.md`

**Structure:**
```markdown
---
type: concept
date_created: YYYY-MM-DD
date_updated: YYYY-MM-DD
tags:
  - wiki/concept
source_count: N
confidence: high | medium | low
---

# Concept Name

[One-sentence summary]

## Definition

[Detailed definition, factual]

## Why It Matters

[Interpretation and significance — this is where you explain the "so what?"]

## Key Examples

- Example 1: [from [[Wiki/sources/source-name]]]
- Example 2: [from [[Wiki/sources/source-name]]]

## Related Concepts

- [[Related Concept 1]] — how they connect
- [[Related Concept 2]] — how they connect

## Key People / Tools / Organizations

- [[Entity Name]] — contributed to this concept
- [[Another Entity]] — applies this concept

## Contradictions

[If sources disagree, note explicitly here]

## Confidence Level

**[high | medium | low]** — How well-supported is this concept?

- high: Multiple independent sources, clear evidence
- medium: Some sources support it, reasonable interpretation
- low: Single source, emerging idea, needs more research

## Sources

- [[Wiki/sources/source1]] — defines or explains this concept
- [[Wiki/sources/source2]] — applies this concept
```

### Synthesis Pages (`Wiki/synthesis/`)

**File naming:** Topic or query, e.g., `How to Build a Wiki.md`

**Structure:**
```markdown
---
type: synthesis
date_created: YYYY-MM-DD
date_updated: YYYY-MM-DD
tags:
  - wiki/synthesis
---

# Query/Topic

[Your question or exploration]

## Answer

[Synthesized answer, drawing from multiple wiki pages]

## Related Concepts

- [[Concept A]] — core to this synthesis
- [[Concept B]] — provides context

## Related Entities

- [[Entity A]] — implements this
- [[Entity B]] — relates to this

## Open Questions

[Questions this raised that need more research]

## Sources Consulted

- [[Wiki/sources/source1]]
- [[Wiki/sources/source2]]
```

---

## Operations

### Ingest

**When:** You're adding a new raw source to the wiki  
**Goal:** Turn a raw source into 5-15 wiki pages (summary + entities + concepts)

**Procedure:**

1. Read the raw source completely. Take notes.
2. Create a source summary in `Wiki/sources/[slug].md`
   - Factual only; no interpretation
   - Extract key entities and concepts
3. Create or update entity pages in `Wiki/entities/`
   - One page per person, tool, org, repository
   - Link back to the source that introduced it
4. Create or update concept pages in `Wiki/concepts/`
   - One page per idea, pattern, technique
   - Link back to sources that explain it
   - Note confidence level
5. Update `Wiki/index.md`
   - Add source to Sources table
   - Remove from Unprocessed list
   - Update concept/entity tables
6. Update `Wiki/overview.md` if the big picture changed
7. Append to `Wiki/log.md`
   - Format: `## [YYYY-MM-DD HH:MM] INGEST | Source Title`
   - List pages created/updated

**Calibration:** Seed with 2-3 rich sources first to calibrate templates, then batch the rest.

### Query

**When:** You're answering a question about a topic  
**Goal:** Synthesize an answer from the wiki (not raw sources)

**Procedure:**

1. Read `Wiki/index.md` to find relevant pages
2. Read relevant wiki pages (not raw sources — the wiki has synthesized them)
3. Synthesize an answer using wikilinks to connect concepts
4. If the answer is substantial (> 1 paragraph), file it as a new page in `Wiki/synthesis/`
5. Update `Wiki/index.md` and `Wiki/log.md`

**Key insight:** Filing query answers back into the wiki is essential. Your explorations compound in the knowledge base.

### Lint

**When:** Every 2-3 weeks or after major ingestion batches  
**Goal:** Health-check the wiki for quality, consistency, and maintenance

**Checks:**

- **Orphan pages** — No inbound links. Should they be deleted or linked from elsewhere?
- **Broken wikilinks** — Links to pages that don't exist. Fix or remove.
- **Stale pages** — `date_updated` older than the newest relevant source. Refresh.
- **Contradictions** — Between pages. Are they noted explicitly?
- **Mentions vs. Pages** — Concepts mentioned in prose but lacking their own page. Create them.
- **Missing cross-references** — Related pages that should link to each other.

**Commands to help:**

```bash
# Find pages without backlinks (orphans)
grep -L "^\[\[" Wiki/**/*.md

# Find broken wikilinks
grep -o "\[\[.*\]\]" Wiki/**/*.md | sort | uniq

# Find stale pages (older than 30 days)
find Wiki -name "*.md" -mtime +30
```

---

## Critical Rules

### Raw Sources
- **IMMUTABLE.** Never modify raw source files.
- Even if metadata is wrong, the wiki layer is where you add clarity.
- If you need to store corrected metadata, do it in the source summary page, not the raw file.

### Wiki Ownership
- **LLM writes, human reads.** All wiki page creation and updates are LLM tasks.
- **Always update** `index.md` and `log.md` on every wiki change.
- Human's job: review ingestions, give feedback on templates, check contradictions, file queries.

### Source Summaries
- Keep factual. Extract what the source says.
- Interpretation goes in concept/synthesis pages.
- Direct quotes required for key claims.

### Contradictions
- When new sources contradict existing wiki content, **note it explicitly.**
- Don't silently overwrite. Use the CONTRADICTION notation.
- Flag for human review.

### Wikilinks
- Use heavily. They're the fabric of the wiki.
- Even single-mention entities/concepts should get pages.
- More links = better Obsidian graph view.

---

## Tools & Workflows

### Obsidian CLI Commands

If the CLI is working, these are useful:

```bash
obsidian read file="Wiki/index.md"              # read a note
obsidian create name="New Note" content="# Hello" silent
obsidian append file="Wiki/log.md" content="New line"
obsidian search query="search term" limit=10
obsidian property:set name="status" value="done" file="My Note"
```

### Image Management

Workflow for clipped articles with remote images:

1. Clip article with Obsidian Web Clipper → saved to vault
2. Open clipped note in Obsidian
3. Press `Ctrl+Shift+D` to download remote images to `assets/`
4. Image URLs auto-rewrite to local paths

### Future: qmd Search

Once you have 10+ sources, install `qmd` for hybrid BM25/vector search:

```bash
go install github.com/tobi/qmd@latest
qmd collection add my-vault /path/to/vault "**/*.md"
qmd update && qmd embed
qmd query "tools for maintaining state across sessions"
```

---

## Tips for Success

1. **Start small.** Ingest 2-3 rich sources manually to calibrate templates before batching the rest.
2. **Let the LLM write.** You read and review; the LLM writes wiki pages. Don't hand-edit.
3. **File query answers.** Synthesis is how explorations compound into knowledge.
4. **Lint periodically.** Health-check the wiki every couple weeks.
5. **The schema evolves.** Update this file as you discover what works for your domain.
6. **Use tools for state management.** Prefer Obsidian CLI for task updates instead of hand-editing.
7. **Graph view is your friend.** Open Obsidian's graph view often. Watch the shape of the wiki.

---

## When to Update This Schema

Update CLAUDE.md when you discover:
- Page templates that work better than current ones
- New frontmatter fields that improve querying
- Procedures that save time or improve quality
- Domain-specific rules for your types of sources

The LLM and human co-evolve this schema over time.

---

**Last updated:** 2026-08-07  
**Status:** Active, ready for source ingestion
