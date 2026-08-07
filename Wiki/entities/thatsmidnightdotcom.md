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

# thatsmidnightdotcom

Personal static website for the ThatsMidnight user, mirroring the [[chadbarteldotcom]] architecture. Demonstrates CDK pattern reuse across multiple domain deployments with identical infrastructure topology.

## Purpose

Deploy thatsmidnight.com using the same proven S3 + CloudFront + ACM + Route 53 pattern as chadbarteldotcom, showing infrastructure-as-code reusability.

## Core Philosophy

**Pattern Reuse:**
- Same CDK stack, different domain configuration
- Proves custom constructs are truly reusable
- Minimal code duplication
- Different deployment context (domain name only changes)

**Consolidation Opportunity:**
- Could merge chadbarteldotcom + thatsmidnightdotcom into single stack
- Use stack-suffix or domain context variable
- Single CDK deploy with multiple stacks
- But currently deployed separately (simpler per-project model)

## Key Features

- **Identical to chadbarteldotcom** — S3 + CloudFront + ACM + Route 53
- **Static content hosting** — thatsmidnight.com domain
- **Global CDN** — CloudFront edge locations worldwide
- **HTTPS** — ACM certificate with DNS validation
- **CORS support** — For embedded content

## Tech Stack

- **Language:** Python 3.12
- **Framework:** AWS CDK v2.202.0
- **Key AWS Services:** S3, CloudFront, ACM, Route 53, IAM
- **Dependencies:** aws-cdk-lib, constructs
- **Custom Constructs:** Identical to chadbarteldotcom (MyBucket, MyCertificate, MyDistribution)

## Architecture

**Identical to [[chadbarteldotcom]]:**
```
User Request (https://thatsmidnight.com)
    ↓
Route 53 (DNS)
    ↓
CloudFront (CDN)
    ↓
Origin Access Control
    ↓
S3 Bucket (private)
    ↓
Response
```

**Project Structure:**
```
thatsmidnightdotcom/
├── app.py              # CDK app (identical pattern)
├── pyproject.toml     # Poetry deps
├── cdk/
│   ├── stacks.py     # MyStaticSiteStack
│   ├── constructs.py # Custom abstractions
│   └── enums.py      # Config (thatsmidnight domain)
```

## Key Differences from chadbarteldotcom

| Aspect | ChadBartel | ThatsMidnight |
|--------|-----------|---------------|
| Domain | chadbartel.com | thatsmidnight.com |
| Stack Name | chadbarteldotcom-stack | thatsmidnight-stack |
| S3 Bucket | chadbarteldotcom-bucket | thatsmidnight-bucket |
| CloudFront ID | Different | Different |
| Route 53 Records | chadbartel.com | thatsmidnight.com |
| Infrastructure | ✅ Identical | ✅ Identical |

**Code:** ~95% identical (only domain config differs)

## Infrastructure Components

| Component | Service | Purpose | Cost |
|-----------|---------|---------|------|
| S3 Bucket | AWS | Store files | $0.023/GB |
| CloudFront | AWS | Global CDN | $0.085/GB |
| ACM Certificate | AWS | HTTPS | FREE |
| Route 53 | AWS | DNS | $0.50/month |

**Total Monthly:** ~$1.00-2.00

## Deployment

```bash
poetry run cdk deploy

# Output: Infrastructure deployed for thatsmidnight.com

# Upload content
aws s3 sync ./public s3://thatsmidnight-bucket --delete

# Verify
curl https://thatsmidnight.com
```

## Cost Optimization

**Same as chadbarteldotcom:**
- CloudFront free tier covers most usage
- ACM is free
- Route 53 is fixed $0.50/month
- S3 storage minimal for static site

## Relationships

**Pattern Source:**
- Reuses architecture from [[chadbarteldotcom]]
- Demonstrates custom constructs portability

**Infrastructure Depends On:**
- [[my-shared-infra]] — Route 53 domain resources

## Consolidation Opportunity

**Current State (Two Separate Stacks):**
- chadbarteldotcom-stack
- thatsmidnight-stack
- Maintenance burden: Update patterns twice

**Potential Future State (One Stack, Multiple Domains):**
```python
# Single stack, multiple domains
StaticSiteStack(scope, "static-sites", {
    "chadbartel.com": {...},
    "thatsmidnight.com": {...}
})
```

**Benefits:**
- Single CDK app maintains both sites
- Pattern updates apply to all domains
- Shared logging/monitoring
- Estimated time to merge: 2-3 hours

## Getting Started

```bash
git clone [repo-url]
cd thatsmidnightdotcom
poetry install
poetry run cdk deploy
```

## Maintenance

**Same as chadbarteldotcom:**
- Monitor CloudFront metrics
- S3 lifecycle policies clean old versions
- ACM auto-renewal (no action needed)
- Periodic CDK updates

## Related Concepts

- [[Static Site Deployment Pattern]] — Architecture
- [[AWS CDK Infrastructure as Code]] — Technology
- [[Pattern Reuse Across Projects]] — Demonstrates reusability

## Open Questions

- [Consolidate into single stack with domain context variable?]
- [Add CloudFront invalidation automation for content changes?]
- [Custom error pages (404, 403)?]

## Key Files

- **Main:** [app.py](app.py)
- **Stack:** [cdk/stacks.py](cdk/stacks.py)
- **Constructs:** [cdk/constructs.py](cdk/constructs.py)

## Sources

- Wiki source: Project repository scan on 2026-08-07
- README analysis from `/mnt/c/Users/Chaddle/PycharmProjects/thatsmidnightdotcom`
- Pattern inherited from [[chadbarteldotcom]]
