---
type: entity
date_created: 2026-08-07
date_updated: 2026-08-07
tags:
  - wiki/entity
  - wiki/learning
source_count: 1
---

# FunWithMusic

Music generation and interactive visualization toolkit for programmatic MIDI composition with real-time playback and mathematical music theory exploration.

## Purpose

FunWithMusic is your sandbox for exploring **algorithmic music generation**—what happens when you apply mathematics, randomness, and composition rules to create sound. It's not a finished application; it's a learning space for experimenting with:
- Symbolic music composition (note sequences, timing, dynamics)
- MIDI routing and real-time playback
- Music visualization and notation
- Music theory concepts (scales, harmony, rhythm)

**Philosophy:** Use code to understand music, not to replace musicians.

## Architecture

### Tech Stack

- **Core:** SCAMP (Symbolic Composition for Algorithmic Music Production)
- **MIDI:** python-rtmidi (MIDI routing to synthesizers/DAWs)
- **Visualization:** matplotlib, abjad (music notation), numpy, scipy
- **GUI:** tkinter for interactive controls
- **Input:** pynput for keyboard/mouse control
- **Language:** Python 3.10+

### SCAMP Framework

SCAMP is a symbolic music notation library that lets you compose music programmatically:

```python
from scamp import *

session = Session()
violin = session.new_part("Violin")

# Create a melody programmatically
for pitch in [60, 62, 64, 65, 67]:
    violin.play_note(pitch, 1.0, 0.5)  # pitch, volume, duration

session.play()
```

Then SCAMP can export to notation (PDF/MusicXML) or play it via MIDI.

### Visualization Approach

Multiple outputs:
1. **Real-time MIDI Visualization:** Show notes as they're played (matplotlib)
2. **Score Notation:** Export as printable sheet music (abjad)
3. **Spectrogram Analysis:** Frequency content over time (scipy)
4. **Interactive GUI:** Play melodies, adjust parameters, hear results immediately

## Project Structure

```
FunWithMusic/
├── main.py                    # Entry point (not yet implemented)
├── scamp_tutorials/           # SCAMP examples and learning code
│   ├── hello_world.py        # First composition
│   ├── scales_and_modes.py   # Music theory experiments
│   └── ...
├── inspiration/              # Research notes, music theory references
└── pyproject.toml
```

## Project Status

- **Status:** Experimental/Learning
- **Maturity:** Research/exploration phase
- **Completeness:** Tutorials present, main application framework incomplete
- **Dependencies:** SCAMP, python-rtmidi, matplotlib, abjad, numpy, scipy
- **Python Version:** 3.10+
- **Code Quality:** Organized, well-commented tutorials

## Use Cases & Learning Paths

### 1. Music Theory Exploration
- Generate scales, modes, chord progressions
- Visualize intervals and harmonic relationships
- Experiment with microtonal tuning systems

### 2. Algorithmic Composition
- Random melody generation with constraints
- Generative music using Markov chains
- Procedural music for games/interactive media

### 3. MIDI Automation
- Generate MIDI sequences for DAWs (Ableton, Logic, Reaper)
- Control synthesizers programmatically
- Time-sync with external tempo/clock

### 4. Audio Processing
- Analyze spectrograms of generated music
- Apply effects and transformations
- Export to standard audio formats

## Relationships

**Related Concepts:**
- [[Wiki/concepts/Experimentation Sandbox]] — Learning-focused project structure
- [[Wiki/concepts/Algorithmic Music Generation]] — Generative approaches
- [[Wiki/concepts/Python Music Libraries]] — SCAMP, python-rtmidi, abjad ecosystem

**Could Integrate With:**
- [[Wiki/entities/GenerateIdeas]] — Generate music ideas with LLM guidance
- [[Wiki/entities/TableTopMaestro]] — Provide campaign soundtrack generation

## Key Directories

- `scamp_tutorials/` — Your entry point for learning SCAMP
- `inspiration/` — Research notes, music theory references
- `main.py` — Where the full application will live (currently a blank slate)

## Cost Model

**Zero cost.** All dependencies are open-source (SCAMP, python-rtmidi, matplotlib, abjad). Optional: MIDI hardware or DAW software (but not required for learning).

## Learning Outcomes

Study this project to learn:
- SCAMP symbolic composition framework
- MIDI protocol and routing concepts
- Music theory fundamentals (scales, intervals, chords, rhythm)
- Real-time audio visualization (matplotlib, scipy.signal)
- Music notation generation (abjad)
- Interactive GUI programming (tkinter)
- Algorithmic music generation techniques

## Next Steps

1. Work through SCAMP tutorials to understand core concepts
2. Experiment with algorithmic melody generation
3. Build a "generative ambient soundscape" generator
4. Connect to external MIDI hardware or DAW
5. Create the main.py application framework (interactive composition tool)

## Open Questions

- What is the final application? A generative music player? An interactive composition tool? A DAW plugin?
- How will users interact? GUI buttons? Command-line? Real-time parameters?
- Target genres or musical styles?

These are future explorations; for now, it's pure learning and experimentation.
