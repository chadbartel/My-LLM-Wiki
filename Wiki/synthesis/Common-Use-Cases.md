---
type: synthesis
date_created: 2026-08-07
date_updated: 2026-08-07
tags:
  - wiki/synthesis
---

# Common Use Cases — "I Want To..." Decision Tree

Quick routing table: "I want to [goal]" → Which projects do I need?

## Gaming & TTRPG

### "I want to run a D&D campaign"

**Minimum Setup:**
1. [[Wiki/entities/UnnamedRPG]] (for your system, if custom)
2. [[Wiki/entities/TTRPG-AI-RAG-Assistant]] OR [[Wiki/entities/Arcane-Scribe]] (rule lookup during play)
3. [[Wiki/entities/Automated-Taskmaster]] (generate encounters on the fly)

**Optional:**
4. [[Wiki/entities/TableTopMaestro]] (campaign planning, when ready)

**Time to First Play:** 30 minutes (depends on RAG setup)

---

### "I want to design my own game system"

**Required:**
1. [[Wiki/entities/UnnamedRPG]] (design document repository)
2. [[Wiki/entities/TTRPG-AI-RAG-Assistant]] (test rules via RAG)

**Optional:**
3. [[Wiki/entities/Automated-Taskmaster]] (test content generation with your system)

**Time to First Test:** 1 hour

---

### "I want to generate random encounters"

**Minimum:**
1. [[Wiki/entities/Automated-Taskmaster]] (with UnnamedRPG rules or standard rules)

**Optional:**
2. [[Wiki/entities/TTRPG-AI-RAG-Assistant]] (validate encounters against rule system)

**Time to First Generated Encounter:** 5 minutes

---

### "I want to manage a campaign (players, NPCs, plot)"

**Requirement:**
1. [[Wiki/entities/TableTopMaestro]] (when implementation ready)

**For Now (Alternative):**
- Manually use [[Wiki/entities/Automated-Taskmaster]] to generate content
- Store content in spreadsheets or GitHub

**Time to First Campaign:** TBD (TableTopMaestro not yet implemented)

---

## AI & Content Generation

### "I want to brainstorm ideas locally (no cloud, no logs)"

**Required:**
1. [[Wiki/entities/brAIniac]] (local LLM, offline capable, uncensored)

**Setup:**
- Docker running Ollama with 7B/8B model
- FastMCP tools for local operations

**Time to First Conversation:** 5 minutes (after Ollama model download)

**Privacy:** 100% local, nothing sent to cloud

---

### "I want to generate ideas fast (no setup)"

**Required:**
1. [[Wiki/entities/GenerateIdeas]] (stateless Gemini API)

**Setup:**
- Python + poetry
- Google Cloud API key

**Time to First Idea:** 2 minutes

**Privacy:** Ideas sent to Google Cloud (not private)

**Cost:** ~$0.01-0.05 per query (very cheap)

---

### "I want to explore novel RAG alternatives"

**Requirement:**
1. [[Wiki/entities/my-cache-augmented-generation]] (research implementation of CAG paper)

**For Production RAG:**
2. [[Wiki/entities/TTRPG-AI-RAG-Assistant]] (proven, local Gemini RAG)

**Time to First Experiment:** 30 minutes

---

### "I want to power my TTRPG rule lookup with LLM"

**Option 1 (Local):**
1. [[Wiki/entities/TTRPG-AI-RAG-Assistant]] (FastAPI + Gemini, local machine)
2. [[Wiki/entities/UnnamedRPG]] (your rule documents, ingested to RAG)

**Option 2 (Serverless):**
1. [[Wiki/entities/Arcane-Scribe]] (AWS Lambda + Bedrock)
2. [[Wiki/entities/my-shared-infra]] (DNS infrastructure)

**Time to First Rule Query:** 1 hour (local) or 2 hours (serverless)

---

## Cloud & Infrastructure

### "I want to host my portfolio website"

**Required:**
1. [[Wiki/entities/my-shared-infra]] (hosted zone, KMS key)
2. [[Wiki/entities/chadbarteldotcom]] (copy, customize domain)
3. [[Wiki/entities/MidnightsGitHubActions]] (CI/CD for deployments)

**Setup Time:** 30 minutes (copy + customize + deploy)

**Monthly Cost:** ~$1-2

**Automation:** Auto-deployed on git push

---

### "I want to build a REST API (serverless)"

**Required:**
1. [[Wiki/entities/my-shared-infra]] (hub)
2. [[Wiki/entities/Cartographers-Cloud-Kit]] (copy, customize)
3. [[Wiki/entities/MidnightsGitHubActions]] (CI/CD)

**Optional:**
4. [[Wiki/entities/My-DDNS-Updater]] (if you need home IP whitelisting)

**Setup Time:** 1-2 hours

**Monthly Cost:** ~$2-5 (depends on usage)

**Language:** Python (FastAPI)

---

### "I want to track my home IP (dynamic DNS)"

**Required:**
1. [[Wiki/entities/my-shared-infra]] (hub)
2. [[Wiki/entities/My-DDNS-Updater]] (deploy)

**Use Case:** Update DNS when home IP changes (ISP resets connection)

**Setup Time:** 30 minutes

**Monthly Cost:** ~$0.50-2

**Benefit:** Cartographers-Cloud-Kit can use this IP for authorization

---

### "I want to run local services (media server, DNS, VPN)"

**Required:**
1. [[Wiki/entities/Homelab-Ansible]] (Ansible playbooks + Docker Compose)

**Included Services:**
- Jellyfin (media streaming)
- Pi-hole (DNS + ad-blocking)
- OpenVPN or Tailscale (VPN access)
- Nginx Proxy Manager (reverse proxy)

**Setup Time:** 1-2 hours (depends on familiarity with Ansible)

**Monthly Cost:** Electricity only (~$2-5)

**Hardware:** Monolith at 192.168.1.17 (Ryzen 9, RTX 2070 SUPER)

---

## Reusable Libraries & Tools

### "I want to build an API client wrapper"

**Use:**
1. [[Wiki/entities/Cellophane]] (inherit from CellophaneBase)

**Benefits:**
- Automatic retry with re-auth
- Type hints for IDE support
- Consistent error handling

**Time to First Wrapper:** 30 minutes

**Example Use Case:**
- Close.com API client (see [[Wiki/entities/Close-Application]])
- Any external REST API

---

### "I want to set up CI/CD for my Python project"

**Use:**
1. [[Wiki/entities/MidnightsGitHubActions]] (reference central workflows)

**Benefits:**
- No duplicate YAML across repos
- Consistent testing (pytest, black, flake8, mypy)
- Automatic release on version tags

**Time to First CI/CD:** 10 minutes

---

### "I want to learn music generation"

**Use:**
1. [[Wiki/entities/FunWithMusic]] (follow SCAMP tutorials)

**Progression:**
- `hello_world.py` → Play a simple note
- `scales_and_modes.py` → Music theory concepts
- `algorithmic_composition.py` → Generative music

**Time to First Sound:** 5 minutes

**Difficulty:** Medium (music theory + programming)

---

### "I want a place to experiment (no pressure)"

**Use:**
1. [[Wiki/entities/My-Mini-Projects]] (monorepo sandbox)

**How:**
- Create `src/my-experiment/`
- Copy `example-project/` structure
- Start coding, no production pressure

**Time to Start:** 5 minutes

**Graduation Path:** When experiment is stable, promote to real project

---

## Quick-Start by Language

### Python

**Want to learn?**
- [[Wiki/entities/FunWithMusic]] (music generation)
- [[Wiki/entities/My-Mini-Projects]] (quick experiments)

**Want to build?**
- [[Wiki/entities/TTRPG-AI-RAG-Assistant]] (FastAPI RAG)
- [[Wiki/entities/brAIniac]] (local AI chat)
- [[Wiki/entities/Cellophane]] (API wrapper library)

**Want cloud?**
- [[Wiki/entities/Arcane-Scribe]] (Lambda + Bedrock)
- [[Wiki/entities/Cartographers-Cloud-Kit]] (FastAPI on Lambda)

### TypeScript/Deno

**Want to learn?**
- [[Wiki/entities/My-Mini-Projects]] → `src/deno-tutorials/`

**Want to build?**
- No current TypeScript projects (but [[Wiki/entities/Arcane-Scribe]] uses TypeScript for CDK)

### YAML (Infrastructure as Code)

**Want to learn?**
- [[Wiki/entities/my-shared-infra]] (AWS CDK, Python)
- [[Wiki/entities/Homelab-Ansible]] (Ansible playbooks)

**Want to build?**
- [[Wiki/entities/MidnightsGitHubActions]] (GitHub Actions workflows)
- [[Wiki/entities/Homelab-Ansible]] (infrastructure automation)

---

## Decision Tree: Pick Your First Project

```
Do you want to play TTRPG?
├─ YES → Start with TTRPG-AI-RAG-Assistant
└─ NO → Do you want to learn AI?
         ├─ YES → Start with brAIniac (privacy) or GenerateIdeas (speed)
         └─ NO → Do you want to deploy to cloud?
                  ├─ YES → Start with my-shared-infra (hub)
                  └─ NO → Do you want to experiment?
                           ├─ YES → Start with My-Mini-Projects
                           └─ NO → Start with this synthesis page again :)
```

---

## Recommendation by Experience Level

### Beginner (No experience with most projects)

**Week 1-2: Explore**
1. Read [[Wiki/synthesis/Project-Dashboard]]
2. Read [[Wiki/synthesis/Quick-Switch-Guide-by-Ecosystem]]
3. Pick one ecosystem, read all entity pages

**Week 3: Try**
1. Follow one quick-start (e.g., TTRPG-AI-RAG or GenerateIdeas)
2. Run `poetry install && poetry run python main.py`
3. Play with it

**Week 4: Plan**
1. Pick your anchor project
2. Read ADHD-Workflow-Optimization patterns
3. Choose 1-2 patterns to try

### Intermediate (Familiar with 5-10 projects)

**Pick your anchor project** (something you want to ship in 4 weeks)
- [[Wiki/entities/TableTopMaestro]] (design phase ready)
- [[Wiki/entities/Cartographers-Cloud-Kit]] (API design)
- [[Wiki/entities/brAIniac]] (Phase 2 features)

**Weekly rhythm:** [[Wiki/synthesis/ADHD-Workflow-Optimization]] Pattern 1 or 7

**Friday synthesis:** Update wiki with learnings

### Advanced (Familiar with most projects)

**You're in architect mode.** Consider:
1. [[Wiki/synthesis/Shared-Infrastructure-Map]] — Adding new projects?
2. [[Wiki/synthesis/Technology-Dependency-Graph]] — What's missing tech-wise?
3. [[Wiki/synthesis/ADHD-Workflow-Optimization]] Pattern 8 — Hyperfocus strategically

---

## Related Synthesis Pages

- [[Wiki/synthesis/Project-Dashboard]] — All projects status
- [[Wiki/synthesis/Quick-Switch-Guide-by-Ecosystem]] — Jump between similar projects
- [[Wiki/synthesis/Shared-Infrastructure-Map]] — Dependencies & integrations
