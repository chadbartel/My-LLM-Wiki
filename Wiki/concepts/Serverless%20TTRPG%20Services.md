---
type: concept
date_created: 2026-08-07
date_updated: 2026-08-07
tags:
  - wiki/concept
  - architecture
  - aws
  - deployment
confidence: high
source_count: 2
---

# Serverless TTRPG Services

Deployment of TTRPG tools (query systems, generators) on AWS Lambda with automatic scaling, pay-per-use billing, and managed infrastructure via AWS CDK.

## Definition

Serverless architecture = Don't manage servers. Write functions, upload to cloud, let it scale.

For TTRPG tools: [[Arcane-Scribe]] and [[Automated-Taskmaster]] run as AWS Lambda functions, scaling from zero to millions of requests automatically.

## Why Serverless for TTRPG?

**Traditional (Local Docker):**
- Server running 24/7 (costs money even if unused)
- You manage infrastructure, updates, backups
- Fixed capacity (if 10 people hit it, it might slow down)

**Serverless (AWS Lambda):**
- Pay only for invocations used
- AWS manages updates, backups, scaling
- Automatic scaling (10 people? 10,000 people? Same code)
- Cold start latency tradeoff (first call takes ~100ms more)

## Architecture Pattern

```
User Request
    ↓
API Gateway (HTTP endpoint)
    ↓
Lambda Function (your code)
    ↓
AWS Services (S3, DynamoDB, Bedrock, etc.)
    ↓
Response → User
    
Key: If no requests for 30 minutes, Lambda "sleeps" (costs $0)
     When request arrives, Lambda wakes up instantly
```

## Two Implementations

### [[Arcane-Scribe]] — Serverless RAG
**Architecture:**
```
PDF Upload → S3 → Lambda Ingestor
                      ↓
                  Bedrock Embeddings
                      ↓
                  FAISS Index + S3 Storage
                      ↓
User Query → API Gateway → Lambda API Handler
                              ↓
                          FAISS Search
                              ↓
                          Bedrock LLM
                              ↓
                          Response
```

**Cost Model:**
- Bedrock: Per-token billing (embeddings + generation)
- Lambda: Per-invocation + duration
- S3: Per GB stored + requests
- DynamoDB: Per request (or on-demand pricing)
- Total: $5-50/month depending on usage

### [[Automated-Taskmaster]] — Serverless Generators
**Architecture:**
```
User Request (HTTP GET)
    ↓
API Gateway
    ↓
Lambda Handler
    ↓ (No LLM, no database)
Stateless Generation
    ↓
JSON Response
```

**Cost Model:**
- Lambda only: Per-invocation + duration
- No database costs
- No Bedrock costs
- Total: ~$1-5/month (very cheap)

## AWS CDK Infrastructure as Code

Both projects use AWS CDK (Python) to define infrastructure:

```python
# Example: Define Lambda function with API Gateway
from aws_cdk import (
    aws_lambda,
    aws_apigateway,
    Stack
)

class MyStack(Stack):
    def __init__(self, scope, id):
        super().__init__(scope, id)
        
        # Define Lambda
        lambda_fn = aws_lambda.Function(
            self, "MyFunction",
            runtime=aws_lambda.Runtime.PYTHON_3_12,
            handler="index.handler",
            code=aws_lambda.Code.from_asset("src")
        )
        
        # Expose via API Gateway
        api = aws_apigateway.RestApi(self, "API")
        api.root.add_resource("query").add_method("POST", ...)
```

**Benefits:**
- Reproducible infrastructure (version control)
- Tear down and redeploy easily
- No manual console clicks
- Team-friendly (everyone uses same code)

## Key AWS Services

| Service | Purpose | Used By |
|---------|---------|---------|
| **Lambda** | Compute (your code) | Both |
| **API Gateway** | HTTP routing | Both |
| **Bedrock** | LLM + embeddings | [[Arcane-Scribe]] |
| **S3** | Document + embedding storage | [[Arcane-Scribe]] |
| **DynamoDB** | Metadata persistence | [[Arcane-Scribe]] |
| **Cognito** | Authentication | [[Arcane-Scribe]] |
| **Route 53** | Custom domain | [[Arcane-Scribe]] |
| **CloudWatch** | Logging & monitoring | Both |

## Scaling Characteristics

```
Requests/sec  | Local Docker      | AWS Lambda
──────────────────────────────────────────────
1-10          | Runs fine         | Runs fine ($0.01/day)
100-1000      | May slow down      | Scales instantly
10,000+       | Needs more servers | Scales to 10,000s
1,000,000     | Needs data center  | Still scales instantly
```

**Practical:** Lambda is overkill for 1-2 users, perfect for public APIs.

## Latency Considerations

**Cold Start:** First invocation after inactivity takes ~100-500ms extra
- Problem: User waits longer
- Solution: Provisioned Concurrency (keep Lambda warm, costs more)

**Warm Invocation:** Subsequent calls are ~50-200ms
- Fast enough for most TTRPG use cases

**Typical Pattern:**
```
Request 1 (after 30min idle): 500ms (cold start)
Request 2 (immediately after): 80ms (warm)
Request 3 (immediately after): 80ms (warm)
```

## Authorization & Security

[[Arcane-Scribe]] uses AWS Cognito + custom authorizer Lambda:

```
Request with Token
    ↓
Custom Authorizer Lambda
    ↓
Validates token / IP
    ↓
Allows/Denies
    ↓
If allowed → Main Lambda
```

[[Automated-Taskmaster]] uses IP-based authorization:

```
IP-Based Authorizer
    ↓
Only whitelist trusted IPs
    ↓
Simpler but less secure
```

## Monitoring & Observability

Both projects use AWS CloudWatch + Lambda Powertools:

```python
from aws_lambda_powertools import Logger

logger = Logger()

@logger.inject_lambda_context
def handler(event, context):
    logger.info("Processing request", extra={"user_id": "123"})
    # Your code
```

**Benefits:**
- Structured logging (JSON format)
- Automatic invocation tracking
- Performance metrics
- Error alerting

## Cost Optimization

**For [[Arcane-Scribe]]:**
1. **Provisioned Concurrency:** Keep 1 Lambda warm ($6/month) to avoid cold starts
2. **Bedrock:** Use cheaper model (Haiku vs. Opus) when possible
3. **FAISS Caching:** Cache embeddings in Lambda memory across invocations
4. **S3 Lifecycle:** Archive old embeddings to Glacier after 30 days

**For [[Automated-Taskmaster]]:**
1. Keep as stateless (cheapest)
2. No optimization needed (already minimal)

## When to Use Serverless vs. Local Docker

| Factor | Local Docker | Serverless Lambda |
|--------|--------------|-------------------|
| **Setup** | `docker-compose up` | `cdk deploy` |
| **Maintenance** | You | AWS |
| **Cost (low usage)** | ~$0 (your hardware) | ~$5/month |
| **Cost (high usage)** | $100+/month (servers) | $50-500/month |
| **Scaling** | Manual (buy more hardware) | Automatic |
| **Complexity** | Lower | Higher |
| **Security** | Self-managed | AWS-managed |

**Rule of Thumb:**
- **1-5 users:** Use local Docker ([[TTRPG-AI-RAG-Assistant]], [[AIO Generative AI Solution]])
- **5-500 users:** Use serverless Lambda ([[Arcane-Scribe]], [[Automated-Taskmaster]])
- **500+ users:** Use both (serverless for public API, local for internal)

## Integration Between Serverless Services

All Lambda functions can call each other via HTTP:

```python
# In Automated-Taskmaster
import requests

def generate_encounter():
    encounter = {...}
    
    # Call Arcane-Scribe to validate monster stats
    response = requests.post(
        "https://api.arcane-scribe.com/query",
        json={"question": f"What are the stats for {encounter['monster']}?"}
    )
    
    return encounter_with_validated_stats
```

## Deployment Workflow

1. **Local Development:** Test with `uvicorn` or `sam local`
2. **Build:** CDK synthesizes CloudFormation template
3. **Deploy:** `cdk deploy` uploads Lambda, creates API Gateway, etc.
4. **Monitor:** CloudWatch shows logs, metrics, errors
5. **Iterate:** Update code, re-deploy (seconds)

## Infrastructure Diagrams in CDK

Both [[Arcane-Scribe]] and [[Automated-Taskmaster]] maintain CDK constructs:

```
src/
├── stacks.py (main infrastructure definition)
├── lambdas/ (individual Lambda handlers)
│   ├── api_handler.py
│   ├── authorizer.py
│   └── ingestor.py
└── resources/ (configuration)
```

## Related Concepts

- [[TTRPG Ecosystem]] — Overview of all 5 projects
- [[Multi-Provider LLM Integration]] — AWS Bedrock usage
- [[AWS Infrastructure Patterns]] — CDK best practices
- [[Microservice Architecture]] — Lambda as microservices

## Monitoring & Alerting Examples

```python
# CloudWatch custom metric
cloudwatch = boto3.client('cloudwatch')
cloudwatch.put_metric_data(
    Namespace='TTRPG-API',
    MetricData=[{
        'MetricName': 'EncounterGenerated',
        'Value': 1,
        'Unit': 'Count'
    }]
)

# Now you can graph "EncounterGenerated" in CloudWatch
# and set alarms (alert if > 1000/hour, etc.)
```

## Open Questions

- [Should [[TTRPG-AI-RAG-Assistant]] be migrated to serverless?]
- [Cost benefit of Provisioned Concurrency for [[Arcane-Scribe]]?]
- [Multi-region deployment for global latency?]
- [Can Lambda and local Docker talk to shared database?]

## Sources

- [[Wiki/entities/Arcane-Scribe]]
- [[Wiki/entities/Automated-Taskmaster]]
- AWS CDK documentation patterns
- Architecture extracted from `cdk/stacks.py` in both projects
