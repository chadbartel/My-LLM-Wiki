---
type: entity
date_created: 2026-08-07
date_updated: 2026-08-07
tags:
  - wiki/entity
  - wiki/utilities
source_count: 1
---

# Close-Application

Utility script for the Close.com "Build With Us" API challenge. Demonstrates API integration with cryptographic hashing of API traits using BLAKE2b.

## Purpose

**Close-Application** is a completed API integration challenge for Close.com's hiring/learning initiative ("Build With Us"). It showcases how to:
1. Integrate with a third-party REST API
2. Fetch structured data (API traits)
3. Perform cryptographic operations (BLAKE2b hashing)
4. Post results back to the API
5. Validate the integration

**Status:** Completed challenge submission. Reference implementation for API integration patterns.

## Architecture

### Challenge Overview

The Close.com API challenge presents:
1. **Fetch Phase** — Call `/api/traits` endpoint to get trait data
2. **Hash Phase** — Calculate BLAKE2b hash of trait data in a specific format
3. **Post Phase** — Submit the hash back to `/api/submit` endpoint
4. **Validation** — API confirms correct hash calculation

### Implementation

```python
import requests
import hashlib
import json

# 1. Fetch traits from API
response = requests.get("https://api.close.com/api/traits")
traits = response.json()

# 2. Hash traits with BLAKE2b
hash_input = json.dumps(traits, sort_keys=True)
hash_result = hashlib.blake2b(hash_input.encode()).hexdigest()

# 3. Submit hash
submit_response = requests.post(
    "https://api.close.com/api/submit",
    json={"hash": hash_result}
)

# 4. Validate response
if submit_response.status_code == 200:
    print("Challenge completed successfully!")
```

## Technology Stack

- **Language:** Python (single file: `handler.py`)
- **HTTP Client:** `requests` library
- **Cryptography:** `hashlib` module (built-in)
- **Data Handling:** `json` module (built-in)
- **No External Dependencies:** Uses only Python standard library + requests

## Project Structure

```
Close-Application/
├── handler.py              # Main implementation
├── hashes.json            # Reference hashes for validation
├── test.py                # Test/verification script
└── LICENSE
```

### Key Files

- **handler.py** — Core implementation of the API integration flow
- **hashes.json** — Pre-computed hashes for testing/validation
- **test.py** — Verification that your hash calculation is correct

## Project Status

- **Status:** Completed
- **Maturity:** Production-ready (for this specific challenge)
- **Testing:** test.py validates hash calculations
- **Dependencies:** `requests` (minimal)
- **Python Version:** 3.10+
- **Code Quality:** Simple, focused, no dependencies on other projects

## Learning Outcomes

Study this project to learn:
- **API Integration** — HTTP requests, JSON parsing, error handling
- **Cryptographic Hashing** — BLAKE2b algorithm, hash validation
- **Data Serialization** — JSON formatting, consistent ordering for hashing
- **Testing Patterns** — How to validate external API integrations
- **Challenge-Driven Learning** — Practical coding challenges as learning tools

## Key Concepts Demonstrated

### 1. Stateless API Integration

No authentication tokens or sessions—just fetch, compute, submit.

### 2. Deterministic Hashing

BLAKE2b hash must be reproducible:
- Same input → Same hash (always)
- JSON key ordering matters (use `sort_keys=True`)
- Encoding consistency (UTF-8)

### 3. Simple Error Handling

```python
try:
    response = requests.get(url)
    response.raise_for_status()  # Raise on 4xx/5xx
except requests.RequestException as e:
    print(f"API error: {e}")
```

## Cost Model

**Zero cost.** Single API client script. No infrastructure, cloud resources, or licenses. The Close.com API is free for this challenge.

## Relationships

**Related Concepts:**
- [[Wiki/concepts/Reusable Utility Libraries]] — Simple utility script pattern
- [[Wiki/concepts/API Integration Patterns]] — How to work with third-party APIs

**Could Extend To:**
- Add more API challenges from Close.com or other platforms
- Generalize handler.py into a [[Wiki/entities/Cellophane]] wrapper for Close.com API
- Build a batch processor for multiple challenges

## Comparison with Cellophane

| Aspect | Close-Application | Cellophane |
|--------|-------------------|-----------|
| **Purpose** | Specific challenge | Reusable wrapper framework |
| **Scope** | Single API | General-purpose abstraction |
| **Auth** | None (public API) | Abstract (to be implemented) |
| **Error Handling** | Basic try-catch | Automatic retry with re-auth |
| **Code Reuse** | Not designed for reuse | Designed for inheritance |

Close-Application is a **specific solution**; Cellophane is a **reusable pattern**.

## Next Steps

1. ✓ Complete the challenge (done)
2. Use this as a reference for other API integrations
3. Extract patterns into [[Wiki/entities/Cellophane]] wrapper
4. Build batch processor for multiple Close.com challenges
5. Create library of challenge-solving utilities

---

**Note:** This is primarily a learning/portfolio piece demonstrating API integration competency. Keep it as a reference implementation.
