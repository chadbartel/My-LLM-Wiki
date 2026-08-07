---
type: entity
date_created: 2026-08-07
date_updated: 2026-08-07
tags:
  - wiki/entity
  - project/aws
  - infrastructure/hub
  - status/active
  - tech/cdk
  - tech/aws
source_count: 1
---

# my-shared-infra

Central AWS infrastructure hub providing DNSSEC signing, Route 53 hosted zone management, and KMS key provisioning. Acts as the foundational infrastructure layer that all other AWS projects reference and depend upon.

## Purpose

Single source of truth for shared AWS resources. Prevents duplicate infrastructure definitions and enables consistent DNS management across all projects in your ecosystem.

## Core Philosophy

**Centralized Infrastructure:**
- One CDK stack managing domain infrastructure (chadbartel.com)
- DNSSEC signing centrally managed via Route 53 + KMS
- CloudFormation exports for cross-project resource sharing
- All AWS projects reference shared resources here

**Hub Pattern:**
- Like `my-shared-infra` in your naming convention
- Other projects depend on this (import its exports)
- Single point of maintenance for DNS and domain security
- Prevents configuration drift

## Key Features

- **Route 53 Hosted Zone Management** — Hosts chadbartel.com domain
- **DNSSEC Signing** — KMS-backed key signing for domain security
- **CloudFormation Exports** — Enables cross-stack resource sharing
- **Custom CDK Constructs** — Abstracted infrastructure patterns for reuse
- **Configuration as Enums** — Domain config in `cdk/enums.py` (DRY principle)

## Tech Stack

- **Language:** Python 3.10+
- **Framework:** AWS CDK v2.90.0+
- **Key AWS Services:** Route 53, KMS, CloudFormation
- **Dependencies:** aws-cdk-lib, constructs
- **Custom abstractions:** MyHostedZone, MyKmsKey, MyKeySigningKey constructs

## Architecture

**Project Structure:**
```
my-shared-infra/
├── app.py                     # CDK app initialization
├── pyproject.toml             # Poetry deps
├── cdk.json                   # CDK context
└── cdk/
    ├── stacks.py             # MyDNSSECStack definition
    ├── constructs.py         # Custom abstractions
    └── enums.py              # Config (HOSTED_ZONE_ID, domain names)
```

**Core Components:**
- **CDK Stack** (`cdk/stacks.py`): `MyDNSSECStack` defines all infrastructure
- **Custom Constructs** (`cdk/constructs.py`): Reusable patterns (Route53HostedZone, KmsKey, etc.)
- **Configuration** (`cdk/enums.py`): Domain names, hosted zone IDs, DNSSEC settings
- **Deployment Model:** CDK synthesize → CloudFormation deploy

**AWS Constructs Used:**
- `Route53HostedZone` — Hosted zone for chadbartel.com
- `KmsKey` (ECC_NIST_P256) — DNSSEC signing key
- `Route53.KeySigningKey` — Maps KMS key to Route 53
- `PolicyStatement` — Least-privilege KMS permissions

## Infrastructure Components

| Component | Type | Purpose | Status |
|-----------|------|---------|--------|
| Route 53 Hosted Zone | AWS Service | DNS for chadbartel.com | active |
| KMS Key (ECC_NIST_P256) | AWS Service | DNSSEC signing key | active |
| Route 53 Key Signing Key | AWS Resource | DNSSEC validation | active |
| CloudFormation Exports | Outputs | Cross-project sharing | active |

## Relationships

**Depended On By:**
- [[My-DDNS-Updater]] — Uses Route 53 hosted zone, creates SSM Parameter export
- [[chadbarteldotcom]] — Creates S3 + CloudFront for chadbartel.com domain
- [[thatsmidnightdotcom]] — Uses Route 53 subdomain
- [[Cartographers-Cloud-Kit]] — Uses subdomain, imports resources

**Pattern Source For:**
- All AWS projects in your workspace
- CDK custom constructs pattern
- Configuration via enums

## Deployment

```bash
cd my-shared-infra
poetry install
poetry run cdk deploy
```

**Outputs:**
```
HostedZoneId: Z1234567890ABC
HostedZoneName: chadbartel.com
```

## Cost Model

**Estimated Monthly Cost:**
- Route 53 Hosted Zone: $0.50
- DNSSEC signing (KMS key + operations): ~$1.00
- CloudFormation: free
- **Total: ~$1.50/month**

## DNSSEC Security

**Why DNSSEC Matters:**
- Prevents DNS hijacking
- Validates domain ownership cryptographically
- Protects against man-in-the-middle attacks on DNS resolution

**How It Works:**
1. KMS key stores DNSSEC signing key (ECC_NIST_P256)
2. Route 53 uses KMS key to sign DNS records
3. Recursive resolvers verify signature before accepting response
4. Unauthorized changes to DNS rejected by validators

**Configuration:**
- Algorithm: ECC_NIST_P256 (modern, smaller key size)
- KMS key permission: route53.amazonaws.com service only
- Zone signing: Automatic (Route 53 manages)

## Key Insights

**Hub Pattern:**
- Centralized = easier to maintain
- Shared exports = avoids duplication
- Single point of truth = prevents config drift

**CDK Patterns:**
- Custom constructs abstract complexity
- Enums provide configuration DRY principle
- Custom parameters enable code reuse

**Cross-Stack Sharing:**
- CloudFormation exports named: `HostedZoneId`, `HostedZoneName`
- Imported by dependent projects: `Fn.import_value("HostedZoneId")`
- Loose coupling between stacks

## Getting Started

```bash
# Clone and install
git clone [repo-url]
cd my-shared-infra
poetry install

# Deploy
poetry run cdk deploy

# Check outputs
poetry run cdk describe

# Destroy (if needed)
poetry run cdk destroy
```

## Maintenance Tasks

**Regular:**
- Monitor DNSSEC status in Route 53 console
- Verify DNS resolution for chadbartel.com
- Check CloudFormation stack events for errors

**Periodic:**
- Renew DNSSEC key (annual, handled by Route 53)
- Update CDK version (follow AWS releases)
- Audit KMS key access policies

## Related Concepts

- [[AWS CDK Infrastructure as Code]] — Technology used
- [[Shared Infrastructure Hub Pattern]] — Architectural pattern
- [[Cross-Stack Resource Sharing]] — How other projects depend on this
- [[AWS Infrastructure Ecosystem]] — Role in your infrastructure

## Open Questions

- [Should add monitoring/alerting for DNS changes?]
- [Multi-region failover for Route 53?]
- [TLS certificates management strategy?]

## Key Files

- **Main:** [app.py](app.py)
- **Stack:** [cdk/stacks.py](cdk/stacks.py)
- **Constructs:** [cdk/constructs.py](cdk/constructs.py)
- **Config:** [cdk/enums.py](cdk/enums.py), [cdk.json](cdk.json)

## Sources

- Wiki source: Project repository scan on 2026-08-07
- README analysis from `/mnt/c/Users/Chaddle/PycharmProjects/my-shared-infra`
- CDK v2.90.0+ documentation
- AWS Route 53 + DNSSEC documentation
