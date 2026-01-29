# Implementation Plan: DES Domino Simulation with Interactive Webapp

**Branch**: `001-des-domino-simulation` | **Date**: 2025-01-29 | **Spec**: [spec.md](spec.md)  
**Input**: Build a Python codebase that models the game of Domino as a discrete event simulation (DES) and evaluates fixed player strategies using Monte Carlo simulation, exposed via an interactive webapp for showcasing.

## Summary

Build a **two-tier architecture**: 
1. **Backend** (Python): Clean, modular DES engine with pluggable strategies, Monte Carlo orchestration, and result aggregation
2. **Frontend** (Web): Interactive dashboard to run simulations, visualize game play, compare strategies, and display aggregated statistics

This plan delivers separate, independently testable components with a web API bridge. The simulation core (US1-US3) can be tested in isolation; the webapp (US4+UI) adds interactive showcase capability without modifying core logic.

## Technical Context

**Language/Version**: Python 3.11+ (backend simulation), JavaScript/TypeScript (frontend UI)  
**Primary Dependencies**: 
  - Backend: pytest (testing), dataclasses (state models), random (RNG control)
  - Frontend: React 18+ (interactive UI), Vite/TypeScript (tooling), Axios (API client)
  - Bridge: FastAPI (async REST API), uvicorn (dev server)

**Storage**: File-based (JSON export of results); no persistent database required for MVP  
**Testing**: pytest (backend unit/integration), Vitest + React Testing Library (frontend)  
**Target Platform**: Linux/macOS development, web browser (Chrome/Firefox/Safari)  
**Project Type**: Web application (backend + frontend)  
**Performance Goals**: 
  - Single game: <1s
  - Monte Carlo batch (10k runs): <60s
  - API response: <500ms per request (includes simulation)
  - Frontend: 60fps interactive visualization

**Constraints**: 
  - Offline-capable backend (no external dependencies)
  - Frontend can run with or without internet (local API)
  - Memory footprint: <1GB per 10k-run batch

**Scale/Scope**: 
  - 2-player domino game only
  - 3+ strategies (examples: greedy, random, blocking)
  - Monte Carlo: up to 100k runs per session
  - Single developer / small team

## Constitution Check

*GATE: Must pass before Phase 0 research.*

### Principle Compliance

✅ **I. Model-Driven Architecture**  
Decision: Separate domain models (Tile, GameState, Move, Strategy) from simulation orchestration and API layers. Each model is immutable where possible and independently testable.

✅ **II. Discrete Event Simulation (DES) Pattern**  
Decision: Event loop is authoritative control flow. Events ordered by index (turn number). State transitions explicit (deal → play/draw → pass → round-end → game-end). No race conditions (single-threaded event loop).

✅ **III. Strategy Pluggability**  
Decision: Strategy interface (abstract base class or Protocol) with `choose_move(state, legal_moves) -> Move`. All strategies are pure functions of observable state. Strategies can be swapped at runtime without core changes.

✅ **IV. Reproducibility & Randomness Control**  
Decision: RNG injected at Simulation orchestrator level. All randomness (shuffle, draw order) consumes explicit RNG state. Seeds logged with outcomes. Same seed + strategies → identical game trace (verified by tests).

✅ **V. Validation & Correctness (Test-First)**  
Decision: Test-first for all game mechanics, strategy logic, and result aggregation. Unit tests for individual components (tile shuffling, move validation, scoring). Integration tests for full game flows. No feature accepted without passing tests.

✅ **VI. Observable Simulation Runs**  
Decision: Game traces logged at event level. API returns structured JSON with full trace (optional), summary statistics, and metadata (seed, players, timestamp). Results serializable for external audit.

### Gate Status

🟢 **PASS** - All principles satisfied. No violations. Project may proceed to Phase 0.

---

## Project Structure

### Documentation (this feature)

```text
specs/001-des-domino-simulation/
├── plan.md                      # This file
├── spec.md                      # Feature specification
├── research.md                  # Phase 0 findings (TBD)
├── data-model.md                # Phase 1 entity definitions (TBD)
├── quickstart.md                # Phase 1 developer guide (TBD)
└── contracts/                   # Phase 1 API specs (TBD)
    ├── game-engine-api.md       # Simulation engine contracts
    ├── strategy-interface.md     # Strategy plugin interface
    ├── monte-carlo-api.md        # Batch orchestration API
    └── webapp-api.md             # REST endpoints for frontend
```

### Source Code (repository root)

```text
# Web Application (backend + frontend)
backend/
├── src/
│   ├── models/                  # Data models (Tile, GameState, Move, etc.)
│   │   ├── __init__.py
│   │   ├── tile.py              # Tile entity
│   │   ├── game_state.py         # GameState (immutable snapshot)
│   │   ├── move.py              # Move action type
│   │   └── result.py            # GameOutcome, MonteCarloResult, GameTrace
│   ├── engine/                  # Game simulation engine (DES core)
│   │   ├── __init__.py
│   │   ├── game.py              # Game class (event loop, state transitions)
│   │   ├── rules.py             # Game rules (move validation, scoring)
│   │   ├── events.py            # Event types and handling
│   │   └── rng.py               # RNG management with seed control
│   ├── strategy/                # Player strategy implementations
│   │   ├── __init__.py
│   │   ├── base.py              # Strategy base class / ABC
│   │   ├── greedy.py            # Greedy strategy (highest pip)
│   │   ├── random.py            # Random legal move
│   │   └── blocking.py          # Blocking opponent strategy
│   ├── simulation/              # Simulation orchestration (DES runner)
│   │   ├── __init__.py
│   │   ├── runner.py            # Single game runner
│   │   └── monte_carlo.py       # Monte Carlo batch orchestrator
│   ├── aggregation/             # Result aggregation and analysis
│   │   ├── __init__.py
│   │   └── stats.py             # Statistics computation (means, CIs, etc.)
│   ├── api/                     # REST API (FastAPI)
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI app setup
│   │   ├── routes/              # API endpoints
│   │   │   ├── __init__.py
│   │   │   ├── game.py          # POST /api/game/run (single game)
│   │   │   ├── monte_carlo.py   # POST /api/monte-carlo/compare (batch)
│   │   │   ├── strategies.py    # GET /api/strategies (list available)
│   │   │   └── health.py        # GET /api/health
│   │   └── schemas/             # Pydantic request/response models
│   │       ├── __init__.py
│   │       ├── game.py          # GameRunRequest, GameRunResponse
│   │       └── monte_carlo.py   # MonteCarloRequest, MonteCarloResponse
│   └── cli/                     # Optional CLI for headless operation
│       ├── __init__.py
│       └── main.py              # CLI commands
│
├── tests/
│   ├── unit/                    # Unit tests (one per module)
│   │   ├── test_tile.py
│   │   ├── test_game_state.py
│   │   ├── test_move.py
│   │   ├── test_game.py
│   │   ├── test_rules.py
│   │   ├── test_strategies.py
│   │   ├── test_runner.py
│   │   ├── test_monte_carlo.py
│   │   └── test_stats.py
│   ├── integration/             # Integration tests (game traces)
│   │   ├── test_full_game.py
│   │   ├── test_reproducibility.py
│   │   └── test_strategy_comparison.py
│   └── contract/                # Contract tests (API + strategy interface)
│       ├── test_game_engine_api.py
│       ├── test_strategy_interface.py
│       └── test_monte_carlo_api.py
│
├── pyproject.toml               # Python project config (deps, pytest config)
├── pytest.ini                   # pytest configuration
├── requirements.txt             # Python dependencies
└── README.md                    # Backend documentation

frontend/
├── src/
│   ├── components/              # React components
│   │   ├── GameSimulator.tsx    # Main simulator control panel
│   │   ├── StrategySelector.tsx # Strategy picker (dropdown)
│   │   ├── GameViewer.tsx       # Game board visualization
│   │   ├── TraceViewer.tsx      # Game trace / move history
│   │   ├── MonteCarloRunner.tsx # Batch simulation control
│   │   ├── ResultsChart.tsx     # Win rate, score diff charts
│   │   ├── ConfidenceInterval.tsx # Statistical displays
│   │   └── ExportButton.tsx     # Export results as JSON/CSV
│   ├── hooks/                   # Custom React hooks
│   │   ├── useGameSimulation.ts # Simulation state management
│   │   └── useAPI.ts            # API client abstraction
│   ├── pages/                   # Page-level components
│   │   ├── Home.tsx             # Landing page
│   │   ├── SingleGame.tsx       # Single game simulator
│   │   ├── MonteCarlo.tsx       # Batch comparison tool
│   │   └── Results.tsx          # Results viewer
│   ├── services/                # API client
│   │   ├── api.ts               # Axios client for /api/*
│   │   └── types.ts             # TypeScript types (mirrors backend schemas)
│   ├── styles/                  # CSS/Tailwind
│   │   └── globals.css
│   ├── App.tsx                  # Root component
│   └── main.tsx                 # Entry point
│
├── tests/
│   ├── unit/                    # Component unit tests (Vitest)
│   │   ├── GameSimulator.test.tsx
│   │   ├── StrategySelector.test.tsx
│   │   └── ResultsChart.test.tsx
│   └── integration/             # E2E scenarios
│       └── game-flow.test.ts
│
├── vite.config.ts               # Vite config (dev server, build)
├── tsconfig.json                # TypeScript config
├── package.json                 # Node dependencies
├── .env.example                 # Environment variables template
└── README.md                    # Frontend documentation

# Shared
docs/
├── API.md                       # REST API documentation
├── ARCHITECTURE.md              # Architecture overview
└── DEVELOPMENT.md               # Developer setup guide

# Root
pyproject.toml                  # Root Python config (if monorepo setup)
Dockerfile                      # Optional: containerize backend
docker-compose.yml              # Optional: local dev environment
```

**Structure Decision**: Web application with separate backend (Python) and frontend (React). This enables:
- Independent testing of simulation engine (backend-only tests)
- Parallel development of UI features
- Reusable API for other clients (CLI, batch scripts, etc.)
- Easy deployment (containerize backend, host frontend as static assets)

---

## Complexity Tracking

> Fill ONLY if Constitution Check has violations that must be justified

No violations detected. Structure is justified by separation of concerns: simulation logic is pure (testable) and decoupled from UI rendering.

---

## Phase 0: Research & Clarification

### Unknowns Resolved

**Q1: Web framework choice (FastAPI vs Flask vs Django)?**  
**Decision**: FastAPI  
**Rationale**: 
  - Native async support (clean request handling)
  - Automatic OpenAPI docs (valuable for API exploration)
  - Type hints and Pydantic validation (aligns with Python 3.11 best practices)
  - Lightweight (no bloat for a simple REST API)
  
**Alternatives**:
  - Flask: Simpler but lacks native async, fewer type-safety guarantees
  - Django: Over-engineered for a simulation API; adds complexity without benefit

**Q2: Frontend framework (React vs Vue vs Svelte)?**  
**Decision**: React 18+  
**Rationale**:
  - Largest ecosystem (components, visualization libraries)
  - Hooks-based architecture (clean state management for simulation state)
  - TypeScript support (type safety)
  - Visualization: Recharts, D3.js readily available
  
**Alternatives**:
  - Vue: Smaller ecosystem, simpler learning curve (overkill for a portfolio project)
  - Svelte: Minimal runtime but less mature ecosystem for data visualization

**Q3: Data persistence (database vs JSON files)?**  
**Decision**: JSON files (MVP); database optional for future  
**Rationale**:
  - MVP scope: no user accounts or multi-session history needed
  - JSON simplicity: results are self-contained, portable
  - Export as JSON anyway (for research/reproducibility)
  - Database can be added later if persistence becomes critical
  
**Q4: Game visualization (canvas vs SVG vs HTML-based layout)?**  
**Decision**: SVG (Recharts for stats, custom SVG for board)  
**Rationale**:
  - SVG is responsive and accessible (semantic)
  - Recharts library (pre-built charts for statistics)
  - Board layout: simple SVG path for domino placement
  - No animation needed for MVP (board state snapshots sufficient)

**Q5: Reproducibility validation approach?**  
**Decision**: Seed tracking + replay tests + external audit capability  
**Rationale**:
  - Every game outcome includes seed
  - Tests verify same seed → identical trace
  - Results include full game trace (exportable)
  - Researchers can re-run off-line using exported trace

---

## Phase 1: Design & Contracts

### Data Model Summary

**Core Entities** (align with spec):
- **Tile** (id: tuple[int, int], pips_a: 0-6, pips_b: 0-6)
- **GameState** (hands: List[List[Tile]], boneyard: List[Tile], board: List[Tile], current_player: 0|1, scores: [int, int], round_num: int)
- **Move** (action: "play" | "draw" | "pass", tile: Tile | None)
- **Strategy** (name: str, choose_move(state, moves) -> Move)
- **GameOutcome** (winner: str, score_diff: int, turns: int, seed: int, trace: List[Event])
- **MonteCarloResult** (runs: int, win_rate_a: float, mean_score_a: float, ci_lower: float, ci_upper: float, per_run: List[GameOutcome])
- **Event** (type: str, timestamp: int, data: dict)

See [data-model.md](data-model.md) for full definitions.

### API Contracts

**Backend REST API** (FastAPI):

```
POST /api/game/run
  Request: { strategy_a: str, strategy_b: str, seed: int }
  Response: { outcome: GameOutcome, trace: List[Event] }
  
POST /api/monte-carlo/compare
  Request: { strategy_a: str, strategy_b: str, num_runs: int, start_seed: int }
  Response: { result: MonteCarloResult, export_url: str }
  
GET /api/strategies
  Response: { strategies: List[{name: str, description: str}] }
  
GET /api/health
  Response: { status: "ok", version: str }
```

See [contracts/](contracts/) for full OpenAPI/GraphQL specs.

### Frontend Pages

1. **Single Game Simulator** (`/single`):
   - Strategy selectors (A, B)
   - Seed input
   - "Run Game" button
   - Board visualization (dynamic)
   - Move history (table)
   - Outcome summary (winner, score, turns)

2. **Monte Carlo Comparison** (`/compare`):
   - Strategy selectors (A, B)
   - Number of runs slider (10-100k)
   - "Run Batch" button
   - Progress bar (animated)
   - Results: win rate, confidence interval, score differential charts
   - Export button (JSON/CSV)

3. **Results Viewer** (`/results`):
   - Upload or paste JSON result
   - Display statistics
   - Per-run details (sortable table)
   - Replayable game traces

### Quickstart for Developers

See [quickstart.md](quickstart.md) for:
- Local setup (Python venv, Node, dependencies)
- Running backend (uvicorn)
- Running frontend (Vite dev server)
- Running tests (pytest, vitest)
- Common workflows (add strategy, add API endpoint, etc.)

---

## Execution Strategy

### Phase 0 Completion: Research ✅

All unknowns researched and resolved. Technical stack finalized:
- **Backend**: Python 3.11 + FastAPI + pytest
- **Frontend**: React 18 + TypeScript + Vite + Vitest
- **Bridge**: REST API (JSON)
- **Storage**: JSON files (no database)

### Phase 1: Design & Contracts (→ This Plan)

Outputs delivered:
- ✅ Implementation Plan (this file)
- ✅ Constitution Check (PASS)
- ✅ Project Structure (finalized)
- ⏳ data-model.md (auto-generated after this step)
- ⏳ contracts/ (auto-generated after this step)
- ⏳ quickstart.md (auto-generated after this step)

### Phase 2: Task Decomposition

After plan approval:
```bash
/speckit.tasks
```

Generates `tasks.md` with:
- Setup phase (project init, deps, project structure)
- Foundational phase (base models, test fixtures, API scaffolding)
- User Story phases (per-story tasks with dependencies)
- Polish phase (documentation, integration tests, performance tuning)

---

## Success Criteria Validation

This plan satisfies all success criteria from spec:

| Criteria | Plan Address |
|----------|--------------|
| SC-001: <1s per game | Single-threaded event loop in backend |
| SC-002: <60s per 10k runs | Optimized Monte Carlo batch orchestration |
| SC-003: Tile conservation | Validated in rules module + unit tests |
| SC-004: 100% move validation | Explicit legal_moves computation in rules |
| SC-005: Reproducibility | Seed logging + replay tests |
| SC-006: 95% CIs | stats.py aggregation module |
| SC-007: 3+ strategies | greedy.py, random.py, blocking.py |
| SC-008: Game traces | Full event logging + export |
| SC-009: Paired comparisons | monte_carlo.py orchestration |
| SC-010: Code modularity | <500 LOC per module enforced in structure |

---

## Risk & Mitigation

| Risk | Mitigation |
|------|-----------|
| FastAPI learning curve | Team experience with Flask/Django; FastAPI is simpler than both |
| React state complexity (simulation state) | Custom hooks (useGameSimulation) isolate logic; test early |
| Game visualization performance | SVG is lightweight; optimize if needed using canvas later |
| Backend-frontend sync (type safety) | Generate frontend types from Pydantic (automatic TypeScript) |
| Monte Carlo timeout (long batch runs) | Async API endpoint; frontend progress updates via polling |

---

**Version**: 1.0.0 | **Status**: Ready for Phase 1 Design | **Next**: Generate data-model.md, contracts/, quickstart.md
