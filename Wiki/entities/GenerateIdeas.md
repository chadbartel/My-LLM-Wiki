---
type: entity
date_created: 2026-08-07
date_updated: 2026-08-07
tags:
  - wiki/entity
  - project/ai-llm
  - status/active
  - tech/gemini
  - philosophy/cloud-api
source_count: 1
---

# GenerateIdeas

Lightweight Gemini API-powered CLI tool that generates programming project ideas based on user-selected keywords. Interactive keyword selection with template-based prompting.

## Purpose

Quick brainstorming tool for developers. When stuck on what to build, select keywords to guide Gemini into generating relevant project ideas.

## Core Philosophy

**Cloud-First Simplicity:**
- Leverage cloud LLM (Google Gemini) instead of running inference locally
- No model downloads, no VRAM requirements
- Minimal code, maximum utility
- Single-file, single-class implementation

**Contrast with brAIniac:**
- brAIniac: Local, uncensored, privacy-focused, complex
- GenerateIdeas: Cloud API, simple, disposable, fast iteration

## Key Features

- **Interactive Keyword Selection** — 4 categories (prefix, adjective, domain, purpose) with 4-6 options each
- **Template-Based Prompting** — Consistent prompt structure for reproducible outputs
- **Gemini 1.0 Pro** — Latest Google Gemini model for high-quality ideas
- **Configurable Parameters** — Temperature, top_p, top_k, max_tokens tuning
- **Loop-Based Workflow** — Generate ideas, then generate more (or exit)
- **Environment-Based Auth** — Store API key in `.env` (not in code)

## Tech Stack

- **Language:** Python 3.12
- **Package Manager:** Poetry (single `pyproject.toml`)
- **LLM API:** Google Generative AI (`google-generativeai` library)
- **Model:** `models/gemini-1.0-pro-latest`
- **CLI:** Native Python `input()` and `print()` (no fancy framework)
- **Auth:** python-dotenv for `.env` file management
- **Dependencies:** Minimal (just Google API library)

## Architecture

**Simple Design:**
```
main.py
├── imports (google.generativeai, dotenv)
├── ProjectIdeaGenerator class
│   ├── __init__() — Connect to Gemini
│   ├── get_keyword_input() — Interactive selection
│   ├── generate_idea() — Call Gemini API
│   └── run() — Main loop
└── main() function — Entry point
```

**Data Flow:**
```
User Launches CLI
    ↓
main() starts loop
    ↓
get_keyword_input() collects selections
    ↓ (4 keywords collected)
Construct prompt template
    ↓
Call Gemini API
    ↓
Display response
    ↓
Ask "Generate another?" → Yes/No
```

## Keyword Categories

**1. Prefix** — Project name prefix
- `web`, `cli`, `mobile`, `game`, `backend`, `ai`

**2. Adjective** — Project quality or style
- `real-time`, `collaborative`, `privacy-focused`, `minimal`, `scalable`, `fun`

**3. Domain** — Problem area
- `productivity`, `security`, `gaming`, `devops`, `research`, `education`

**4. Purpose** — What it accomplishes
- `automates`, `predicts`, `visualizes`, `connects`, `optimizes`, `learns`

**Example Keywords:** `web`, `real-time`, `gaming`, `connects`
**Generated Prompt:** "Generate a real-time web gaming project that connects players..."

## Deployment Model

- **Execution:** Standalone Python script
- **Dependencies:** Just Poetry + Google API
- **Authentication:** `GOOGLE_API_KEY` in `.env`
- **Runtime:** Seconds per idea (depends on Gemini response time)
- **Cost:** Google Generative AI free tier limits; per-token after

## Relationships

**Opposite of [[brAIniac]]:**
- brAIniac: Local, offline, uncensored, complex
- GenerateIdeas: Cloud, online, filtered, simple

**Could Integrate With:**
- [[brAIniac]] — GenerateIdeas ideas as FastMCP tool input
- [[TTRPG Ecosystem]] — Generate adventure/campaign ideas using same template

**Similar to:**
- [[my-cache-augmented-generation]] — Both use cloud APIs (Gemini, no local inference)
- CLI tools in general — Lightweight, single-purpose

## Key Insights for Context-Switching

**When to use:**
- You're stuck on what to build
- Need quick idea brainstorming (seconds, not minutes)
- Don't want to run local inference
- Exploring programming domains outside your expertise
- Priming creative thinking

**Quick facts:**
- **Speed:** ~5-30 seconds per idea (depends on Gemini)
- **Cost:** Free tier available; per-token after
- **Privacy:** Sends keywords to Google (no private info)
- **Reliability:** Depends on Google API availability
- **Quality:** Gemini 1.0 Pro is high-quality (good ideas)

## Getting Started

```bash
# Setup
cd GenerateIdeas
poetry install

# Create .env file
echo "GOOGLE_API_KEY=your_api_key_here" > .env

# Run
poetry run python main.py

# Follow prompts to select keywords and generate ideas
```

## Example Session

```
Select prefix (web/cli/mobile/game/backend/ai): web
Select adjective (real-time/collaborative/privacy-focused/minimal/scalable/fun): collaborative
Select domain (productivity/security/gaming/devops/research/education): research
Select purpose (automates/predicts/visualizes/connects/optimizes/learns): connects

Generating idea...

"A collaborative web research platform that connects researchers
across institutions, enabling real-time document annotation,
citation sharing, and peer review workflows. Features:
- Multi-user document editor
- Real-time commenting
- Research graph visualization
- Automated citation formatting"

Generate another? (y/n): y
```

## Design Patterns

**Template-Based Prompting:**
```python
prompt = f"""Generate a programming project idea that:
- Is a {adjective} {prefix} application
- Solves problems in {domain}
- {purpose} users' workflows
- Is novel and interesting

Be specific about features and technology choices."""
```

**Configuration via Environment:**
```python
# Separate secrets from code
api_key = os.getenv("GOOGLE_API_KEY")
model = GenerativeModel("models/gemini-1.0-pro-latest")
```

## Limitations

- **Generic Ideas** — Templates can be repetitive; variety depends on keywords
- **No Persistence** — Ideas aren't saved; run multiple times to collect
- **Cost at Scale** — Free tier limited; per-token billing after
- **Internet Dependent** — Requires Google API access
- **Simple Prompting** — Doesn't have context from previous ideas (no memory)

## Enhancement Ideas

- Save ideas to file (JSON, CSV, markdown)
- Add conversation history (remember earlier ideas, build on them)
- Multi-language support (generate ideas in different languages)
- Rate ideas (save favorites, filter by rating)
- Integration with project scaffolding (auto-create project structure)

## Open Questions

- [Should ideas be saved to persistent storage?]
- [Add memory/conversation history for better ideas?]
- [Integration with [[brAIniac]] as FastMCP tool?]
- [Gemini Pro vs. Flash trade-off (cost vs. quality)?]

## Related Concepts

- [[Cloud vs. On-Device LLM Strategy]] — Why GenerateIdeas chose cloud
- [[AI/LLM Ecosystem]] — Role in your AI projects
- [[Minimal CLI Tools]] — Design philosophy

## Tech Patterns Used

- **Template-Based Prompting:** Reproducible prompt structure
- **Interactive CLI:** User-friendly keyword selection
- **Environment-Based Config:** Secrets not in code
- **Stateless Design:** Each run is independent
- **Minimal Dependencies:** Only what's necessary

## Cost Analysis

**Free Tier (Google Generative AI):**
- 60 requests/minute limit
- Good for daily brainstorming
- Perfect for this use case

**Paid Tier:**
- Gemini 1.0: ~$0.075 / 1M input tokens, ~$0.30 / 1M output tokens
- Typical idea: ~100-200 input tokens, ~200-300 output tokens
- Cost per idea: ~$0.00005-0.0001
- Monthly budget for 1000 ideas: ~$0.05-0.10

## Sources

- Wiki source: Project repository scan on 2026-08-07
- README analysis from `/mnt/c/Users/Chaddle/PycharmProjects/GenerateIdeas`
- pyproject.toml dependency analysis
- Architecture extracted from `main.py` (single-file implementation)
