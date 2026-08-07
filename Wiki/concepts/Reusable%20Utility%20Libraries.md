---
type: concept
date_created: 2026-08-07
date_updated: 2026-08-07
tags:
  - wiki/concept
source_count: 2
confidence: high
---

# Reusable Utility Libraries

Pattern for creating small, focused Python libraries that solve a specific problem and can be imported into multiple projects without duplication.

## Definition

A **reusable utility library** is a self-contained, well-tested Python package designed to solve one problem elegantly and can be used as a dependency in multiple projects. Think of it as a "micro-library" — smaller than a full framework, focused on one responsibility.

**Core Traits:**
- **Single Responsibility** — Solves one problem well
- **Importable** — Can be installed via pip or poetry
- **Type-Safe** — Full type hints for IDE support
- **Well-Tested** — Unit tests demonstrate usage
- **Documented** — README explains purpose and API
- **Minimal Dependencies** — Uses standard library where possible

## Why It Matters

**Without Reusable Libraries:**
```python
# In Project A: api_wrapper_a.py
class APIClient:
    def GET(self, url): ...
    def POST(self, data): ...
    def _handle_errors(self): ...

# In Project B: api_wrapper_b.py (copy-paste of same code!)
class APIClient:
    def GET(self, url): ...
    def POST(self, data): ...
    def _handle_errors(self): ...
```

You duplicate code across projects. Updates require changes in multiple places.

**With Reusable Libraries:**
```python
# In Cellophane (library)
class CellophaneBase:
    def GET(self, url): ...
    def POST(self, data): ...
    def _handle_errors(self): ...

# In Project A
from cellophane import CellophaneBase
class MyAPIClient(CellophaneBase): ...

# In Project B
from cellophane import CellophaneBase
class AnotherAPIClient(CellophaneBase): ...
```

Code lives once. Both projects inherit improvements. Single source of truth.

## Pattern Components

### 1. Core Implementation

**Cellophane Example:**
```python
# cellophane/base.py
from abc import ABC, abstractmethod

class CellophaneBase(ABC):
    """Abstract base for building API wrappers."""
    
    @abstractmethod
    def _authenticate(self) -> str:
        """Subclasses implement their auth logic."""
        pass
    
    def GET(self, endpoint: str) -> dict:
        """Standard GET with error handling."""
        # ... implementation
        pass
```

### 2. Type Hints

Make the API clear and enable IDE autocomplete:

```python
def GET(self, endpoint: str, params: dict | None = None) -> dict:
    """Fetch from endpoint. Returns JSON response."""
    ...

def POST(self, endpoint: str, data: dict) -> dict:
    """POST data to endpoint. Returns JSON response."""
    ...
```

### 3. Error Handling

Standardized error responses:

```python
class APIError(Exception):
    """Base exception for API errors."""
    def __init__(self, status: int, message: str):
        self.status = status
        self.message = message

try:
    response = self.GET("/users")
except APIError as e:
    if e.status == 401:
        # Re-authenticate and retry
        self._authenticate()
except Exception as e:
    # Log unexpected errors
    logger.error(f"Unexpected error: {e}")
```

### 4. Testing

Comprehensive unit tests that demonstrate usage:

```python
# tests/unit/test_cellophane_base.py
def test_get_success(mock_session):
    client = MyTestClient(session=mock_session)
    response = client.GET("/endpoint")
    assert response == {"status": "ok"}

def test_get_with_401_retry(mock_session):
    # First call returns 401, then 200 after re-auth
    client = MyTestClient(session=mock_session)
    response = client.GET("/endpoint")
    assert response == {"status": "ok"}
    assert client._authenticate.call_count == 2
```

### 5. Documentation

Clear README explaining the purpose and usage:

```markdown
# Cellophane

Abstract base class library for HTTP API wrappers.

## Quick Start

```python
from cellophane import CellophaneBase

class MyAPI(CellophaneBase):
    def _authenticate(self) -> str:
        return "token123"

client = MyAPI()
user = client.GET("/users/123")
```

## API

- `GET(endpoint, params)` — Fetch resource
- `POST(endpoint, data)` — Create resource
- ...
```

## Design Patterns Within Reusable Libraries

### Pattern 1: Template Method

Define the structure in the base class; subclasses implement specifics:

```python
class CellophaneBase:
    def GET(self, url):
        # Template: always ensure authentication first
        if not self.token:
            self._authenticate()  # Subclass implements this
        return self._make_request("GET", url)
    
    @abstractmethod
    def _authenticate(self):
        """Subclass must implement."""
        pass
```

### Pattern 2: Dependency Injection

Allow swappable implementations for testing:

```python
class CellophaneBase:
    def __init__(self, session: requests.Session = None):
        self.session = session or requests.Session()
        
# In tests, inject mock session
mock_session = Mock()
client = MyAPI(session=mock_session)
```

### Pattern 3: Composition Over Inheritance

For more flexibility than inheritance:

```python
class APIClient:
    def __init__(self, authenticator: Authenticator):
        self.auth = authenticator
    
    def GET(self, url):
        self.auth.ensure_valid()  # Delegate to authenticator
        return requests.get(url)
```

## Your Reusable Utility Libraries

### [[Wiki/entities/Cellophane]]

**Purpose:** Abstract base class for API wrappers  
**Scope:** HTTP GET/POST/PUT/PATCH/DELETE with auth and error handling  
**Usage:** Inherit and implement `_authenticate()` for your API  
**Status:** Production-ready  
**Extensibility:** Add OAuth, mTLS, API key rotation

**Could Be Used By:**
- [[Wiki/entities/GenerateIdeas]] (Gemini API wrapper)
- [[Wiki/entities/Cartographers-Cloud-Kit]] (backend services)
- Any project integrating with external APIs

### [[Wiki/entities/Close-Application]]

**Purpose:** Specific API integration (Close.com API challenge)  
**Scope:** Fetch traits, hash, submit results  
**Status:** Completed reference implementation  
**Relationship to Cellophane:** Close-Application is a specific solution; could be refactored to use Cellophane as a base

## Anti-Patterns to Avoid

### ❌ God Library
A library that does too much:
```python
# Don't do this—split into separate libraries
class UltilityLibrary:
    def http_get(...): ...
    def parse_csv(...): ...
    def hash_file(...): ...
    def send_email(...): ...
    def connect_database(...): ...
```

**Fix:** Each library has one responsibility.

### ❌ Heavy Dependencies
A library with too many transitive dependencies:
```python
# Don't do this
dependencies = [
    "pandas",
    "numpy",
    "scikit-learn",
    "tensorflow",
    "torch",
]
```

**Fix:** Use standard library where possible. Minimize external deps.

### ❌ Unclear API
Inconsistent, unexplained methods:
```python
# Don't do this
def fetch_data(x): ...
def get_stuff(y, z=None): ...
def retrieve(a, b, c, d): ...
```

**Fix:** Consistent naming. Type hints. Docstrings.

### ❌ No Tests
A library without unit tests:
```python
# Don't ship this—you have no idea if it works
class MyLibrary:
    def process(...): ...
    # No tests = unknown behavior
```

**Fix:** Tests document usage and validate behavior.

## Lifecycle: From Specific to Reusable

### Stage 1: Specific (One Project)

Start with Close-Application—solve your immediate problem.

```python
# close_application/handler.py
def submit_traits():
    response = requests.get("https://api.close.com/traits")
    hash = hashlib.blake2b(json.dumps(response).encode()).hexdigest()
    requests.post("https://api.close.com/submit", json={"hash": hash})
```

### Stage 2: Extract Pattern

Recognize the pattern (HTTP + auth + error handling):

```python
# cellophane/base.py
class CellophaneBase(ABC):
    @abstractmethod
    def _authenticate(self): pass
    
    def GET(self, url): ...
    def POST(self, url): ...
```

### Stage 3: Generalize

Remove project-specific logic; add configuration:

```python
class CellophaneBase:
    def __init__(self, base_url: str, auth_strategy: AuthStrategy):
        self.base_url = base_url
        self.auth = auth_strategy
```

### Stage 4: Test & Document

Add comprehensive tests and README:

```
cellophane/
├── cellophane/base.py
├── tests/unit/test_base.py
├── README.md
└── pyproject.toml
```

### Stage 5: Reuse

Import in multiple projects:

```python
from cellophane import CellophaneBase

class MyAPI(CellophaneBase): ...
class AnotherAPI(CellophaneBase): ...
```

## When to Build a Reusable Library

✓ **Yes, build a library when:**
- Code is used in 2+ projects
- Logic is generic and reusable
- You've solved the same problem twice
- You want to avoid maintaining copy-paste code
- The library's scope is clear and focused

✗ **No, don't build a library when:**
- Code is used in only one place
- It's still changing rapidly (wait until it stabilizes)
- The problem is project-specific
- You haven't proven the pattern works

## Publishing Your Libraries

### Option 1: Local Import

For private use within your workspace:

```python
# In poetry.toml
[tool.poetry.dependencies]
cellophane = {path = "../Cellophane", develop = true}
```

### Option 2: Git Reference

Reference directly from GitHub:

```toml
cellophane = {git = "https://github.com/thatsmidnight/Cellophane.git", branch = "main"}
```

### Option 3: PyPI

Publish to Python Package Index for public use:

```bash
poetry publish  # Requires PyPI account
```

## Related Concepts

- [[Wiki/concepts/GitHub Actions CI/CD Automation]] — Test and publish libraries automatically
- [[Wiki/concepts/Experimentation Sandbox]] — Test utility patterns before extracting into libraries

## Key Takeaway

**Reusable utility libraries eliminate duplication and provide a single source of truth.** When you find yourself writing the same code twice, extract it into a library. Test it once. Use it everywhere.
