---
type: concept
date_created: 2026-08-07
date_updated: 2026-08-07
tags:
  - wiki/concept
source_count: 1
confidence: high
---

# Wikilinks

Bidirectional links between notes that work in both directions, enabling navigation in all directions.

## Definition

Traditional markdown links are one-way: `[text](link)` creates a link from A to B, but B doesn't know about A.

Wikilinks are bidirectional: `[[Note Name]]` creates a link from A to B, and Obsidian automatically shows that link on B's backlinks section. This creates true bidirectional navigation.

## Syntax

```markdown
[[Note Name]]                    # Link to another note
[[Note Name#Section]]            # Link to a section in a note
[[File|Display Text]]            # Link with custom display text
```

## Why It Matters

- **Navigation**: You can discover related notes both forward and backward
- **Emergence**: Wikilinks create unexpected connections as you add more notes
- **Graph View**: The link structure visualizes your knowledge network
- **Lower Friction**: Easier to link than in traditional markdown

## Contrast

**Traditional One-Way Links:**
```markdown
# Note A
See [Note B](./note-b.md)   # A knows about B, but B doesn't know about A
```

**Wikilinks (Bidirectional):**
```markdown
# Note A
See [[Note B]]              # A knows about B, AND B automatically shows this link in backlinks
```

## Backlinks

Every note shows a "Backlinks" section with all notes that link to it. This enables discovery:

```
Note B
↑
Mentioned in:
- [[Note A]]
- [[Note C]]
- [[Note E]]
```

## Related Concepts

- [[Graph View]] — Visualizes wikilink network
- [[Emergence]] — Wikilinks enable unexpected pattern discovery
- [[Networked Thinking]] — Thinking through connections rather than hierarchy

## Key Entities

- [[Obsidian]] — Supports wikilinks natively

## Confidence Level

**High** — Wikilinks are a core feature of knowledge graphs and are widely adopted in tools like Obsidian, Roam, Logseq, etc.

## Sources

- [[Wiki/sources/obsidian-second-brain]] — Explains wikilinks as foundational feature
