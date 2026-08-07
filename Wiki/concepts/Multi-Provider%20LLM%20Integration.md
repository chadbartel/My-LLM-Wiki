---
type: concept
date_created: 2026-08-07
date_updated: 2026-08-07
tags:
  - wiki/concept
  - ai
  - llm-strategy
  - cost-optimization
confidence: high
source_count: 3
---

# Multi-Provider LLM Integration

Strategy of using different LLM providers (Google Gemini vs. AWS Bedrock) for different deployment models across your TTRPG ecosystem.

## Definition

Don't lock into one LLM provider. Use Gemini for local deployments (simpler, cheaper for low volume). Use Bedrock for enterprise/serverless (AWS-native, managed). Design code to swap providers easily.

## The Two Provider Strategies in Your TTRPG Projects

### Strategy 1: Google Gemini (Local-First)
**Used By:**
- [[TTRPG-AI-RAG-Assistant]]
- [[AIO Generative AI Solution]]

**Characteristics:**
```
Model Selection:
  • Gemini 1.5 Pro (most capable, higher cost)
  • Gemini 1.0 (balanced)
  • Gemini Flash (fastest, cheapest)

Embeddings:
  • `embedding-001` (older, faster)
  • `text-embedding-004` (newer, higher quality)

Cost:
  • $0.075/million tokens (embeddings)
  • $0.075/million tokens (generation input)
  • $0.30/million tokens (generation output)
  • Free tier: 60 requests/minute
```

**Advantages:**
- Simple API (no AWS account complexity)
- Works local (just API key)
- Fast iteration
- Familiar for rapid prototyping

**Disadvantages:**
- External dependency (internet required)
- Rate limiting (60 req/min free tier)
- Privacy (queries sent to Google)
- Cost scales with usage (per-token billing)

### Strategy 2: AWS Bedrock (Enterprise)
**Used By:**
- [[Arcane-Scribe]]

**Characteristics:**
```
Model Selection:
  • Claude 3.5 Haiku (fast, cheap)
  • Claude 3.5 Sonnet (balanced)
  • Claude 3 Opus (most capable, expensive)
  • Amazon Titan (alternative, AWS-native)

Embeddings:
  • Titan Embeddings G1 (AWS-native)
  • Cohere Embed English (alternative)

Cost:
  • Haiku: $0.80/million tokens
  • Sonnet: $3.00/million tokens
  • Opus: $15.00/million tokens
  • Same pricing for embeddings
  • Minimum charge per month
```

**Advantages:**
- AWS-native (integrated with Lambda, S3, etc.)
- Batch processing discount (20% cheaper)
- Request throttling (100 requests/second, scalable)
- Private VPC option (no internet exposure)
- Provisioned throughput (predictable costs)

**Disadvantages:**
- Requires AWS account setup
- Higher initial complexity
- More expensive per-token (but higher scale)
- Still internet-dependent (AWS regions available)

## Cost Comparison for Real-World Usage

### Scenario 1: Low Usage (10 queries/day)

| Provider | Daily Queries | Tokens/Query | Daily Cost | Monthly Cost |
|----------|---------------|--------------|-----------|-------------|
| Gemini | 10 | 5,000 | $0.01 | $0.30 |
| Bedrock | 10 | 5,000 | $0.04 | $1.20 |

**Winner:** Gemini (local is free tier territory)

### Scenario 2: Medium Usage (1,000 queries/day)

| Provider | Daily Queries | Tokens/Query | Daily Cost | Monthly Cost |
|----------|---------------|--------------|-----------|-------------|
| Gemini | 1,000 | 5,000 | $0.38 | $11 |
| Bedrock (Haiku) | 1,000 | 5,000 | $0.04 | $1.20 |

**Winner:** Bedrock (scales cheaper, especially Haiku)

### Scenario 3: High Usage (100,000 queries/day)

| Provider | Daily Queries | Tokens/Query | Daily Cost | Monthly Cost |
|----------|---------------|--------------|-----------|-------------|
| Gemini | 100,000 | 5,000 | $37.50 | $1,125 |
| Bedrock (Haiku) | 100,000 | 5,000 | $4.00 | $120 |
| Bedrock (Provisioned) | 100,000 | 5,000 | $0.50 | $15 (base) |

**Winner:** Bedrock with Provisioned Throughput (10x cheaper at scale)

## Model Capability Comparison

| Capability | Gemini 1.5 Pro | Claude 3.5 Haiku | Claude 3.5 Sonnet |
|-----------|---|---|---|
| **Reasoning** | Good | Fair | Excellent |
| **TTRPG Rule Understanding** | Good | Good | Excellent |
| **Speed** | Medium | Fast | Medium |
| **Token Context Window** | 1M | 200K | 200K |
| **Cost** | Medium | Cheap | Expensive |
| **Best For** | RAG + Generation | Budget serverless | Premium accuracy |

**For TTRPG:** Haiku is surprisingly good (99% of reasoning needed for rule lookups).

## How Your Projects Choose

### [[TTRPG-AI-RAG-Assistant]] & [[AIO Generative AI Solution]] Use Gemini

**Why?**
- Running locally (Docker container)
- Low volume (1-10 users)
- Simpler setup (just API key)
- Free tier covers experiments

**Flow:**
```
Question
  ↓ (Google API)
Gemini Embedding API
  ↓ (local vector search)
Chromadb semantic match
  ↓ (Google API again)
Gemini Generation
  ↓
Answer
```

### [[Arcane-Scribe]] Uses AWS Bedrock

**Why?**
- Running serverless (Lambda)
- Potential for high volume
- AWS-native (CDK integration)
- Private/enterprise deployments
- Batch processing available
- Provisioned throughput for predictable costs

**Flow:**
```
Question (via API Gateway)
  ↓
Lambda receives request
  ↓ (AWS Bedrock API)
Bedrock Embeddings (Titan)
  ↓ (Lambda memory or FAISS)
Semantic search
  ↓ (AWS Bedrock API again)
Bedrock Generation (Haiku/Sonnet)
  ↓
Response via API Gateway
```

## Abstraction Pattern: Provider-Agnostic

**Best Practice:** Write code that doesn't assume a specific LLM provider.

**Example (NOT recommended - tightly coupled):**
```python
# Bad: Tightly coupled to Gemini
from google.generativeai import GenerativeModel

model = GenerativeModel("gemini-1.5-pro")
response = model.generate_content("Query...")
```

**Example (Recommended - abstracted):**
```python
# Good: Provider agnostic
class LLMProvider(ABC):
    @abstractmethod
    def embed(self, text: str) -> List[float]:
        pass
    
    @abstractmethod
    def generate(self, prompt: str) -> str:
        pass

class GeminiProvider(LLMProvider):
    def embed(self, text: str):
        # Gemini implementation
        pass

class BedrockProvider(LLMProvider):
    def embed(self, text: str):
        # Bedrock implementation
        pass

# Usage: Switch providers via config
provider = GeminiProvider() if LOCAL else BedrockProvider()
```

**Benefit:** Switch between Gemini and Bedrock by changing one config variable.

## Migration Path: Local → Enterprise

As your TTRPG tools grow:

```
Phase 1: Start with Gemini + Local Docker
  [[TTRPG-AI-RAG-Assistant]] ← Simple, free, local
         ↓
Phase 2: Move to Bedrock + Serverless
  [[Arcane-Scribe]] ← Scalable, managed, enterprise
         ↓
Phase 3: Hybrid
  Keep local for internal tools
  Use [[Arcane-Scribe]] for public API
  Share models via provider abstraction
```

## Practical Switching Example

**Situation:** Your Gemini [[TTRPG-AI-RAG-Assistant]] hits rate limits

**Options:**
1. Upgrade Gemini tier (pay more to Google)
2. Migrate to Bedrock (use abstraction to swap easily)
3. Hybrid (Gemini for local cache, Bedrock for public API)

**With abstraction:**
```python
# Configuration
PROVIDER = "bedrock"  # Just change this line
EMBEDDING_MODEL = "titan"
GENERATION_MODEL = "haiku"

# Code stays the same
response = provider.generate("What is fireball?")
```

## Long-term Provider Strategy

| Usage Level | Recommendation | Provider | Deployment |
|-----------|---|---|---|
| **Personal/Small Group** | Start here | Gemini | Local Docker |
| **Growing (50-500 users)** | Experiment | Bedrock | Serverless |
| **Large Scale (500+ users)** | Optimize | Both | Hybrid |

## API Design for Easy Swapping

Your services should accept provider config:

```python
# In pyproject.toml or config file
[tool.ttrpg]
llm_provider = "gemini"  # or "bedrock"
gemini_model = "gemini-1.5-pro"
bedrock_model = "claude-3-5-haiku"
bedrock_region = "us-east-1"
```

**Benefit:** Same code works with different providers.

## When to Use Each Provider

| Decision | Gemini | Bedrock |
|----------|--------|---------|
| **Prototyping** | ✓ (faster setup) | - |
| **Local Development** | ✓ | - (requires AWS) |
| **Small Deployments** | ✓ (free tier) | - |
| **Scaling to 1000s/queries/day** | - | ✓ (cheaper) |
| **Enterprise/Private** | - | ✓ (VPC option) |
| **AWS-native Stack** | - | ✓ (Lambda integration) |
| **Multi-provider Resilience** | Consider both | - |

## Future-Proofing

**Always assume LLMs will change:**
- New models released frequently
- Pricing fluctuates
- Providers add/remove models
- Regulations might affect availability

**Defend against this:**
1. Use provider abstraction
2. Version your model choices in code
3. Monitor cost monthly
4. Plan migration path (Gemini → Bedrock vice versa)

## Hybrid Approach Example

```
User in low-volume region:
  Query → Gemini (fast, cached locally)
  
User needs enterprise features:
  Query → [[Arcane-Scribe]] (Bedrock, auth, history)
  
Corporate TTRPG tool:
  Query → Private Bedrock (VPC, audit trail)
```

All three use same API (provider abstraction).

## Open Questions

- [Should [[TTRPG-AI-RAG-Assistant]] support Bedrock as fallback?]
- [Cost analysis: When does Bedrock cheaper than Gemini?]
- [Multi-model strategy (Gemini + Bedrock simultaneously)?]
- [Fine-tuned models for TTRPG domain?]

## Related Concepts

- [[RAG Pattern for TTRPG]] — LLM integration architecture
- [[Serverless TTRPG Services]] — Bedrock deployment via Lambda
- [[TTRPG Ecosystem]] — How providers affect your project choices

## Sources

- [[Wiki/entities/TTRPG-AI-RAG-Assistant]] (Gemini user)
- [[Wiki/entities/Arcane-Scribe]] (Bedrock user)
- Google Gemini API pricing and documentation
- AWS Bedrock pricing and documentation
- Cost analysis from pyproject.toml dependencies
