---
type: concept
date_created: 2026-08-07
date_updated: 2026-08-07
tags:
  - wiki/concept
  - infrastructure/aws
  - pattern/sharing
  - tech/cloudformation
source_count: 2
confidence: high
---

# Cross-Stack Resource Sharing

Pattern for sharing AWS resources between independently deployed CDK stacks using CloudFormation exports and imports. Enables one "hub" stack to publish resources that other "spoke" stacks consume.

## Definition

**Cross-Stack Sharing:** CloudFormation exports allow one stack to publish resource values (outputs), and other stacks to import those values using `Fn.import_value()`.

**Use Case:** Central infrastructure stack (e.g., Route 53 hosted zone, KMS key) shared by multiple application stacks.

## Why It Matters

**Alternative Approaches (and problems):**

| Approach | Problem |
|----------|---------|
| Hardcode IDs in each stack | Brittle, breaks if central resource moves |
| Env vars passed at deploy time | Error-prone, hard to track dependencies |
| Monolithic stack (everything in one) | Can't deploy services independently |
| CloudFormation parameters | Manual input required, error-prone |

**Cross-Stack Sharing Advantages:**
- Automatic dependency tracking
- Central "source of truth"
- Safe (exported values validated)
- Easy to trace (CloudFormation console shows dependencies)
- Enables service autonomy (each team manages their stack)

## How It Works

**Hub Stack (my-shared-infra):**

```python
# Central infrastructure stack
class MySharedInfraStack(cdk.Stack):
    def __init__(self, scope, id, **kwargs):
        super().__init__(scope, id, **kwargs)
        
        # Create central resources
        hosted_zone = route53.HostedZone(self, "HostedZone",
            zone_name="chadbartel.com"
        )
        
        # EXPORT the resource ID for other stacks
        cdk.CfnOutput(self, "HostedZoneIdExport",
            export_name="HostedZoneId",  # Export name
            value=hosted_zone.hosted_zone_id
        )
```

**Spoke Stack (chadbarteldotcom or My-DDNS-Updater):**

```python
# Application stack that depends on central resources
class MyAppStack(cdk.Stack):
    def __init__(self, scope, id, **kwargs):
        super().__init__(scope, id, **kwargs)
        
        # IMPORT the resource from central stack
        hosted_zone_id = cdk.Fn.import_value("HostedZoneId")
        
        # Use imported resource
        route53.ARecord(self, "DnsRecord",
            zone=route53.HostedZone.from_hosted_zone_id(self, "ImportedZone", hosted_zone_id),
            record_name="myservice",
            target=route53.RecordTarget.from_ip_address("192.168.1.17")
        )
```

**CloudFormation Mechanism:**

```yaml
# Hub stack output (my-shared-infra)
Outputs:
  HostedZoneId:
    Value: Z1234567890ABC
    Export:
      Name: HostedZoneId

# Spoke stack imports
Resources:
  DnsRecord:
    Type: AWS::Route53::RecordSet
    Properties:
      HostedZoneId: !ImportValue HostedZoneId  # Imports the exported value
```

## Your Projects' Hub-and-Spoke Architecture

**Hub:** [[my-shared-infra]]
- Central Route 53 hosted zone
- Central KMS key (DNSSEC)
- Exports:
  - `HostedZoneId`
  - `HostedZoneName`
  - `KmsKeyId`

**Spokes:**
- [[chadbarteldotcom]] — Imports hosted zone for chadbartel.com DNS
- [[thatsmidnightdotcom]] — Imports hosted zone for thatsmidnight.com DNS
- [[My-DDNS-Updater]] — Imports hosted zone, creates SSM exports
- [[Cartographers-Cloud-Kit]] — Imports my-ddns-updater SSM parameter for IP whitelisting

**Dependency Chain:**
```
my-shared-infra (central)
    ↑
    ├─ chadbarteldotcom (imports hosted zone)
    ├─ thatsmidnightdotcom (imports hosted zone)
    ├─ My-DDNS-Updater (imports hosted zone)
    │   ↑
    │   └─ Cartographers-Cloud-Kit (imports SSM parameter from DDNS-Updater)
```

## Export Naming Conventions

**Best Practice: Use Human-Readable Names**

```python
# Good: descriptive, clear intent
cdk.CfnOutput(self, "HostedZoneOutput",
    export_name="SharedInfraHostedZoneId",
    value=hosted_zone.hosted_zone_id
)

# Avoid: cryptic, hard to find
cdk.CfnOutput(self, "Out1",
    export_name="val123",
    value=hosted_zone.hosted_zone_id
)
```

**Naming Pattern:**
```
{ComponentName}{ResourceType}{Detail}
```

Examples:
- `SharedInfraHostedZoneId`
- `MyDdnsUpdaterCurrentHomeIpParam`
- `MyAppDynamoDbTableName`

## Deployment Order

**Critical:** Hub stack must deploy FIRST, before spokes.

```bash
# Step 1: Deploy hub
cd my-shared-infra
cdk deploy
# Exports are now available

# Step 2: Deploy spokes (in any order)
cd ../chadbarteldotcom
cdk deploy

cd ../My-DDNS-Updater
cdk deploy

cd ../Cartographers-Cloud-Kit
cdk deploy
```

**Why Order Matters:**
- Spokes try to import at synthesis time
- If hub exports don't exist, import fails with "Export not found"
- Solution: Deploy hub first, then spokes

## CloudFormation Dependencies

**Automatic Dependency Tracking:**

When spoke stack imports hub export, CloudFormation tracks dependency:
- Spoke cannot be deleted before hub (deletion would break import)
- Hub export cannot be renamed/removed while spoke depends on it
- Console shows dependency graph

**Visual in AWS CloudFormation Console:**
```
Stacks:
├─ my-shared-infra (parent)
│   └─ Exports:
│       ├─ HostedZoneId
│       ├─ HostedZoneName
│       └─ KmsKeyId
│
├─ chadbarteldotcom (imports HostedZoneId)
├─ My-DDNS-Updater (imports HostedZoneId)
└─ Cartographers-Cloud-Kit (imports SSM param from DDNS-Updater)
```

## Updating Shared Resources

**Changing an Export (Safely):**

```python
# Current export
cdk.CfnOutput(self, "HostedZoneIdOutput",
    export_name="HostedZoneId",
    value=hosted_zone.hosted_zone_id
)

# If you need to change the value:
# 1. Update hub stack (cdk deploy)
# 2. All spokes automatically use new value
# 3. No spoke changes needed (import name stays same)
```

**Removing an Export (Carefully):**

```python
# Before: export exists, spokes import it
# After: remove export line, deploy hub

# Problem: Spokes now fail to import
# Solution: Update ALL spokes to not import before removing export

# Better: Keep export for 1-2 releases, mark deprecated
# Then remove when confident spokes updated
```

## Cost and Limits

**CloudFormation Export Limits:**
- 200 exports per account (soft limit, increase by request)
- Export names must be unique per region
- Exports live as long as importing stack exists

**Cross-Account Exports:**
- CloudFormation exports are per-account only
- For cross-account sharing: use Lambda or Parameter Store
- Your setup is single-account (all projects in one AWS account)

## Related Concepts

- [[Shared Infrastructure Hub Pattern]] — Hub-and-spoke architecture
- [[AWS CDK Infrastructure as Code]] — How exports defined in code
- [[Multi-Environment Deployment via Stack Suffix]] — Exports for each environment

## Gotchas

**Gotcha 1: Export Name Conflicts**
- If two stacks try to export same name, second deploy fails
- Solution: Include stack/component name in export
```python
# Good
export_name=f"MyComponent-{suffix}-HostedZoneId"

# Bad (conflicts if multiple stacks)
export_name="HostedZoneId"
```

**Gotcha 2: Circular Dependencies**
- Stack A imports from B, Stack B imports from A
- CloudFormation detects and fails
- Solution: Reorganize into clear hierarchy (A → B → C, no circles)

**Gotcha 3: Breaking Imports**
- Remove export → spoke stacks fail
- Solution: Deprecate gradually, update spokes, then remove

## Open Questions

- [Use Parameter Store exports instead of CloudFormation (more flexible)?]
- [Cross-account exports via Parameter Store?]
- [Automated dependency graph visualization?]
- [Versioned exports (v1, v2, etc.)?]

## Key Insights

**Why Hub-and-Spoke Works:**
- Clear ownership (hub team manages central resources)
- Loose coupling (spokes only depend on exports, not implementation)
- Easy to scale (add new spokes without hub changes)
- Natural for shared infrastructure

**When to Use:**
- Shared central resources (DNS, KMS, networking)
- Multiple application stacks
- Single AWS account
- Clear hub ownership

**When NOT to Use:**
- Simple single-stack application
- Cross-account resources (use Parameter Store)
- Highly coupled interdependencies (monolith better)

## Your Implementation

**Hub Stack:** [[my-shared-infra]]
- Exports: `HostedZoneId`, `HostedZoneName`, `KmsKeyId`

**Spoke Stacks:**
- [[chadbarteldotcom]] — Imports HostedZoneId
- [[thatsmidnightdotcom]] — Imports HostedZoneId
- [[My-DDNS-Updater]] — Imports HostedZoneId, exports SSM parameter
- [[Cartographers-Cloud-Kit]] — Imports My-DDNS-Updater SSM export

## Key Files

- [[my-shared-infra]] — [cdk/stacks.py](cdk/stacks.py) exports definition
- [[chadbarteldotcom]] — [cdk/stacks.py](cdk/stacks.py) imports from my-shared-infra
- [[Cartographers-Cloud-Kit]] — Authorizer imports SSM parameter

## Sources

- AWS CloudFormation cross-stack references documentation
- AWS CDK cross-stack sharing documentation
- Your project repositories (my-shared-infra, chadbarteldotcom, My-DDNS-Updater, Cartographers-Cloud-Kit)
