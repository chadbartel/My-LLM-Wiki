---
type: entity
date_created: 2026-08-07
date_updated: 2026-08-07
tags:
  - wiki/entity
  - project/ttrpg
  - status/in-progress
source_count: 1
---

# UnnamedRPG

Ultra-minimalist tabletop RPG system designed to fit on ~10 pages with complete character creation freedom and card-based conflict resolution.

## Purpose

Foundation game system for your TTRPG ecosystem. Provides the ruleset upon which [[TTRPG-AI-RAG-Assistant]], [[AIO Generative AI Solution]], and [[Automated-Taskmaster]] can build tools and extensions.

## Core Mechanics

**Character Creation:**
- Complete freedom (Risus: The Anything RPG inspiration)
- Flaw-based incentives (Mouse Guard-inspired)
- No restrictive classes or archetypes

**Conflict Resolution:**
- Card-based using standard 52-card deck
- Combat via poker hands (5-card draws with modifiers)
- Suits map to ability types:
  - Hearts: Emotional/Social abilities
  - Diamonds: Intellectual/Mental abilities
  - Clubs: Physical/Action abilities
  - Spades: Willpower/Determination

**Session Flexibility:**
- Single-session play or campaign campaigns
- Adaptable to any setting
- The Echoing Expanse as default setting

## Tech Stack

- **Language:** Python ~3.12
- **Package Management:** Poetry
- **Code Quality:** Black (formatter), isort (imports)
- **Current Status:** Pure design documentation (no external runtime dependencies)

## Architecture

- **Entry Point:** `main.py` (currently minimal—design documentation focus)
- **Core Documentation:** 
  - `breakdown_of_design.md` — Full system design rationale
  - `character_creation.md` — Character building rules
- **Key Reference Files:** Poker hand DC tables, suit mappings, conflict resolution matrices

## Relationships

**Provides Foundation For:**
- [[TTRPG-AI-RAG-Assistant]] — Can query UnnamedRPG rules via RAG
- [[AIO Generative AI Solution]] — Could ingest rulebook as source material
- [[Arcane-Scribe]] — Rules available for Bedrock-based lookup
- [[Automated-Taskmaster]] — Encounter generation respects UnnamedRPG mechanics

**Differs From:**
- [[AIO Generative AI Solution]] — Design documentation vs. PDF Q&A system
- [[TTRPG-AI-RAG-Assistant]] — Game mechanics vs. query interface

## Project Status

- **Status:** In Progress
- **Completeness:** Core mechanics designed; combat and conflict resolution frameworks established
- **Deployment Model:** Documentation-focused (no server/API)

## Key Insights for Context-Switching

**When to use:** 
- You're designing a new mechanic or need to reference base game rules
- GM preparing for a session
- Creating new content that needs to respect UnnamedRPG rules

**Quick facts:**
- Minimalist design (intentionally small ruleset)
- Card-based (no dice required—uses playing cards)
- Character-driven (flaw incentives encourage role-play)

## Open Questions

- [Should UnnamedRPG be automatically ingested into [[TTRPG-AI-RAG-Assistant]]?]
- [Combat resolution edge cases for multi-suit conflicts?]
- [Integration with [[Automated-Taskmaster]] encounter generation?]

## Related Concepts

- [[TTRPG Ecosystem]] — Overview of how all 5 projects connect
- [[Game System Design]] — Design philosophy behind minimalist RPG
- [[Card-Based Resolution]] — Poker hand mechanic explanation

## Sources

- Wiki source: Project repository scan on 2026-08-07
- README analysis from `/mnt/c/Users/Chaddle/PycharmProjects/UnnamedRPG`
- Architecture extracted from `breakdown_of_design.md` and `character_creation.md`
