---
type: concept
date_created: 2026-08-07
date_updated: 2026-08-07
tags:
  - wiki/concept
  - infrastructure/aws
  - pattern/iac
  - tech/cdk
source_count: 2
confidence: high
---

# AWS CDK Infrastructure as Code

Infrastructure as Code (IaC) using AWS Cloud Development Kit (CDK) — a programmatic way to define cloud infrastructure using Python, TypeScript, or other languages instead of manually writing YAML CloudFormation templates.

## Definition

**AWS CDK** is an open-source framework for defining AWS infrastructure using general-purpose programming languages. Converts code to CloudFormation templates at synthesis time, then deploys via CloudFormation.

**Key Principle:** "Infrastructure" is treated as first-class code with reusability, testability, and composability.

## Why It Matters

**Advantages Over Manual CloudFormation YAML:**

| Aspect | CloudFormation YAML | AWS CDK |
|--------|-----------------|---------|
| Code Reuse | Copy-paste templates | Constructs + classes |
| Abstractions | Limited (nested stacks) | Full programming languages |
| Type Safety | None | Type hints (Python) |
| Testing | Cloud-based (expensive) | Local unit tests |
| Composition | Limited | Inheritance, mixins |
| DRY Principle | Hard to achieve | Natural with classes |
| Error Detection | Runtime | Compile-time (TypeScript) |

**Your Use Case:**
- Custom constructs for S3, CloudFront, Route 53, DynamoDB
- Reusable across multiple projects (chadbarteldotcom + thatsmidnightdotcom)
- Type hints for IDE autocomplete
- Programmatic naming conventions

## Key Concepts

**Constructs:**
- Basic building blocks of CDK
- L1 constructs: Low-level (1:1 with CloudFormation)
- L2 constructs: Higher-level (convenience, sensible defaults)
- L3 constructs: Custom domain-specific abstractions
- Example L3 construct in your code:
```python
class MyBucket(s3.Bucket):
    def __init__(self, scope, id, **kwargs):
        super().__init__(scope, id,
            encryption=s3.BucketEncryption.S3_MANAGED,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            versioned=True,
            enforce_ssl=True,
            **kwargs
        )
```

**Stacks:**
- CDK equivalent of CloudFormation stack
- One stack = one CloudFormation deployment
- Isolated infrastructure lifecycle
- Example:
```python
class MyStaticSiteStack(cdk.Stack):
    def __init__(self, scope, id, **kwargs):
        super().__init__(scope, id, **kwargs)
        bucket = MyBucket(self, "Bucket")
        distribution = MyDistribution(self, "Distribution", bucket=bucket)
```

**Apps:**
- Top-level container for stacks
- Synthesizes to CloudFormation templates
- Example:
```python
app = cdk.App()
MyStaticSiteStack(app, "static-site-stack")
app.synth()
```

**Synthesis:**
- `cdk synth` command converts Python code to CloudFormation JSON
- Output: cloud-assembly directory with templates + metadata
- Can inspect before deploying: `cat cdk.out/MyStaticSiteStack.json`

## CDK Deployment Workflow

```
1. cdk init                    # Create new CDK project
2. Edit app.py, stacks.py      # Define infrastructure
3. poetry install              # Install dependencies
4. cdk synth                   # Generate CloudFormation
5. cdk deploy                  # Deploy to AWS
6. cdk outputs                 # View outputs (Bucket name, etc.)
7. cdk destroy                 # Tear down
```

## Composition and Reusability

**Custom Constructs as Building Blocks:**

Your projects use a pattern of custom L3 constructs:

```python
# Custom constructs (reusable abstractions)
class MyBucket(s3.Bucket):
    # Enforces security defaults
    
class MyCertificate(acm.Certificate):
    # Enforces DNS validation + auto-renewal
    
class MyDistribution(cloudfront.Distribution):
    # Enforces HTTPS + modern TLS + caching headers
    
# Stack composition
class MyStaticSiteStack(cdk.Stack):
    def __init__(self, scope, id, domain_name):
        bucket = MyBucket(self, "Bucket")
        cert = MyCertificate(self, "Cert", domain=domain_name)
        dist = MyDistribution(self, "Distribution", bucket=bucket, cert=cert)
```

**Benefits:**
- Constructs enforce security defaults
- Consistent naming conventions
- Reusable across projects
- Type-safe (IDE autocomplete)
- Easier to maintain

## Context Variables

**Configuration Without Code Changes:**

```bash
# Production deployment
cdk deploy --context environment="prod" --context domain="chadbartel.com"

# Development deployment
cdk deploy --context environment="dev" --context domain="dev.chadbartel.com"
```

**In Code:**
```python
class MyStack(cdk.Stack):
    def __init__(self, scope, id, **kwargs):
        environment = self.node.try_get_context("environment") or "dev"
        domain = self.node.try_get_context("domain") or "localhost"
        # Use environment and domain variables
```

**Better Than:**
- ❌ Environment variables (not version-controlled)
- ❌ Hardcoded in Python (hard to change)
- ✅ Context variables (cdk.json or CLI, repeatable)

## Your Projects' CDK Patterns

**Pattern 1: Static Site Stack (chadbarteldotcom, thatsmidnightdotcom)**
- Custom constructs for bucket, certificate, distribution
- Exports CloudFormation outputs
- Reusable for multiple domains

**Pattern 2: Serverless API Stack (Cartographers-Cloud-Kit)**
- API Gateway, Lambda, DynamoDB, S3, Cognito
- Token Authorizer for authentication
- Multi-environment via stack-suffix context variable

**Pattern 3: Shared Infrastructure Hub (my-shared-infra)**
- Central Route 53 hosted zone
- KMS key for DNSSEC
- CloudFormation exports for other stacks to import

## Testing CDK

**Local Unit Tests:**
```python
# test_stack.py
from aws_cdk.assertions import Template

def test_bucket_encryption():
    stack = MyStaticSiteStack()
    template = Template.from_stack(stack)
    template.has_resource_properties("AWS::S3::Bucket", {
        "BucketEncryption": Match.objectLike({
            "ServerSideEncryptionConfiguration": [...]
        })
    })
```

**Benefits:**
- Fast feedback (no AWS calls)
- Catch typos and config errors early
- Safe refactoring
- Regression tests

## CDK Best Practices (From Your Code)

1. **Custom Constructs for Abstraction**
   - Hide complexity behind simple interfaces
   - Enforce security defaults
   
2. **Environment-Driven Configuration**
   - Use context variables, not env vars
   - cdk.json for version-controlled config
   
3. **Naming Conventions**
   - Consistent stack names (stack-suffix)
   - CloudFormation exports (human-readable keys)
   
4. **Least-Privilege IAM**
   - Constructs grant minimal permissions
   - Role restrictions at source
   
5. **Composition Over Inheritance**
   - Stack composes multiple constructs
   - Constructs compose simpler constructs

## Related Concepts

- [[Shared Infrastructure Hub Pattern]] — Uses CDK constructs
- [[Multi-Environment Deployment via Stack Suffix]] — Uses CDK context
- [[Cross-Stack Resource Sharing]] — Uses CDK exports/imports
- [[Static Site Deployment Pattern]] — Example application

## Open Questions

- [Add CDK unit tests to CI/CD pipeline?]
- [Create custom construct library (separate npm/pypi package)?]
- [Use CDK pipelines for CI/CD-integrated deployments?]
- [Cost estimation tools for CDK stacks?]

## Key Insights

**Why CDK for Your Projects:**
- Infrastructure mirrors application complexity
- Reusable patterns (constructs)
- Type-safe (IDE support)
- Programmatic naming (stack-suffix)
- Testable before deployment

**When NOT to Use CDK:**
- Simple, one-time deployments (CloudFormation YAML sufficient)
- No code reuse needed
- Team unfamiliar with programming

**Your Use Case:** Perfect CDK fit because:
1. Multiple projects with similar patterns
2. Infrastructure evolves (refactoring needed)
3. Multi-environment deployments (context variables)
4. Custom security defaults (constructs)

## Key Files in Your Projects

- [[chadbarteldotcom]] — `cdk/constructs.py` for static site constructs
- [[My-DDNS-Updater]] — Custom Lambda construct pattern
- [[Cartographers-Cloud-Kit]] — Multi-service orchestration pattern
- [[my-shared-infra]] — Shared exports pattern

## Sources

- AWS CDK Developer Guide (https://docs.aws.amazon.com/cdk/latest/)
- Your project repositories (chadbarteldotcom, My-DDNS-Updater, Cartographers-Cloud-Kit, my-shared-infra)
- CDK best practices from AWS Well-Architected Framework
