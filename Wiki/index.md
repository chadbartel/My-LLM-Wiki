---
type: wiki-index
date_created: 2026-08-07
date_updated: 2026-08-07
tags:
  - wiki/index
---

# LLM Wiki Index

**Start here.** This is the content catalog for the LLM Wiki—your all-encompassing knowledge base covering learning materials and all projects in your workspace.

---

## Wiki Ecosystems

Your workspace organized into project clusters with shared themes, architectures, and dependencies.

### 🎲 TTRPG Ecosystem (5 projects) — PHASE 1 COMPLETE ✓

Interconnected TTRPG tools built around game system design, rule lookup, and procedural generation.

**Overview:** [[Wiki/concepts/TTRPG Ecosystem]]

**Projects:**
- [[Wiki/entities/UnnamedRPG]] — Base game system (minimalist design)
- [[Wiki/entities/TTRPG-AI-RAG-Assistant]] — Rule lookup (local Gemini RAG)
- [[Wiki/entities/AIO Generative AI Solution]] — Rule lookup (local Gemini RAG, alternative)
- [[Wiki/entities/Arcane-Scribe]] — Rule lookup (serverless Bedrock)
- [[Wiki/entities/Automated-Taskmaster]] — Content generation (encounters, loot)

**Key Patterns:**
- [[Wiki/concepts/RAG Pattern for TTRPG]] — Document ingestion + semantic search
- [[Wiki/concepts/Serverless TTRPG Services]] — AWS Lambda architecture
- [[Wiki/concepts/Multi-Provider LLM Integration]] — Gemini vs. Bedrock strategy

### 🤖 AI/LLM Ecosystem (3 projects) — PHASE 2 COMPLETE ✓

Three distinct approaches to AI: local-first, research-driven, and cloud-based. Explores trade-offs in privacy, cost, capability, and architecture.

**Overview:** [[Wiki/concepts/AI-LLM Ecosystem]]

**Projects:**
- [[Wiki/entities/brAIniac]] — Local-first conversational AI (8GB VRAM, uncensored, offline)
- [[Wiki/entities/my-cache-augmented-generation]] — Research implementation of CAG paper (novel RAG alternative)
- [[Wiki/entities/GenerateIdeas]] — Cloud-based Gemini idea generator (quick, stateless, minimal setup)

**Key Patterns:**
- [[Wiki/concepts/Local-First AI Architecture]] — Privacy and control philosophy
- [[Wiki/concepts/Cloud vs. On-Device LLM Strategy]] — Cost, capability, and latency comparison
- [[Wiki/concepts/Cache-Augmented Generation]] — Novel approach vs. traditional RAG
- [[Wiki/concepts/FastMCP Protocol]] — Tool integration for LLMs

### ☁️ AWS Infrastructure Ecosystem (6 projects) — PHASE 3 COMPLETE ✓

Cloud-native infrastructure patterns using AWS CDK, demonstrating hub-and-spoke architecture, serverless APIs, static site hosting, and centralized DNS management.

**Overview:** [[Wiki/concepts/AWS Infrastructure Ecosystem]]

**Projects:**
- [[Wiki/entities/my-shared-infra]] — Central infrastructure hub (Route 53, KMS, DNSSEC)
- [[Wiki/entities/My-DDNS-Updater]] — Dynamic DNS resolver (home IP tracking, Lambda authorizer)
- [[Wiki/entities/chadbarteldotcom]] — Static site hosting (S3 + CloudFront + ACM + Route 53)
- [[Wiki/entities/thatsmidnightdotcom]] — Pattern reuse (identical static site, different domain)
- [[Wiki/entities/Cartographers-Cloud-Kit]] — Serverless API (FastAPI + Lambda + DynamoDB + S3 + Cognito)
- [[Wiki/entities/Homelab-Ansible]] — Local Docker orchestration (single-node, media server stack)

**Key Patterns:**
- [[Wiki/concepts/AWS CDK Infrastructure as Code]] — Programmatic infrastructure definition
- [[Wiki/concepts/Shared Infrastructure Hub Pattern]] — Central resources for multiple projects
- [[Wiki/concepts/Cross-Stack Resource Sharing]] — CloudFormation exports/imports
- [[Wiki/concepts/Multi-Environment Deployment via Stack Suffix]] — dev/staging/prod isolation
- [[Wiki/concepts/Lambda Authorizer Pattern]] — Custom authentication/authorization
- [[Wiki/concepts/Static Site Deployment Pattern]] — S3 + CloudFront architecture
- [[Wiki/concepts/API Gateway + Lambda Backend Pattern]] — Serverless backend infrastructure

### 🛠️ Utilities & Learning Ecosystem (6 projects) — PHASE 4 COMPLETE ✓

Reusable libraries, experimentation sandboxes, and learning-focused projects. Utilities solve specific problems; learning projects explore new technologies.

**Overview:** [[Wiki/concepts/Utilities & Learning Ecosystem]]

**Projects:**
- [[Wiki/entities/Cellophane]] — Reusable API wrapper library (abstract base class pattern)
- [[Wiki/entities/Close-Application]] — API integration utility (Close.com challenge)
- [[Wiki/entities/MidnightsGitHubActions]] — GitHub Actions CI/CD workflow templates
- [[Wiki/entities/FunWithMusic]] — Music generation sandbox (SCAMP, MIDI, visualization)
- [[Wiki/entities/My-Mini-Projects]] — Monorepo sandbox (Deno tutorials, quick experiments)
- [[Wiki/entities/TableTopMaestro]] — Early-stage campaign management (planning phase)

**Key Patterns:**
- [[Wiki/concepts/Reusable Utility Libraries]] — API wrapper scaffolding and pattern extraction
- [[Wiki/concepts/Experimentation Sandbox]] — Low-friction learning and prototyping
- [[Wiki/concepts/GitHub Actions CI/CD Automation]] — Automated testing and deployment

---

## Learning Sources (Calibration)

External learning materials about wiki patterns, knowledge management, and technologies.

| Source | Type | Date Added | Status |
|--------|------|-----------|--------|
| The LLM Wiki Pattern | [[Wiki/sources/karpathy-llm-wiki-pattern]] | 2026-08-07 | active |
| Obsidian: Second Brain Development | [[Wiki/sources/obsidian-second-brain]] | 2026-08-07 | active |
| Vector Search and Knowledge Systems | [[Wiki/sources/vector-search-knowledge-systems]] | 2026-08-07 | active |

*These were ingested for calibration. See [[Wiki/sources/]] for complete library.*

---

## Entities

Projects, tools, people, organizations. Your workspace entities.

### TTRPG Project Entities

| Project | File | Ecosystem | Status | Updated |
|---------|------|-----------|--------|---------|
| UnnamedRPG | [[Wiki/entities/UnnamedRPG]] | TTRPG | in-progress | 2026-08-07 |
| TTRPG-AI-RAG-Assistant | [[Wiki/entities/TTRPG-AI-RAG-Assistant]] | TTRPG | active | 2026-08-07 |
| AIO Generative AI Solution | [[Wiki/entities/AIO Generative AI Solution]] | TTRPG | active | 2026-08-07 |
| Arcane-Scribe | [[Wiki/entities/Arcane-Scribe]] | TTRPG | active | 2026-08-07 |
| Automated-Taskmaster | [[Wiki/entities/Automated-Taskmaster]] | TTRPG | active | 2026-08-07 |

### AI/LLM Project Entities

| Project | File | Ecosystem | Status | Updated |
|---------|------|-----------|--------|---------|
| brAIniac | [[Wiki/entities/brAIniac]] | AI/LLM | active | 2026-08-07 |
| my-cache-augmented-generation | [[Wiki/entities/my-cache-augmented-generation]] | AI/LLM | in-progress | 2026-08-07 |
| GenerateIdeas | [[Wiki/entities/GenerateIdeas]] | AI/LLM | active | 2026-08-07 |

### AWS Infrastructure Project Entities

| Project | File | Ecosystem | Status | Updated |
|---------|------|-----------|--------|---------|
| my-shared-infra | [[Wiki/entities/my-shared-infra]] | AWS | active | 2026-08-07 |
| My-DDNS-Updater | [[Wiki/entities/My-DDNS-Updater]] | AWS | active | 2026-08-07 |
| chadbarteldotcom | [[Wiki/entities/chadbarteldotcom]] | AWS | active | 2026-08-07 |
| thatsmidnightdotcom | [[Wiki/entities/thatsmidnightdotcom]] | AWS | active | 2026-08-07 |
| Cartographers-Cloud-Kit | [[Wiki/entities/Cartographers-Cloud-Kit]] | AWS | in-progress | 2026-08-07 |
| Homelab-Ansible | [[Wiki/entities/Homelab-Ansible]] | AWS | active | 2026-08-07 |
### Utilities & Learning Project Entities

| Project | File | Ecosystem | Focus | Status | Updated |
|---------|------|-----------|-------|--------|----------|
| Cellophane | [[Wiki/entities/Cellophane]] | Utilities | API wrapper library | active | 2026-08-07 |
| Close-Application | [[Wiki/entities/Close-Application]] | Utilities | API integration | completed | 2026-08-07 |
| MidnightsGitHubActions | [[Wiki/entities/MidnightsGitHubActions]] | Utilities | CI/CD workflows | experimental | 2026-08-07 |
| FunWithMusic | [[Wiki/entities/FunWithMusic]] | Learning | Music generation | experimental | 2026-08-07 |
| My-Mini-Projects | [[Wiki/entities/My-Mini-Projects]] | Learning | Monorepo sandbox | active | 2026-08-07 |
| TableTopMaestro | [[Wiki/entities/TableTopMaestro]] | Learning | Campaign management | planning | 2026-08-07 |
### Tool & Technology Entities

| Entity | Type | Ecosystem | Updated |
|--------|------|-----------|---------|
| Obsidian | tool | Learning | 2026-08-07 |
| qmd | tool | Learning | 2026-08-07 |
| Obsidian CLI | tool | Learning | 2026-08-07 |
| Obsidian Web Clipper | plugin | Learning | 2026-08-07 |
| Dataview Plugin | plugin | Learning | 2026-08-07 |
| Vector Embeddings | technique | Learning | 2026-08-07 |
| FAISS | tool | Learning | 2026-08-07 |

*See [[Wiki/entities/]] for complete directory.*

---

## Concepts

Patterns, architectural insights, techniques, design decisions.

### TTRPG Ecosystem Concepts (Phase 1)

| Concept | Confidence | Updated |
|---------|-----------|---------|
| [[Wiki/concepts/TTRPG Ecosystem]] | high | 2026-08-07 |
| [[Wiki/concepts/RAG Pattern for TTRPG]] | high | 2026-08-07 |
| [[Wiki/concepts/Serverless TTRPG Services]] | high | 2026-08-07 |
| [[Wiki/concepts/Multi-Provider LLM Integration]] | high | 2026-08-07 |

### AI/LLM Ecosystem Concepts (Phase 2)

| Concept | Confidence | Updated |
|---------|-----------|---------|
| [[Wiki/concepts/AI-LLM Ecosystem]] | high | 2026-08-07 |
| [[Wiki/concepts/Local-First AI Architecture]] | high | 2026-08-07 |
| [[Wiki/concepts/Cloud vs. On-Device LLM Strategy]] | high | 2026-08-07 |
| [[Wiki/concepts/Cache-Augmented Generation]] | medium | 2026-08-07 |
| [[Wiki/concepts/FastMCP Protocol]] | high | 2026-08-07 |

### AWS Infrastructure Concepts (Phase 3)

| Concept | Confidence | Updated |
|---------|-----------|---------|
| [[Wiki/concepts/AWS Infrastructure Ecosystem]] | high | 2026-08-07 |
| [[Wiki/concepts/AWS CDK Infrastructure as Code]] | high | 2026-08-07 |
| [[Wiki/concepts/Shared Infrastructure Hub Pattern]] | high | 2026-08-07 |
| [[Wiki/concepts/Cross-Stack Resource Sharing]] | high | 2026-08-07 |
| [[Wiki/concepts/Multi-Environment Deployment via Stack Suffix]] | high | 2026-08-07 |
| [[Wiki/concepts/Lambda Authorizer Pattern]] | high | 2026-08-07 |
| [[Wiki/concepts/Static Site Deployment Pattern]] | high | 2026-08-07 |
| [[Wiki/concepts/API Gateway + Lambda Backend Pattern]] | high | 2026-08-07 |
### Utilities & Learning Concepts (Phase 4)

| Concept | Confidence | Updated |
|---------|-----------|----------|
| [[Wiki/concepts/Reusable Utility Libraries]] | high | 2026-08-07 |
| [[Wiki/concepts/Experimentation Sandbox]] | high | 2026-08-07 |
| [[Wiki/concepts/GitHub Actions CI/CD Automation]] | high | 2026-08-07 |
### Learning Ecosystem Concepts

| Concept | Confidence | Updated |
|---------|-----------|---------|
| [[Wiki/concepts/LLM Wiki Pattern]] | high | 2026-08-07 |
| [[Wiki/concepts/Compound Learning]] | high | 2026-08-07 |
| [[Wiki/concepts/Source Immutability]] | high | 2026-08-07 |
| [[Wiki/concepts/Second Brain]] | high | 2026-08-07 |
| [[Wiki/concepts/Vector Search]] | high | 2026-08-07 |
| [[Wiki/concepts/Hybrid Search]] | high | 2026-08-07 |
| [[Wiki/concepts/Wikilinks]] | high | 2026-08-07 |
| [[Wiki/concepts/Graph View]] | high | 2026-08-07 |

*See [[Wiki/concepts/]] for complete concept library.*

---

## Synthesis (Phase 5 COMPLETE ✓) + Phase 6 AUTOMATION

Query answers and explorations filed back into the wiki. ADHD-optimized navigation and context-switching guides. Plus automated monitoring system.

### Synthesis Pages (6 Created) + Automation

| Synthesis Page | Purpose | Use Case |
|---|---|---|
| [[Wiki/synthesis/Project-Dashboard]] | All 20+ projects at a glance | Quick status reference |
| [[Wiki/synthesis/Quick-Switch-Guide-by-Ecosystem]] | Fast jumps within ecosystems | Context-switching |
| [[Wiki/synthesis/Shared-Infrastructure-Map]] | Dependencies and integrations | Understanding architecture |
| [[Wiki/synthesis/ADHD-Workflow-Optimization]] | 8 patterns for rapid switching | ADHD workflow design |
| [[Wiki/synthesis/Common-Use-Cases]] | "I want to..." decision tree | Finding right projects |
| [[Wiki/synthesis/Technology-Dependency-Graph]] | Tech stacks and learning paths | Tech decisions |
| [[Wiki/synthesis/Phase-6-Automated-Monitoring]] | Wiki auto-sync system guide | Setup and usage |

*See [[Wiki/synthesis/]] for complete synthesis library.*

---

## Progress

### Phase 1: TTRPG Ecosystem ✓ COMPLETE
- Ingested 5 TTRPG projects (UnnamedRPG, TTRPG-AI-RAG-Assistant, AIO AI, Arcane-Scribe, Automated-Taskmaster)
- Created 5 entity pages + 4 concept pages
- Documented RAG pattern, serverless architecture, LLM provider strategy
- Wiki pages: 21 (original) + 9 (Phase 1) = 30 total

### Phase 2: AI/LLM Ecosystem ✓ COMPLETE
- Ingested 3 AI/LLM projects (brAIniac, my-cache-augmented-generation, GenerateIdeas)
- Created 3 entity pages + 5 concept pages
- Documented local-first philosophy, cloud vs. on-device trade-offs, CAG research, FastMCP tools
- Wiki pages: 30 (Phase 1) + 8 (Phase 2) = 38 total

### Phase 3: AWS Infrastructure ✓ COMPLETE
- Ingested 6 AWS infrastructure projects (my-shared-infra, My-DDNS-Updater, chadbarteldotcom, thatsmidnightdotcom, Cartographers-Cloud-Kit, Homelab-Ansible)
- Created 6 entity pages + 8 concept pages (14 pages)
- Documented CDK patterns, hub-and-spoke architecture, serverless APIs, static site hosting, DNSSEC, home IP tracking, multi-environment deployment
- Entity pages: my-shared-infra (central DNS hub), My-DDNS-Updater (dynamic DNS + authorizer), chadbarteldotcom & thatsmidnightdotcom (static sites), Cartographers-Cloud-Kit (serverless API), Homelab-Ansible (local Docker orchestration)
- Concept pages: AWS CDK IaC, Shared Infrastructure Hub, Cross-Stack Sharing, Multi-Environment via Stack Suffix, Lambda Authorizer, Static Site Pattern, API Gateway + Lambda
- Wiki pages: 38 (Phase 1+2) + 14 (Phase 3) = 52 total

### Phase 4: Utilities & Learning ✓ COMPLETE
- Ingested 6 projects (Cellophane, Close-Application, MidnightsGitHubActions, FunWithMusic, My-Mini-Projects, TableTopMaestro)
- Created 6 entity pages + 3 concept pages (9 pages)
- Documented reusable library patterns, experimentation sandboxes, CI/CD automation
- Entity pages: Cellophane (API wrapper library), Close-Application (API integration utility), MidnightsGitHubActions (CI/CD workflows), FunWithMusic (music generation), My-Mini-Projects (sandbox monorepo), TableTopMaestro (campaign management planning)
- Concept pages: Reusable Utility Libraries, Experimentation Sandbox, GitHub Actions CI/CD Automation
- Wiki pages: 52 (Phase 1-3) + 9 (Phase 4) = 61 total

### Phase 5: Cross-Project Synthesis ✓ COMPLETE
- Created: 6 synthesis pages for ADHD-optimized context-switching
- Synthesis pages: Project Dashboard, Quick-Switch Guide, Shared Infrastructure Map, ADHD Workflow Optimization, Common Use Cases, Technology Dependency Graph
- Focus: Cross-ecosystem navigation, project relationships, dependency mapping, workflow patterns
- Benefit: Rapid context-switching support tailored for ADHD workflow management
- Wiki pages: 61 (Phase 1-4) + 6 (Phase 5) = 67 total

### Phase 6: Automated Monitoring ✓ COMPLETE
- Created: Wiki auto-sync script (`scripts/sync-wiki.py`, 700+ lines)
- Features: Project scanning, change detection, wiki page updates, state management
- Automation: GitHub Actions workflow runs every Monday 9 AM UTC
- State tracking: `.last-sync.json` stores project metadata for change detection
- Manual usage: `python scripts/sync-wiki.py [--dry-run] [--verbose]`
- Documentation: Phase-6-Automated-Monitoring.md (comprehensive guide)
- Status: Ready for weekly automated sync or manual on-demand runs
- Total wiki pages: 68 (67 + 1 Phase 6 guide)

---

## Quick Navigation

### For Context-Switching
- [[Wiki/concepts/TTRPG Ecosystem]] — Overview of your TTRPG tools
- [[Wiki/concepts/AWS Infrastructure Ecosystem]] — Overview of your cloud infrastructure
- [[Wiki/entities/]] — Find any project, tool, or entity

### For Learning
- [[Wiki/overview]] — High-level wiki synthesis
- [[Wiki/sources/]] — External learning materials
- [[Wiki/log]] — Operation log (what I've ingested, when)

### For Maintenance
- [[Wiki/log]] — Append-only operation record
- Phase tracking above for current progress
- CLAUDE.md in repo root — Schema and procedures

---

## Unprocessed Workspaces

**PHASE 1 COMPLETE:** 0 projects remaining (5 TTRPG projects fully ingested)

**NEXT:** AI/LLM Ecosystem (brAIniac, my-cache-augmented-generation, GenerateIdeas)
