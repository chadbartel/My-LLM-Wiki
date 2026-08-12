# My LLM Wiki

A personal knowledge management system built on Karpathy's LLM wiki pattern, adapted for Obsidian. Comprehensive documentation of 20+ workspace projects across 4 interconnected ecosystems, with automated monitoring and ADHD-optimized navigation.

**Status:** ✅ **All 6 Phases Complete** — Wiki fully operational with automated synchronization

---

## What Is This?

This is your **personal knowledge base** covering:

### Hybrid knowledge lifecycle

This repository now follows a hybrid model inspired by the second-brain workflow:

1. **Raw sources** live in `raw/` and are treated as immutable input material.
2. **Wiki pages** in `Wiki/` are curated, linked, and synthesized knowledge.
3. **Generated outputs** live in `output/` for reports, summaries, or exports.
4. **Agent workflows** are rule-driven and wiki-first, so queries look in the wiki before code or memory.

This preserves the workspace portfolio model while adding a cleaner source-to-knowledge pipeline.

- **20+ workspace projects** (TTRPG, AI/LLM, AWS Infrastructure, Utilities & Learning)
- **68 wiki pages** (26 entity pages + 25 concept pages + 7 synthesis/navigation pages + 10 supporting pages)
- **Automated monitoring** (project scanner + change detector + GitHub Actions)
- **ADHD-optimized workflows** (synthesis pages designed for rapid context-switching)
- **Rich cross-references** (200+ wikilinks, Obsidian graph view)

### The Pattern

Three interconnected layers:

1. **Raw Sources** → Your actual project code and configs (immutable)
2. **Wiki** → LLM-generated summaries, architecture docs, decision logs (in `Wiki/`)
3. **Schema** → Maintenance procedures (`CLAUDE.md`)

---

## Quick Start

### Open in Obsidian

1. Clone this repo
2. Open `/mnt/c/Users/Chaddle/Documents/ObsidianVault` as an Obsidian vault
3. Start at `Wiki/overview.md` or `Wiki/index.md`

### Run Local Sync

Preview what would change (safe, no modifications):
```bash
python3.12 scripts/sync-wiki.py --verbose --dry-run
```

Apply changes:
```bash
python3.12 scripts/sync-wiki.py --verbose
```

For details, see `scripts/README.md`.

### Automated Sync (GitHub Actions)

- **Runs:** Every Monday 9 AM UTC
- **Does:** Scans projects, detects changes, updates wiki, commits & pushes
- **Manual trigger:** Go to GitHub → Actions → "Wiki Auto-Sync" → Run workflow
- **No setup required:** Runs on GitHub's servers

---

## Structure

```
.
├── Wiki/                              # Your knowledge base
│   ├── index.md                       # Content catalog (START HERE)
│   ├── overview.md                    # High-level synthesis
│   ├── log.md                         # Append-only operation log
│   ├── .last-sync.json                # State file for change detection
│   ├── entities/                      # 26 project & tool pages
│   ├── concepts/                      # 25 pattern & architecture pages
│   ├── sources/                       # 3 source summaries
│   └── synthesis/                     # 7 navigation & workflow guides
├── scripts/
│   ├── sync-wiki.py                   # Main sync orchestrator (700+ lines)
│   └── README.md                      # Sync script guide
├── .github/workflows/
│   └── wiki-sync.yml                  # GitHub Actions automation
├── .obsidian/                         # Obsidian vault config
├── CLAUDE.md                          # LLM wiki maintenance schema
└── README.md                          # This file
```

---

## The 4 Ecosystems

### 🎲 TTRPG Ecosystem (5 projects)
Game system design, rule lookup via RAG, procedural content generation.
- **Projects:** UnnamedRPG, TTRPG-AI-RAG-Assistant, AIO Generative AI, Arcane-Scribe, Automated-Taskmaster

### 🤖 AI/LLM Ecosystem (3 projects)
Local-first (8GB VRAM ceiling), research implementations, cloud-based solutions.
- **Projects:** brAIniac, my-cache-augmented-generation, GenerateIdeas

### ☁️ AWS Infrastructure Ecosystem (6 projects)
CDK Infrastructure as Code, serverless APIs, static sites, local orchestration.
- **Projects:** my-shared-infra (hub), My-DDNS-Updater, chadbarteldotcom, thatsmidnightdotcom, Cartographers-Cloud-Kit, Homelab-Ansible

### 🛠️ Utilities & Learning Ecosystem (6 projects)
Reusable libraries, CI/CD templates, learning sandboxes.
- **Projects:** Cellophane, MidnightsGitHubActions, FunWithMusic, My-Mini-Projects, TableTopMaestro, Close-Application

---

## Navigation Guide

### For Quick Lookup
1. Start: `Wiki/overview.md`
2. Find project: `Wiki/synthesis/Project-Dashboard.md`
3. Deep dive: Click through to project entity page

### For Context-Switching (ADHD-Optimized)
1. Read: `Wiki/synthesis/ADHD-Workflow-Optimization.md` (pick a pattern)
2. Navigate: `Wiki/synthesis/Quick-Switch-Guide-by-Ecosystem.md`
3. Understand: `Wiki/synthesis/Shared-Infrastructure-Map.md`

### For Learning a Technology
1. Go to: `Wiki/synthesis/Technology-Dependency-Graph.md`
2. Find your tech
3. Follow the learning path with project examples

### For Understanding Architecture
1. Read ecosystem overview (e.g., `Wiki/concepts/AWS CDK Infrastructure as Code.md`)
2. Read pattern pages (e.g., `Wiki/concepts/Shared Infrastructure Hub Pattern.md`)
3. Reference entity pages for concrete examples

---

## The 6 Phases

### Phase 1: TTRPG Ecosystem ✅
- 5 projects documented (entity pages)
- 4 key concepts (RAG pattern, serverless services, multi-provider LLM)

### Phase 2: AI/LLM Ecosystem ✅
- 3 projects documented
- 5 key concepts (local-first architecture, cache-augmented generation, FastMCP)

### Phase 3: AWS Infrastructure ✅
- 6 projects documented
- 8 key concepts (CDK patterns, Lambda authorizer, shared infrastructure hub)

### Phase 4: Utilities & Learning ✅
- 6 projects documented
- 3 key concepts (reusable libraries, experimentation sandbox, CI/CD)

### Phase 5: Cross-Project Synthesis ✅
- 6 navigation pages created
- ADHD-optimized workflow patterns
- Quick-jump guides and decision trees

### Phase 6: Automated Monitoring ✅
- Wiki auto-sync script (`sync-wiki.py`)
- Change detection via state file
- GitHub Actions workflow (weekly + manual trigger)
- Comprehensive automation guide

---

## How Automated Sync Works

### The Flow

1. **Scanner** → Reads all 20+ workspace projects, extracts metadata
2. **Detector** → Compares current state vs. `.last-sync.json`
3. **Updater** → Creates/updates wiki pages based on changes
4. **Persister** → Saves new state to `.last-sync.json`

### What Gets Detected

- ✅ New projects (auto-creates entity pages)
- ✅ Status changes (planning → active → archived)
- ✅ File modifications (tracked by timestamp)
- ✅ Dependency updates
- ✅ Removed projects

### What Gets Updated

- `Wiki/entities/*.md` — Project pages (status, metadata)
- `Wiki/synthesis/Shared-Infrastructure-Map.md` — Dependencies
- `Wiki/log.md` — Operation log with timestamp and summary
- `.last-sync.json` — State file (auto-updated, never manually edit)

### Dry-Run Mode (Safe)

```bash
python3.12 scripts/sync-wiki.py --verbose --dry-run
```

Shows exactly what would change without applying changes.

---

## Maintenance

### Weekly Workflow

1. **Monday 9 AM UTC:** GitHub Actions runs automatically
2. **Pull latest:** `git pull` to get updated wiki
3. **Review changes:** Check `Wiki/log.md` for what changed
4. **Validate:** Check updated entity pages if needed

### Manual Sync (Anytime)

```bash
cd /mnt/c/Users/Chaddle/Documents/ObsidianVault
python3.12 scripts/sync-wiki.py --verbose
git add .
git commit -m "Wiki sync: [describe changes]"
git push
```

### Adding a New Project

1. Add project to workspace (one of 4 root directories)
2. Run sync script (detects new project automatically)
3. Entity page created, added to log
4. Push changes to GitHub

### Updating Wiki Schema

See `CLAUDE.md` for:
- Page template conventions (frontmatter, wikilinks, metadata)
- Operation procedures (Ingest, Query, Lint)
- Critical rules (raw source immutability, contradiction handling)
- Tools & workflows (Obsidian CLI, image management)

---

## Key Features

### Automation
- ✅ Weekly project scanning
- ✅ Automatic change detection
- ✅ Smart page updates
- ✅ Append-only operation log
- ✅ GitHub Actions integration

### ADHD-Optimized
- ✅ 8 context-switching patterns
- ✅ Quick-jump guides by ecosystem
- ✅ "I want to..." decision trees
- ✅ Technology dependency graphs
- ✅ Shared infrastructure mapping

### Knowledge Management
- ✅ 200+ wikilinks (Obsidian graph view)
- ✅ Type-tagged pages (entity/concept/synthesis)
- ✅ Comprehensive frontmatter (dates, tags, confidence)
- ✅ Source attribution and contradiction tracking
- ✅ Bidirectional cross-references

### Developer Experience
- ✅ Python 3.12+ scripts
- ✅ Dry-run mode for safe previews
- ✅ Verbose logging for debugging
- ✅ Git-based version control
- ✅ GitHub Actions automation

---

## Files Reference

### Core Wiki Files
- `Wiki/index.md` — Master navigation hub (start here)
- `Wiki/overview.md` — High-level synthesis of entire wiki
- `Wiki/log.md` — Append-only operation log (auto-updated)
- `CLAUDE.md` — Complete LLM wiki maintenance schema

### Wiki Content
- `Wiki/entities/` — 26 project/tool/org pages
- `Wiki/concepts/` — 25 pattern/architecture/technique pages
- `Wiki/sources/` — 3 source summary pages
- `Wiki/synthesis/` — 7 navigation/workflow/guide pages

### Automation
- `scripts/sync-wiki.py` — Main sync orchestrator (700+ lines)
- `scripts/README.md` — Sync script quick reference
- `.github/workflows/wiki-sync.yml` — GitHub Actions workflow
- `Wiki/.last-sync.json` — State file (DO NOT EDIT)

### Configuration
- `.obsidian/app.json` — Obsidian vault settings
- `.obsidian/hotkeys.json` — Keyboard shortcuts

---

## Stats

- **Total Pages:** 68
- **Entity Pages:** 26 (projects, tools, organizations)
- **Concept Pages:** 25 (patterns, architectures, techniques)
- **Synthesis Pages:** 7 (navigation, workflows, guides)
- **Source Pages:** 3 (learning materials)
- **Wikilinks:** 200+
- **Projects Documented:** 20+
- **Ecosystems:** 4

---

## Getting Started

### 1. Clone & Setup
```bash
git clone git@github.com:chadbartel/My-LLM-Wiki.git
cd My-LLM-Wiki  # (which is the ObsidianVault folder)
```

### 2. Open in Obsidian
- File → Open Vault → Select this directory
- Enable: Graph View, Wikilinks, Backlinks

### 3. Start Exploring
- `Wiki/overview.md` — Big picture
- `Wiki/index.md` — Full content catalog
- `Wiki/synthesis/Project-Dashboard.md` — All projects at a glance
- `Wiki/synthesis/ADHD-Workflow-Optimization.md` — Your workflow patterns

### 4. Optional: Run Local Sync
```bash
python3.12 scripts/sync-wiki.py --verbose --dry-run  # Preview
python3.12 scripts/sync-wiki.py --verbose              # Apply
git push                                               # Push changes
```

---

## Contributing

### Adding/Updating Content
1. Edit wiki pages in Obsidian
2. Keep frontmatter (type, dates, tags, metadata)
3. Use wikilinks liberally (`[[page-name]]`)
4. Commit & push changes

### Improving Sync Script
1. Edit `scripts/sync-wiki.py`
2. Test with `--dry-run` mode first
3. Commit & push when working

### Updating Schema
1. Edit `CLAUDE.md` as you discover what works
2. Commit & push changes
3. Update wiki maintenance procedures if needed

---

## License

[Add your license here]

---

## Maintenance Log

See `Wiki/log.md` for complete operation history and sync records.

**Last Updated:** 2026-08-07  
**Status:** ✅ All 6 phases complete. Automated monitoring active.  
**Next Sync:** Monday 9 AM UTC (automatic)

---

**Built with:** LLM wiki pattern (Karpathy), Obsidian, Python 3.12, GitHub Actions

**For detailed maintenance procedures, see:** `CLAUDE.md`
