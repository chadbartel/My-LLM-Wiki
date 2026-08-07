---
type: entity
date_created: 2026-08-07
date_updated: 2026-08-07
tags:
  - wiki/entity
  - wiki/utilities
source_count: 1
---

# MidnightsGitHubActions

Central repository for reusable GitHub Actions CI/CD workflows and automation templates. Store, version, and share custom actions across your project portfolio.

## Purpose

**MidnightsGitHubActions** is your CI/CD workflow library. Instead of duplicating test/lint/build configurations across all your projects, you define them once here and reference them as reusable actions.

**Value Proposition:**
- **Single Source of Truth** — Define CI/CD logic once, use everywhere
- **Semantic Versioning** — Release stable versions (`@v1`, `@v2`)
- **Consistency** — All projects follow identical linting, testing, formatting standards
- **Maintainability** — Update workflow once; all projects inherit the fix
- **Discoverability** — Centralized documentation of all available workflows

## Architecture

### GitHub Actions Reusability Model

GitHub Actions support **workflow reuse**. You can define a workflow in one repo and reference it from another:

**In MidnightsGitHubActions (this repo):**
```yaml
# .github/workflows/python-test.yml
name: Python Test & Lint

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.12'
      - run: pip install poetry
      - run: poetry install
      - run: poetry run pytest tests/
      - run: poetry run black --check .
      - run: poetry run isort --check-only .
      - run: poetry run flake8 .
      - run: poetry run mypy .
```

**In Your Other Projects (e.g., Cellophane):**
```yaml
# .github/workflows/ci.yml
name: CI

on: [push, pull_request]

jobs:
  build:
    uses: thatsmidnight/MidnightsGitHubActions/.github/workflows/python-test.yml@v1
```

This is **workflow composition**—reference external workflows instead of duplicating them.

## Planned Workflow Suite

```
MidnightsGitHubActions/
├── .github/workflows/
│   ├── python-test.yml           # pytest, black, isort, flake8, mypy
│   ├── python-build.yml          # poetry build, package creation
│   ├── python-lint.yml           # Linting only (separate from test)
│   ├── python-format.yml         # Code formatting (black, isort)
│   ├── docker-build.yml          # Docker image build & registry push
│   ├── auto-release.yml          # Semantic versioning + GitHub releases
│   ├── security-scan.yml         # SAST, dependency scanning
│   └── documentation.yml         # Build & publish docs
├── README.md                      # Usage guide and workflow catalog
└── LICENSE
```

## Technology Stack

- **Platform:** GitHub Actions
- **Configuration:** YAML workflows
- **Integrations:** Python (poetry, pytest, black, flake8, mypy)
- **Future Integrations:** Docker, security scanners, release automation

## Workflow Categories

### 1. Python Testing & Linting

**python-test.yml**
- Install dependencies with Poetry
- Run pytest (unit + integration tests)
- Black code formatting check
- isort import sorting check
- flake8 linting
- mypy type checking
- Publish coverage reports

**Usage:**
```yaml
jobs:
  build:
    uses: thatsmidnight/MidnightsGitHubActions/.github/workflows/python-test.yml@v1
```

### 2. Build & Release

**python-build.yml**
- Build Python package with Poetry
- Create wheel and sdist distributions
- Optional: Push to PyPI

**auto-release.yml**
- Semantic versioning from commit messages
- Create GitHub release tag
- Generate changelog from commit log

### 3. Docker Integration

**docker-build.yml**
- Build Docker image
- Push to Docker Hub or GitHub Container Registry
- Tag with version and latest

### 4. Security

**security-scan.yml**
- Dependency vulnerability scanning (Snyk, Dependabot)
- Static application security testing (SAST)
- Secret scanning

### 5. Documentation

**documentation.yml**
- Build docs (Sphinx, MkDocs, etc.)
- Deploy to GitHub Pages or ReadTheDocs
- Publish API documentation

## Current Status

- **Status:** Experimental/Early-Stage
- **Completeness:** Template repository created; core workflows not yet implemented
- **Maturity:** Roadmap defined; implementation pending
- **Dependencies:** None (GitHub Actions built-in)
- **Discoverability:** README needs workflow catalog with usage examples

## Project Structure

```
MidnightsGitHubActions/
├── .github/
│   └── workflows/
│       ├── README.md                    # Workflow documentation
│       └── [workflow-name].yml         # Individual workflow definitions
├── docs/
│   ├── python-workflows.md             # Python CI/CD guide
│   ├── docker-workflows.md             # Docker build guide
│   └── composing-workflows.md          # How to use these in your projects
├── README.md                           # Project overview
└── LICENSE
```

## Usage Pattern

### Step 1: Reference in Your Project

In any of your projects (e.g., Cellophane, Arcane-Scribe), create `.github/workflows/ci.yml`:

```yaml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    uses: thatsmidnight/MidnightsGitHubActions/.github/workflows/python-test.yml@v1
    with:
      python-version: '3.12'
```

### Step 2: GitHub Actions Runs Workflow

GitHub automatically fetches the workflow from MidnightsGitHubActions and executes it in your project's context.

### Step 3: Results

Pull requests show test/lint results. Failures block merges. Passes enable auto-deployment.

## Relationships

**Used By (Planned):**
- [[Wiki/entities/Cellophane]] — Test suite on all commits
- [[Wiki/entities/Arcane-Scribe]] — AWS Lambda deployment automation
- [[Wiki/entities/Automated-Taskmaster]] — CDK synthesis + deployment
- [[Wiki/entities/my-cache-augmented-generation]] — RAG pipeline testing
- [[Wiki/entities/brAIniac]] — FastMCP server testing
- [[Wiki/entities/Cartographers-Cloud-Kit]] — CDK + FastAPI testing
- All other Python projects in your workspace

**Related Concepts:**
- [[Wiki/concepts/GitHub Actions CI/CD Automation]] — Workflow composition pattern
- [[Wiki/concepts/Reusable Utility Libraries]] — Central workflows as reusable tools

## Benefits

### For You (Project Owner)

1. **Consistency** — All projects follow same code quality standards
2. **Maintenance** — Update linting rules once; applies everywhere
3. **Speed** — No need to write CI/CD for new projects
4. **Versioning** — Use @v1, @v2 to control when projects adopt changes

### For Collaborators

1. **Clarity** — Everyone knows exactly how code is tested
2. **Reproducibility** — Same CI/CD locally and in GitHub
3. **Trust** — Security and linting checks run automatically

### For Automation

1. **Auto-Release** — Semantic versioning from commits
2. **Auto-Deploy** — Trigger deployments on version tags
3. **Auto-Update** — Dependabot keeps dependencies current

## Implementation Roadmap

### Phase 1: Foundation (Now)
- [ ] Setup repository structure
- [ ] Document workflow patterns
- [ ] Create python-test.yml template

### Phase 2: Python Suite (Next)
- [ ] python-test.yml (pytest, linting, type-checking)
- [ ] python-build.yml (Poetry packaging)
- [ ] python-format.yml (Auto-formatting with Black/isort)

### Phase 3: DevOps Suite (Later)
- [ ] docker-build.yml (Docker image CI/CD)
- [ ] auto-release.yml (Semantic versioning)
- [ ] security-scan.yml (Dependency + SAST scanning)

### Phase 4: Integrations (Future)
- [ ] AWS CDK deployment workflows
- [ ] Terraform validation workflows
- [ ] Documentation generation
- [ ] Slack/Discord notifications

## Cost Model

**Zero cost.** GitHub Actions includes 2,000 free runner minutes per month for public repos.

**For Private Repos:** 3,000 free minutes per month; overage is $0.008/minute.

Most of your projects will stay under this limit.

## Learning Outcomes

Study this project to learn:
- **GitHub Actions** — Workflow syntax, triggers, secrets, artifacts
- **CI/CD Concepts** — Automated testing, linting, deployment
- **Workflow Composition** — Reusing actions and workflows
- **YAML Configuration** — Declarative workflow definitions
- **Version Management** — Semantic versioning and releases
- **Automation Best Practices** — What to automate, when, and how

## Next Steps

1. Create repository structure (`.github/workflows/`)
2. Document first workflow (python-test.yml)
3. Implement Python testing workflow
4. Test in one of your projects (Cellophane)
5. Roll out to other projects
6. Build Docker and release workflows
7. Implement security scanning
8. Create comprehensive documentation

---

**Note:** This is a force-multiplier. Once set up, it saves time and ensures quality across all your projects. Start with Python workflows; expand as you add more project types.
