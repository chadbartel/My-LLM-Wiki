---
type: concept
date_created: 2026-08-07
date_updated: 2026-08-07
tags:
  - wiki/concept
  - infrastructure/aws
  - pattern/deployment
  - tech/s3
  - tech/cloudfront
  - tech/route53
source_count: 2
confidence: high
---

# Static Site Deployment Pattern

Hosting static websites on AWS using the combination of S3 (storage), CloudFront (CDN), ACM (HTTPS), and Route 53 (DNS). Enterprise-grade pattern suitable for blogs, personal sites, and documentation.

## Definition

**Static Site Pattern:** Website served entirely from S3 buckets with CloudFront edge caching for global distribution and HTTPS via ACM certificates.

**Architecture:**
```
User Request → Route 53 DNS → CloudFront Global Network → S3 Origin → User
```

## Why It Matters

**Alternatives (and their tradeoffs):**

| Approach | Cost | Scalability | Complexity |
|----------|------|-------------|-----------|
| Self-hosted (VPS) | $5-20/month | Limited (can hit CPU/RAM) | Medium (manage server) |
| Traditional web host | $5-15/month | Limited | Low (managed) |
| S3 Only (no CloudFront) | $0.023/GB | Good | Low (but slower) |
| S3 + CloudFront (this pattern) | $0.50-2/month | Excellent | Low (managed services) |
| Heroku/Vercel | $7-50/month | Good | Medium (platform features) |

**Static Site Pattern Advantages:**
- Ultra-low cost (~$1-2/month for personal site)
- Globally distributed (CloudFront edge nodes worldwide)
- Zero maintenance (AWS manages infrastructure)
- High security (no server code, immutable content)
- Scales infinitely (AWS handles load)

## Your Projects Using This Pattern

**[[chadbarteldotcom]]** (primary implementation)
- S3 bucket stores HTML/CSS/JavaScript
- CloudFront distribution caches globally
- ACM certificate for HTTPS
- Route 53 records for chadbartel.com and www.chadbartel.com

**[[thatsmidnightdotcom]]** (pattern reuse)
- Identical architecture for different domain
- Demonstrates construct reusability

## Architecture Components

**S3 Bucket (Origin):**
- Stores website files (HTML, CSS, JavaScript, images)
- Private (not publicly accessible)
- Versioned for safe updates
- Encrypted at rest (default)

**CloudFront Distribution:**
- Global content delivery network
- Caches content at 200+ edge locations worldwide
- HTTPS termination
- DDoS protection (embedded AWS Shield)
- Origin Access Control (OAC) authentication

**ACM Certificate:**
- HTTPS/TLS certificate (free)
- Auto-renews
- Covers multiple domains (wildcard or SAN)
- DNS validation (automatic via Route 53)

**Route 53 DNS:**
- DNS records for domain
- Alias records point to CloudFront distribution
- Health checks (optional)

## How It Works

**Request Flow:**

```
1. User: https://chadbartel.com
2. Browser DNS lookup: Route 53 returns CloudFront domain
3. Browser connects to CloudFront (nearest edge location)
4. CloudFront checks if content cached
   - Hit: Return cached content (fast)
   - Miss: Fetch from S3, cache, return
5. S3 returns object (authenticated via OAC)
6. CloudFront caches and returns to user
```

**Caching Behavior:**

```
Content-Type        Cache-Control                  TTL
-----------         -----------                    ---
HTML               Cache-Control: max-age=3600     1 hour (refresh often)
CSS/JS             Cache-Control: max-age=31536000 1 year (immutable)
Images             Cache-Control: max-age=86400    1 day
```

## Origin Access Control (OAC)

**Why Private S3 Bucket:**

```
Option 1: Public S3 Bucket
- Users can access S3 directly (bypassing CloudFront)
- No caching benefit
- Harder to control access
- More expensive (S3 egress charges)

Option 2: Private S3 + CloudFront (this pattern)
- CloudFront only way to reach S3
- All requests cached at edge
- Consistent authentication
- Cheaper (CloudFront cheaper than S3 egress)
```

**OAC Mechanism:**

```python
# In CDK
oac = cloudfront.OriginAccessControl(self, "OAC")

distribution = cloudfront.Distribution(self, "Distribution",
    default_behavior=cloudfront.BehaviorOptions(
        origin=cloudfront.S3Origin(bucket, origin_access_control=oac),
        viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
    ),
)

# CloudFront signs requests with AWS Signature V4
# S3 bucket policy validates signature
```

**S3 Bucket Policy (Generated automatically):**

```json
{
  "Effect": "Allow",
  "Principal": {
    "Service": "cloudfront.amazonaws.com"
  },
  "Action": "s3:GetObject",
  "Resource": "arn:aws:s3:::my-bucket/*",
  "Condition": {
    "StringEquals": {
      "aws:SourceArn": "arn:aws:cloudfront::123456789012:distribution/E1234567890ABC"
    }
  }
}
```

## Cost Model

**Monthly Estimate (Typical Static Site):**

| Service | Usage | Cost |
|---------|-------|------|
| S3 Storage | 100MB site | $0.002 |
| S3 Requests | 100K/month | $0.0005 |
| CloudFront Data Transfer | 10GB out | $0.85* |
| CloudFront Requests | 10K/month | $0.075 |
| Route 53 Hosted Zone | 1 zone | $0.50 |
| ACM Certificate | 1 cert | FREE |
| **Total** | | **~$1.43/month** |

\* CloudFront pricing varies by region ($0.085-$0.170/GB)

**Cost Optimization Tips:**
1. **Compression:** CloudFront gzip (reduces transfer 60-70%)
2. **Caching Headers:** Set long TTL (avoids cache misses)
3. **Image Optimization:** Resize images, use WebP format
4. **Lazy Loading:** Load images on-demand (JS)

## HTTPS/TLS Setup

**Certificate Validation (Automatic):**

```python
cert = acm.Certificate(self, "Certificate",
    domain_name="chadbartel.com",
    validation=acm.CertificateValidation.from_dns(hosted_zone)
)
```

**Route 53 Auto-Validates:**
1. ACM creates CNAME record in Route 53
2. Validates CNAME exists
3. Certificate issued
4. Route 53 records automatically managed
5. Certificate auto-renews every year

**No Manual Work Required** ✅

## Route 53 DNS Records

**Alias Records (CloudFront):**

```python
route53.ARecord(self, "WebsiteAlias",
    zone=hosted_zone,
    target=route53.RecordTarget.from_alias(
        cloudfront.CloudFrontTarget(distribution)
    )
)
```

**Creates in Route 53:**
```
Name: chadbartel.com
Type: A (IPv4)
Alias: d1234567890abc.cloudfront.net
```

**Subdomain (www):**
```python
route53.ARecord(self, "WebsiteAliasWww",
    zone=hosted_zone,
    record_name="www",
    target=route53.RecordTarget.from_alias(
        cloudfront.CloudFrontTarget(distribution)
    )
)
```

## Content Deployment

**Upload Files to S3:**

```bash
# Sync local files to S3
aws s3 sync ./public s3://my-bucket --delete

# Or using CDK asset
s3_deploy.BucketDeployment(self, "DeployWebsite",
    sources=[s3_deploy.Source.asset("./public")],
    destination_bucket=bucket
)
```

**Cache Invalidation (if needed):**

```bash
# Invalidate entire CloudFront cache
aws cloudfront create-invalidation \
  --distribution-id E1234567890ABC \
  --paths "/*"

# Cost: $0.005 per invalidation
```

## Security Considerations

**Built-In Protections:**
- SSL/TLS encryption (HTTPS only)
- DDoS protection (AWS Shield Standard)
- Origin is private (no direct S3 access)
- IAM policies restrict access

**Optional Enhancements:**
- AWS WAF (Web Application Firewall)
- CloudFront geo-restriction (block by country)
- S3 bucket versioning (rollback safety)
- Custom headers (security headers)

## Related Concepts

- [[AWS CDK Infrastructure as Code]] — How to define pattern
- [[Shared Infrastructure Hub Pattern]] — Uses [[my-shared-infra]] for DNS
- [[Cross-Stack Resource Sharing]] — Imports Route 53 hosted zone

## Open Questions

- [Add custom error pages (404, 403)?]
- [Implement CDN cache invalidation strategy?]
- [Add analytics (CloudFront access logs)?]
- [Set up staging/preview deployment?]

## Key Insights

**Why This Pattern Works:**
- S3 is dirt cheap for storage
- CloudFront handles all the hard parts (caching, HTTPS, DDoS)
- No servers to manage (fully managed AWS services)
- Scales infinitely (no code to break under load)
- Perfect for static content (HTML, CSS, JS, images)

**When to Use:**
- Marketing websites
- Personal blogs
- Documentation sites
- Project landing pages
- Content delivery where updates are infrequent

**When NOT to Use:**
- Dynamic content (requires backend)
- User logins (serverless functions needed)
- Real-time updates
- Database-backed sites (use Lambda + RDS)

## Performance Optimization

**Cache Behavior (by file type):**

```python
# HTML: Short TTL (get updates quickly)
distribution.add_behavior(
    path_pattern="*.html",
    origin=s3_origin,
    viewer_protocol_policy=ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
    cache_policy=CachePolicy.CACHING_OPTIMIZED,  # 1-day TTL
)

# CSS/JS: Long TTL (immutable assets)
distribution.add_behavior(
    path_pattern=["*.css", "*.js"],
    origin=s3_origin,
    cache_policy=CachePolicy.CACHING_OPTIMIZED,  # 1-year TTL
)

# Images: Medium TTL
distribution.add_behavior(
    path_pattern=["*.jpg", "*.png", "*.webp"],
    origin=s3_origin,
    cache_policy=CachePolicy.CACHING_OPTIMIZED,  # 30-day TTL
)
```

## Monitoring

**CloudFront Metrics:**
- Requests count (traffic)
- Data transferred (cost driver)
- Cache hit ratio (efficiency)
- Error rates (4xx, 5xx)

**Enable Logging:**

```python
distribution = cloudfront.Distribution(self, "Distribution",
    enable_logging=True,
    logging_format=cloudfront.LogFormat.default()
)
# Logs written to S3 bucket hourly
```

## Your Implementation

**[[chadbarteldotcom]]:**
- S3 bucket + CloudFront distribution
- ACM certificate (free, auto-renews)
- Route 53 DNS records
- Uses custom constructs (MyBucket, MyDistribution, MyCertificate)

**[[thatsmidnightdotcom]]:**
- Identical pattern, different domain
- Demonstrates construct reusability

## Key Files

- [[chadbarteldotcom]] — [cdk/constructs.py](cdk/constructs.py) defines MyBucket, MyDistribution
- [[chadbarteldotcom]] — [cdk/stacks.py](cdk/stacks.py) orchestrates pattern

## Sources

- AWS S3 + CloudFront documentation
- AWS CDK construct library
- Your project repositories (chadbarteldotcom, thatsmidnightdotcom)
- CloudFront best practices guide
