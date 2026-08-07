---
type: concept
date_created: 2026-08-07
date_updated: 2026-08-07
tags:
  - wiki/concept
  - infrastructure/aws
  - pattern/backend
  - tech/apigateway
  - tech/lambda
  - tech/dynamodb
source_count: 2
confidence: high
---

# API Gateway + Lambda Backend Pattern

Serverless REST API architecture combining AWS API Gateway (HTTP routing) with Lambda (compute) and DynamoDB (storage). Provides scalable, cost-effective backend without managing servers.

## Definition

**API Gateway + Lambda Pattern:** HTTP API requests routed through API Gateway to Lambda functions, which process requests and interact with databases/external services.

**Architecture:**
```
Client Request → API Gateway → Lambda Functions → DynamoDB/S3/External Services
                      ↓
               Token Authorizer Lambda
               (validates auth before routing)
```

## Why It Matters

**Alternative Backend Approaches:**

| Approach | Scalability | Cost | Ops Burden |
|----------|-------------|------|-----------|
| Self-managed VPS | Manual | $5-50/month | High (maintain server) |
| Container (ECS) | Good | $50-200/month | Medium (Docker ops) |
| App Platform (Heroku) | Good | $7-100+/month | Low (managed) |
| API Gateway + Lambda (this) | Unlimited | $0-20/month | Very Low (serverless) |

**Lambda Backend Advantages:**
- Auto-scaling (handles traffic spikes automatically)
- Pay-per-use (only charged for actual execution)
- No servers to manage
- Fast deployment (seconds)
- Integrates with AWS ecosystem

## Your Projects Using This Pattern

**[[Cartographers-Cloud-Kit]]:**
- API Gateway REST API
- FastAPI backend running in Lambda (via Mangum ASGI adapter)
- Token Authorizer for authentication
- DynamoDB for metadata, S3 for assets

**[[My-DDNS-Updater]]:**
- Lambda Authorizer for IP-based access control
- Could extend with backend API for configuration

## Architecture Components

**API Gateway:**
- HTTP/REST endpoint
- Route requests to Lambda
- Attach authorizers (authentication)
- Transform requests/responses (CORS, etc.)
- Rate limiting
- Request logging

**Lambda Functions:**
- Backend compute (FastAPI, Flask, pure Python, etc.)
- Stateless (no local storage)
- Cold starts (~100-500ms first invocation)
- Automatic scaling
- Max timeout: 15 minutes

**DynamoDB (Optional):**
- NoSQL database (serverless)
- On-demand or provisioned capacity
- Auto-scaling included
- Perfect for Lambda (no connection pooling needed)

**S3 (Optional):**
- File storage (images, documents, etc.)
- Lambda can read/write files
- Integrates with DynamoDB for metadata

**CloudFront (Optional):**
- CDN for API responses (cache frequently-accessed data)
- Not suitable for all APIs (only cacheable requests)

## Request/Response Flow

**Typical Request:**

```
1. Client: POST /assets -H "Authorization: Bearer token" -d '{...}'

2. API Gateway:
   - Receives request
   - Routes to Token Authorizer Lambda
   
3. Token Authorizer Lambda:
   - Validates JWT token
   - Checks home IP (from SSM)
   - Returns Allow or Deny policy
   
4. If Allow:
   - API Gateway routes to backend Lambda
   - Passes request context (authorization claims)
   
5. Backend Lambda (FastAPI):
   - Receives request
   - Processes (query DynamoDB, upload to S3, etc.)
   - Returns response (JSON)
   
6. API Gateway:
   - Applies response mapping
   - Handles CORS headers
   - Returns to client
```

## Backend Framework Integration

**FastAPI on Lambda (Mangum Adapter):**

```python
# app.py
from fastapi import FastAPI
from mangum import Mangum

app = FastAPI()

@app.get("/assets")
async def list_assets(owner_id: str):
    # Query DynamoDB
    response = dynamodb.query(
        TableName='assets',
        KeyConditionExpression='owner_id = :owner_id',
        ExpressionAttributeValues={':owner_id': {'S': owner_id}}
    )
    return response['Items']

@app.post("/assets")
async def create_asset(asset_data: AssetSchema):
    # Insert into DynamoDB
    # Upload file to S3
    return {"asset_id": asset_id}

# Handler for Lambda
handler = Mangum(app)
```

**Why Mangum:**
- Converts ASGI (FastAPI) to AWS Lambda handler
- Handles request/response translation
- Minimal overhead

## Cost Model

**API Gateway:**
- $3.50 per 1M requests
- Example: 100K requests/month = $0.35

**Lambda (Backend):**
- 1M free invocations/month
- $0.20 per 1M after
- Memory: 128MB-10GB (larger = faster, higher cost)
- Typical: 256MB-512MB for API workload

**DynamoDB (On-Demand):**
- $1.25 per 1M read units
- $6.25 per 1M write units
- Example: 100K reads/month = $0.125

**Total for Small API:**
```
API Gateway:    $0.35 (100K requests)
Lambda:         FREE (within 1M free tier)
DynamoDB:       $0.50 (light usage)
S3:             $0.023/GB stored
---------
Total:          ~$1-2/month
```

**Scaling to Medium Traffic (1M requests/month):**
```
API Gateway:    $3.50 (1M requests)
Lambda:         $0.20 (after free tier)
DynamoDB:       $5.00 (proportional to load)
S3:             $0.50/GB
---------
Total:          ~$9-15/month
```

## Cold Start Optimization

**Problem:** First Lambda invocation takes 500ms+ (container startup)

**Solutions:**

1. **Provisioned Concurrency**
   - Pre-warm Lambda containers
   - Cost: ~$0.015/hour per concurrent execution
   - Use for critical APIs

2. **Lambda Extensions**
   - Lightweight code to reduce package size
   - Faster startup

3. **Larger Memory**
   - More CPU allocated → faster startup
   - Cost trade-off (faster startup, higher per-invocation cost)

4. **Accept Cold Starts**
   - For non-critical APIs, cold start acceptable
   - Not noticeable with caching

## DynamoDB Integration

**Access Patterns:**

```python
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('assets')

# Query (get items by partition key)
response = table.query(
    KeyConditionExpression='owner_id = :owner_id',
    ExpressionAttributeValues={':owner_id': 'user123'}
)

# Scan (get all items, slow for large tables)
response = table.scan()

# Put (insert/update)
table.put_item(Item={'owner_id': 'user123', 'asset_id': 'asset1', 'tags': ['tag1']})

# Get (retrieve single item)
response = table.get_item(Key={'owner_id': 'user123', 'asset_id': 'asset1'})

# Update (modify item)
table.update_item(
    Key={'owner_id': 'user123', 'asset_id': 'asset1'},
    UpdateExpression='SET tags = :tags',
    ExpressionAttributeValues={':tags': ['new-tag']}
)

# Delete
table.delete_item(Key={'owner_id': 'user123', 'asset_id': 'asset1'})
```

**Designing Schema:**

```
Table: assets
├─ Partition Key: owner_id (string)
├─ Sort Key: asset_id (string)
└─ Attributes:
    ├─ tags (list of strings)
    ├─ created_at (timestamp)
    ├─ s3_key (string, path to file in S3)
    └─ size_bytes (number)
```

## Error Handling

**Lambda Errors:**

```python
def lambda_handler(event, context):
    try:
        # Process request
        result = process_request(event)
        return {
            'statusCode': 200,
            'body': json.dumps(result)
        }
    except ValidationError as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Invalid input'})
        }
    except AuthorizationError as e:
        return {
            'statusCode': 403,
            'body': json.dumps({'error': 'Unauthorized'})
        }
    except Exception as e:
        # Log error, return 500
        logger.error(f"Unhandled error: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal server error'})
        }
```

**API Gateway Mapping:**
- Lambda returns structured response
- API Gateway maps to HTTP status/headers
- Error responses automatically formatted

## Monitoring and Logging

**CloudWatch Logs:**

```python
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info(f"Received request: {event}")
    
    try:
        result = process(event)
        logger.info(f"Success: {result}")
        return result
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        raise
```

**Metrics:**
- Invocations (total requests)
- Duration (execution time)
- Errors (failed invocations)
- Throttles (rate limits hit)

## Related Concepts

- [[Lambda Authorizer Pattern]] — Authentication layer
- [[Multi-Environment Deployment via Stack Suffix]] — Deploy across environments
- [[Cross-Stack Resource Sharing]] — Share auth rules between stacks
- [[AWS CDK Infrastructure as Code]] — Define via CDK

## Security Best Practices

1. **IAM Least Privilege**
   - Lambda execution role has minimal permissions
   - Can access only required DynamoDB/S3

2. **Environment Variables**
   - Store configuration (table names, bucket names)
   - Secrets in Secrets Manager or Parameter Store

3. **CORS Configuration**
   - API Gateway handles CORS headers
   - Restrict allowed origins

4. **Request Validation**
   - API Gateway validates schema (optional)
   - Lambda validates further (defense-in-depth)

5. **Rate Limiting**
   - API Gateway throttling
   - DynamoDB capacity limits (prevent runaway costs)

## Deployment Strategy

**CDK + GitHub Actions:**

```yaml
# .github/workflows/deploy.yml
on: [push]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: aws-actions/configure-aws-credentials@v1
      - run: npm install -g cdk
      - run: cdk deploy --require-approval never
```

**Lambda Packaging:**

```bash
# Docker image for complex dependencies
poetry export --format requirements.txt > requirements.txt
docker build -t my-lambda:latest .

# Or zip for simple functions
zip -r lambda.zip lambda_function.py
aws lambda update-function-code --function-name my-function --zip-file fileb://lambda.zip
```

## Open Questions

- [Implement API versioning strategy?]
- [Add request/response caching (CloudFront)?]
- [GraphQL instead of REST?]
- [Streaming responses (large data sets)?]

## Key Insights

**Why This Pattern Works:**
- Scales infinitely (no infrastructure limits)
- Cheap for low/medium traffic
- Fast to develop (focus on code, not ops)
- Integrates with AWS ecosystem

**When to Use:**
- RESTful APIs
- Microservices
- Webhooks
- Real-time processing (with SQS/SNS)

**When NOT to Use:**
- Long-running processes (15-min limit)
- Persistent connections (WebSockets, different pattern)
- High memory requirements (>10GB not available)

## Your Implementation

**[[Cartographers-Cloud-Kit]]:**
- Sophisticated example: FastAPI + Lambda + DynamoDB + S3
- Token Authorizer for multi-factor auth
- Full CRUD operations on assets

**[[My-DDNS-Updater]]:**
- Simpler example: Lambda-only (no API Gateway in main flow)
- Authorizer Lambda pattern

## Key Files

- [[Cartographers-Cloud-Kit]] — [src/cck-api-backend/main.py](src/cck-api-backend/main.py) FastAPI backend
- [[Cartographers-Cloud-Kit]] — [cdk/stacks.py](cdk/stacks.py) infrastructure definition

## Sources

- AWS Lambda Developer Guide
- AWS API Gateway documentation
- AWS DynamoDB best practices
- Your project repositories (Cartographers-Cloud-Kit)
- Mangum (ASGI adapter) documentation
