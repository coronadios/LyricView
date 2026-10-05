# LyricView Roadmap

This roadmap captures the intended direction for the project while keeping the architecture flexible enough for contributors to steer the project in different directions.

## Phase 1 — Stabilize the core

Goals:

- finalize the engine lifecycle
- keep the timing model deterministic
- clean up public API contracts
- improve regression coverage for playback, seek, and state transitions

Status: in progress

## Phase 2 — Expand parsers and schema support

Goals:

- support more lyric formats
- improve validation and error handling for malformed files
- add robust fixtures and examples
- document parser registry contracts

Candidate formats:

- LRC
- SRT/VTT
- JSON
- YAML
- custom or vendor-specific lyric schemas

## Phase 3 — Renderer ecosystem

Goals:

- support multiple display backends
- keep renderers dumb consumers of engine state
- add theme portability across renderers
- make frontends easier to swap without changing the model

Likely targets:

- Tkinter
- web renderer
- Qt renderer
- terminal renderer
- plugin-based custom renderer experiments

## Phase 4 — Motion and UX polish

Goals:

- improve scroll behavior and damping
- add richer easing presets and animation states
- improve reduced-motion behavior
- tune word and syllable-level transitions

## Phase 5 — OSS maturity and contributor experience

Goals:

- better contributor docs
- public roadmap and changelog
- issue and PR templates
- example repositories and benchmark pages
- stronger public API documentation

## Long-term vision

LyricView should become a reusable engine and ecosystem for synchronized text experiences, not only a single-view lyric app. The core idea is simple: the engine owns the truth, the parser defines the input, and the renderer decides how to present it.

## Community priorities

The strongest near-term contributions are likely to be:

- parser support
- visibility and docs improvements
- motion tuning
- renderer experiments
- real-world integrations with music or playback tools
