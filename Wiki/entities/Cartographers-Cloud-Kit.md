---
type: entity
date_created: 2026-08-07
date_updated: 2026-08-07
tags:
  - wiki/entity
  - project/aws
  - application
  - status/in-progress
  - tech/cdk
  - tech/fastapi
  - tech/lambda
  - tech/cognito
  - tech/dynamodb
source_count: 1
---

# Cartographers-Cloud-Kit

Cloud-native game asset management application for Dungeons & Masters (GMs) to upload, tag, search, and manage TTRPG digital assets (map icons, NPC portraits, location images). Demonstrates sophisticated AWS architecture with Cognito authentication, API Gateway, Lambda backend, DynamoDB metadata, and S3 asset storage.

## Purpose

Enable GMs to manage a library of reusable digital assets with secure access, flexible tagging, and cloud-native scalability. Showcases enterprise-grade cloud architecture applied to a game tools use case.

## Core Architecture

**Three-Tier Architecture:**
```
Cognito User Pool
    ↓ (authentication)
API Gateway + Token Authorizer Lambda
    ↓ (authorization via SSM home IP + Cognito tokens)
FastAPI Backend (Lambda + Mangum)
    ├─ DynamoDB (asset metadata: owner_id, asset_id, tags)
    └─ S3 (asset binary files: versioned bucket)
    ↓
CloudFront (optional, for CDN caching)
    ↓
User (web client or mobile)
```

**Access Pattern:**
1. User authenticates with Cognito
2. Cognito returns JWT token
3. User includes token in API requests
4. Token Authorizer Lambda validates token + checks home IP
5. If valid, routes to FastAPI backend
6. Backend accesses DynamoDB for metadata, S3 for files

## Key Features

- **Cognito User Pool** — Managed user authentication (sign-up, login, MFA)
- **FastAPI Backend** — Modern Python async web framework
- **DynamoDB Metadata** — Scalable, serverless database
- **S3 Asset Storage** — Unlimited asset storage with versioning
- **Token Authorizer** — Custom Lambda authorizer for fine-grained access control
- **Home IP Whitelisting** — Imports SSM Parameter from [[My-DDNS-Updater]] for IP-based access
- **Multi-Environment Support** — Stack suffix for dev/staging/prod
- **REST API** — Standardized endpoints for CRUD operations on assets

## Tech Stack

- **Language:** Python 3.12
- **Framework:** AWS CDK v2.199.0, FastAPI
- **Key AWS Services:** API Gateway, Lambda, Cognito, DynamoDB, S3, IAM
- **Lambda Runtime:** Python 3.12 (Docker image)
- **Adapters:** Mangum (ASGI to Lambda)
- **Dependencies:** fastapi, mangum, boto3, aws-lambda-powertools, constructs
- **Custom Constructs:** RestApi, CognitoUserPool, DynamoDBTable, S3Bucket, Lambda, TokenAuthorizer

## Architecture

**Project Structure:**
```
cartographers-cloud-kit/
├── app.py                          # CDK app (context-driven)
├── pyproject.toml                  # Poetry deps
├── cdk.context.json               # Domain config
├── cdk/
│   ├── stacks.py                  # CartographersCloudKitStack
│   └── custom_constructs/         # 5+ constructs
│       ├── rest_api.py
│       ├── cognito.py
│       ├── dynamodb.py
│       ├── s3.py
│       ├── lambda.py
│       ├── iam.py
│       └── token_authorizer.py
└── src/
    ├── cck-api-backend/           # FastAPI app
    │   └── main.py
    └── cck-api-authorizer/        # Token authorizer Lambda
        └── app.py
```

**Core AWS Constructs:**
- `RestApi` — API Gateway REST API with CORS
- `CognitoUserPool` — User management (sign-up, login, JWT)
- `DynamoDBTable` — On-demand pricing, partition key (owner_id), sort key (asset_id)
- `S3Bucket` — Versioned, encrypted, private (Cognito access only)
- `Lambda` — Custom Mangum adapter for FastAPI
- `TokenAuthorizer` — Validates Cognito tokens + home IP

## Deployment Model

```bash
# Deploy with stack suffix for multi-environment
poetry run cdk deploy --context stack-suffix="dev"

# Outputs:
# API Endpoint: https://cartographers-cloud-kit-dev-api.chadbartel.com
# Cognito Client ID: [client-id]
# DynamoDB Table: cartographers-cloud-kit-dev-metadata
# S3 Bucket: cartographers-cloud-kit-dev-assets
```

**Domain:** cartographers-cloud-kit.chadbartel.com (via [[chadbarteldotcom]])

## Infrastructure Components

| Component | Type | Purpose | Scaling |
|-----------|------|---------|---------|
| Cognito User Pool | Managed | User auth + JWT | Scales to millions |
| API Gateway | AWS Service | HTTP routing | Auto-scales |
| Lambda Backend | Compute | FastAPI runtime | Auto-scales (cold start ~500ms) |
| Lambda Authorizer | Compute | Token validation | Auto-scales |
| DynamoDB | Database | Asset metadata | On-demand or provisioned |
| S3 | Storage | Asset files | Unlimited, pay per GB |
| IAM Roles | Security | Least-privilege | Static |

## API Design

**FastAPI Endpoints (in backend Lambda):**

```python
@app.get("/assets")
async def list_assets(owner_id: str):
    """List all assets for authenticated user"""
    
@app.post("/assets")
async def create_asset(asset_data: AssetSchema):
    """Upload new asset to S3, store metadata in DynamoDB"""
    
@app.get("/assets/{asset_id}")
async def get_asset(asset_id: str):
    """Retrieve asset metadata or presigned URL for download"""
    
@app.put("/assets/{asset_id}")
async def update_asset(asset_id: str, update_data: AssetSchema):
    """Update asset tags/metadata"""
    
@app.delete("/assets/{asset_id}")
async def delete_asset(asset_id: str):
    """Mark asset as deleted (soft delete)"""
    
@app.get("/search")
async def search_assets(query: str, tags: List[str]):
    """Full-text search on tags + metadata"""
```

## Security Patterns

**Authentication (Cognito):**
- Managed user pool (no password storage)
- JWT tokens returned on login
- Optional MFA support
- Token expiration (default 1 hour)

**Authorization (Token Authorizer Lambda):**
```python
def authorize(event):
    # Extract token from Authorization header
    token = event['authorizationToken']
    
    # Validate JWT with Cognito
    claims = validate_jwt(token)
    
    # Check home IP (imported from My-DDNS-Updater)
    current_home_ip = read_ssm_param('/my-ddns-updater/current-home-ip')
    request_ip = event['requestContext']['identity']['sourceIp']
    
    if request_ip != current_home_ip:
        return deny_policy()  # Not from home
    
    return allow_policy(claims['sub'])  # Allow with user ID
```

**Data Access Control:**
- User can only access their own assets (owner_id = user_id)
- DynamoDB query filtered by user ID
- S3 presigned URLs generated per user

**Encryption:**
- S3: Server-side encryption (default)
- DynamoDB: At-rest encryption
- Transit: HTTPS (CloudFront + API Gateway)

## Cost Model

**Estimated Monthly Cost (Dev Environment):**
- API Gateway: $3.50 per 1M requests → ~$0.35 for 100K requests/month
- Lambda Backend: Free tier 1M invocations → **FREE** for dev usage
- Lambda Authorizer: Free tier → **FREE**
- Cognito: Free up to 50K users/month → **FREE**
- DynamoDB: On-demand billing ~$1.25 per 1M reads + $6.25 per 1M writes
  - Dev usage (100 reads/day, 10 writes/day): ~$0.50/month
- S3: $0.023/GB stored + data transfer
  - Dev usage (100 assets @ 5MB average = 500MB): ~$0.01/month
  - Data transfer (10GB/month): ~$0.90/month
- **Total Dev: ~$2.00/month**

**Production Scaling:**
- Add CloudFront for asset CDN ($0.085/GB)
- DynamoDB provisioned capacity or DAX for caching
- Lambda Provisioned Concurrency to avoid cold starts ($6/month)

## Access Control Pattern

**Home IP Whitelisting:**
- Cartographers-Cloud-Kit imports SSM Parameter from [[My-DDNS-Updater]]
- Only requests from current home IP allowed
- Protects against unauthorized access from elsewhere
- Secure because:
  1. Home IP stored in AWS (not in code)
  2. Updated every 5 minutes
  3. Lambda Authorizer checks before route to backend

## Relationships

**Depends On:**
- [[my-shared-infra]] — Route 53 hosted zone for domain
- [[My-DDNS-Updater]] — Imports SSM Parameter for IP whitelisting
- [[chadbarteldotcom]] — Uses subdomain from same domain

**Provides Patterns For:**
- API Gateway + Lambda architecture
- Token Authorizer implementation
- DynamoDB access patterns
- Cognito integration

## Multi-Environment Deployment

**Stack Suffix Pattern:**

```bash
# Dev environment
poetry run cdk deploy --context stack-suffix="dev"
# Creates: cartographers-cloud-kit-dev-api, CCK-dev-metadata, cck-dev-assets

# Staging environment
poetry run cdk deploy --context stack-suffix="staging"
# Creates: cartographers-cloud-kit-staging-api, CCK-staging-metadata, cck-staging-assets

# Production
poetry run cdk deploy --context stack-suffix="prod"
# Creates: cartographers-cloud-kit-prod-api, CCK-prod-metadata, cck-prod-assets

# Or feature branch
poetry run cdk deploy --context stack-suffix="feature/xyz"
# Creates: cartographers-cloud-kit-feature-xyz-api, etc.
```

**Benefits:**
- Isolated environments (no cross-environment data)
- Feature branches can test new code safely
- Staging mirrors production for testing
- Production is stable

## Getting Started

```bash
git clone [repo-url]
cd cartographers-cloud-kit
poetry install

# Deploy
poetry run cdk deploy --context stack-suffix="dev"

# Access API
curl https://cartographers-cloud-kit-dev-api.chadbartel.com/docs

# Test Cognito login
# 1. Sign up user
# 2. Get JWT token
# 3. Send token in Authorization header
```

## Maintenance

**Regular:**
- Monitor Lambda cold starts (should be <1s for FastAPI)
- Check DynamoDB metrics (read/write throttling)
- Monitor Cognito sign-ups and failed logins
- S3 bucket size tracking

**Periodic:**
- Update FastAPI version
- Audit IAM permissions
- Review Cognito security settings
- Backup DynamoDB (optional, AWS handles)

**Troubleshooting:**
- "Unauthorized" errors → Check token validity in Authorizer logs
- "503 Service Unavailable" → Check Lambda cold starts, increase timeout
- "Access Denied from S3" → Verify IAM role has S3 permissions

## Related Concepts

- [[API Gateway + Lambda Backend Pattern]] — Architecture
- [[Lambda Authorizer Pattern]] — Security
- [[Multi-Environment Deployment via Stack Suffix]] — Deployment pattern
- [[AWS Infrastructure Ecosystem]] — Role in your infrastructure

## Open Questions

- [Add GraphQL API (alternative to REST)?]
- [Implement asset versioning (track historical versions)?]
- [Add CloudFront caching for asset downloads?]
- [Set up automated DynamoDB backups?]

## Key Files

- **Main:** [app.py](app.py)
- **Stack:** [cdk/stacks.py](cdk/stacks.py)
- **Backend:** [src/cck-api-backend/main.py](src/cck-api-backend/main.py)
- **Authorizer:** [src/cck-api-authorizer/app.py](src/cck-api-authorizer/app.py)
- **Config:** [cdk.context.json](cdk.context.json)

## Sources

- Wiki source: Project repository scan on 2026-08-07
- README analysis from `/mnt/c/Users/Chaddle/PycharmProjects/Cartographers-Cloud-Kit`
- AWS CDK constructs documentation
- FastAPI documentation
