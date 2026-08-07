---
type: concept
date_created: 2026-08-07
date_updated: 2026-08-07
tags:
  - wiki/concept
  - infrastructure/aws
  - pattern/security
  - tech/lambda
  - tech/apigateway
source_count: 2
confidence: high
---

# Lambda Authorizer Pattern

Custom API Gateway authorizer implemented as a Lambda function that validates authentication/authorization before routing requests to backend services. Enables flexible, serverless access control.

## Definition

**Lambda Authorizer (Custom Authorizer):** Lambda function that intercepts API Gateway requests, validates tokens/credentials, and returns an IAM policy allowing or denying access.

**Execution Model:**
```
Client Request with Token
    ↓
API Gateway → Lambda Authorizer
    ├─ Validate token
    ├─ Check permissions
    └─ Return IAM policy
        ├─ Allow → Route to backend
        ├─ Deny → Return 403 Forbidden
        └─ Error → Return 401 Unauthorized
```

## Why It Matters

**Alternative Authorization Approaches:**

| Method | Pros | Cons |
|--------|------|------|
| Cognito User Pools | Managed, standard | Limited flexibility |
| IAM Policies | Fine-grained, audit-logged | Complex, OTT for simple APIs |
| Custom Lambda Authorizer | Flexible, serverless | Must maintain security |
| API Keys | Simple | Weak security, not suitable for user auth |

**Lambda Authorizer Advantages:**
- Flexible: Implement custom logic (IP checking, token validation, etc.)
- Serverless: Pay per invocation, auto-scales
- Cacheable: API Gateway caches decisions (reduces Lambda calls)
- Composable: Chain with Cognito or other auth sources

## How It Works

**Lambda Authorizer Handler:**

```python
import json
import boto3

ssm = boto3.client('ssm')

def lambda_handler(event, context):
    # Extract token from header
    token = event['authorizationToken']
    
    # Custom validation logic
    if not is_valid_token(token):
        raise Exception('Unauthorized')
    
    # Extract claims
    claims = decode_token(token)
    
    # Return IAM policy allowing access
    return {
        "principalId": claims['user_id'],
        "policyDocument": {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Action": "execute-api:Invoke",
                    "Effect": "Allow",
                    "Resource": "arn:aws:execute-api:region:account:api-id/*"
                }
            ]
        },
        "context": {
            "userId": claims['user_id'],
            "scope": claims['scope']
        }
    }
```

**API Gateway Integration:**

```python
# In CDK stack
authorizer_lambda = aws_lambda.Function(...)

authorizer = apigateway.TokenAuthorizer(self, "Authorizer",
    handler=authorizer_lambda
)

api = apigateway.RestApi(self, "MyApi")

# Attach authorizer to method
api.root.add_resource("protected").add_method("GET",
    authorizer=authorizer
)
```

**Request Flow:**

```
1. Client: GET /protected -H "Authorization: Bearer token123"
2. API Gateway: Invokes Lambda Authorizer with token
3. Lambda Authorizer: Validates token, returns Allow policy
4. API Gateway: Caches policy (default 300 seconds)
5. API Gateway: Routes to backend Lambda
6. Backend: Processes request, returns response
```

## Your Projects Using Lambda Authorizer

**[[My-DDNS-Updater]]:**
- Authorizer Lambda: Validates home IP + Cognito token
- Checks SSM Parameter (current-home-ip) every request
- Returns Allow if request from home IP, Deny otherwise

**[[Cartographers-Cloud-Kit]]:**
- Authorizer Lambda: Validates Cognito JWT token
- Checks home IP via SSM import from My-DDNS-Updater
- Only allows requests from home IP AND valid token
- Dual authentication (location + identity)

## IP-Based Authorization Pattern

**Home Network Whitelisting:**

```python
def lambda_handler(event, context):
    # Get request source IP
    source_ip = event['requestContext']['identity']['sourceIp']
    
    # Read current home IP from SSM
    ssm = boto3.client('ssm')
    response = ssm.get_parameter(
        Name='/my-ddns-updater/current-home-ip',
        WithDecryption=True
    )
    current_home_ip = response['Parameter']['Value']
    
    # Compare
    if source_ip == current_home_ip:
        return allow_policy()
    else:
        return deny_policy()
```

**Why Useful:**
- Restricts access to home network only
- Works without VPN/proxy setup
- Updates automatically (My-DDNS-Updater updates SSM every 5 min)
- Cheap (SSM reads free, Lambda free tier covers 1M/month)

## Token Validation Pattern

**JWT Token with Cognito:**

```python
def lambda_handler(event, context):
    import jwt
    
    token = event['authorizationToken'].split()[-1]  # Extract bearer token
    
    try:
        # Decode JWT (without validation first, get header)
        header = jwt.get_unverified_header(token)
        kid = header['kid']
        
        # Get public key from Cognito
        key = get_cognito_public_key(kid)
        
        # Validate signature
        claims = jwt.decode(token, key, algorithms=['RS256'])
        
        # Check expiration, scopes, etc.
        if claims['exp'] < time.time():
            return deny_policy()
        
        return allow_policy(claims['sub'])
    
    except Exception as e:
        return deny_policy()
```

## Caching Strategy

**Authorization Cache:**

```python
# API Gateway caches authorizer responses by default
# TTL = 300 seconds (5 minutes)

# Configure in CDK
authorizer = apigateway.TokenAuthorizer(self, "Authorizer",
    handler=authorizer_lambda,
    identity=apigateway.TokenAuthorizerCredentials(
        assume_role=role
    ),
    result_cache_ttl=cdk.Duration.seconds(300)  # Cache 5 min
)
```

**Why Cache:**
- Reduces Lambda invocations (saves cost)
- Speeds up API Gateway response
- Risk: Token revocation delayed by cache TTL

**How Caching Works:**
```
Request 1: GET /protected -H "Authorization: Bearer token123"
    → Lambda Authorizer invoked (compute cost)
    → Response cached for 5 minutes
    
Request 2 (within 5 min): Same token
    → Cached response used (no Lambda invocation)
    → Request allowed immediately

Request 3 (after 5 min): Same token
    → Cache expired, Lambda Authorizer invoked again
```

## Security Considerations

**Best Practices:**

1. **Validate Early:** Don't trust client-provided claims
2. **Use HTTPS:** Always (API Gateway default)
3. **Rotate Keys:** Cognito handles automatically
4. **Log Attempts:** CloudWatch logs auth failures
5. **Cache Wisely:** Balance cost vs. freshness

**Anti-Patterns (Avoid):**
- ❌ Storing secrets in code (use Secrets Manager)
- ❌ Trusting unvalidated JWT claims (validate signature)
- ❌ Long cache TTL for sensitive operations (user revocation delayed)
- ❌ Returning detailed error messages (reveals implementation)

## Composite Authorization

**Multi-Factor Authorization (IP + Token):**

```python
def lambda_handler(event, context):
    # Factor 1: Validate token
    if not is_valid_token(event['authorizationToken']):
        return deny_policy()
    
    # Factor 2: Validate IP
    source_ip = event['requestContext']['identity']['sourceIp']
    home_ip = get_home_ip_from_ssm()
    if source_ip != home_ip:
        return deny_policy()
    
    # Both factors pass
    return allow_policy()
```

**Use Cases:**
- Secure APIs: Require both identity (token) + location (IP)
- Internal APIs: Allow only from corporate network
- Home services: Allow only from home IP

## Cost Model

**Lambda Authorizer Costs:**

Per invocation:
- 1M free invocations/month (Lambda free tier)
- $0.20 per 1M invocations after

With caching:
- 300-second cache → ~4 hits per minute per token → ~240 invocations/day
- ~7.2K invocations/month
- **Cost: FREE** (within free tier)

Without caching:
- 100 requests/minute = 4.3M requests/month
- **Cost: ~$0.86/month**

## Related Concepts

- [[API Gateway + Lambda Backend Pattern]] — Where authorizer sits
- [[AWS CDK Infrastructure as Code]] — How to define in code
- [[Shared Infrastructure Hub Pattern]] — Sharing auth rules

## Open Questions

- [Add request logging for audit trail?]
- [Implement token refresh pattern?]
- [Add rate limiting per user?]
- [Support multiple auth methods (token vs. IP vs. API key)?]

## Key Insights

**Why Lambda Authorizer for Your Setup:**
1. Flexible (custom IP checking logic)
2. Serverless (no VPN server overhead)
3. Integrates with existing auth (Cognito)
4. Cacheable (low cost)

**When to Use:**
- Custom authorization logic needed
- Need to integrate multiple auth sources
- Require location-based access (IP whitelisting)
- Flexible policy enforcement

**When NOT to Use:**
- Simple API key authentication (API Gateway API Keys sufficient)
- Cognito alone adequate (use Cognito Authorizer)
- No custom logic needed

## Your Implementation

**[[My-DDNS-Updater]]:**
- Authorizer checks home IP
- Integrated with API Gateway

**[[Cartographers-Cloud-Kit]]:**
- Authorizer checks Cognito token + home IP
- Dual-factor authorization

## Key Files

- [[My-DDNS-Updater]] — [src/cck-api-authorizer/app.py](src/cck-api-authorizer/app.py)
- [[Cartographers-Cloud-Kit]] — Token Authorizer Lambda implementation

## Sources

- AWS API Gateway Lambda Authorizer documentation
- AWS CDK TokenAuthorizer construct
- Your project repositories (My-DDNS-Updater, Cartographers-Cloud-Kit)
- JWT validation best practices
