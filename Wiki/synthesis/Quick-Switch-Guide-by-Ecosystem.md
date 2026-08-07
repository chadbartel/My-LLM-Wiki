---
type: synthesis
date_created: 2026-08-07
date_updated: 2026-08-07
tags:
  - wiki/synthesis
  - adhd-workflow
---

# Quick-Switch Guide by Ecosystem

Rapid context-jumping between projects within the same ecosystem. No deep context needed—just the essentials to get started.

## 🎲 TTRPG Ecosystem — Which Project First?

**You're designing encounter rules → You need:**
1. [[Wiki/entities/UnnamedRPG]] (system foundation)
2. [[Wiki/entities/Automated-Taskmaster]] (test encounters)
3. [[Wiki/entities/TTRPG-AI-RAG-Assistant]] (validate rules via RAG)

**You're running a campaign → You need:**
1. [[Wiki/entities/TableTopMaestro]] (campaign hub, when ready)
2. [[Wiki/entities/TTRPG-AI-RAG-Assistant]] or [[Wiki/entities/Arcane-Scribe]] (rule lookup during play)
3. [[Wiki/entities/Automated-Taskmaster]] (generate encounters on the fly)

**You want to test rule system locally → You need:**
1. [[Wiki/entities/TTRPG-AI-RAG-Assistant]] (FastAPI, local Gemini)
2. [[Wiki/entities/UnnamedRPG]] (your system definition)
3. [[Wiki/entities/AIO Generative AI Solution]] (Docker alternative)

**You want serverless rule lookup → You need:**
1. [[Wiki/entities/Arcane-Scribe]] (AWS Lambda + Bedrock)
2. [[Wiki/entities/my-shared-infra]] (DNS infrastructure)
3. [[Wiki/entities/Cartographers-Cloud-Kit]] (API authorization, if needed)

### Quick Reference
| Scenario | Start Here | Then | Finally |
|----------|-----------|------|---------|
| Design rules | UnnamedRPG | TTRPG-AI-RAG | Automated-Taskmaster |
| Run campaign | TTRPG-AI-RAG | Automated-Taskmaster | TableTopMaestro (TBD) |
| Deploy serverless | Arcane-Scribe | my-shared-infra | (Done) |
| Test locally | AIO AI or TTRPG-RAG | UnnamedRPG | (Done) |

---

## 🤖 AI/LLM Ecosystem — Pick Your Approach

**You want private, local AI → Choose:**
[[Wiki/entities/brAIniac]]
- No cloud. Everything local. Offline-capable.
- 8GB VRAM ceiling (RTX 2070 SUPER)
- FastMCP tools for local integrations
- **When:** Privacy is critical, you're comfortable with 8B model limits

**You want to generate ideas fast → Choose:**
[[Wiki/entities/GenerateIdeas]]
- Stateless. No history. Just Gemini API calls.
- Minimal setup. No dependencies. Fast feedback.
- **When:** Quick iteration, don't need context, okay with cloud

**You want to research RAG alternatives → Choose:**
[[Wiki/entities/my-cache-augmented-generation]]
- Experiment with Cache-Augmented Generation (CAG)
- Alternative to traditional RAG
- Research-oriented, not production
- **When:** Exploring novel approaches, okay with instability

### Decision Tree

```
Do you need privacy/offline?
  ├─ YES → brAIniac (local, no cloud)
  └─ NO → Do you need to maintain conversation history?
           ├─ NO → GenerateIdeas (stateless, fast)
           └─ YES → Consider integrating brAIniac or CAG
```

### Project Relationships
- **brAIniac** uses Ollama (4-bit GGUF models, local inference)
- **GenerateIdeas** uses Google Gemini API (cloud, cost-per-call)
- **my-cache-augmented-generation** uses LLMs as research platform

---

## ☁️ AWS Infrastructure Ecosystem — Deploy Strategy

**You're deploying a new service → Follow this order:**

1. **Check my-shared-infra** — Do you need a hosted zone or KMS key?
   - If YES: [[Wiki/entities/my-shared-infra]] is already deployed (or deploy it first)
   - If NO: Skip to next step

2. **Choose your pattern:**
   
   **Static Site?** → [[Wiki/entities/chadbarteldotcom]] (template)
   - S3 + CloudFront + ACM + Route 53
   - Deploy via `cdk deploy`
   
   **REST API?** → [[Wiki/entities/Cartographers-Cloud-Kit]] (template)
   - FastAPI + Lambda + API Gateway + DynamoDB
   - Deploy via `cdk deploy`
   
   **DNS Service?** → [[Wiki/entities/My-DDNS-Updater]] (template)
   - Lambda authorizer + EventBridge scheduler
   - Deploy via `cdk deploy`

3. **Need home IP whitelisting?** → [[Wiki/entities/My-DDNS-Updater]]
   - Automatically tracks your home IP
   - Lambda Authorizer uses it for IP-based access control

4. **Need local services?** → [[Wiki/entities/Homelab-Ansible]]
   - Ansible playbooks for Docker Compose
   - Media server, DNS (Pi-hole), VPN
   - Not AWS, but part of infrastructure ecosystem

### Quick Commands

```bash
# Deploy new static site (using chadbarteldotcom as template)
cd chadbarteldotcom && cdk deploy

# Deploy new API (using Cartographers-Cloud-Kit as template)
cd Cartographers-Cloud-Kit && cdk deploy

# Verify infrastructure
aws cloudformation list-stacks --query "StackSummaries[].StackName"
```

---

## 🛠️ Utilities & Learning Ecosystem — Pick Your Context

**You're building a new API wrapper → Start with:**
[[Wiki/entities/Cellophane]]
- Inherit from CellophaneBase
- Implement your authentication logic
- Get automatic retry, error handling, type hints

**You need CI/CD for your project → Use:**
[[Wiki/entities/MidnightsGitHubActions]]
- Reference central workflows from your project
- No duplicate YAML across repos
- Consistent testing, linting, deployment

**You want to learn music generation → Explore:**
[[Wiki/entities/FunWithMusic]]
- Follow SCAMP tutorials
- Start simple (hello_world.py)
- Progress to algorithmic composition

**You want to experiment with something new → Use:**
[[Wiki/entities/My-Mini-Projects]]
- Create new subdirectory under `src/`
- Copy structure from `example-project/`
- No repo overhead, easy to discard

**You need a campaign management tool → Plan with:**
[[Wiki/entities/TableTopMaestro]]
- Read design docs (breakdown_of_design.md, character_creation.md)
- Contribute to roadmap
- Implementation coming soon

---

## Cross-Ecosystem Jumps

**"I'm in TTRPG, need to switch to AI":**
1. Close your TTRPG project
2. Read [[Wiki/concepts/AI-LLM Ecosystem]] (30 seconds)
3. Choose: Privacy (brAIniac) or Speed (GenerateIdeas)
4. Jump to that project

**"I'm in AWS, need to switch to TTRPG":**
1. Save your CDK changes
2. Read [[Wiki/concepts/TTRPG Ecosystem]] (30 seconds)
3. Choose: Local (TTRPG-AI-RAG) or Serverless (Arcane-Scribe)
4. Jump to that project

**"I'm in Utilities, need game asset API":**
1. You might already have it: [[Wiki/entities/Cartographers-Cloud-Kit]] is both
2. If not, use [[Wiki/entities/Cellophane]] as template for new API

---

## One-Command Quick Start

### TTRPG Projects
```bash
cd TTRPG-AI-RAG-Assistant && poetry install && poetry run python main.py

cd Arcane-Scribe && poetry install && cdk deploy

cd Automated-Taskmaster && poetry install && poetry run python main.py
```

### AI/LLM Projects
```bash
cd brAIniac && poetry install && docker compose up -d ollama && poetry run python main.py

cd GenerateIdeas && poetry install && poetry run python main.py --idea "medieval fantasy"

cd my-cache-augmented-generation && poetry install && poetry run pytest
```

### AWS Infrastructure
```bash
cd my-shared-infra && poetry install && cdk deploy

cd chadbarteldotcom && poetry install && cdk deploy

cd Cartographers-Cloud-Kit && poetry install && cdk deploy --context stack-suffix=dev
```

### Utilities & Learning
```bash
cd Cellophane && poetry install && poetry run pytest

cd FunWithMusic && python scamp_tutorials/hello_world.py

cd My-Mini-Projects && deno run src/deno-tutorials/hello_world.ts
```

---

## When to Switch Projects

### 🟢 GOOD Reasons to Switch
- ✓ You've hit a wall; fresh eyes help (come back later)
- ✓ You're waiting for deployment/tests to finish
- ✓ You had a sudden idea in a different project
- ✓ You need to reference another project's code

### 🔴 NOT Good Reasons to Switch
- ✗ Distraction (discipline: finish the task)
- ✗ Task is 90% done (finish it first)
- ✗ "Let me just quickly check..." (you'll lose context)

### Context-Switch Checklist

Before switching, do this (takes 2 minutes):
- [ ] Commit/save your current work
- [ ] Write a 1-line note in project README: "Stopped here: [what I was doing]"
- [ ] Read the quick-switch guide for target project (this page)
- [ ] Jump to target project

Coming back to old project? Read your note first to restore context.

---

## Related Synthesis Pages

- [[Wiki/synthesis/Project-Dashboard]] — Full status of all projects
- [[Wiki/synthesis/Shared-Infrastructure-Map]] — How projects depend on each other
- [[Wiki/synthesis/ADHD-Workflow-Optimization]] — Patterns for rapid context-switching
- [[Wiki/synthesis/Technology-Dependency-Graph]] — Which projects use which tech
