---
type: entity
date_created: 2026-08-07
date_updated: 2026-08-07
tags:
  - wiki/entity
  - project/aws
  - website
  - status/active
  - tech/cdk
  - tech/s3
  - tech/cloudfront
source_count: 1
---

# chadbarteldotcom

Personal static website deployment on AWS demonstrating best-practice secure static site hosting with S3, CloudFront global edge caching, ACM TLS certificates, and Route 53 DNS. Shows enterprise-grade CDK patterns applied to a simple use case.

## Purpose

Showcase professional-grade cloud architecture for static content. Serve chadbartel.com and www.chadbartel.com from S3 (private bucket) via CloudFront (global CDN) with HTTPS via ACM and DNS via Route 53.

## Core Architecture Pattern

**The Pattern (S3 + CloudFront + ACM + Route 53):**
```
User Request (https://chadbartel.com)
    ↓
Route 53 (DNS resolution)
    ↓
CloudFront (global edge locations, HTTPS termination)
    ↓
Origin Access Control (OAC) verification
    ↓
S3 Bucket (private, encrypted)
    ↓
Response (HTML, CSS, images)
```

**Why This Architecture:**
- S3 is cheap ($0.023/GB stored)
- CloudFront caches globally (fast for users everywhere)
- Origin Access Control ensures only CloudFront accesses S3
- Private S3 bucket (no public access)
- ACM certificates are free

## Key Features

- **S3 Bucket (Private)** — Stores website files, encrypted by default
- **CloudFront Distribution** — Global edge network for fast content delivery
- **Origin Access Control (OAC)** — Modern authentication (replaces deprecated OAI)
- **ACM TLS Certificate** — Free HTTPS certificate
- **Route 53 Records** — DNS for root domain and www subdomain
- **CORS Support** — Enable embedded content (SoundCloud, YouTube, etc.)
- **Versioning** — S3 object versioning for safe updates

## Tech Stack

- **Language:** Python 3.12
- **Framework:** AWS CDK v2.205.0
- **Key AWS Services:** S3, CloudFront, ACM, Route 53, IAM
- **Dependencies:** aws-cdk-lib, constructs
- **Custom Constructs:** MyBucket, MyHostedZone, MyCertificate, MyCloudFrontOAC, MyDistribution

## Architecture

**Project Structure:**
```
chadbarteldotcom/
├── app.py                  # CDK app (environment-aware, local .env support)
├── pyproject.toml         # Poetry dependencies
├── cdk/
│   ├── stacks.py         # MyStaticSiteStack definition
│   ├── constructs.py     # Custom abstractions (Bucket, Certificate, Distribution)
│   └── enums.py          # Configuration (domain names, hosted zone ID)
└── resources/            # CloudFormation designer exports (reference)
```

**Core Stack:**
- **CDK App** (`app.py`): Loads environment (local .env or AWS context)
- **Custom Constructs** (`cdk/constructs.py`): Reusable patterns for each AWS service
- **Configuration** (`cdk/enums.py`): Domain names, hosted zone ID, region
- **Deployment:** CDK synthesize → CloudFormation deploy

## Deployment Model

```bash
# Deploy
poetry run cdk deploy

# Output:
# CloudFrontDistributionId: E1234567890ABC
# S3BucketName: chadbarteldotcom-bucket-xyz
# DomainName: chadbartel.com

# Upload website files
aws s3 sync ./public s3://chadbarteldotcom-bucket-xyz --delete

# Invalidate CloudFront cache (optional, if making changes)
aws cloudfront create-invalidation \
  --distribution-id E1234567890ABC \
  --paths "/*"
```

## Infrastructure Components

| Component | Type | Purpose | Cost |
|-----------|------|---------|------|
| S3 Bucket | AWS Service | Store website files | ~$0.50/month (small site) |
| CloudFront | AWS Service | Global edge caching | ~$0.085/GB transferred |
| ACM Certificate | AWS Service | HTTPS | FREE |
| Route 53 | AWS Service | DNS | $0.50/month (hosted zone) |
| IAM Policies | AWS IAM | Permissions | FREE |

**Total Monthly Estimate:** $1.00-2.00 for small website

## Security Patterns

**Private S3 Bucket:**
- ❌ NOT publicly accessible (block all public access enabled)
- ✅ CloudFront accesses via Origin Access Control
- ✅ Only CloudFront can retrieve objects

**Origin Access Control (OAC):**
- Modern replacement for deprecated Origin Identity (OAI)
- CloudFront signs requests with AWS Signature V4
- S3 bucket policy validates CloudFront's signature
- Example policy:
```json
{
  "Effect": "Allow",
  "Principal": {
    "Service": "cloudfront.amazonaws.com"
  },
  "Action": "s3:GetObject",
  "Resource": "arn:aws:s3:::chadbarteldotcom/*",
  "Condition": {
    "StringEquals": {
      "aws:SourceArn": "arn:aws:cloudfront::123456789012:distribution/E1234567890ABC"
    }
  }
}
```

**HTTPS via ACM:**
- Certificate covers chadbartel.com + www.chadbartel.com
- DNS validation via Route 53 (automatic)
- Certificates renew automatically
- No manual renewal needed

## Cost Optimization

**For Small Sites:**
- S3 storage: $0.023/GB (under 1GB per month typical)
- CloudFront: Usually under $0.10/month (free tier covers most usage)
- Route 53: $0.50/month (fixed)
- ACM: FREE
- **Total:** ~$0.50-1.00/month

**How to Reduce Further:**
- S3 lifecycle policies: Delete old versions after 90 days
- CloudFront caching: Long TTL for static assets (1 year)
- Gzip compression: Enable in CloudFront behavior

## Custom Constructs Pattern

**MyBucket Construct:**
```python
class MyBucket(s3.Bucket):
    def __init__(self, scope, id, **kwargs):
        super().__init__(scope, id,
            versioned=True,
            encryption=s3.BucketEncryption.S3_MANAGED,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            enforce_ssl=True,
            **kwargs
        )
```

**MyDistribution Construct:**
```python
class MyDistribution(cloudfront.Distribution):
    def __init__(self, scope, id, bucket, certificate, **kwargs):
        super().__init__(scope, id,
            default_behavior=cloudfront.BehaviorOptions(
                origin=cloudfront.S3Origin(bucket, origin_access_control=oac),
                viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
            ),
            certificate=certificate,
            **kwargs
        )
```

**Benefit:** Consistent security defaults across projects

## Relationships

**Pattern Source For:**
- [[thatsmidnightdotcom]] — Identical architecture for different domain
- [[Cartographers-Cloud-Kit]] — Uses similar S3 + CloudFront pattern for assets

**Infrastructure Depends On:**
- [[my-shared-infra]] — Route 53 hosted zone
- [[My-DDNS-Updater]] — (Optional) for dynamic IP services

## Getting Started

```bash
git clone [repo-url]
cd chadbarteldotcom
poetry install

# Deploy infrastructure
poetry run cdk deploy

# Upload website files
aws s3 sync ./public s3://[bucket-name] --delete

# Verify
curl https://chadbartel.com
```

## CORS Configuration

**Enable embedded content:**

```python
bucket.add_cors_rule(
    allowed_methods=[s3.HttpMethods.GET, s3.HttpMethods.HEAD],
    allowed_origins=["https://chadbartel.com", "https://www.chadbartel.com"],
    allowed_headers=["*"],
    max_age=Duration.days(1),
)
```

**Use cases:**
- Embedded SoundCloud player
- Embedded YouTube videos
- Cross-domain image loading

## Maintenance

**Regular:**
- Monitor CloudFront metrics in console
- Check S3 bucket size
- Verify DNS resolution

**Periodic:**
- ACM certificate automatically renews (no action needed)
- S3 object lifecycle policies clean old versions
- Update CDK version annually

**Troubleshooting:**
- "Access Denied" from CloudFront → Check S3 bucket policy and OAC
- Slow loads → Check CloudFront cache status
- HTTPS errors → Check ACM certificate validity

## Related Concepts

- [[Static Site Deployment Pattern]] — The S3 + CloudFront pattern
- [[AWS CDK Infrastructure as Code]] — Technology
- [[Shared Infrastructure Hub Pattern]] — Uses my-shared-infra

## Open Questions

- [Add versioning + rollback strategy?]
- [WAF (Web Application Firewall) for DDoS protection?]
- [Custom error pages (404, 403)?]

## Key Files

- **Main:** [app.py](app.py)
- **Stack:** [cdk/stacks.py](cdk/stacks.py)
- **Constructs:** [cdk/constructs.py](cdk/constructs.py)
- **Config:** [cdk/enums.py](cdk/enums.py)

## Sources

- Wiki source: Project repository scan on 2026-08-07
- README analysis from `/mnt/c/Users/Chaddle/PycharmProjects/chadbarteldotcom`
- AWS S3 + CloudFront documentation
- AWS CDK Constructs documentation
