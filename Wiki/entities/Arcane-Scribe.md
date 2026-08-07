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
  - tech/bedrock
  - deployment/serverless
source_count: 1
---

# Arcane-Scribe

Serverless AWS-native TTRPG SRD query system using Lambda functions, API Gateway, and Bedrock AI models. Provides scalable, authenticated REST API for querying rulebooks with persistent vector search via FAISS-CPU.

## Purpose

Enterprise-grade TTRPG query system. Scalable, authenticated, production-ready alternative to local RAG solutions. AWS-native with automatic scaling and persistent storage across Lambda invocations.

## Core Features

- **Serverless Architecture:** AWS Lambda functions (API backend + PDF ingestor)
- **REST API:** HTTP API via API Gateway (fast, scalable)
- **AWS Bedrock LLM:** Amazon Titan embeddings + Claude 3.5 Haiku generation
- **Persistent Storage:** S3 (documents + embeddings), DynamoDB (metadata)
- **Vector Search:** FAISS-CPU for semantic search within Lambda
- **Authentication:** AWS Cognito + custom authorizer Lambda
- **Infrastructure as Code:** AWS CDK (Python v2.201.0+)
- **Custom Domain:** Route 53 + Certificate Manager integration
- **Frontend Included:** UI application for web-based query interface

## Tech Stack

- **Language:** Python ~3.12
- **Infrastructure:** AWS CDK (v2.201.0+)
- **Framework:** FastAPI (Lambda handler via Mangum ASGI adapter)
- **AWS Services:**
  - Lambda (compute)
  - API Gateway (REST routing)
  - Bedrock (embeddings & LLM)
  - S3 (document/embedding storage)
  - DynamoDB (metadata persistence)
  - Cognito (authentication)
  - Route 53 + Certificate Manager (custom domains)
- **Vector Search:** FAISS-CPU (local indexing within Lambda)
- **SDK:** Boto3 (AWS interactions)
- **RAG Framework:** LangChain + LangChain-Community + LangChain-AWS
- **PDF Processing:** PyPDF (text extraction)
- **Observability:** AWS Lambda Powertools (logging, tracing)
- **Security:** Cryptography (token handling)

## Architecture

- **Entry Point:** `app.py` (AWS CDK stack definition)
- **Lambda Functions:**
  - **API Backend:** `src/as-api-backend/` (FastAPI handlers)
    - `/query` endpoint (natural language questions)
    - `/add_document` (ingest new rulebooks)
    - Authentication via Cognito
  - **PDF Ingestor:** `src/as-pdf-ingestor/` (batch document processing)
    - S3 trigger on new PDFs
    - Bedrock embedding generation
    - FAISS index creation
- **Core Utilities:** `src/core/` (shared logic across Lambdas)
- **Infrastructure:** `cdk/` folder (stack definitions, resource configuration)
- **Data Flow:**
  1. PDF upload to S3 → Ingestor Lambda triggered
  2. Text extraction → Bedrock embeddings → FAISS index + S3 storage
  3. User query → API Lambda → FAISS semantic search → Bedrock generation
  4. Response → API Gateway → Client

## Deployment Model

- **Platform:** AWS (serverless, managed)
- **Scaling:** Automatic Lambda scaling (pay per invocation)
- **Persistence:** S3 for documents/embeddings, DynamoDB for metadata
- **Access:** Custom domain via Route 53, Cognito authentication
- **Cost:** AWS Bedrock + Lambda + storage charges (scales with usage)

## Relationships

**Similar To:**
- [[TTRPG-AI-RAG-Assistant]] and [[AIO Generative AI Solution]] — Same RAG pattern (document → embedding → search → generation)
- **Key Difference:** AWS Bedrock/Lambda (serverless) vs. Gemini/local Docker (simple)

**More Mature Than:**
- [[AIO Generative AI Solution]] — Production-ready infrastructure
- [[TTRPG-AI-RAG-Assistant]] — Scalable vs. single-instance

**Could Integrate With:**
- [[Automated-Taskmaster]] — Could call via API for rule lookups
- [[UnnamedRPG]] — Ingests rulebook if added as PDF

**Uses Shared Infrastructure:**
- Potentially [[my-shared-infra]] (EventBridge, API bus) for cross-project integration

## Project Status

- **Status:** Active (production-ready)
- **Version:** v0.3.0
- **Completeness:** Full feature set implemented
- **Deployment:** Ready for AWS deployment
- **Maintenance:** Actively developed

## Key Insights for Context-Switching

**When to use:**
- Need production-grade TTRPG query system
- Want automatic scaling for variable traffic
- Prefer AWS-managed infrastructure
- Multi-team access with authentication
- Building public-facing TTRPG tools

**Quick facts:**
- **Scalability:** Unlimited concurrent queries (Lambda auto-scales)
- **Cost:** AWS billing model (Bedrock + compute + storage)
- **Performance:** Millisecond latency with Lambda warm starts
- **Security:** Cognito authentication + custom authorizer
- **Data Persistence:** S3 + DynamoDB (durable across invocations)
- **Complexity:** More infrastructure than local solutions

## Infrastructure & Cost Considerations

- **Lambda Cost:** Per-invocation billing ($0.20 per million invocations + duration)
- **Bedrock Cost:** Per token for embeddings and generation
- **Storage:** S3 + DynamoDB charges
- **Custom Domain:** Route 53 hosted zone ($0.50/month)
- **Total for Low Usage:** <$5/month. High usage: $50-500+/month

## Integration with TTRPG Ecosystem

```
PDF Rulebook (S3)
    ↓ (PDF Ingestor Lambda)
Bedrock Embeddings + FAISS Index
    ↓ (S3 + DynamoDB)
API Lambda (FastAPI)
    ↓ (Cognito Auth)
User Query
    ↓ (FAISS Search + Bedrock Generation)
Response → API Gateway → Custom Domain
```

## Open Questions

- [Should [[Automated-Taskmaster]] integrate via this API?]
- [Cost optimization for high-volume query workloads?]
- [Multi-region deployment for global access?]
- [Could this replace local [[AIO Generative AI Solution]]?]

## Related Concepts

- [[TTRPG Ecosystem]] — How this fits in your project cluster
- [[RAG Pattern for TTRPG]] — Document + vector search + generation
- [[Serverless TTRPG Services]] — Lambda-based architecture approach
- [[Multi-Provider LLM Integration]] — AWS Bedrock vs. Google Gemini
- [[AWS Infrastructure Patterns]] — CDK best practices

## Tech Patterns Used

- **Serverless RAG:** Lambda-based document processing + query handling
- **Infrastructure as Code:** AWS CDK for reproducible infrastructure
- **FAISS Vector Search:** CPU-based semantic search (no separate database)
- **Cognito Authentication:** OAuth 2.0 for user access control
- **S3 as Data Lake:** Durable, scalable document storage
- **API Gateway + Lambda:** REST API without managing servers

## Sources

- Wiki source: Project repository scan on 2026-08-07
- README analysis from `/mnt/c/Users/Chaddle/PycharmProjects/Arcane-Scribe`
- pyproject.toml dependency analysis
- Architecture extracted from `app.py` (CDK stack), `src/` folder structure
- Infrastructure patterns from `cdk/stacks.py`
