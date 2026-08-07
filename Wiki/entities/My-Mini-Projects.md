---
type: entity
date_created: 2026-08-07
date_updated: 2026-08-07
tags:
  - wiki/entity
  - wiki/learning
source_count: 1
---

# My-Mini-Projects

Monorepo container for disparate small projects created for learning or experimentation. Lightweight sandbox for quick prototypes without individual repository overhead.

## Purpose

**My-Mini-Projects** is your rapid-experimentation space—a place to throw together learning projects, quick prototypes, and exploratory code without the overhead of creating a full repository for each one. Instead of spinning up 10 separate repos, you keep them all organized here in clear subdirectories.

**Philosophy:** Low friction for trying new technologies. Easy to share and reference. No CI/CD overhead for small experiments.

## Architecture

### Monorepo Structure

```
My-Mini-Projects/
├── README.md
├── src/
│   ├── example-project/        # Template for new projects
│   │   ├── README.md
│   │   ├── main.py
│   │   └── tests/
│   ├── deno-tutorials/         # Deno/TypeScript learning
│   │   ├── hello_world.ts
│   │   ├── file_io.ts
│   │   ├── http_server.ts
│   │   ├── oak_web_framework.ts
│   │   └── README.md
│   └── [future-projects]/
└── LICENSE
```

### Project Types Hosted Here

1. **Deno/TypeScript Tutorials** — Learning modern TypeScript with Deno runtime
   - File I/O operations
   - HTTP servers
   - Web frameworks (Oak)
   - CLI tools

2. **Example Projects** — Template-driven scaffolding for new mini-projects
   - Shows recommended structure
   - Includes basic testing setup
   - Serves as documentation

3. **Experimental Code** — One-off projects for quick learning
   - New language/framework exploration
   - Algorithm implementations
   - Data science notebooks
   - Proof-of-concept prototypes

## Technologies Supported

- **Deno** (TypeScript, modern JavaScript)
- **Python** (quick scripts, algorithms)
- **Other:** Flexible—whatever your quick experiment needs

## Project Status

- **Status:** Learning/Experimental
- **Maturity:** Sandbox (not production-grade)
- **Completeness:** Deno tutorials mostly complete; example template ready; room for more mini-projects
- **Dependencies:** Per-project (deno runtime for Deno projects, Python 3.10+ for Python projects)
- **Code Quality:** Tutorial-grade code with explanations

## Use Cases

### Learning New Technologies

Add a new directory:
```
src/rust-learning/
src/go-microservices/
src/webassembly-experiments/
```

No need to manage separate repos. Structure is built for discovery.

### Quick Prototypes

- Test an API design before building full service
- Validate a new library or framework
- Benchmark algorithms
- Build a proof-of-concept

### Teaching/Documentation

Use `example-project/` as a template to show others how to structure small Python or Deno projects. Include README explaining the pattern.

## Relationships

**Related Concepts:**
- [[Wiki/concepts/Experimentation Sandbox]] — Learning-focused project management
- [[Wiki/concepts/Rapid Prototyping Pattern]] — Monorepo for low-overhead exploration

**Could Share Utilities With:**
- [[Wiki/entities/GenerateIdeas]] — Share Python utility scripts
- [[Wiki/entities/FunWithMusic]] — Share MIDI or music-related Python prototypes

## Key Directories

- `src/deno-tutorials/` — Your entry point for learning Deno
- `src/example-project/` — Template for adding new mini-projects
- `src/` — Where all projects live (organized by technology or purpose)

## Cost Model

**Zero cost.** All technologies are open-source (Deno, Python). No cloud resources or licenses.

## Learning Outcomes

Study this monorepo to learn:
- **Deno Fundamentals** — TypeScript runtime, modules, permissions model, built-in APIs
- **Modern TypeScript** — Type safety, async/await, functional patterns
- **Project Organization** — How to structure multiple small projects in one repo
- **Cross-Language Learning** — How different languages solve the same problems
- **Rapid Prototyping** — Building fast without infrastructure overhead

### Specific Tutorials Included

- **hello_world.ts** — Deno basics
- **file_io.ts** — Reading/writing files
- **http_server.ts** — Building an HTTP server
- **oak_web_framework.ts** — Web framework patterns
- **example-project/** — Python project template

## Adding a New Mini-Project

1. Create new directory: `src/[project-name]/`
2. Copy structure from `example-project/`
3. Implement your experiment
4. Update top-level README with link
5. Keep it self-contained (no shared dependencies unless necessary)

## Next Steps

1. Complete remaining Deno tutorials (CLI tools, database, testing)
2. Add a Python mini-project (e.g., data analysis, machine learning experiment)
3. Build a mini web app (React + Deno backend)
4. Explore WebAssembly projects
5. Create a "mini-projects" showcase in main README

## Scalability Consideration

**When to graduate to full repo:** If a mini-project:
- Becomes your primary tool/service
- Needs independent CI/CD and versioning
- Has external users or team
- Requires complex deployment

Then move it to its own repository and link from here as a "graduated project."

---

**Note:** This is your learning playground. Low structure, high flexibility. Add projects freely; organize as you discover what sticks.
