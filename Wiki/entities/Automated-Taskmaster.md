---
type: entity
date_created: 2026-08-07
date_updated: 2026-08-07
tags:
  - wiki/entity
  - project/ttrpg
  - status/active
  - tech/fastapi
  - tech/aws
  - deployment/serverless
source_count: 1
---

# Automated-Taskmaster

AWS-based serverless TTRPG utility microservice for generating random encounters, loot, character backstories, and other procedural content. Exposes FastAPI REST API via Lambda with IP-based authorization.

## Purpose

Supplement to your TTRPG tooling. Stateless generation of encounters, treasure, and character prompts. No document ingestion (unlike [[TTRPG-AI-RAG-Assistant]], [[AIO Generative AI Solution]], [[Arcane-Scribe]]). Lightweight, fast, and cheap to run.

## Core Features

- **REST API:** FastAPI endpoints for encounter, loot, prompt generation
- **Serverless Lambda:** AWS Lambda deployment via CDK infrastructure
- **Authorization:** IP-based custom Lambda authorizer (secure within trusted networks)
- **Swagger UI:** Auto-generated API documentation
- **Extensible Routers:** Easy to add new generator types
- **Stateless:** No database; generators are pure functions
- **Docker Support:** Local development with Uvicorn

## Tech Stack

- **Language:** Python ~3.12
- **Framework:** FastAPI (REST API)
- **Serverless Compute:** AWS Lambda
- **Infrastructure:** AWS CDK (Python)
- **ASGI Adapter:** Mangum (FastAPI → Lambda handler)
- **AWS SDK:** Boto3
- **Observability:** AWS Lambda Powertools (logging, structured output)
- **HTTP Client:** Requests (for inter-service calls)
- **Local Development:** Uvicorn (dev server)
- **Testing:** Pytest (unit and integration tests)

## Architecture

- **Entry Point:** `app.py` (AWS CDK stack definition)
- **API Handler:** `src/at-api-backend/` (FastAPI application)
  - Main app: `automated_taskmaster/main.py` or `app.py`
  - Routers: `/routers` directory (modular endpoint definitions)
- **Authorization:** `src/at-ip-authorizer/` (separate Lambda authorizer)
  - IP whitelist validation
  - Token generation/verification
- **Infrastructure:** `cdk/stacks.py` (CDK stack definitions)
- **Data Flow:**
  1. HTTP request to API Gateway
  2. IP Authorization Lambda (validates sender)
  3. Route to appropriate generator
  4. Generate stateless content
  5. Return JSON response

## Generator Types

**Implemented:**
- Encounter generator (random combat scenarios)
- Loot generator (treasure drops with rarity levels)
- Character backstory prompts (narrative hooks)

**Extensible:** Easy to add new routers for additional generator types (tavern names, dungeon layouts, NPC traits, etc.)

## Deployment Model

- **Platform:** AWS (serverless)
- **Scaling:** Automatic Lambda scaling
- **Cost:** Per invocation + duration (very cheap; mostly free tier eligible)
- **Access:** IP-authorized (no database; trust-based)
- **Data Persistence:** None (stateless generators)

## Relationships

**Complements:**
- [[TTRPG-AI-RAG-Assistant]] — Could call for rule lookups mid-encounter
- [[AIO Generative AI Solution]] — Could use for rule verification
- [[Arcane-Scribe]] — Could integrate via API for enterprise deployments

**Distinct From:**
- [[UnnamedRPG]] — Utilities built on top of game system, not the system itself
- All RAG projects — Generation (no documents) vs. query (document-based)

**Could Feed Into:**
- GM campaign planning tools
- Automated scenario generation
- Batch encounter prep

## Project Status

- **Status:** Active (MVP with encounter generation)
- **Completeness:** Core generators implemented
- **Extensibility:** Ready for new generator types
- **Deployment:** AWS CDK stack complete, ready to deploy
- **Maintenance:** Stable

## Key Insights for Context-Switching

**When to use:**
- Need random encounter/loot/NPC quickly
- Generating content procedurally for variance
- Prototyping new generator ideas
- Expanding [[UnnamedRPG]] campaign content

**Quick facts:**
- **Performance:** <100ms response time
- **Cost:** Essentially free (low invocation volume)
- **Complexity:** Simpler than RAG projects (no ML, no storage)
- **Reliability:** Fully managed AWS service
- **Extensibility:** Add new routers for new content types

## Generator Architecture Example

```python
# Router pattern for easy extension
@router.get("/encounter/{difficulty}")
async def generate_encounter(difficulty: str):
    # Simple stateless generation
    return {
        "encounter": build_encounter(difficulty),
        "monsters": select_monsters(difficulty),
        "treasure": estimate_loot(difficulty)
    }
```

## Integration Opportunities

**With RAG Systems:**
```
1. User asks: "Can I use fireball against 3 kobolds?"
2. [[Arcane-Scribe]] looks up spell rules
3. [[Automated-Taskmaster]] suggests encounter variants
4. Response: Rule + tactical advice
```

**With Campaign Tools:**
```
Generate encounter
  → Check [[Arcane-Scribe]] for NPC stat validation
  → Generate loot matching encounter difficulty
  → Provide NPC personality from backstory prompts
```

## Open Questions

- [Should integrate with [[Arcane-Scribe]] for rule lookups?]
- [Add more generator types (tavern names, dungeon layouts)?]
- [Multi-region deployment for global access?]
- [Support custom rule systems ([[UnnamedRPG]] vs. D&D 5e)?]

## Related Concepts

- [[TTRPG Ecosystem]] — Role in your project cluster
- [[Serverless TTRPG Services]] — Lambda-based generation pattern
- [[Procedural Content Generation]] — Stateless generation approach
- [[Microservice Architecture]] — Single responsibility (generation only)

## Tech Patterns Used

- **Serverless Functions:** AWS Lambda for pay-per-use compute
- **Router Pattern:** Modular endpoint organization
- **Stateless Design:** No database dependencies (scalable)
- **Infrastructure as Code:** AWS CDK for reproducible deployment
- **Custom Authorizer:** Lambda-based auth before main logic
- **ASGI Adapter:** Mangum bridge (FastAPI → Lambda)

## Development & Testing

- **Local Dev:** `uvicorn automated_taskmaster:app --reload`
- **Testing:** Pytest with mock AWS services
- **Deployment:** `cdk deploy` (builds and deploys to AWS)

## Sources

- Wiki source: Project repository scan on 2026-08-07
- README analysis from `/mnt/c/Users/Chaddle/PycharmProjects/Automated-Taskmaster`
- pyproject.toml dependency analysis
- Architecture extracted from `app.py` (CDK) and `/routers` structure
- Infrastructure patterns from `cdk/stacks.py`
