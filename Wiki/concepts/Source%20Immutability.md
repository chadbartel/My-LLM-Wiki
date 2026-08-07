---
type: concept
date_created: 2026-08-07
date_updated: 2026-08-07
tags:
  - wiki/concept
source_count: 1
confidence: high
---

# Source Immutability

The principle that raw source files should never be modified, even if they contain errors or outdated information.

## Definition

In the LLM Wiki pattern, raw sources (the immutable layer) are the ground truth. The KB and wiki layer exist to add clarity, interpretation, and cross-references, but the original sources remain unchanged.

## Why It Matters

- **Reproducibility**: You can always go back to what the source actually said
- **Auditability**: Any claim in the KB can be traced to its source
- **Separation of Concerns**: Raw facts stay separate from interpretation
- **Safety**: Prevents accidental corruption of primary data
- **Long-term Durability**: Original sources survive changes to the KB schema

## How It Works in Practice

If a raw source has metadata or formatting issues, you **don't fix the source**. Instead:

1. Note the issue in the source summary page (in the KB)
2. Add clarification or correction in concept or entity pages (in the KB)
3. Link to the source from the corrected content

## Example

Raw source says: "ChatGPT was released in November 2022"
Correction in KB: "Clarification: ChatGPT was released November 30, 2022 (from [[Wiki/sources/chatgpt-timeline]])"

The raw source remains untouched. The KB adds precision.

## Related Concepts

- [[LLM Wiki Pattern]] — Immutability is a core principle
- [[Contradiction Handling]] — How to manage conflicting claims without modifying sources

## Confidence Level

**High** — This is a foundational principle in the LLM wiki pattern and all knowledge management systems.

## Sources

- [[Wiki/sources/karpathy-llm-wiki-pattern]] — Emphasizes source immutability
