# Contributing to LyricView

Thanks for your interest in improving LyricView. This project is intentionally designed as an engine-first, extensible lyric system, so contributions that keep the model, timing, and renderer layers clean are especially valuable.

## Ways to contribute

- improve the core engine and timing logic
- add new parsers or schema support
- improve motion, auto-scroll, and accessibility behavior
- add or refine renderer backends
- expand tests and documentation
- propose better examples or real-world integrations

## Development setup

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -e .
python -m pytest
```

## Contribution guidelines

### 1. Keep architectural boundaries clear

Respect the separation between:

- model layer
- engine and time state
- parser registry
- motion system
- rendering and UI adapters

If a change crosses layers, explain the reason clearly in the PR and keep the scope focused.

### 2. Prefer deterministic behavior

LyricView should be predictable. Avoid hidden state, timing hacks, or UI-only logic leaking into the engine. When you change timing, playback, or scroll behavior, add a test where possible.

### 3. Make small, reviewable changes

Large refactors are harder to validate and review. Prefer a narrow, well-scoped patch that solves a concrete problem and ships with docs or tests when needed.

### 4. Write tests for behavior changes

Use pytest for regression cases, especially when changing:

- seek and playback behavior
- parser output
- event emissions
- visual state transitions
- theme or configuration resolution

### 5. Document public-facing API changes

If you add a new public capability or alter an existing contract, update the docs and, if needed, the examples in README or the WebDocs site.

## Suggested contribution paths

### Core engine

Best for contributors who want to improve:

- timeline calculation
- state resolution
- event delivery
- deterministic playback

### Parser work

Best for contributors working on:

- format importers
- normalization rules
- validation and file compatibility
- metadata parsing

### Motion and renderer work

Best for contributors focused on:

- easing curves
- autoplay scroll control
- reduced-motion handling
- new renderer adapters or UI frontends

## Pull request checklist

Before submitting a PR, confirm that:

- [ ] the change is scoped and clearly explained
- [ ] tests pass locally
- [ ] there are no unrelated modifications
- [ ] documentation is updated when needed
- [ ] behavior is consistent with the engine-first architecture

## Code of conduct

This project aims to be welcoming, respectful, and collaborative. We encourage thoughtful discussion, clear communication, and constructive feedback.

## Good first issues

Examples of good entry points include:

- improving parser validation
- adding simple tests for edge cases
- documenting a public API
- polishing motion behavior
- creating examples for new renderers

We appreciate contributions at every level, from a tiny docs fix to a new parser or animation system.
