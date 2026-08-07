---
type: synthesis
date_created: 2026-08-07
date_updated: 2026-08-07
tags:
  - wiki/synthesis
---

# Technology Dependency Graph — Tech Stack Overview

Map of which technologies are used across your 20+ projects. Use this to understand tech patterns, identify opportunities for reuse, and plan learning priorities.

## Language Distribution

### Python (Dominant Language)

**Python 3.12+ Projects (13 total):**

Core TTRPG:
- [[Wiki/entities/UnnamedRPG]]
- [[Wiki/entities/TTRPG-AI-RAG-Assistant]] (FastAPI)
- [[Wiki/entities/AIO Generative AI Solution]] (FastAPI, Docker)
- [[Wiki/entities/Arcane-Scribe]] (FastAPI, CDK)
- [[Wiki/entities/Automated-Taskmaster]] (FastAPI)

Core AI/LLM:
- [[Wiki/entities/brAIniac]] (Ollama, FastMCP)
- [[Wiki/entities/my-cache-augmented-generation]]
- [[Wiki/entities/GenerateIdeas]] (Gemini API)

Core AWS:
- [[Wiki/entities/my-shared-infra]] (CDK)
- [[Wiki/entities/My-DDNS-Updater]] (CDK, Lambda)
- [[Wiki/entities/Cartographers-Cloud-Kit]] (CDK, Lambda, FastAPI)

Core Utilities:
- [[Wiki/entities/Cellophane]] (base library)
- [[Wiki/entities/FunWithMusic]] (SCAMP)
- [[Wiki/entities/TableTopMaestro]]

**Shared Stack Across Python Projects:**
- Poetry (dependency management)
- pytest (testing)
- Black (formatting)
- isort (import sorting)
- flake8 (linting)
- mypy (type checking)
- Type hints (required in all projects)

---

### TypeScript / Deno

**TypeScript Projects (3 total):**
- [[Wiki/entities/Arcane-Scribe]] (CDK for AWS)
- [[Wiki/entities/chadbarteldotcom]] (CDK for AWS)
- [[Wiki/entities/thatsmidnightdotcom]] (CDK for AWS)

**Deno Projects (1 total):**
- [[Wiki/entities/My-Mini-Projects]] (tutorials only)

**Shared Stack:**
- AWS CDK v2 (Infrastructure as Code)
- Type hints (required)

---

### YAML (Infrastructure)

**YAML Projects (2 total):**
- [[Wiki/entities/Homelab-Ansible]] (Ansible playbooks)
- [[Wiki/entities/MidnightsGitHubActions]] (GitHub Actions workflows)

---

### Others

- **Bash:** Homelab-Ansible (task scripts)
- **HCL:** AWS configuration files
- **Markdown:** Documentation (all projects)

---

## Framework & Library Distribution

### Web Frameworks

**FastAPI (HTTP APIs):**
- [[Wiki/entities/TTRPG-AI-RAG-Assistant]] (local rule lookup)
- [[Wiki/entities/AIO Generative AI Solution]] (Docker RAG)
- [[Wiki/entities/Automated-Taskmaster]] (encounter/NPC/loot generation)
- [[Wiki/entities/Cartographers-Cloud-Kit]] (serverless via Lambda + Mangum)
- Potential: [[Wiki/entities/brAIniac]] (API server, TBD)

**Static Sites (S3 + CloudFront):**
- [[Wiki/entities/chadbarteldotcom]]
- [[Wiki/entities/thatsmidnightdotcom]]

---

### LLM & AI

**Cloud LLM APIs:**
- Google Gemini → [[Wiki/entities/GenerateIdeas]], [[Wiki/entities/TTRPG-AI-RAG-Assistant]]
- AWS Bedrock → [[Wiki/entities/Arcane-Scribe]]

**Local LLM:**
- Ollama (4-bit GGUF) → [[Wiki/entities/brAIniac]]

**RAG Frameworks:**
- LlamaIndex → [[Wiki/entities/TTRPG-AI-RAG-Assistant]], [[Wiki/entities/AIO Generative AI Solution]]
- LangChain → [[Wiki/entities/Arcane-Scribe]]

**Research/Experimental:**
- Cache-Augmented Generation → [[Wiki/entities/my-cache-augmented-generation]]

---

### Data & Storage

**Databases:**
- **DynamoDB** (AWS) → [[Wiki/entities/Cartographers-Cloud-Kit]]
- **SQLite** (local) → [[Wiki/entities/brAIniac]], [[Wiki/entities/my-cache-augmented-generation]]

**File Storage:**
- **S3** (cloud) → [[Wiki/entities/chadbarteldotcom]], [[Wiki/entities/thatsmidnightdotcom]]
- **Local filesystem** → [[Wiki/entities/UnnamedRPG]], [[Wiki/entities/TTRPG-AI-RAG-Assistant]]

**Caching:**
- **Redis** → Not currently used (could add to brAIniac)
- **Application cache** → [[Wiki/entities/my-cache-augmented-generation]]

---

### Music & Audio

**Music Notation & Generation:**
- **SCAMP** (Symbolic Composition And Music Processing) → [[Wiki/entities/FunWithMusic]]
- **python-rtmidi** (MIDI control) → [[Wiki/entities/FunWithMusic]]
- **matplotlib** (visualization) → [[Wiki/entities/FunWithMusic]]

---

### Orchestration & Deployment

**Infrastructure as Code:**
- **AWS CDK v2** (Python) → my-shared-infra, My-DDNS-Updater, Cartographers-Cloud-Kit, chadbarteldotcom, thatsmidnightdotcom
- **Ansible** → [[Wiki/entities/Homelab-Ansible]]
- **Docker Compose V2** → Homelab-Ansible, brAIniac, my-cache-augmented-generation

**Container Runtime:**
- **Docker Engine** (standalone, not Swarm) → Homelab-Ansible
- **Ollama** (containerized LLM) → [[Wiki/entities/brAIniac]]

**Cloud Platform:**
- **AWS** (Lambda, API Gateway, S3, CloudFront, DynamoDB, Route 53, KMS, Cognito, SSM) → all AWS projects
- **Google Cloud** (Gemini API) → GenerateIdeas, TTRPG-AI-RAG-Assistant

---

### Testing & Quality

**Shared Across All Python Projects:**
- pytest (test framework)
- unittest.mock (mocking)
- pytest fixtures (test setup)

**Project-Specific Testing:**
- moto (AWS service mocking) → CDK projects
- Docker testing → brAIniac, my-cache-augmented-generation

---

### Development Tools

**All Python Projects:**
- Poetry (dependency management)
- Black (code formatting)
- isort (import sorting)
- flake8 (linting)
- mypy (static type checking)

**Infrastructure Projects:**
- AWS CDK CLI
- Ansible CLI
- Docker CLI / Docker Compose

**CI/CD:**
- GitHub Actions → [[Wiki/entities/MidnightsGitHubActions]]

---

## Tech Debt & Opportunities

### Currently Underutilized

| Technology | Where It Could Help | Current Use |
|------------|---------------------|------------|
| Redis | Caching, session management | Unused |
| WebSockets | Real-time updates (campaigns, games) | Unused |
| PostgreSQL | Relational data with complex queries | DynamoDB used instead |
| Vector Databases | Specialized RAG (Pinecone, Weaviate) | In-memory cache used |

### Potential Improvements

1. **Reduce Python Boilerplate** → Use Pydantic v2 everywhere (already in some projects)
2. **Standardize Async** → Move TTRPG-AI-RAG to async/await throughout
3. **Add Observability** → Structured logging (structlog), distributed tracing (Jaeger)
4. **Containerize More** → TTRPG-AI-RAG could be Docker container
5. **Add Caching Layer** → Redis for Gemini API responses (cost reduction)

---

## Tech Stack by Project: Complete Reference

### TTRPG Ecosystem

| Project | Languages | Frameworks | Database | Deployment |
|---------|-----------|-----------|----------|------------|
| UnnamedRPG | Python | None (data model) | Filesystem | Local |
| TTRPG-AI-RAG | Python | FastAPI, LlamaIndex | Filesystem | Local/Docker |
| AIO AI | Python | FastAPI, LlamaIndex | Filesystem | Docker |
| Arcane-Scribe | Python, TypeScript | FastAPI, LangChain, CDK | Filesystem | Lambda |
| Taskmaster | Python | FastAPI | Filesystem | Lambda |

### AI/LLM Ecosystem

| Project | Languages | Frameworks | Database | Deployment |
|---------|-----------|-----------|----------|------------|
| brAIniac | Python | FastMCP, Ollama | SQLite | Local (Docker) |
| CAG | Python | Custom | SQLite | Local/Research |
| GenerateIdeas | Python | None (API wrapper) | None | Stateless CLI |

### AWS Infrastructure

| Project | Languages | Frameworks | Database | Deployment |
|---------|-----------|-----------|----------|------------|
| my-shared-infra | Python | CDK | Hosted Zone, KMS | CloudFormation |
| My-DDNS-Updater | Python, TypeScript | CDK, Lambda | SSM Parameter | Lambda |
| chadbarteldotcom | TypeScript | CDK | None (static) | S3 + CloudFront |
| thatsmidnightdotcom | TypeScript | CDK | None (static) | S3 + CloudFront |
| Cartographers-Cloud-Kit | Python, TypeScript | FastAPI, CDK | DynamoDB | Lambda + API Gateway |
| Homelab-Ansible | YAML, Bash | Ansible, Docker Compose | Varies (Docker volumes) | Local Docker |

### Utilities & Learning

| Project | Languages | Frameworks | Database | Deployment |
|---------|-----------|-----------|----------|------------|
| Cellophane | Python | None (base class) | None | PyPI library |
| Close-Application | Python | Custom (API wrapper) | None | Executable |
| MidnightsGitHubActions | YAML | GitHub Actions | None | GitHub workflows |
| FunWithMusic | Python | SCAMP, matplotlib | None | Local execution |
| My-Mini-Projects | Python, Deno | Various (tutorials) | None | Local |
| TableTopMaestro | Python | TBD | TBD | TBD (planning phase) |

---

## Learning Paths by Technology Interest

### "I want to master FastAPI"
1. Start: [[Wiki/entities/TTRPG-AI-RAG-Assistant]] (simple RAG API)
2. Intermediate: [[Wiki/entities/AIO Generative AI Solution]] (Docker deployment)
3. Advanced: [[Wiki/entities/Cartographers-Cloud-Kit]] (Lambda deployment, auth)

**Time:** 2-3 weeks

---

### "I want to master AWS CDK"
1. Start: [[Wiki/entities/chadbarteldotcom]] (static site)
2. Intermediate: [[Wiki/entities/my-shared-infra]] (hub-and-spoke, exports)
3. Advanced: [[Wiki/entities/Cartographers-Cloud-Kit]] (Lambda, API Gateway, DynamoDB)

**Time:** 3-4 weeks

---

### "I want to master Docker & Ansible"
1. Start: [[Wiki/entities/Homelab-Ansible]] (Docker Compose playbooks)
2. Intermediate: Learn to extend existing services
3. Advanced: Add new services (VPN, databases, monitoring)

**Time:** 2-3 weeks

---

### "I want to master LLM integration"
1. Start: [[Wiki/entities/GenerateIdeas]] (simple API wrapper)
2. Intermediate: [[Wiki/entities/TTRPG-AI-RAG-Assistant]] (RAG pattern)
3. Advanced: [[Wiki/entities/brAIniac]] (local LLM, tool integration)

**Time:** 2-3 weeks

---

### "I want to master Python testing & CI/CD"
1. Learn: [[Wiki/entities/MidnightsGitHubActions]] (workflow patterns)
2. Apply: Any Python project
3. Master: Add new workflows, improve coverage

**Time:** 1-2 weeks

---

## Common Tech Patterns in Your Codebase

### Pattern 1: API Wrapper (Cellophane)

**Used By:** Close-Application, potentially others

**Core Concept:**
```python
from cellophane import CellophaneBase

class MyAPI(CellophaneBase):
    def _authenticate(self):
        # Your auth logic
```

**When to Use:** Any REST API integration

---

### Pattern 2: FastAPI + RAG

**Used By:** TTRPG-AI-RAG, AIO AI, Arcane-Scribe

**Core Concept:**
1. Ingest documents to LlamaIndex/LangChain
2. Expose query endpoint via FastAPI
3. Deploy locally or serverless

**When to Use:** Knowledge lookup, question-answering APIs

---

### Pattern 3: CDK + CloudFormation Exports

**Used By:** my-shared-infra, all dependent projects

**Core Concept:**
```python
self.hosted_zone_id = hosted_zone.hosted_zone_id  # Export
# Other project imports:
hosted_zone_id = self.node.try_get_context("HostedZoneId")
```

**When to Use:** Shared infrastructure across multiple stacks

---

### Pattern 4: Lambda Authorizer

**Used By:** Cartographers-Cloud-Kit, potentially others

**Core Concept:**
1. Lambda validates token
2. Lambda checks IP whitelist (from My-DDNS-Updater)
3. Returns IAM policy allowing/denying access

**When to Use:** Securing APIs without changing code

---

### Pattern 5: Docker Compose + Ansible

**Used By:** Homelab-Ansible

**Core Concept:**
1. Ansible playbooks define services
2. Docker Compose files define containers
3. Idempotent orchestration

**When to Use:** Managing multiple services on single host

---

## Recommendations

### Short-term (Next 2 weeks)
- Continue with current tech stack
- No major version upgrades
- Focus on Python 3.12 standardization

### Medium-term (Next 1-2 months)
- Consider adding Redis caching (cost reduction)
- Explore WebSockets for real-time features (future TableTopMaestro)
- Add observability (structured logging)

### Long-term (Next 3-6 months)
- Consider vector database for specialized RAG
- Evaluate PostgreSQL for complex data (TableTopMaestro)
- Potentially add Kubernetes if projects scale beyond single node

---

## Related Synthesis Pages

- [[Wiki/synthesis/Project-Dashboard]] — Project overview
- [[Wiki/synthesis/Shared-Infrastructure-Map]] — Project dependencies
- [[Wiki/synthesis/Common-Use-Cases]] — "I want to..." routing
