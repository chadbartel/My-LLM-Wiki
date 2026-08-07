---
type: wiki-synthesis
date_created: 2026-08-07
date_updated: 2026-08-07
tags:
  - wiki/synthesis
  - wiki/overview
---

# Wiki Overview — Your Workspace at Scale

Your personal knowledge management system covering 20+ workspace projects across 4 interconnected ecosystems.

---

## What This Wiki Is

**An LLM-powered knowledge base** built using Karpathy's wiki pattern adapted for Obsidian.

**Purpose:** Help you navigate, understand, and make decisions across 20+ projects while optimizing for ADHD context-switching.

**Three Layers:**
1. **Raw Sources** → Immutable project code and configs (in workspace)
2. **Wiki** → Generated summaries, architecture docs, guides (in Wiki/)
3. **Schema** → Maintenance procedures (in CLAUDE.md)

---

## What's In It

### 4 Interconnected Ecosystems (50+ entity & concept pages)

**🎲 TTRPG Ecosystem** (5 projects)
- Game system design, rule lookup via RAG, procedural content generation
- Projects: UnnamedRPG, TTRPG-AI-RAG-Assistant, AIO AI, Arcane-Scribe, Automated-Taskmaster

**🤖 AI/LLM Ecosystem** (3 projects)
- Local-first (brAIniac), research (CAG), cloud-based (GenerateIdeas)
- Trade-offs: privacy vs. speed, on-device vs. cloud, traditional vs. novel approaches

**☁️ AWS Infrastructure Ecosystem** (6 projects)
- CDK Infrastructure as Code, serverless APIs, static sites, home automation
- Hub-and-spoke pattern: my-shared-infra exports to chadbarteldotcom, My-DDNS-Updater, Cartographers-Cloud-Kit
- Plus Homelab-Ansible for local Docker orchestration

**🛠️ Utilities & Learning Ecosystem** (6 projects)
- Reusable libraries (Cellophane), CI/CD templates (MidnightsGitHubActions), sandboxes (My-Mini-Projects)
- Learning spaces for music generation, quick experiments, campaign management

### 7 Cross-Project Synthesis Pages

- [[Wiki/synthesis/Project-Dashboard]] — Quick status check
- [[Wiki/synthesis/Quick-Switch-Guide-by-Ecosystem]] — Fast context-switching
- [[Wiki/synthesis/Shared-Infrastructure-Map]] — Dependencies & data flows
- [[Wiki/synthesis/ADHD-Workflow-Optimization]] — 8 patterns for rapid switching
- [[Wiki/synthesis/Common-Use-Cases]] — "I want to..." decision tree
- [[Wiki/synthesis/Technology-Dependency-Graph]] — Tech stacks & learning paths
- [[Wiki/synthesis/Phase-6-Automated-Monitoring]] — Wiki auto-sync guide

### Automated Monitoring (Phase 6)

Wiki stays in sync automatically via:
- `scripts/sync-wiki.py` — Scans projects, detects changes
- `Wiki/.last-sync.json` — Tracks state for change detection
- GitHub Actions — Runs every Monday 9 AM UTC
- Auto-updates: entity pages, synthesis pages, log.md

---

## Key Insights

### Architecture Patterns
- **Hub-and-Spoke:** Central infrastructure hub (my-shared-infra) exports to dependent projects
- **RAG Pattern:** LLM-powered rule lookup across TTRPG projects
- **Lambda Authorizer:** Custom API auth with IP whitelisting
- **Docker Compose V2:** Local orchestration on single-node monolith

### Design Philosophy
- **Local-First:** When possible (brAIniac, Homelab)
- **Cloud-Efficient:** Minimal AWS cost (~$7-20/month)
- **ADHD-Optimized:** Wiki synthesis pages designed for rapid context-switching
- **Automation-Ready:** Phase 6 keeps wiki current without manual maintenance

### Cross-Project Dependencies
- Python 3.12 everywhere (Poetry, pytest, Black, isort, flake8, mypy)
- AWS CDK for all cloud projects
- Ansible + Docker Compose for local infrastructure
- FastAPI for REST APIs

---

## How to Use This Wiki

### For Quick Lookup
1. Start at [[Wiki/synthesis/Project-Dashboard]]
2. Find your project
3. Click through to full entity page

### For Context-Switching
1. Read [[Wiki/synthesis/ADHD-Workflow-Optimization]] (pick a pattern)
2. Use [[Wiki/synthesis/Quick-Switch-Guide-by-Ecosystem]] (find your next project)
3. Check [[Wiki/synthesis/Shared-Infrastructure-Map]] (understand dependencies)

### For Learning a Technology
1. Go to [[Wiki/synthesis/Technology-Dependency-Graph]]
2. Find your tech of interest
3. Follow the learning path (project examples provided)

### For Understanding Architecture
1. Read ecosystem overview (e.g., [[Wiki/concepts/AWS Infrastructure Ecosystem]])
2. Read pattern pages (e.g., [[Wiki/concepts/Shared Infrastructure Hub Pattern]])
3. Reference entity pages for concrete examples

### For Maintenance
1. Review [[Wiki/synthesis/Phase-6-Automated-Monitoring]] for auto-sync guide
2. Run `python3.12 scripts/sync-wiki.py --verbose --dry-run` weekly
3. Check [[Wiki/log]] for operation history

---

## Stats

- **Total Pages:** 68 (14 calibration + 9 Phase 1 + 8 Phase 2 + 14 Phase 3 + 9 Phase 4 + 6 Phase 5 + 1 Phase 6)
- **Projects Documented:** 20+
- **Entity Pages:** 26 (projects, tools, organizations)
- **Concept Pages:** 25 (patterns, techniques, architectures)
- **Synthesis Pages:** 7 (navigation, workflows, guides)
- **Source Pages:** 3 (calibration sources)
- **Wikilinks:** 200+ connecting pages
- **Graph Connections:** Highly interconnected (explore via Obsidian Graph View)

---

## Status

✅ **Phase 1-6 COMPLETE**

All workspace projects documented. Cross-project synthesis complete. Automated monitoring operational.

Ready for:
- Deep project work
- Weekly automated syncs
- Continuous wiki refinement

---

**Next:** Pick your [[Wiki/synthesis/ADHD-Workflow-Optimization]] pattern and start working!

**Related:**
- [[Wiki/index]] — Full content catalog
- [[Wiki/log]] — Operation log
- [[Wiki/synthesis/]] — All synthesis pages
