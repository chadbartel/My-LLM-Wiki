---
type: concept
date_created: 2026-08-07
date_updated: 2026-08-07
tags:
  - wiki/concept
  - strategy
  - cost-optimization
  - architecture
confidence: high
source_count: 3
---

# Cloud vs. On-Device LLM Strategy

Strategic comparison of where LLM inference happens: on your hardware (local) vs. external cloud services. Different projects choose different strategies based on their constraints and goals.

## Definition

**Where LLM inference runs:**
- **On-Device:** Your GPU/CPU runs the model locally
- **Cloud (API):** You send query to external service; they run the model

**Your projects demonstrate both:**
- [[brAIniac]] — On-device (Ollama on RTX 2070 SUPER)
- [[GenerateIdeas]] — Cloud API (Google Gemini)
- [[my-cache-augmented-generation]] — Research (flexible, experiments with both)

## The Core Trade-Off

```
ON-DEVICE
├─ More Private
├─ Fully Offline
├─ Lower Ongoing Cost
├─ Full Control
└─ Lower Capability + Higher Latency

vs.

CLOUD API
├─ Frontier Capability
├─ Lower Setup Effort
├─ Higher Cost (per-token billing)
├─ Vendor Lock-in
└─ No Infrastructure Burden
```

## Head-to-Head Comparison

### Privacy & Security

**On-Device (brAIniac):**
- ✅ Query never leaves your computer
- ✅ No logs on external servers
- ✅ No tracking or analytics
- ✅ GDPR/HIPAA compliant (you're not sending data out)
- ✅ Total confidentiality guarantee
- Use case: Healthcare, legal, financial records

**Cloud API (GenerateIdeas + Gemini):**
- ❌ Query sent to Google/OpenAI/etc.
- ❌ Stored in logs (retention varies by provider)
- ❌ May be used to improve models
- ⚠️ GDPR-compliant (user consent, deletion possible)
- ⚠️ Confidentiality depends on provider policy
- Use case: Non-sensitive brainstorming

### Cost Structure

**On-Device (brAIniac):**
```
Initial hardware investment:
- RTX 2070 SUPER: ~$400 (amortized over 5 years)
- Electricity: ~$0.10/hour (during use)

Monthly cost for 8 hours/day usage:
- Hardware: $6.67 (400 ÷ 60 months)
- Electricity: $24 (240 hours × $0.10)
Total: ~$30/month

For 1000 queries/day for a year:
Cost per query: $0.08 (way lower than cloud)
```

**Cloud API (GenerateIdeas + Gemini):**
```
Free tier:
- 60 requests/minute
- Perfect for casual use
- Monthly cost: $0

Paid tier (Gemini 1.0):
- Input: $0.075 / 1M tokens
- Output: $0.30 / 1M tokens

Example: 100 queries/day, 300 input + 200 output tokens avg:
- Monthly tokens: 100 × 30 days × 500 = 1.5M tokens
- Input cost: 0.3M × $0.075 = $22.50
- Output cost: 1.2M × $0.30 = $360
Total: ~$382/month

For 1000 queries/day:
Cost per query: $3.82 (way higher than local)
```

**CAG (Research, Varies):**
```
If using cloud LLM + embeddings:
- Sentence-Transformers: free (local)
- ChromaDB: free (local)
- Cloud LLM calls: depends on usage
- Estimated: $10-50/month (research use)
```

### Break-Even Analysis

**When does on-device become cheaper?**

```
On-Device Total Cost = Hardware (amortized) + Electricity
Cloud Total Cost = Per-token billing × queries

Break-even: ~500 queries/day (for Gemini 1.0)

Below 500/day → Cloud is cheaper
Above 500/day → On-device is cheaper
```

Your usage: Varies by project
- TTRPG lookups: ~10-50/day (use cloud)
- brAIniac conversation: ~100-1000/day (on-device cheaper)
- GenerateIdeas brainstorming: ~5-20/day (cloud perfect)

### Speed & Latency

**On-Device (brAIniac):**
- Time to first token: ~500ms (GPU inference startup)
- Per-token generation: 150-300ms (8B model)
- 10-token response: ~2 seconds
- Network latency: 0ms (local)
- Example: Conversation feels interactive

**Cloud API (GenerateIdeas + Gemini):**
- Time to first token: ~1-2s (network + processing)
- Per-token generation: 20-50ms (Gemini server)
- 10-token response: ~1-2 seconds (faster generation)
- Network latency: 500ms-1s round-trip
- Example: Quick, but not as interactive as local

**Real-World Feel:**
- Local: Typing feels like talking to a program
- Cloud: More like waiting for a web request

### Model Capability

**On-Device Constraints:**
- Best available: 70B Llama 3.1 (with aggressive quantization, needs 28GB VRAM)
- brAIniac limit: 8GB VRAM → 8B model (llama3.1:8b)
- Quality: ~75-80% of GPT-4 for most tasks
- Trade-off: Speed vs. capability

**Cloud Frontier Models:**
- Gemini 2.0 (state-of-the-art)
- Claude 3.5 Sonnet (excellent reasoning)
- GPT-4 Turbo (broad capability)
- Quality: 95-100% capability
- Trade-off: Slower, more expensive, less control

**Capability Comparison (for TTRPG use case):**

| Task | 8B Local | Gemini 1.0 | Claude 3.5 |
|------|---------|-----------|-----------|
| **Rule lookup** | 95% | 99% | 99% |
| **Encounter gen** | 90% | 98% | 99% |
| **NPC backstory** | 85% | 95% | 98% |
| **Complex reasoning** | 70% | 90% | 95% |
| **Creative writing** | 88% | 92% | 96% |

8B is sufficient for 90% of TTRPG tasks!

### Offline Availability

**On-Device:**
- ✅ Works offline
- ✅ No internet required
- ✅ No ISP outages
- ✅ Perfect for travel
- ✅ Zero external dependencies
- Ideal for: ADHD offline work sessions

**Cloud API:**
- ❌ Requires internet
- ❌ Subject to ISP outages
- ❌ Subject to provider downtime
- ❌ Won't work without connectivity
- ❌ Rate limit if too many queries

### Control & Customization

**On-Device (brAIniac):**
- ✅ Modify system prompt freely
- ✅ Customize personality vectors
- ✅ Run uncensored models
- ✅ Add custom tools
- ✅ Fine-tune weights (QLoRA)
- ✅ Archive model versions
- ✅ No guardrails or filters

**Cloud API (GenerateIdeas):**
- ❌ Can't modify model weights
- ❌ Can't change system prompt (provider decides)
- ❌ Content filters applied
- ❌ Limited customization
- ❌ Provider can change behavior anytime
- ❌ No direct fine-tuning

## Decision Matrix: Which Strategy?

### Use On-Device When:

✅ Privacy critical (medical, legal, financial data)
✅ High query volume (>500/day)
✅ Need offline capability
✅ Want full customization
✅ Building ADHD assistant (instant access)
✅ Exploring uncensored models
✅ Long-term cost matters
✅ Running in restricted networks

**Your on-device project:** [[brAIniac]]

### Use Cloud API When:

✅ Need frontier capability (GPT-4, Claude)
✅ Low query volume (<100/day)
✅ Quick time-to-market
✅ No infrastructure burden desired
✅ One-off brainstorming task
✅ Privacy not critical
✅ Can accept vendor lock-in
✅ Want minimal setup

**Your cloud projects:** [[GenerateIdeas]], TTRPG RAG systems (Gemini)

### Use Research/Hybrid When:

✅ Exploring novel architectures
✅ Benchmarking approaches
✅ Need both local + cloud comparison
✅ Publishing results
✅ Tuning for specific use case

**Your research project:** [[my-cache-augmented-generation]]

## Your Ecosystem Strategy

### Tier 1: Conversational (Local - brAIniac)
```
Why local?
- High query volume expected
- Privacy for personal assistant
- Always-on offline capability
- Customization for ADHD persona
- Long-term cost efficiency
```

### Tier 2: Brainstorming (Cloud - GenerateIdeas)
```
Why cloud?
- Low volume (brainstorming ≠ constant use)
- One-off, stateless task
- Free tier sufficient
- No infrastructure burden
- Quick iteration
```

### Tier 3: Knowledge (Flexible - CAG + TTRPG RAG)
```
Why flexible?
- For TTRPG: Both local (fast) + cloud (better) options
- For CAG: Research lab (both approaches)
- Easy to swap providers
- Benchmark and compare
```

## Migration Path (Optional)

**Phase 1 (Current):**
- brAIniac: Local only
- GenerateIdeas: Cloud only
- CAG: Research only

**Phase 2 (Planned):**
- brAIniac + GenerateIdeas integration (local calls cloud as tool)
- CAG Phase 2: Compare results with RAG systems

**Phase 3 (Optional):**
- Hybrid routing: Send to local if privacy-sensitive, cloud otherwise
- Cost-based routing: Send to local if high volume, cloud if occasional

## Cost Optimization Tips

### For On-Device:
- Use 4-bit quantization (saves VRAM, minimal quality loss)
- Batch requests when possible
- Cache embeddings (don't re-encode same texts)
- Use rolling context (don't accumulate infinite history)
- Monitor power consumption during peak usage

### For Cloud:
- Use free tier aggressively (Gemini, Claude, etc.)
- Batch API calls (reduce overhead)
- Choose model by need (Haiku cheaper than Opus)
- Cache results when possible
- Monitor usage to stay under limits

### For Hybrid:
- Route high-priority queries to cloud (frontier capability)
- Route low-priority queries to local (cost savings)
- Use local for privacy, cloud for capability
- Example: brAIniac handles most, calls Gemini when stuck

## Long-Term Trends

**On-Device:**
- More efficient models (distillation, quantization)
- Larger context windows (cheaper memory)
- Better VRAM optimization tools
- Growing market for consumer AI

**Cloud API:**
- Cheaper per-token (competition increases)
- Multimodal (images, audio, video)
- Specialized models for domains
- Enterprise features

**Prediction:** Hybrid will win. Use both strategically.

## Related Concepts

- [[Local-First AI Architecture]] — Deep dive on on-device
- [[AI/LLM Ecosystem]] — Your three projects
- [[brAIniac]] — On-device implementation
- [[GenerateIdeas]] — Cloud implementation
- [[my-cache-augmented-generation]] — Research comparison

## Open Questions

- [When should brAIniac call GenerateIdeas as tool?]
- [Should CAG benchmark both local + cloud approaches?]
- [Phase 2: Hybrid routing strategy for brAIniac?]
- [Cost-benefit of multi-GPU setup for larger local models?]

## Cost Calculators

**For your usage patterns:**

```
brAIniac (conversational, daily):
- Estimated queries: 200/day
- Cost: $30/month (hardware + electricity)
- Breaks even vs. cloud at $0.05/query

GenerateIdeas (brainstorming, occasional):
- Estimated queries: 10/day
- Cost: $0/month (free tier)
- Breaks even vs. local never (low volume)

TTRPG lookups (mixed):
- Using Gemini for RAG: $5-10/month
- Could use brAIniac tool: $0.05/month
- Recommendation: Use local when available, Gemini for corner cases
```

## Sources

- [[Wiki/entities/brAIniac]] — Local implementation
- [[Wiki/entities/GenerateIdeas]] — Cloud implementation
- Ollama documentation + cost analysis
- Google Gemini pricing
- OpenAI pricing documentation
