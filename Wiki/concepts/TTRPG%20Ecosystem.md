---
type: concept
date_created: 2026-08-07
date_updated: 2026-08-07
tags:
  - wiki/concept
  - project/ttrpg
  - ecosystem
confidence: high
source_count: 5
---

# TTRPG Ecosystem

Your interconnected cluster of 5 TTRPG projects providing complete toolkit for game design, rule lookup, and procedural content generation.

## Definition

Integrated ecosystem of tabletop RPG tools built around [[UnnamedRPG]] base game system, with AI-powered query interfaces, serverless utilities, and both local/cloud deployment options. Designed to support game mastering, player support, and campaign automation.

## Ecosystem Map

```
┌─────────────────────────────────────────────────┐
│           TTRPG Ecosystem (5 Projects)          │
└─────────────────────────────────────────────────┘

                 [[UnnamedRPG]]
            (Base Game System)
                     ↓
            Rules Source Material
                     ↓
     ┌───────────────┼───────────────┐
     ↓               ↓               ↓
[Rule Lookup]  [Content Gen]  [Deployment]
     
┌──────────────────┐     ┌──────────────┐
│  Local RAG       │     │ Serverless   │
│  (Gemini-based)  │     │ (Bedrock)    │
├──────────────────┤     ├──────────────┤
│ · TTRPG-AI-RAG   │     │ · Arcane-    │
│ · AIO Generative │     │   Scribe     │
│   AI Solution    │     └──────────────┘
└──────────────────┘             │
        ↓                        ↓
[Rule Query]              [Enterprise Query]
                                 │
                         ┌───────┴────────┐
                         ↓                ↓
                    [Rule Lookup]    [Data Persistence]
                         
                  ┌─────────────────┐
                  │ Automated-      │
                  │ Taskmaster      │
                  ├─────────────────┤
                  │ · Encounters    │
                  │ · Loot Tables   │
                  │ · NPC Prompts   │
                  └─────────────────┘
                         ↓
                  [Content Generation]
```

## The Five Projects

### 1. [[UnnamedRPG]] — Foundation
- **Role:** Base game system (rules, mechanics, design philosophy)
- **Type:** Documentation-focused
- **Delivers:** Card-based RPG with minimalist design
- **Unique Aspect:** Ultra-lightweight (fits on ~10 pages)

### 2. [[TTRPG-AI-RAG-Assistant]] — Local Query #1
- **Role:** AI-powered rule lookup (local deployment)
- **Type:** FastAPI + Chromadb + Google Gemini
- **Delivers:** Natural language queries against rulebooks (Docker)
- **Unique Aspect:** Local persistence, Gemini embeddings

### 3. [[AIO Generative AI Solution]] — Local Query #2
- **Role:** AI-powered rule lookup (local deployment)
- **Type:** FastAPI + Chromadb + Google Gemini
- **Delivers:** Same as TTRPG-AI-RAG-Assistant (alternative implementation)
- **Unique Aspect:** Identical to TTRPG-AI-RAG-Assistant (future consolidation candidate)

### 4. [[Arcane-Scribe]] — Enterprise Query
- **Role:** Serverless, authenticated rule lookup
- **Type:** AWS Lambda + Bedrock + FAISS
- **Delivers:** Production-grade API for TTRPG queries
- **Unique Aspect:** Scalable, secure, cost-optimized for high volume

### 5. [[Automated-Taskmaster]] — Content Generation
- **Role:** Procedural encounter/loot/NPC generation
- **Type:** AWS Lambda + stateless generators
- **Delivers:** Fast, cheap random content (no documents)
- **Unique Aspect:** Complements query systems, pure generation

## Why It Works Together

| Component | Solves | Used For |
|-----------|--------|----------|
| [[UnnamedRPG]] | Need a game system | Campaign foundation |
| [[TTRPG-AI-RAG-Assistant]] + [[AIO Generative AI Solution]] | Quick rule lookup | Rules clarification mid-session |
| [[Arcane-Scribe]] | Enterprise deployment | Public-facing tools |
| [[Automated-Taskmaster]] | Content variety | Encounters, NPCs, treasure |

## Key Patterns Across Ecosystem

1. **RAG (Retrieval Augmented Generation)** — 3/5 projects
   - Document → PDF parse → Embeddings → Vector search → LLM response
   - Used by: [[TTRPG-AI-RAG-Assistant]], [[AIO Generative AI Solution]], [[Arcane-Scribe]]

2. **Serverless Deployment** — 2/5 projects
   - AWS Lambda for auto-scaling, pay-per-use
   - Used by: [[Arcane-Scribe]], [[Automated-Taskmaster]]

3. **FastAPI REST API** — 4/5 projects
   - Standardized HTTP endpoints
   - Used by: [[TTRPG-AI-RAG-Assistant]], [[AIO Generative AI Solution]], [[Arcane-Scribe]], [[Automated-Taskmaster]]

4. **Python 3.12 + Poetry** — All 5 projects
   - Consistent language, dependency management, code quality tools

## Deployment Strategies

### Local-First (Default for Development)
- **Projects:** [[UnnamedRPG]], [[TTRPG-AI-RAG-Assistant]], [[AIO Generative AI Solution]]
- **Setup:** Docker Compose or local install
- **Cost:** Free (self-hosted)
- **Access:** Localhost or LAN
- **Best For:** Personal use, campaign groups, offline play

### Enterprise/Serverless (Scalable)
- **Projects:** [[Arcane-Scribe]], [[Automated-Taskmaster]]
- **Setup:** AWS CDK deployment
- **Cost:** AWS billing (pay per use)
- **Access:** Public via custom domain + Cognito auth
- **Best For:** Public APIs, multi-team access, zero infrastructure management

## Interconnections & Data Flow

### Scenario 1: GM Needs Quick Rule Lookup
```
GM: "Can I use fireball on this group of kobolds?"
  → Call [[TTRPG-AI-RAG-Assistant]] or [[Arcane-Scribe]]
  → LLM queries D&D 5e rulebook in vector store
  → Response: "Yes, spell affects 20-foot radius sphere..."
```

### Scenario 2: Generate Complete Encounter
```
GM: "I need a random encounter for level 3 party"
  → Call [[Automated-Taskmaster]]
  → Get: 3 kobolds + 50 GP loot + story hook
  → Call [[Arcane-Scribe]] to verify monster stats
  → Result: Ready-to-use encounter
```

### Scenario 3: Design New Campaign
```
1. Start with [[UnnamedRPG]] mechanics as reference
2. Generate NPCs via [[Automated-Taskmaster]]
3. Store encounter data in [[Arcane-Scribe]]
4. Query rules on-the-fly via any RAG system
5. Result: Campaign fully supported by tools
```

## Shared Infrastructure Opportunities

**Potential Consolidations:**
- [[TTRPG-AI-RAG-Assistant]] + [[AIO Generative AI Solution]] → Duplicate implementations (could merge into one)
- [[Arcane-Scribe]] + [[Automated-Taskmaster]] → Both serverless (could share Lambda layer)
- All APIs → Central API Gateway (single entry point with routing)

**Potential Expansions:**
- Shared caching layer (Redis for frequently asked questions)
- Unified authentication (Cognito across all services)
- Analytics (CloudWatch logs for gameplay patterns)
- UI dashboard (web app to orchestrate all 5 projects)

## Why This Matters for ADHD Context-Switching

**Unified Knowledge System:** When you jump between TTRPG work and other projects, you have:
1. One place to find all TTRPG tools
2. Clear understanding of what each project does
3. Fast navigation to code/docs
4. No time lost searching "which query tool was which?"

**Ecosystem View:** Understanding these 5 projects as a connected whole means:
- Decisions about one tool affect others
- Refactoring opportunities (e.g., consolidate duplicate RAG projects)
- Integration points are clear (e.g., Automated-Taskmaster calls Arcane-Scribe)

## Related Concepts

- [[RAG Pattern for TTRPG]] — Document ingestion + semantic search details
- [[Serverless TTRPG Services]] — AWS Lambda architecture approach
- [[Game System Design]] — UnnamedRPG philosophy
- [[Multi-Provider LLM Integration]] — Gemini vs. Bedrock comparison
- [[Microservice Architecture]] — How tools decouple and communicate

## Open Questions for Ecosystem

1. [Should [[TTRPG-AI-RAG-Assistant]] and [[AIO Generative AI Solution]] be consolidated?]
2. [Is [[Automated-Taskmaster]] used enough to justify maintaining separately?]
3. [Should all projects share a single UI dashboard?]
4. [What's the priority: expand local tools or move to enterprise (Arcane-Scribe)?]
5. [Should [[UnnamedRPG]] rules be auto-ingested into RAG systems?]

## Maintenance & Evolution

- **Weekly:** Check if any project has breaking changes
- **Monthly:** Evaluate if consolidations make sense
- **Quarterly:** Add new features to [[Automated-Taskmaster]] (new generator types)
- **As-needed:** Ingest new rulebooks into RAG systems

## Sources

- [[Wiki/entities/UnnamedRPG]]
- [[Wiki/entities/TTRPG-AI-RAG-Assistant]]
- [[Wiki/entities/AIO Generative AI Solution]]
- [[Wiki/entities/Arcane-Scribe]]
- [[Wiki/entities/Automated-Taskmaster]]
- Project repository scans on 2026-08-07
