---
type: synthesis
date_created: 2026-08-07
date_updated: 2026-08-07
tags:
  - wiki/synthesis
  - adhd-workflow
---

# Project Dashboard — Your Workspace at a Glance

Quick reference for all 20+ projects: status, ecosystem, purpose, and quick-jump links.

## The Ecosystem Map

Your workspace is organized into 4 major ecosystems. Each ecosystem has its own purpose and tech stack.

```
┌─────────────────────────────────────────────────────────────┐
│                   YOUR WORKSPACE                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  🎲 TTRPG            🤖 AI/LLM          ☁️ AWS INFRA       │
│  ──────────────────────────────────────────────────────────│
│  • UnnamedRPG        • brAIniac         • my-shared-infra  │
│  • TTRPG-AI-RAG      • CAG Research     • My-DDNS-Updater  │
│  • AIO Generative    • GenerateIdeas    • chadbarteldotcom │
│  • Arcane-Scribe     (3 projects)       • thatsmidnight    │
│  • Taskmaster                           • Cartographers    │
│  (5 projects)                           • Homelab-Ansible  │
│                                         (6 projects)       │
│                                                             │
│  🛠️ UTILITIES & LEARNING                                  │
│  ──────────────────────────────────────────────────────────│
│  • Cellophane (API wrapper library)                        │
│  • Close-Application (API integration utility)             │
│  • MidnightsGitHubActions (CI/CD workflows)               │
│  • FunWithMusic (music generation sandbox)                │
│  • My-Mini-Projects (experiment monorepo)                 │
│  • TableTopMaestro (campaign management planning)         │
│  (6 projects)                                              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Status Dashboard

### 🎲 TTRPG Ecosystem (5 projects, Phase 1 COMPLETE ✓)

| Project | Status | Language | Primary Use | Documentation |
|---------|--------|----------|-------------|----------------|
| [[Wiki/entities/UnnamedRPG]] | in-progress | Python | Game system design | Minimalist RPG framework |
| [[Wiki/entities/TTRPG-AI-RAG-Assistant]] | active | Python | Rule lookup (local) | FastAPI + Gemini RAG |
| [[Wiki/entities/AIO Generative AI Solution]] | active | Python | Rule lookup (alternative) | Docker-based RAG MVP |
| [[Wiki/entities/Arcane-Scribe]] | active | Python/TypeScript | Rule lookup (serverless) | AWS Lambda + Bedrock |
| [[Wiki/entities/Automated-Taskmaster]] | active | Python | Content generation | Encounters, NPCs, loot |

**Quick Context:** Your primary TTRPG stack. Choose based on deployment model:
- **Local:** TTRPG-AI-RAG-Assistant or AIO (Gemini RAG)
- **Serverless:** Arcane-Scribe (AWS Lambda, cost-optimized)
- **Generation:** Automated-Taskmaster (procedural content)

### 🤖 AI/LLM Ecosystem (3 projects, Phase 2 COMPLETE ✓)

| Project | Status | Language | Approach | When to Use |
|---------|--------|----------|----------|------------|
| [[Wiki/entities/brAIniac]] | active | Python | Local-first, uncensored | Private conversations, offline, full control |
| [[Wiki/entities/my-cache-augmented-generation]] | in-progress | Python | Research (CAG) | Experimental RAG alternative |
| [[Wiki/entities/GenerateIdeas]] | active | Python | Cloud (Gemini API) | Quick idea generation, low setup |

**Quick Context:** Three different AI approaches:
- **Privacy:** brAIniac (local, offline)
- **Research:** CAG (novel approach)
- **Quick:** GenerateIdeas (cloud API, stateless)

### ☁️ AWS Infrastructure Ecosystem (6 projects, Phase 3 COMPLETE ✓)

| Project | Status | Type | Cost | When to Use |
|---------|--------|------|------|------------|
| [[Wiki/entities/my-shared-infra]] | active | Hub | ~$1.50/mo | Central DNS, certificates, keys |
| [[Wiki/entities/My-DDNS-Updater]] | active | Lambda | ~$0.50-2/mo | Home IP tracking, Lambda authorizer |
| [[Wiki/entities/chadbarteldotcom]] | active | Static site | ~$1-2/mo | Portfolio hosting |
| [[Wiki/entities/thatsmidnightdotcom]] | active | Static site | ~$1-2/mo | Secondary domain hosting |
| [[Wiki/entities/Cartographers-Cloud-Kit]] | in-progress | API | ~$2-9/mo | Game asset management API |
| [[Wiki/entities/Homelab-Ansible]] | active | Orchestration | Local | Media server, DNS, VPN |

**Quick Context:** Cloud infrastructure in hub-and-spoke pattern:
- **Hub:** my-shared-infra (Route 53, KMS, exports resources)
- **Spokes:** chadbarteldotcom, My-DDNS-Updater, Cartographers-Cloud-Kit (import from hub)
- **Local:** Homelab-Ansible (Docker Compose, not AWS)

### 🛠️ Utilities & Learning Ecosystem (6 projects, Phase 4 COMPLETE ✓)

| Project | Status | Type | Language | Purpose |
|---------|--------|------|----------|---------|
| [[Wiki/entities/Cellophane]] | active | Library | Python | Reusable API wrapper scaffolding |
| [[Wiki/entities/Close-Application]] | completed | Utility | Python | API integration reference |
| [[Wiki/entities/MidnightsGitHubActions]] | experimental | Workflows | YAML | Central CI/CD templates |
| [[Wiki/entities/FunWithMusic]] | experimental | Sandbox | Python | Music generation learning |
| [[Wiki/entities/My-Mini-Projects]] | active | Sandbox | Deno/Python | Quick experiments monorepo |
| [[Wiki/entities/TableTopMaestro]] | planning | Framework | Python | Campaign management (TBD) |

**Quick Context:** Support infrastructure and learning spaces:
- **Reusable:** Cellophane (use in new API projects)
- **CI/CD:** MidnightsGitHubActions (all projects reference)
- **Exploration:** FunWithMusic, My-Mini-Projects (learning sandboxes)
- **Future:** TableTopMaestro (campaign hub, not yet implemented)

---

## Quick Jump by Use Case

**"I want to..."** → Which project(s)?

### TTRPG Gaming
- **Look up rules:** [[Wiki/entities/TTRPG-AI-RAG-Assistant]] (local) or [[Wiki/entities/Arcane-Scribe]] (serverless)
- **Generate encounter:** [[Wiki/entities/Automated-Taskmaster]]
- **Design system:** [[Wiki/entities/UnnamedRPG]]
- **Manage campaign:** [[Wiki/entities/TableTopMaestro]] (coming soon)

### AI & Content Generation
- **Local AI chat:** [[Wiki/entities/brAIniac]]
- **Generate ideas:** [[Wiki/entities/GenerateIdeas]]
- **RAG research:** [[Wiki/entities/my-cache-augmented-generation]]
- **Research RAG:** [[Wiki/entities/TTRPG-AI-RAG-Assistant]] or [[Wiki/entities/Arcane-Scribe]]

### Cloud Infrastructure
- **Host website:** [[Wiki/entities/chadbarteldotcom]] or [[Wiki/entities/thatsmidnightdotcom]]
- **Build API:** [[Wiki/entities/Cartographers-Cloud-Kit]]
- **DNS management:** [[Wiki/entities/my-shared-infra]]
- **Home IP tracking:** [[Wiki/entities/My-DDNS-Updater]]
- **Media server:** [[Wiki/entities/Homelab-Ansible]]

### Learning & Utilities
- **Build API wrapper:** [[Wiki/entities/Cellophane]]
- **Setup CI/CD:** [[Wiki/entities/MidnightsGitHubActions]]
- **Music generation:** [[Wiki/entities/FunWithMusic]]
- **Quick experiment:** [[Wiki/entities/My-Mini-Projects]]

---

## Dependency Map at a Glance

### Who Depends on Whom?

```
my-shared-infra (Hub)
  ├── chadbarteldotcom (imports hosted zone, KMS key)
  ├── thatsmidnightdotcom (imports hosted zone, KMS key)
  ├── My-DDNS-Updater (imports hosted zone, KMS key)
  └── Cartographers-Cloud-Kit (imports hosted zone, IP whitelist from DDNS)

MidnightsGitHubActions (Central CI/CD)
  ├── Cellophane (runs tests, linting)
  ├── TTRPG-AI-RAG-Assistant (runs tests)
  ├── Arcane-Scribe (runs tests)
  ├── brAIniac (runs tests)
  └── All Python projects

Homelab-Ansible (Local Docker)
  └── Jellyfin, Pi-hole, OpenVPN, Nginx (services)
```

---

## Technology Quick Reference

### Languages
- **Python 3.12:** Cellophane, TTRPG-AI-RAG, AIO AI, Arcane-Scribe, Taskmaster, brAIniac, CAG, GenerateIdeas, TableTopMaestro, FunWithMusic
- **TypeScript/Deno:** My-Mini-Projects (tutorials)
- **YAML:** MidnightsGitHubActions (workflows)
- **HCL/CDK:** my-shared-infra, My-DDNS-Updater, chadbarteldotcom, thatsmidnightdotcom, Cartographers-Cloud-Kit
- **Ansible:** Homelab-Ansible

### Cloud Providers
- **AWS:** my-shared-infra, My-DDNS-Updater, chadbarteldotcom, thatsmidnightdotcom, Cartographers-Cloud-Kit (6 projects)
- **Google Cloud:** GenerateIdeas (Gemini API)
- **Local:** brAIniac (Ollama), Homelab-Ansible (Docker)

### Frameworks
- **Web:** FastAPI (Arcane-Scribe, Cartographers-Cloud-Kit, TTRPG-AI-RAG)
- **Music:** SCAMP (FunWithMusic)
- **Orchestration:** Ansible (Homelab-Ansible), Docker Compose (local)
- **CDK:** AWS CDK v2 (infrastructure projects)

---

## Status Symbols Explained

- ✓ **Active:** In production or regular use
- ⏳ **In-Progress:** Under active development
- 📋 **Planning:** Design phase, minimal implementation
- 🧪 **Experimental:** Early-stage, learning/exploration
- ✅ **Completed:** Finished (reference implementation)

---

## Next Steps

1. **Quick Context:** Read the table for your target ecosystem
2. **Jump to Project:** Click the project link to read full entity page
3. **Understand Dependencies:** Check Dependency Map if context-switching
4. **Learn Patterns:** Visit [[Wiki/concepts/]] for architectural deep dives

See [[Wiki/synthesis/Quick-Switch-Guide-by-Ecosystem]] for faster jumps between similar projects.
