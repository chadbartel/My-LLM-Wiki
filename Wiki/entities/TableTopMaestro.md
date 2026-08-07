---
type: entity
date_created: 2026-08-07
date_updated: 2026-08-07
tags:
  - wiki/entity
  - wiki/learning
  - wiki/ttrpg
source_count: 1
---

# TableTopMaestro

Early-stage TTRPG campaign management tool for organizing world-building, encounter creation, dice rolling, and campaign data. Currently in planning phase with framework design underway.

## Purpose

**TableTopMaestro** is a comprehensive campaign management hub designed to centralize everything a TTRPG game master needs:
- **Campaign Management** — Track storylines, NPCs, locations, plot threads
- **Encounter Design** — Create combat encounters with monsters, loot, tactical maps
- **World-Building** — Organize setting details, factions, lore, timelines
- **Dice & Randomization** — Integrated dice roller with weighted tables
- **Integration** — Connect to music playlists, rule systems, external tools

**Vision:** Single source of truth for all campaign data. Export to PDF, sync with players, automate routine tasks.

**Status:** Early Planning (Framework design, empty main.py). Implementation roadmap defined but not yet executed.

## Architecture

### Conceptual Layers

```
TableTopMaestro (Core Framework)
├── Campaign Management (Data Model)
│   ├── Campaigns (root container)
│   ├── Characters (NPCs, player info)
│   ├── Locations (maps, descriptions, connections)
│   ├── Encounters (combat, roleplay, exploration)
│   └── Story (plot threads, arcs, events)
├── Content Generation (Features)
│   ├── Encounter Generator (random encounters)
│   ├── NPC Generator (personality, motivation, secrets)
│   ├── Loot Generator (treasure, magical items)
│   ├── Dice Roller (d20, d100, custom)
│   └── Random Tables (procedural generation)
├── Integration Layer
│   ├── Music Playlists (thematic soundtracks)
│   ├── Rule Systems (D&D 5e, Pathfinder, custom)
│   └── Export (PDF, JSON, CSV)
└── UI/CLI
    ├── Terminal CLI (management, quick queries)
    └── Web Dashboard (future: visualizations, collaborative editing)
```

### Design Principles

1. **Data-Centric** — Campaign data is canonical; UI is secondary
2. **Export-Friendly** — All data in portable formats (JSON, CSV, Markdown)
3. **Offline-First** — Works without internet; sync when connected
4. **Extensible** — Plugin system for custom generators and rule systems
5. **DM-Centric** — Designed for game masters, not players (initially)

## Technology Stack

- **Language:** Python 3.12
- **Data Storage:** SQLite (local) or JSON (portable)
- **CLI Framework:** Click or Typer (command-line interface)
- **Web (Future):** FastAPI + React
- **Music Integration:** Spotify API or local playlist manager
- **Rule Systems:** Pluggable system adapters
- **Export:** ReportLab (PDF), built-in JSON/CSV

## Current State

```
TableTopMaestro/
├── main.py                 # Empty (waiting for implementation)
├── pyproject.toml         # Metadata only
├── README.md              # Roadmap and vision
├── breakdown_of_design.md # Architecture notes
├── character_creation.md  # Character system spec
└── LICENSE
```

**Status:** Pre-implementation. Design documents exist; code framework not yet started.

## Feature Roadmap

### Phase 1: Core Data Model

- [ ] Campaign data structure (JSON schema)
- [ ] Character/NPC model
- [ ] Location/Map model
- [ ] Encounter structure
- [ ] Story/Plot tracking

### Phase 2: Core Features

- [ ] Dice roller (d20, d100, custom dice pools)
- [ ] Random encounter generator
- [ ] NPC generator (personality, motivation)
- [ ] Loot generator (treasure tables)
- [ ] Basic CLI for data manipulation

### Phase 3: Integration

- [ ] Music playlist manager
- [ ] PDF export
- [ ] Rule system adapters (D&D 5e, Pathfinder)
- [ ] Import/export compatibility

### Phase 4: UI & Collaboration

- [ ] Web dashboard
- [ ] Player portal (view-only access)
- [ ] Collaborative editing
- [ ] Real-time dice rolling

### Phase 5: Advanced Features

- [ ] Campaign templates
- [ ] NPC relationship graph
- [ ] Plot timeline visualization
- [ ] Procedural dungeon generation
- [ ] Mobile companion app

## Relationships

**Related TTRPG Projects:**
- [[Wiki/entities/UnnamedRPG]] — Game system definition (TableTopMaestro could support running UnnamedRPG campaigns)
- [[Wiki/entities/Automated-Taskmaster]] — Encounter/loot generation (TableTopMaestro would integrate this service)
- [[Wiki/entities/TTRPG-AI-RAG-Assistant]] — Rule lookup integration (TableTopMaestro could query this for ruling clarity)

**Related Utilities:**
- [[Wiki/entities/FunWithMusic]] — Music integration for ambiance during gameplay

**Related Concepts:**
- [[Wiki/concepts/TTRPG Ecosystem]] — Your 5-project cluster (TableTopMaestro is a new addition to this)
- [[Wiki/concepts/Campaign Management Pattern]] — Framework design philosophy

## Use Cases

### 1. Solo Campaign Planning
- Build a campaign from scratch
- Generate random encounters
- Track story threads and secrets
- Export session notes to PDF

### 2. Multi-Session Management
- Store session recaps
- Track NPC relationships and secrets
- Manage inventory and treasure
- Timeline of in-game events

### 3. Integration Hub
- Query UnnamedRPG rules via TTRPG-AI-RAG-Assistant
- Generate encounters via Automated-Taskmaster
- Play thematic music via FunWithMusic
- Export to VTT (Virtual Tabletop) like Foundry or Roll20

## Data Model Considerations

### Campaign Structure
```json
{
  "campaign": {
    "name": "The Lost Tombs",
    "system": "D&D 5e",
    "status": "active",
    "characters": [...],
    "locations": [...],
    "encounters": [...],
    "plot_arcs": [...]
  }
}
```

### Extensibility

Pluggable adapters for:
- **Rule Systems** — D&D 5e, Pathfinder, Blades in the Dark, UnnamedRPG
- **Generators** — Encounter, NPC, Loot, Dungeon
- **Export Formats** — PDF, Markdown, VTT JSON
- **Integrations** — Music, Rule lookup, Character sheets

## Cost Model

**Zero cost** (as hobby project).

**Potential Future Costs:**
- Spotify API tier (if integrating music)
- Hosting for web dashboard (if collaborative)
- Database (SQLite is free; PostgreSQL would have costs)

## Learning Outcomes

Building TableTopMaestro teaches:
- **Data Modeling** — Designing complex, hierarchical data structures
- **CLI Development** — Building command-line tools with Click/Typer
- **JSON Schema Validation** — Ensuring data consistency
- **Export Patterns** — Generating multiple output formats from single data source
- **Game Design** — Campaign structure, encounter balance, narrative flow
- **Python Architecture** — Building extensible, plugin-based systems

## Next Steps

1. **Design Phase** — Finalize data schemas and API contracts
2. **Data Model** — Implement Campaign, Character, Location, Encounter classes
3. **CLI Framework** — Build basic CLI for CRUD operations
4. **Generators** — Implement encounter, NPC, and loot generators
5. **Integration** — Connect to existing TTRPG tools ([[Wiki/entities/Automated-Taskmaster]], rule lookup)
6. **Export** — PDF and JSON export capabilities
7. **Web Dashboard** — Visualize campaign data
8. **Player Portal** — Share campaign world with players (view-only)

---

**Note:** This is your most ambitious TTRPG tool. It brings together campaign management, content generation, and integration in one hub. Start with the data model; everything else flows from there.
