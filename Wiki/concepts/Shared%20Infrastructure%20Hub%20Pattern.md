---
type: concept
date_created: 2026-08-07
date_updated: 2026-08-07
tags:
  - wiki/concept
  - infrastructure/aws
  - pattern/architecture
  - tech/cdk
source_count: 2
confidence: high
---

# Shared Infrastructure Hub Pattern

Architectural pattern where a central "hub" stack manages shared infrastructure (DNS, security keys, networking) that multiple "spoke" application stacks depend upon and reference via CloudFormation exports.

## Definition

**Hub-and-Spoke Architecture:** Central infrastructure stack (hub) provides shared resources that multiple application stacks (spokes) consume via CloudFormation cross-stack references.

**Hub Responsibilities:**
- Route 53 hosted zones (DNS)
- KMS keys (encryption, DNSSEC signing)
- VPCs and networking (if multi-project)
- Shared IAM roles (if appropriate)
- Central logging/monitoring (if centralized)

**Spoke Responsibilities:**
- Application-specific infrastructure
- Import shared resources from hub
- Independent deployment lifecycle

## Why It Matters

**Alternative Architectures (and problems):**

| Approach | Problem |
|----------|---------|
| Monolithic Stack | All-or-nothing deployment, hard to scale teams |
| Per-Project Stack (no hub) | Duplication, inconsistency, hard to manage |
| Shared Infrastructure Library | Code reuse OK, but still need central state |

**Hub-and-Spoke Advantages:**
- Single source of truth (hub owns shared infrastructure)
- Decoupling (spokes can deploy independently)
- Cost efficiency (shared resources amortized)
- Security (centralized control)
- Easy to onboard new projects (just import hub exports)

## Your Hub-and-Spoke Implementation

**Hub:** [[my-shared-infra]]
```
Responsibilities:
├─ Route 53 Hosted Zone (chadbartel.com)
├─ KMS Key (ECC_NIST_P256 for DNSSEC)
├─ DNSSEC signing configuration
└─ CloudFormation Exports:
    ├─ HostedZoneId: Z1234567890ABC
    ├─ HostedZoneName: chadbartel.com
    └─ KmsKeyId: arn:aws:kms:...
```

**Spokes:**
```
[[chadbarteldotcom]]
├─ Imports: HostedZoneId
├─ Creates: S3 bucket, CloudFront distribution
└─ Exports: None (application-specific)

[[thatsmidnightdotcom]]
├─ Imports: HostedZoneId
├─ Creates: S3 bucket, CloudFront distribution (different domain)
└─ Exports: None

[[My-DDNS-Updater]]
├─ Imports: HostedZoneId
├─ Creates: Lambda functions, EventBridge, SSM Parameter
└─ Exports: CurrentHomeIpParameter (for other spokes)

[[Cartographers-Cloud-Kit]]
├─ Imports: HostedZoneId (from hub)
├─ Imports: CurrentHomeIpParameter (from My-DDNS-Updater)
├─ Creates: API Gateway, Lambda, DynamoDB, S3, Cognito
└─ Exports: None
```

## Design Principles

**1. Hub Stability**
- Hub changes rarely (DNS infrastructure stable)
- Updates coordinated across spokes
- Breaking changes avoided (backward-compatible exports)

**2. Export Naming**
- Clear, descriptive names
- Include component name and resource type
- Examples: `SharedInfraHostedZoneId`, `MyDdnsUpdaterCurrentHomeIp`

**3. Loose Coupling**
- Spokes know only export names
- Spokes don't know hub implementation details
- Hub can change implementation (e.g., switch DNS provider) without spoke changes

**4. Clear Dependencies**
- Spoke lists its imports explicitly
- CloudFormation tracks dependencies automatically
- Can visualize dependency graph in console

## Deployment Model

**Step 1: Deploy Hub First**

```bash
cd my-shared-infra
cdk deploy
# Creates: Hosted Zone, KMS Key, CloudFormation exports
```

**Step 2: Deploy Spokes (in any order)**

```bash
cd ../chadbarteldotcom
cdk deploy  # Imports HostedZoneId

cd ../My-DDNS-Updater
cdk deploy  # Imports HostedZoneId, creates exports

cd ../Cartographers-Cloud-Kit
cdk deploy  # Imports from both hub and DDNS-Updater
```

**Why Order Matters:**
- Spokes need hub exports to exist
- If spoke exports needed by others, deploy spoke first
- Generally: hub → spokes with exports → spokes without exports

## Multi-Project Cost Analysis

**Without Hub-and-Spoke (Duplication):**
```
Project 1: Custom Route 53 setup     $0.50/month
Project 2: Custom Route 53 setup     $0.50/month
Project 3: Custom Route 53 setup     $0.50/month
Project 4: Custom Route 53 setup     $0.50/month
Total: $2.00/month (redundant)
```

**With Hub-and-Spoke (Shared):**
```
Hub: Central Route 53               $0.50/month
Project 1: Import (free)
Project 2: Import (free)
Project 3: Import (free)
Project 4: Import (free)
Total: $0.50/month (shared)
```

**Savings:** $1.50/month for this example (scales with more projects)

## Extending the Hub

**Adding New Shared Resource:**

```python
# In my-shared-infra stack

# Add S3 bucket for shared logs
log_bucket = s3.Bucket(self, "LogBucket",
    block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
    versioned=True,
)

# Export for spokes to use
cdk.CfnOutput(self, "LogBucketNameOutput",
    export_name="SharedLogBucketName",
    value=log_bucket.bucket_name
)

# Spoke uses it
from aws_cdk import Fn
log_bucket_name = Fn.import_value("SharedLogBucketName")
```

**Adding New Spoke:**

```bash
# Create new project
cdk init app --language python

# In stack, import from hub
hosted_zone_id = Fn.import_value("HostedZoneId")

# Deploy
cdk deploy
```

## Multi-Region Considerations

**Current Setup (Single Region):**
- All resources in us-east-1 (or your region)
- Hub creates hosted zone in single region
- Spokes deploy to same region

**Multi-Region Hub (Advanced):**
- Hub creates Route 53 hosted zone (global)
- Hub creates regional KMS keys per region
- Spokes in each region import regional exports
- Requires separate exports per region:
  - `KmsKeyIdUsEast1`
  - `KmsKeyIdEuWest1`
  - etc.

**Current Recommendation:** Single-region hub (simpler)

## Hub Governance

**Who Manages Hub:**
- Infrastructure team or single owner
- Changes coordinated with spoke owners
- Formal change process (if org-driven)

**For Personal Projects:**
- You manage hub
- Simple change process
- Less ceremony

**Hub SLO (Service Level Objective):**
- Hosted zone: 99.99% availability (AWS managed)
- KMS key: 99.99% availability (AWS managed)
- Hub stack deployments: No more than 1x/quarter (stability)

## Related Concepts

- [[Cross-Stack Resource Sharing]] — Mechanism (exports/imports)
- [[AWS CDK Infrastructure as Code]] — How hub defined
- [[Multi-Environment Deployment via Stack Suffix]] — Can combine patterns

## Open Questions

- [Multi-region hub topology?]
- [Hub auto-discovery (spokes find hub exports)?]
- [Hub versioning strategy (v1, v2 exports)?]
- [Automated compliance/audit of hub exports?]

## Real-World Examples

**Enterprise Hub-and-Spoke:**
```
Hub (Central IT)
├─ VPC, subnets, security groups
├─ Route 53 private zone (corp.example.com)
├─ KMS keys for encryption
├─ CloudTrail for audit logging
└─ Exports: VpcId, SubnetIds, HostedZoneId, KmsKeyId

Spoke 1: Web Application
├─ Imports: VpcId, SubnetIds
├─ Creates: EC2, RDS, ALB
├─ Manages: App-specific security groups

Spoke 2: Data Pipeline
├─ Imports: KmsKeyId
├─ Creates: Lambda, SQS, S3 buckets
├─ Uses: Hub's KMS key for encryption

Spoke 3: API Service
├─ Imports: VpcId, SubnetIds
├─ Creates: API Gateway, Lambda, DynamoDB
```

**Your Setup (Simpler):**
```
Hub (my-shared-infra)
├─ Route 53 hosted zone (chadbartel.com)
├─ KMS key (DNSSEC)

Spokes:
├─ chadbarteldotcom (imports HostedZoneId)
├─ thatsmidnightdotcom (imports HostedZoneId)
├─ My-DDNS-Updater (imports HostedZoneId, exports SSM param)
└─ Cartographers-Cloud-Kit (imports from hub + DDNS-Updater)
```

## Migration Path

**If Starting Without Hub:**

```
Before:
Project A: Custom Route 53
Project B: Custom Route 53
Project C: Custom Route 53

Migrate:
1. Create my-shared-infra stack with Route 53
2. Update Project A CDK to import HostedZoneId
3. Redeploy Project A
4. Update Project B, Redeploy
5. Update Project C, Redeploy
6. Delete custom Route 53 from Projects A, B, C

After:
my-shared-infra: Central Route 53
Project A: Imports HostedZoneId
Project B: Imports HostedZoneId
Project C: Imports HostedZoneId
```

**Effort:** ~2-3 hours per project (test thoroughly)

## Scaling as You Add Projects

**Year 1 (2 projects):**
- Hub: Route 53, KMS key
- Spokes: Static sites
- Shared cost: $0.50/month (split)

**Year 2 (4 projects):**
- Hub: + WAF (Web Application Firewall)
- Spokes: + APIs, databases
- Shared cost: $2-5/month (split 4 ways)

**Year 3 (6+ projects):**
- Hub: + VPC, +Network Load Balancer
- Spokes: Complex (apps, data pipelines, microservices)
- Shared cost: $10-20/month (split 6+ ways)

## Key Insights

**Why Hub-and-Spoke Works:**
- Mirrors organizational structure (central team + project teams)
- Reduces duplication (shared infra = shared cost)
- Enables autonomy (spokes deploy independently)
- Clear ownership (hub owner known, spoke owners clear)

**When to Use:**
- Multiple projects sharing infrastructure
- Stable, non-changing shared resources
- Different teams/owners per project
- Cost matters (shared = cheaper)

**When NOT to Use:**
- Single project (monolith sufficient)
- Highly coupled projects (merge into monolith)
- Unstable, rapidly-changing shared resources

## Your Implementation

**[[my-shared-infra]]:** The hub
- Route 53 hosted zone
- KMS key for DNSSEC
- CloudFormation exports

**Spoke Projects:**
- [[chadbarteldotcom]]
- [[thatsmidnightdotcom]]
- [[My-DDNS-Updater]]
- [[Cartographers-Cloud-Kit]]

## Key Files

- [[my-shared-infra]] — Hub stack definition
- Each spoke — CDK code with `Fn.import_value()` calls

## Sources

- AWS CDK cross-stack references
- AWS Well-Architected Framework (multi-account/multi-project patterns)
- Your project repositories
