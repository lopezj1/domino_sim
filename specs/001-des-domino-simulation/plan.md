# Implementation Plan: Discrete Event Simulation (DES) for Domino Game with Monte Carlo Strategy Evaluation

**Branch**: `001-des-domino-simulation` | **Date**: 2025-01-29 | **Spec**: `/specs/001-des-domino-simulation/spec.md`
**Input**: Feature specification from `/specs/001-des-domino-simulation/spec.md`

## Summary

Build a Python codebase modeling the game of Domino as a discrete event simulation (DES) with Monte Carlo strategy evaluation. Core deliverable: immutable game state model, event-driven game loop, pluggable strategy interface, and Monte Carlo batch orchestration for statistical strategy comparison. The implementation follows model-driven architecture with strict test-first discipline and full reproducibility via seeded RNG.

## Technical Context

**Language/Version**: Python 3.11+ (type hints required, mypy type-checking enforced)  
**Primary Dependencies**: FastAPI (API), uvicorn (server), pytest (testing), pydantic (validation), uv (Python package/environment management)  
**Storage**: JSON/structured logs (event traces, results); no database required for MVP  
**Testing**: pytest with pytest-cov, fixtures for game state setup and replay  
**Target Platform**: Linux/Unix server (simulator backend), REST API interface  
**Project Type**: Web application (backend simulator + frontend dashboard for Phase 2)  
**Performance Goals**: Single game <1s, Monte Carlo 10k runs <60s, memory <1GB per batch  
**Constraints**: Tile conservation invariant (28 tiles always), 100% legal move validation, reproducibility (same seed → identical outcome)  
**Scale/Scope**: 2-4 player support, 3+ strategy implementations, 100+ Monte Carlo runs per comparison

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

✅ **Model-Driven Architecture**: Game state and rules modeled as immutable dataclasses with clear contracts. Event queue is authoritative control flow.  
✅ **Discrete Event Simulation**: Event ordering by timestamp, deterministic processing, no race conditions. Event loop enforces game semantics.  
✅ **Strategy Pluggability**: Abstract Strategy base class with `choose_move(game_state, legal_moves) -> Move` interface. Pure function of observable state.  
✅ **Reproducibility & Randomness**: SeededRNG at simulator level, all random decisions explicit and logged. Fixed seed → identical outcome guaranteed.  
✅ **Test-First Validation**: Unit tests for models/rules, integration tests for game flow, coverage for invariants and edge cases.  
✅ **Observable Simulation**: Event traces logged as JSON with state snapshots for debugging and result auditing.  
**GATE STATUS**: ✅ PASS - No constitution violations. Python 3.11+, test-first, immutable models, deterministic RNG.

## Project Structure

### Documentation (this feature)

```text
specs/001-des-domino-simulation/
├── plan.md              # This file (implementation plan with uv setup)
├── research.md          # Phase 0 output (to be generated)
├── data-model.md        # Phase 1 output (to be generated)
├── quickstart.md        # Phase 1 output (to be generated)
├── contracts/           # Phase 1 output (to be generated)
├── spec.md              # Feature specification
├── tasks.md             # Phase 2 task tracking
└── checklists/          # Task checklists
```

### Source Code (repository root)

```text
domino_sim/
├── .specify/                    # Specification kit configuration
│   ├── memory/
│   │   └── constitution.md      # Project governance and principles
│   ├── scripts/bash/
│   │   ├── setup-plan.sh        # Plan initialization script
│   │   └── update-agent-context.sh
│   └── templates/
│
├── backend/                     # Python simulator backend
│   ├── pyproject.toml           # uv project config (Python 3.11+)
│   ├── uv.lock                  # uv dependency lock file
│   ├── .venv/                   # Virtual environment (created by uv venv)
│   ├── src/
│   │   ├── models/
│   │   │   ├── tile.py          # Tile model (immutable)
│   │   │   ├── move.py          # Move model (action + tile)
│   │   │   ├── game_state.py    # GameState model
│   │   │   ├── events.py        # Event model
│   │   │   └── result.py        # GameOutcome, MonteCarloResult
│   │   ├── engine/
│   │   │   ├── rng.py           # SeededRNG for reproducibility
│   │   │   ├── tiles.py         # Tile factory + shuffler
│   │   │   ├── dealer.py        # Tile distribution
│   │   │   └── rules.py         # Move validation + scoring
│   │   ├── strategy/
│   │   │   ├── base.py          # Strategy abstract base class
│   │   │   ├── greedy.py        # GreedyStrategy (highest pips)
│   │   │   ├── random.py        # RandomStrategy (uniform random)
│   │   │   └── blocking.py      # BlockingStrategy (block opponent)
│   │   ├── simulation/
│   │   │   ├── game.py          # Game event loop orchestrator
│   │   │   └── runner.py        # GameRunner for single-game simulation
│   │   ├── aggregation/
│   │   │   └── monte_carlo.py   # Monte Carlo batch orchestration
│   │   ├── api/
│   │   │   ├── schemas/         # Pydantic request/response schemas
│   │   │   └── routes/          # API endpoints (simulation, results)
│   │   ├── cli/
│   │   │   └── main.py          # CLI entry point for batch runs
│   │   └── __init__.py
│   │
│   └── tests/
│       ├── conftest.py          # Pytest fixtures (tile_set, seeded_rng, game_state)
│       ├── unit/
│       │   ├── test_tile.py     # Tile model tests
│       │   ├── test_move.py     # Move model tests
│       │   ├── test_game_state.py
│       │   ├── test_events.py
│       │   ├── test_rng.py
│       │   ├── test_tiles.py    # Tile factory tests
│       │   ├── test_dealer.py
│       │   ├── test_rules.py    # Move validation, scoring
│       │   ├── test_strategies.py
│       │   └── test_game.py     # Game class tests
│       ├── integration/
│       │   ├── test_game_flow.py     # Full game simulation
│       │   ├── test_reproducibility.py # Seed-based determinism
│       │   ├── test_tile_conservation.py
│       │   └── test_strategies.py  # Strategy comparison
│       └── contract/
│           ├── test_game_initialization.py
│           ├── test_move_validation.py
│           └── test_state_transitions.py
│
├── frontend/                    # TypeScript/React dashboard (Phase 2)
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── services/
│   └── tests/
│
├── specs/                       # Specification documents
│   └── 001-des-domino-simulation/
│       ├── spec.md             # Feature specification
│       ├── plan.md             # This implementation plan
│       ├── research.md         # Phase 0 research output
│       ├── data-model.md       # Phase 1 data model
│       ├── quickstart.md       # Phase 1 quickstart guide
│       └── contracts/          # Phase 1 API contracts
│
├── .gitignore
├── Dockerfile                  # Docker image (Python 3.11, uv setup)
├── docker-compose.yml          # Local dev environment
└── README.md                   # Project overview
```

**Structure Decision**: Web application with separate backend (Python simulator) and frontend (Phase 2). Backend uses uv for environment and dependency management via `pyproject.toml`. Tests organized in unit/integration/contract layers. API layer (FastAPI) will expose simulation endpoints in Phase 2.

## Environment Setup (using Astral `uv`)

### Installation

The project uses **Astral's `uv`** for fast, deterministic Python environment and dependency management.

**Install uv** (if not present):
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Virtual Environment Setup

```bash
# Create virtual environment in backend directory
cd backend
uv venv .venv

# Activate environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies from pyproject.toml
uv pip install -e .

# Verify installation
python --version  # Should be 3.11+
pytest --version
```

### pyproject.toml Structure

The `pyproject.toml` file configures:
- **Tool**: uv with Python 3.11+ requirement
- **Dependencies**: FastAPI, uvicorn, pydantic, pytest, mypy, black, flake8, isort
- **Scripts**: Commands for running tests, linting, formatting
- **Package**: editable install with src layout

### Key uv Commands

```bash
# Sync dependencies (install/update from lock file)
uv sync

# Add new dependency
uv add package-name

# Run scripts defined in pyproject.toml
uv run pytest
uv run pytest --cov

# Format and lint
uv run black src/ tests/
uv run flake8 src/ tests/
uv run isort src/ tests/

# Type checking
uv run mypy src/
```

### Reproducibility

- `uv.lock` file pins exact dependency versions for team consistency
- Seed management via SeededRNG ensures deterministic game outcomes
- Virtual environment isolation prevents host system interference
- CI/CD uses `uv sync` for reproducible builds
