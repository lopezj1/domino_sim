# Domino Simulation Constitution

## Core Principles

### I. Model-Driven Architecture
The simulation engine is organized around data models that cleanly separate concerns: Game state, Player strategies, Event queue, and Result aggregation. Each model MUST be independently testable and documented with clear contracts. Models are immutable where possible to ensure reproducibility across Monte Carlo runs.

### II. Discrete Event Simulation (DES) Pattern
Event handling MUST follow strict DES semantics: events ordered by timestamp, deterministic processing, and no race conditions. The event loop is the authoritative control flow. All game mechanics (player moves, game state transitions, outcome determination) manifest as discrete events with well-defined pre/post-conditions.

### III. Strategy Pluggability
Player strategies MUST implement a common interface allowing arbitrary strategy substitution without modifying core simulation code. Strategies are pure functions of observable game state (hand, boneyard, board layout, opponent info). All strategy implementations MUST be independently testable and include docstring specifications of assumptions and behavior.

### IV. Reproducibility & Randomness Control
Monte Carlo runs MUST be deterministic given a fixed random seed. Random number generation is controlled at the Simulation orchestrator level. All random decisions (drawing tiles, strategy randomness if any) explicitly consume RNG state. Random seeds MUST be logged with results for result replication.

### V. Validation & Correctness (Test-First)
Test-first discipline is NON-NEGOTIABLE for game rules, strategy evaluation, and result aggregation. Unit tests verify model contracts and invariants (e.g., total tiles constant, valid move enforcement). Integration tests verify end-to-end game traces and strategy performance metrics. No feature accepted without green tests.

### VI. Observable Simulation Runs
All simulation state transitions and outcomes MUST be logged with sufficient detail to support debugging, result auditing, and scientific reproducibility. Logs capture: event sequence, player actions, game state snapshots, final statistics. Output defaults to structured JSON for machine parsing; human-readable summaries available on demand.

## Technical Stack & Constraints

- **Language**: Python 3.11+ (type hints required; mypy type-checking enforced)
- **Testing**: pytest with fixtures for game state setup and replay
- **Randomness**: `random.Random` with explicit seed management
- **Performance**: Monte Carlo batches MUST complete in <60s per 10k runs on standard hardware; memory footprint <1GB per run batch
- **No external game engines**: Rules, state, and strategy logic implemented in-house for full transparency and reproducibility

## Development Workflow

- All new features/bug fixes start with failing tests (Red → Green → Refactor)
- Game rule changes require updating both rules module AND validation test suite
- Strategy implementations come with reference docstrings and benchmark results
- Simulation results MUST include run metadata (seed, player count, strategy names, tile distribution) for external reproducibility

## Governance

**Amendment Procedure**: Constitution changes require re-validation of all existing tests and a summary of impacted modules.

**Versioning**: MAJOR version for backward-incompatible rule/model changes; MINOR for new strategies or metrics; PATCH for fixes/clarifications.

**Compliance Review**: All PRs checked that:
- Tests cover new game mechanics / strategy logic
- Model invariants documented and validated
- Randomness sourcing is explicit and seedable
- Results include sufficient metadata for reproducibility

**Version**: 1.0.0 | **Ratified**: 2025-01-29 | **Last Amended**: 2025-01-29
