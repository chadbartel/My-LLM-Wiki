---
type: concept
date_created: 2026-08-07
date_updated: 2026-08-07
tags:
  - wiki/concept
source_count: 1
confidence: high
---

# GitHub Actions CI/CD Automation

Design pattern for automating software quality, testing, and deployment using GitHub Actions workflows. Enables continuous integration and continuous deployment with minimal manual overhead.

## Definition

**GitHub Actions** is GitHub's built-in automation platform. You define workflows in YAML that run on every push, pull request, or schedule. Common automations:
- **Continuous Integration (CI)** — Run tests, linting, type-checking automatically
- **Continuous Deployment (CD)** — Build and deploy on successful tests
- **Quality Gates** — Block merges if tests fail
- **Release Management** — Auto-tag versions, publish packages
- **Security Scanning** — Detect vulnerabilities automatically

**Philosophy:** Automate the tedious parts (testing, linting, building). Let humans focus on code review and decision-making.

## Why CI/CD Matters

### The Manual Way (Painful)

1. Developer writes code
2. Developer manually runs tests locally
3. Developer submits pull request
4. Reviewer manually checks out branch
5. Reviewer manually runs tests and linter
6. Reviewer manually checks for security issues
7. If everything passes, someone manually runs deployment
8. If production breaks, manual rollback

**Result:** Slow, error-prone, tedious.

### The Automated Way (Modern)

1. Developer writes code and pushes
2. GitHub Actions automatically runs tests, linting, security checks
3. Pull request shows test results (pass/fail)
4. Reviewer checks results; doesn't need to run tests locally
5. On merge, GitHub Actions automatically deploys
6. On failure, GitHub Actions automatically rolls back

**Result:** Fast, reliable, consistent.

## Core Concepts

### 1. Workflows

A workflow is a YAML file that defines automation. It lives in `.github/workflows/`:

```yaml
# .github/workflows/test.yml
name: Test & Lint

on:                          # When to run
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:                      # Job name
    runs-on: ubuntu-latest   # Runner (machine to run on)
    steps:                   # Individual steps
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.12'
      - run: pip install -r requirements.txt
      - run: pytest tests/
      - run: black --check .
```

**Anatomy:**
- **`on:`** — Trigger conditions (push, pull_request, schedule, etc.)
- **`jobs:`** — Parallel containers that run the workflow
- **`runs-on:`** — Type of machine (ubuntu, macos, windows, self-hosted)
- **`steps:`** — Sequential commands in a job
- **`uses:`** — Pre-built actions from GitHub Actions marketplace
- **`run:`** — Shell commands

### 2. Triggers

What causes a workflow to run:

```yaml
on:
  push:                        # On every push
    branches: [main]           # Only to main branch
    paths: ['src/**', 'tests/**']  # Only if these paths change
  pull_request:                # On every pull request
  schedule:
    - cron: '0 2 * * *'       # Daily at 2 AM UTC
  workflow_dispatch:           # Manual trigger
```

### 3. Actions

Reusable workflow components from the marketplace:

```yaml
steps:
  # GitHub's official checkout action
  - uses: actions/checkout@v3
  
  # GitHub's Python setup action
  - uses: actions/setup-python@v4
    with:
      python-version: '3.12'
  
  # Third-party action for coverage
  - uses: codecov/codecov-action@v3
```

Find actions at https://github.com/marketplace

### 4. Secrets

Sensitive data (API keys, tokens) accessed securely:

```yaml
steps:
  - run: pip publish
    env:
      PYPI_TOKEN: ${{ secrets.PYPI_TOKEN }}  # Access from GitHub secrets
```

Set secrets in repo settings → Secrets and variables → Actions.

### 5. Artifacts

Output files from a job available for download/inspection:

```yaml
steps:
  - run: pytest tests/ --cov=src --cov-report=html
  - uses: actions/upload-artifact@v3
    with:
      name: coverage-report
      path: htmlcov/
```

Download coverage reports from pull request details.

## Common Workflow Patterns

### Pattern 1: Test on Every Commit

```yaml
name: Test

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.10', '3.11', '3.12']  # Test all versions
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
      - run: pip install poetry
      - run: poetry install
      - run: poetry run pytest
      - run: poetry run black --check .
      - run: poetry run isort --check-only .
      - run: poetry run flake8 .
      - run: poetry run mypy .
```

**Result:** Every commit verified. Multi-version testing. No manual test runs.

### Pattern 2: Deploy on Successful Test

```yaml
name: Deploy

on:
  push:
    branches: [main]
    tags: ['v*']  # Only on version tags

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: pip install -r requirements.txt
      - run: pytest tests/      # Must pass to continue
      - run: aws s3 sync ./dist s3://my-bucket/  # Deploy if tests pass
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_KEY }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET }}
```

**Result:** Automatic deployment on every tag, only if tests pass.

### Pattern 3: Auto-Release

```yaml
name: Release

on:
  push:
    branches: [main]

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.12'
      - run: npm install -g semantic-release  # Semantic versioning
      - run: semantic-release                  # Auto-tag version
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

**Result:** Automatic version bumping and GitHub releases.

### Pattern 4: Security Scanning

```yaml
name: Security

on: [push, pull_request]

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: aquasecurity/trivy-action@master  # Vulnerability scanning
        with:
          scan-type: 'fs'
          scan-ref: '.'
```

**Result:** Automatic vulnerability detection on every commit.

## Workflow Composition

GitHub Actions allows **reusable workflows**. Define once, use everywhere:

**In MidnightsGitHubActions (central repo):**
```yaml
# .github/workflows/python-test.yml
name: Python Test

on:
  workflow_call:  # This workflow can be called by others

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
      - run: poetry run pytest
```

**In Your Projects (e.g., Cellophane):**
```yaml
# .github/workflows/ci.yml
name: CI

on: [push, pull_request]

jobs:
  test:
    uses: thatsmidnight/MidnightsGitHubActions/.github/workflows/python-test.yml@v1
```

**Benefit:** No duplicate CI config across projects. Update once; applies everywhere.

## Your CI/CD Strategy

### Phase 1: Basic Testing

All projects automatically run:
- Tests (pytest)
- Linting (black, flake8, isort)
- Type checking (mypy)

**Trigger:** Every push and pull request

**Action:** Fail the check if any step fails. Block merge.

### Phase 2: Multi-Version Testing

Test against multiple Python versions (3.10, 3.11, 3.12):

```yaml
strategy:
  matrix:
    python-version: ['3.10', '3.11', '3.12']
```

**Benefit:** Catch version-specific bugs early.

### Phase 3: Coverage Tracking

Report test coverage to PR comments:

```yaml
- uses: codecov/codecov-action@v3
  with:
    files: ./coverage.xml
```

**Benefit:** See coverage trends. Require minimum coverage.

### Phase 4: Auto-Release

Semantic versioning + auto-publish:

```yaml
- run: poetry publish
  env:
    POETRY_PYPI_TOKEN_PYPI: ${{ secrets.PYPI_TOKEN }}
```

**Benefit:** Version automatically bumped. Package auto-published.

### Phase 5: Deploy

Auto-deploy on successful release:

```yaml
- run: aws lambda update-function-code ...
  if: startsWith(github.ref, 'refs/tags/')
```

**Benefit:** Tags trigger deployments. Manual deployment eliminated.

## Real Examples from Your Projects

### [[Wiki/entities/Cellophane]] CI Workflow

```yaml
# .github/workflows/ci.yml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.10', '3.11', '3.12']
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
      - run: pip install poetry
      - run: poetry install
      - run: poetry run pytest tests/ --cov=cellophane
      - run: poetry run black --check cellophane/
      - run: poetry run isort --check-only cellophane/
      - run: poetry run flake8 cellophane/
      - run: poetry run mypy cellophane/
      - uses: codecov/codecov-action@v3
```

**On Every Commit:**
- ✓ Tests pass (Python 3.10, 3.11, 3.12)
- ✓ Code is properly formatted (Black)
- ✓ Imports sorted (isort)
- ✓ No lint warnings (flake8)
- ✓ No type errors (mypy)
- ✓ Coverage > 80%

### [[Wiki/entities/Cartographers-Cloud-Kit]] Deploy Workflow

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    tags: ['v*']

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: poetry install && poetry run pytest
  
  deploy:
    needs: test  # Deploy only if test passes
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: cdk deploy --require-approval=never
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_KEY }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET }}
```

**On Every Tag (v1.0, v1.1, etc.):**
- ✓ Tests pass
- ✓ CDK synthesizes
- ✓ Stack deploys to AWS
- ✓ No manual deployment needed

## Benefits

### For You (Developer)

1. **Confidence** — Tests run automatically. No manual step forgotten.
2. **Speed** — Push code, tests run while you work on next thing.
3. **Catch Bugs Early** — Linting catches style issues immediately.
4. **Consistent Quality** — Same standards across all projects.

### For Collaborators

1. **Trust** — Every pull request validated automatically.
2. **Clarity** — Tests pass = safe to merge.
3. **Reproducibility** — Same CI everywhere (no "works on my machine").

### For Production

1. **Reliability** — Automatic testing prevents bad code from shipping.
2. **Safety** — Auto-deployments on tags are safer than manual.
3. **Traceability** — Every release is linked to commit and tests.

## Cost

- **Free Tier:** 2,000 runner minutes/month for public repos, 3,000 for private
- **Most Projects:** Stay well under limit (1,000 lines of tests = ~30 seconds each run)
- **No Cost:** Unless you run thousands of minutes/month

## Anti-Patterns

### ❌ Never Run Tests

```yaml
# Don't do this—no automated testing
name: Nothing
on: [push]
jobs:
  do-nothing:
    runs-on: ubuntu-latest
    steps:
      - run: echo "No tests! Anything could break!"
```

**Fix:** Always run tests on every commit.

### ❌ Flaky Tests

```python
# Test that passes sometimes, fails sometimes
def test_order_matters():
    results = fetch_data_unordered()  # Returns in random order
    assert results == [1, 2, 3]       # Fails sometimes
```

**Fix:** Sort before comparing, or use set assertions.

### ❌ Long-Running Tests

Workflow takes 30 minutes to run. Developers get slow feedback.

**Fix:** Run fast tests in main workflow, slow tests nightly.

### ❌ No Code Coverage

```yaml
# Testing but not checking if tests cover the code
- run: pytest tests/
```

**Fix:** Run with coverage, enforce minimum (80%+).

## Next Steps

1. **Add CI to Cellophane** — Test/lint on every push
2. **Multi-version Testing** — Test Python 3.10, 3.11, 3.12
3. **Coverage Tracking** — Report coverage to pull requests
4. **Create Central Workflows** — Define in [[Wiki/entities/MidnightsGitHubActions]]
5. **Reference from Projects** — All projects use central workflows
6. **Auto-Release** — Semantic versioning + auto-publish
7. **Deploy on Release** — Push tags trigger AWS deployments

## Related Concepts

- [[Wiki/concepts/Reusable Utility Libraries]] — CI ensures library quality
- [[Wiki/concepts/GitHub Actions CI/CD Automation]] — This pattern
- [[Wiki/entities/MidnightsGitHubActions]] — Your central workflow repository

## Key Takeaway

**Automated testing and deployment eliminate manual drudgery and catch bugs early.** Set up GitHub Actions once for each project type; reap benefits forever.
