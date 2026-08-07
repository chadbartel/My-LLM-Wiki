---
type: entity
date_created: 2026-08-07
date_updated: 2026-08-07
tags:
  - wiki/entity
  - project/aws
  - infrastructure/network
  - status/active
  - tech/cdk
  - tech/lambda
  - tech/ssm
source_count: 1
---

# My-DDNS-Updater

Automated service that resolves a Dynamic DNS (DDNS) hostname to obtain the current public IP address of your home network, stores it in AWS SSM Parameter Store, and provides a Lambda Authorizer for API Gateway to whitelist access based on source IP.

## Purpose

Enable secure home network access to cloud services by automatically tracking your current home IP (which changes) and using it as an authorization mechanism. Minimal-cost solution for dynamic IP management.

## Core Philosophy

**Minimal AWS Costs:**
- Leverages free tiers (Lambda free tier, SSM Parameter free tier)
- Serverless = pay only for usage (5-min checks = minimal cost)
- Estimated cost: ~$0.50-2.00/month

**Home Network IP Tracking:**
- Resolves DDNS hostname (e.g., yourname.ddns.net from NETGEAR router)
- Updates SSM Parameter Store with current IP
- Other services read this parameter for IP whitelisting
- Enables Cartographers-Cloud-Kit to restrict access to home IP only

**Extensible Authorizer Pattern:**
- Lambda Authorizer validates API Gateway requests
- Reads SSM Parameter to get current home IP
- Returns allow/deny policy for API access
- Reusable pattern for other APIs

## Key Features

- **EventBridge Scheduled Lambda** — Runs every 5 minutes automatically
- **Dynamic IP Resolution** — Queries DDNS hostname (your router's public IP)
- **SSM Parameter Storage** — Persists current IP for other services to read
- **Lambda Authorizer** — API Gateway integration for IP whitelisting
- **Multi-Environment Support** — Stack suffix for dev/staging/prod
- **Feature Branch Deployments** — Each branch gets its own IP tracking
- **Least-Privilege IAM** — Each Lambda has only required permissions

## Tech Stack

- **Language:** Python 3.12
- **Framework:** AWS CDK v2.199.0
- **Key AWS Services:** Lambda, EventBridge, SSM Parameter Store, API Gateway, IAM
- **Lambda Runtime:** Python 3.12 (Docker image)
- **Dependencies:** boto3, aws-lambda-powertools, dnspython, constructs
- **Custom construct:** LambdaFunction (from Docker image)

## Architecture

**Project Structure:**
```
my-ddns-updater/
├── app.py                        # CDK app initialization
├── pyproject.toml               # Poetry deps
├── cdk.json                     # CDK context
├── cdk/
│   ├── stacks.py               # MyDdnsResolverStack
│   └── custom_constructs/
│       └── lambda_function.py   # Custom Lambda construct
└── src/
    └── my-ddns-hostname-resolver/
        ├── app.py              # Lambda handler
        └── requirements.txt    # Python dependencies
```

**Data Flow:**
```
EventBridge Trigger (every 5 minutes)
    ↓
Lambda Function: DDNS Resolver
├─ Resolve DDNS hostname (e.g., yourname.ddns.net)
├─ Get current public IP
└─ Update SSM Parameter: /my-ddns-updater/current-home-ip
    ↓
SSM Parameter Store
├─ Parameter name: /my-ddns-updater/current-home-ip{suffix}
├─ Value: "203.0.113.42" (example IP)
└─ Exportable for other stacks
    ↓
Cartographers-Cloud-Kit (or other services)
├─ Read SSM Parameter
├─ Use in Lambda Authorizer
└─ Whitelist requests from that IP
```

## Deployment

```bash
# Basic deployment
poetry run cdk deploy --context ddns-hostname="yourname.ddns.net"

# Feature branch deployment (dev environment)
poetry run cdk deploy \
  --context ddns-hostname="yourname.ddns.net" \
  --context stack-suffix="dev"

# Outputs
SSM Parameter Name: /my-ddns-updater/current-home-ip-dev
Lambda Function: MyDdnsResolverStack-HomeIPResolverLambda-ABC123
Authorizer Lambda: MyDdnsResolverStack-AuthorizerLambda-XYZ789
```

## Infrastructure Components

| Component | Type | Purpose | Schedule |
|-----------|------|---------|----------|
| EventBridge Rule | AWS Service | Trigger schedule | every 5 min |
| Lambda: DDNS Resolver | AWS Lambda | Resolve hostname + update SSM | triggered by EB |
| Lambda: Authorizer | AWS Lambda | Validate API requests by IP | on-demand |
| SSM Parameter Store | AWS Service | Store current home IP | updated every 5 min |
| IAM Roles | AWS IAM | Permissions for Lambda functions | static |

## Cost Model

**Monthly Estimate:**
- Lambda invocations: ~8,640/month (5-min schedule)
  - Free tier: 1,000,000 invocations/month → **FREE**
- EventBridge rule: ~288 triggers/month
  - Free tier: 21 free PutEvents → **FREE** (well below limit)
- SSM Parameter: 1 parameter, read-heavy
  - Free tier: Unlimited standard parameters → **FREE**
- **Total Monthly Cost: ~$0.50-1.00** (minimal)

## Security Patterns

**IP Whitelisting:**
- Lambda Authorizer reads current home IP
- Only requests from that IP are allowed
- Other IPs get 403 Forbidden
- Prevents unauthorized access from elsewhere

**Least-Privilege IAM:**
- DDNS Resolver Lambda: read-only SSM (for logging), write SSM parameter
- Authorizer Lambda: read-only SSM parameter, no write access
- No EC2, S3, or other service access

**DDNS Hostname:**
- Stored in CDK context (cdk.json or command-line `--context`)
- Not in code, not in Lambda env variables
- Passed via CDK synthesis

## Related Infrastructure

**Used By:**
- [[Cartographers-Cloud-Kit]] — Imports SSM Parameter export
- Any API Gateway needing IP-based authorization

**Exports:**
- CloudFormation Export: `home-ip-ssm-param-name`
- Value: `/my-ddns-updater/current-home-ip{suffix}`
- Imported by dependent stacks via `Fn.import_value()`

## Maintenance

**Regular:**
- Verify Lambda executions in CloudWatch Logs
- Check SSM Parameter updates (should update every 5 min)
- Monitor Authorizer function performance

**One-Time Setup:**
- Configure DDNS hostname (from your router settings)
- Deploy stack with correct hostname
- Verify first Lambda execution

**Troubleshooting:**
- If IP not updating: Check Lambda logs in CloudWatch
- If DDNS resolution fails: Verify hostname is accessible via DNS
- If authorization failing: Check SSM Parameter value in console

## Lambda Authorizer Pattern

**How It Works:**

```python
# Authorizer Lambda receives API Gateway request
def lambda_handler(event, context):
    # Event contains request metadata (source IP, headers, etc.)
    source_ip = event['requestContext']['identity']['sourceIp']
    
    # Read current home IP from SSM
    current_home_ip = ssm.get_parameter(
        Name='/my-ddns-updater/current-home-ip'
    )['Parameter']['Value']
    
    # Compare
    if source_ip == current_home_ip:
        return allow_policy()  # Allow request
    else:
        return deny_policy()   # Deny request
```

**Reusable Pattern:**
- Same pattern used by [[Cartographers-Cloud-Kit]]
- Extract to shared Lambda authorizer construct
- Enable IP-based or token-based authorization

## Getting Started

```bash
# Clone and install
git clone [repo-url]
cd my-ddns-updater
poetry install

# Deploy
poetry run cdk deploy --context ddns-hostname="yourname.ddns.net"

# Check Parameter
aws ssm get-parameter \
  --name /my-ddns-updater/current-home-ip \
  --query 'Parameter.Value'

# View Lambda Logs
aws logs tail /aws/lambda/MyDdnsResolverStack-HomeIPResolverLambda --follow
```

## Key Insights

**Why This Design:**
- Serverless = no always-on costs
- 5-minute schedule = quick updates, low cost
- EventBridge trigger = reliable scheduling
- SSM Parameter = simple distributed storage
- Authorizer Lambda = reusable security layer

**Cost Optimization:**
- Uses free tiers heavily
- Minimal API calls (<9K/month)
- No data transfer costs
- Multi-environment via stack-suffix (share free tier quota)

**Pattern Reusability:**
- Lambda Authorizer pattern used by other projects
- Custom Lambda construct (Docker image) used elsewhere
- Stack-suffix context variable enables feature branches

## Related Concepts

- [[AWS CDK Infrastructure as Code]] — Technology used
- [[Lambda Authorizer Pattern]] — Reusable security pattern
- [[Multi-Environment Deployment via Stack Suffix]] — Architecture pattern
- [[Cross-Stack Resource Sharing]] — How others use this

## Open Questions

- [Add CloudWatch alarms for Lambda failures?]
- [Support multiple home IPs (failover)?]
- [Add DNS TXT record verification for security?]

## Key Files

- **Main:** [app.py](app.py)
- **Stack:** [cdk/stacks.py](cdk/stacks.py)
- **Lambda:** [src/my-ddns-hostname-resolver/app.py](src/my-ddns-hostname-resolver/app.py)
- **Config:** [cdk.json](cdk.json)

## Sources

- Wiki source: Project repository scan on 2026-08-07
- README analysis from `/mnt/c/Users/Chaddle/PycharmProjects/My-DDNS-Updater`
- AWS CDK Lambda Authorizer documentation
- AWS EventBridge documentation
