---
type: concept
date_created: 2026-08-07
date_updated: 2026-08-07
tags:
  - wiki/concept
  - infrastructure/aws
  - pattern/deployment
  - tech/cdk
source_count: 1
confidence: high
---

# Multi-Environment Deployment via Stack Suffix

Pattern for deploying CDK applications to multiple environments (dev, staging, production, or feature branches) using a single codebase with dynamic stack naming via a `stack-suffix` context variable.

## Definition

**Stack Suffix Pattern:** CDK synthesizes infrastructure with names like `MyStack-{stack-suffix}`, enabling isolated copies of the same infrastructure for different environments without code duplication.

**Example:**
```bash
# Same code, different environments
cdk deploy --context stack-suffix="dev"      # Creates: MyStack-dev, MyApi-dev, etc.
cdk deploy --context stack-suffix="staging"  # Creates: MyStack-staging, MyApi-staging
cdk deploy --context stack-suffix="prod"     # Creates: MyStack-prod, MyApi-prod
```

## Why It Matters

**Alternative Approaches (and their problems):**

| Approach | Problem |
|----------|---------|
| Separate Git branches per environment | Merging conflicts, hard to sync |
| Multiple copy-paste codebases | Maintenance nightmare (bug fixes replicated) |
| Hardcoded environment in code | Can't deploy to new environment without code change |
| Env vars only (no stack names) | CloudFormation stacks have same name (conflicts) |

**Stack Suffix Advantages:**
- Single codebase for all environments
- Isolated AWS resources per environment
- Same code, different configuration
- Easily add new environments (just pass different suffix)
- Feature branches as temporary environments

## How It Works

**In CDK Code:**

```python
class MyStack(cdk.Stack):
    def __init__(self, scope, id, **kwargs):
        super().__init__(scope, id, **kwargs)
        
        # Read suffix from context
        suffix = self.node.try_get_context("stack-suffix") or "dev"
        
        # Use suffix in resource naming
        bucket_name = f"my-bucket-{suffix}"
        api_name = f"my-api-{suffix}"
        db_table = f"my-table-{suffix}"
        
        # CloudFormation resources get suffixed names
        s3.Bucket(self, "Bucket", bucket_name=bucket_name)
        # Creates S3 bucket: my-bucket-dev, my-bucket-staging, my-bucket-prod
```

**In App Definition:**

```python
app = cdk.App()

# Single stack definition
MyStack(app, "MyStack")  # Stack ID always "MyStack"
                         # But suffix changes via context

# When deployed:
# cdk deploy --context stack-suffix="prod"
# → CloudFormation stack name: MyStack (same as dev!)
# → But resources inside use prod suffix
```

**CloudFormation Stack Naming:**

Confusing but important distinction:
- CloudFormation stack name: `MyStack` (from stack ID, always the same)
- Resource names inside: `my-bucket-prod`, `my-api-prod` (use suffix)
- Outputs: `MyBucketNameProd`, `MyApiEndpointProd` (suffix in output key)

**Why This Design:**
- Stack ID stable (for CDK targeting)
- Resource names isolated per environment (no conflicts)
- Exports have suffixes too (each env gets separate export)

## Your Projects Using This Pattern

**[[My-DDNS-Updater]]:**
```bash
poetry run cdk deploy --context ddns-hostname="yourname.ddns.net" \
                      --context stack-suffix="dev"
# Creates: 
#   Parameter: /my-ddns-updater/current-home-ip-dev
#   Lambda: MyDdnsResolverStack-HomeIPResolverLambda-dev
#   Authorizer: MyDdnsResolverStack-AuthorizerLambda-dev
```

**[[Cartographers-Cloud-Kit]]:**
```bash
poetry run cdk deploy --context stack-suffix="staging"
# Creates:
#   DynamoDB: cartographers-cloud-kit-staging-metadata
#   S3 Bucket: cartographers-cloud-kit-staging-assets
#   API Endpoint: cartographers-cloud-kit-staging-api
#   Cognito: cck-staging-user-pool
```

**Feature Branch Deployments:**
```bash
# Test new feature in isolated environment
cdk deploy --context stack-suffix="feature/new-auth"
# Creates: cartographers-cloud-kit-feature-new-auth-* resources
# No interference with dev/staging/prod
# Delete after testing: cdk destroy --context stack-suffix="feature/new-auth"
```

## Deployment Workflow

**Step 1: Define contexts in cdk.json (optional, can override at CLI):**

```json
{
  "context": {
    "stack-suffix": "dev",
    "domain": "dev.chadbartel.com"
  }
}
```

**Step 2: Deploy with context override:**

```bash
# Override via CLI (takes precedence over cdk.json)
cdk deploy --context stack-suffix="prod" --context domain="chadbartel.com"
```

**Step 3: Verify outputs:**

```bash
cdk outputs --context stack-suffix="prod"
# Shows: MyBucketName = my-bucket-prod, MyApiEndpoint = https://my-api-prod.example.com
```

## Cost Implications

**Per-Environment Costs:**
```
Dev environment:   $10/month (low traffic, small resources)
Staging:           $25/month (mirror production, higher load)
Production:        $100+/month (full capacity)
Feature branch:    $5/month (temporary, small)
---------
Total:             $140+/month for full pipeline
```

**Cost Optimization:**
- Dev: Smaller instances, on-demand DynamoDB
- Staging: Same as prod (for accurate testing)
- Prod: Full capacity
- Delete feature branches after testing (save costs)

## Managing Multiple Environments

**Infrastructure as Environment Metadata:**

```python
# Define environment config
ENVIRONMENTS = {
    "dev": {
        "stack_suffix": "dev",
        "lambda_memory": 256,        # Small Lambda
        "dynamodb_billing": "PAY_PER_REQUEST",  # Cheap
        "api_throttle": 10,          # Low throttle
    },
    "prod": {
        "stack_suffix": "prod",
        "lambda_memory": 512,        # Larger Lambda
        "dynamodb_billing": "PROVISIONED",     # Faster
        "api_throttle": 1000,        # High throttle
    }
}

class MyStack(cdk.Stack):
    def __init__(self, scope, id, env_name, **kwargs):
        env_config = ENVIRONMENTS[env_name]
        suffix = env_config["stack_suffix"]
        
        # Size Lambda based on environment
        lambda_fn = aws_lambda.Function(self, "MyFunction",
            memory_size=env_config["lambda_memory"],
        )
```

## Gotchas and Considerations

**Gotcha 1: CloudFormation Export Naming**
- Exports must be unique across ALL stacks in account
- If not using suffix in export names, conflicts occur
- Solution: Include suffix in export names
```python
cdk.CfnOutput(self, "MyBucketNameOutput",
    export_name=f"MyBucketName{suffix}",
    value=bucket.bucket_name
)
```

**Gotcha 2: Stack Outputs**
- Outputs are per-stack
- Multiple stacks with same stack ID → outputs overwrite
- Solution: Use suffix in output keys
```python
output_key = f"ApiEndpoint{suffix}"
# Dev: ApiEndpointDev
# Prod: ApiEndpointProd
```

**Gotcha 3: IAM Cross-Environment Access**
- Dev Lambda can't access Prod DynamoDB
- Intentional isolation (security)
- Solution: Explicit IAM grants if needed
```python
# Only if dev needs prod data
prod_table.grant_read_data(dev_lambda)
```

## Related Concepts

- [[AWS CDK Infrastructure as Code]] — Technology used
- [[Cross-Stack Resource Sharing]] — How environments share resources (if needed)
- [[Shared Infrastructure Hub Pattern]] — Infrastructure shared across environments

## Open Questions

- [Promote stacks between environments (dev → staging → prod)?]
- [Automated testing between environment deployments?]
- [Environment-specific CI/CD gates?]
- [Cost tagging per environment for chargeback?]

## Key Insights

**Why Stack Suffix Works:**
- Single deployment command with context
- CloudFormation isolation (separate stacks possible, but shared OK)
- Resource naming isolation (no conflicts)
- Easy cleanup (cdk destroy removes entire environment)

**When to Use:**
- Multiple projects with similar infrastructure
- Need dev/staging/prod isolation
- Want single codebase
- ADHD-friendly (context-driven, repeatable)

**When NOT to Use:**
- Simple one-time deployment
- Fundamentally different architecture per environment
- Multiple teams (use separate repos instead)

## Your Implementation

**In Your Projects:**
- [[My-DDNS-Updater]]: Stack-suffix for dev/staging/prod
- [[Cartographers-Cloud-Kit]]: Stack-suffix for dev/staging/prod
- [[My-DDNS-Updater]]: Stack-suffix + feature branches
- Feature branch isolation: `--context stack-suffix="feature/x"`

## Key Files

- [[My-DDNS-Updater]] — [cdk.json](cdk.json) context config
- [[Cartographers-Cloud-Kit]] — Stack definition with suffix handling
- [[my-shared-infra]] — Environment-agnostic (no suffix, central hub)

## Sources

- AWS CDK Context documentation
- Your project repositories (My-DDNS-Updater, Cartographers-Cloud-Kit)
- AWS Well-Architected Framework (environment separation)
