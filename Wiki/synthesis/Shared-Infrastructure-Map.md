---
type: synthesis
date_created: 2026-08-07
date_updated: 2026-08-07
tags:
  - wiki/synthesis
  - adhd-workflow
---

# Shared Infrastructure Map — Project Dependencies & Integrations

Understand how your 20+ projects connect via shared infrastructure, APIs, and data flows.

## Hub-and-Spoke Architecture (AWS)

```
┌─────────────────────────────────────────────────────────┐
│           my-shared-infra (Hub)                         │
│   ┌─────────────────────────────────────────────┐      │
│   │ • Route 53 hosted zone (chadbartel.com)     │      │
│   │ • KMS key (ECC_NIST_P256)                   │      │
│   │ • DNSSEC signing                            │      │
│   │ • CloudFormation exports                    │      │
│   └─────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────┘
     ↓↓↓↓↓↓↓↓↓↓ Exports: HostedZoneId, KmsKeyId ↓↓↓↓↓↓↓↓↓
┌──────────┬──────────┬──────────┬──────────┬──────────────┐
│          │          │          │          │              │
▼          ▼          ▼          ▼          ▼              ▼
[DNS]  [DDNS+Auth] [Static]  [Static]  [Asset API]     [Local]
[chadbartel.com]  [Home IP]  [Web 1]   [Web 2]      [Docker]
 Route 53 only    Lambda+    S3+       S3+        Ansible
                  SSM Param  CloudFront CloudFront
```

### What Each Export Provides

#### my-shared-infra Exports

| Export | Consumers | Purpose |
|--------|-----------|---------|
| **HostedZoneId** | chadbarteldotcom, thatsmidnightdotcom, My-DDNS-Updater | Domain delegation |
| **HostedZoneName** | All AWS projects | Zone name for Route 53 records |
| **KmsKeyId** | All projects needing encryption | Encryption key for secrets |

#### My-DDNS-Updater Exports

| Export | Consumers | Purpose |
|--------|-----------|---------|
| **HomeIPAddress** (SSM Param) | Cartographers-Cloud-Kit | IP whitelisting in Lambda Authorizer |

---

## Project Dependency Graph

### Direct Dependencies (Imports/Calls Other Projects)

```
TTRPG Ecosystem:
├── TTRPG-AI-RAG-Assistant → UnnamedRPG (rule system)
├── AIO Generative AI → UnnamedRPG (rule system)
├── Arcane-Scribe → UnnamedRPG (rule system)
└── Automated-Taskmaster → UnnamedRPG (system baseline)

AWS Infrastructure:
├── chadbarteldotcom → my-shared-infra (hosted zone, KMS)
├── thatsmidnightdotcom → my-shared-infra (hosted zone, KMS)
├── My-DDNS-Updater → my-shared-infra (hosted zone, KMS)
└── Cartographers-Cloud-Kit → my-shared-infra (hosted zone, KMS) + My-DDNS-Updater (IP)

CI/CD:
└── All Python projects → MidnightsGitHubActions (test workflows)

Local Infrastructure:
└── Homelab-Ansible → (standalone, no dependencies)
```

### Indirect Dependencies (Uses Service/Tool)

```
Cloud Infrastructure:
├── my-shared-infra → AWS Route 53, KMS
├── chadbarteldotcom → AWS S3, CloudFront, ACM, Route 53
├── thatsmidnightdotcom → AWS S3, CloudFront, ACM, Route 53
├── My-DDNS-Updater → AWS Lambda, EventBridge, SSM Parameter
└── Cartographers-Cloud-Kit → AWS Lambda, API Gateway, DynamoDB, Cognito

Local AI:
├── brAIniac → Ollama (local LLM inference)
└── FunWithMusic → SCAMP (music notation), python-rtmidi

CI/CD:
└── MidnightsGitHubActions → GitHub Actions platform

LLM Services:
├── GenerateIdeas → Google Gemini API
├── TTRPG-AI-RAG → Google Gemini API
├── my-cache-augmented-generation → LLM research platforms
└── brAIniac → Ollama local models
```

---

## Data Flow Map

### TTRPG Campaign Workflow

```
User writes rules in UnnamedRPG
         ↓
TTRPG-AI-RAG-Assistant ingests via RAG
         ↓
User queries rule system via TTRPG-AI-RAG
         ↓
Automated-Taskmaster uses rules to generate content (encounters, NPCs, loot)
         ↓
TableTopMaestro (TBD) stores generated content in campaign database
         ↓
DM references content during live play
```

### Infrastructure Deployment Workflow

```
Developer writes code in chadbarteldotcom
         ↓
Git push triggers GitHub Actions (MidnightsGitHubActions)
         ↓
Tests pass → CDK deploys to AWS
         ↓
my-shared-infra provides hosted zone, KMS key
         ↓
CloudFront caches site, Route 53 routes traffic
         ↓
Site live at chadbartel.com
```

### Dynamic DNS + API Authorization Flow

```
Home router restarts, IP changes
         ↓
My-DDNS-Updater Lambda runs (EventBridge every 5 min)
         ↓
Queries home IP, stores in SSM Parameter
         ↓
Cartographers-Cloud-Kit Lambda Authorizer checks IP
         ↓
If IP matches whitelist (from SSM Param), grant access
         ↓
API call allowed for authenticated user
```

---

## Integration Points

### Where to Add New Projects

#### Option 1: Add to TTRPG Ecosystem
**If:** Your project helps with tabletop gaming
**How:** Import UnnamedRPG or Automated-Taskmaster rules
**Example:** Character sheet generator, encounter balancer, world-building tool

#### Option 2: Add to AI/LLM Ecosystem
**If:** Your project uses AI for content generation or chatting
**How:** Use brAIniac (local) or GenerateIdeas (cloud) as backbone
**Example:** Creative writing assistant, NPC behavior generator, dialogue optimizer

#### Option 3: Add to AWS Infrastructure Ecosystem
**If:** Your project needs cloud hosting or services
**How:** Use my-shared-infra as hub (import hosted zone, KMS key)
**Example:** New website, new API service, new data pipeline

#### Option 4: Add to Utilities & Learning
**If:** Your project is a reusable library or learning sandbox
**How:** Standalone, but reference MidnightsGitHubActions for CI/CD
**Example:** New library, new experimental sandbox, new learning tool

---

## Deployment Dependencies

### Must Deploy in This Order

```
1. my-shared-infra (hub must exist)
   ↓
2. Any of:
   • chadbarteldotcom (uses hub)
   • thatsmidnightdotcom (uses hub)
   • My-DDNS-Updater (uses hub)
   ↓
3. Cartographers-Cloud-Kit (uses hub + DDNS)
```

### Can Deploy Independently

```
• Homelab-Ansible (no cloud dependencies)
• brAIniac (local only)
• FunWithMusic (no cloud)
• Cellophane (library, no deployment needed)
• GenerateIdeas (stateless cloud API, no infrastructure)
• All TTRPG projects (local or serverless independently)
```

---

## Shared Utilities

### MidnightsGitHubActions Workflow Reference

All Python projects use workflows from MidnightsGitHubActions:

```yaml
# In your project's .github/workflows/ci.yml
jobs:
  test:
    uses: thatsmidnight/MidnightsGitHubActions/.github/workflows/python-test.yml@v1
```

**Benefits:**
- Consistent testing across all projects
- Update once, applies everywhere
- No duplicate YAML

### Cellophane Library Reference

Any project building an API wrapper can import:

```python
from cellophane import CellophaneBase

class MyAPI(CellophaneBase):
    def _authenticate(self):
        # Your auth logic
        pass
```

**Benefits:**
- Standard error handling
- Automatic retry with re-auth
- Type-safe API calls

---

## Cost Analysis

### Free or Nearly Free
- **Homelab-Ansible:** Hardware only (electricity)
- **TTRPG projects:** Free tier (local or Gemini credits)
- **brAIniac:** Free (Ollama local, hardware only)
- **FunWithMusic:** Free (SCAMP, python-rtmidi free)
- **My-Mini-Projects:** Free (local, Deno free)
- **Cellophane:** Free (library, no deployment)

### Minimal Cost (< $10/month combined)
- **my-shared-infra:** ~$1.50/month (Route 53)
- **My-DDNS-Updater:** ~$0.50-2/month (Lambda, mostly free tier)
- **chadbarteldotcom:** ~$1-2/month (S3, CloudFront, Route 53)
- **thatsmidnightdotcom:** ~$1-2/month (S3, CloudFront, Route 53)
- **Cartographers-Cloud-Kit:** ~$2-9/month (Lambda, API Gateway, DynamoDB)

### Total AWS Monthly: ~$7-20/month

(Covered by Google Cloud / AWS free tiers for most activity)

---

## Resilience & Failover

### If my-shared-infra Goes Down

- **Impact:** All dependent projects lose DNS routing
- **Recovery:** Redeploy from CDK code (infrastructure is code)
- **Time:** ~5 minutes
- **Mitigation:** Use Route 53 private hosted zone + public zone separation

### If My-DDNS-Updater Fails

- **Impact:** Dynamic DNS stops updating; home IP whitelisting fails
- **Recovery:** Redeploy Lambda function
- **Time:** ~2 minutes
- **Mitigation:** Manually update SSM Parameter with current IP

### If Homelab-Ansible Services Go Down

- **Impact:** Local media, DNS, VPN stop
- **Recovery:** Restart Ansible playbooks or individual services
- **Time:** ~10 minutes per service
- **Mitigation:** Docker volumes persist data; restart is safe

---

## Monitoring & Alerts

### What to Monitor

| Resource | Metric | Action |
|----------|--------|--------|
| my-shared-infra | CloudFormation stack status | Re-deploy if drifted |
| My-DDNS-Updater | Lambda execution time | Check CloudWatch logs |
| Route 53 | DNS query failures | Check health checks |
| chadbarteldotcom | CloudFront error rates | Check S3 bucket permissions |
| Homelab-Ansible | Docker container status | Restart via playbook |

### Where to Check

```bash
# AWS infrastructure status
aws cloudformation list-stacks --query "StackSummaries[?contains(StackStatus, 'CREATE_COMPLETE')].StackName"

# Lambda execution logs
aws logs tail /aws/lambda/my-ddns-updater --follow

# Docker container status (Homelab)
ansible monolith -m community.docker.docker_container_info
```

---

## Related Synthesis Pages

- [[Wiki/synthesis/Project-Dashboard]] — All projects at a glance
- [[Wiki/synthesis/Technology-Dependency-Graph]] — Tech stack overview
- [[Wiki/synthesis/Common-Use-Cases]] — "I want to..." → projects needed
