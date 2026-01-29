# Feature Specification: Discrete Event Simulation (DES) for Domino Game with Monte Carlo Strategy Evaluation

**Feature Branch**: `001-des-domino-simulation`  
**Created**: 2025-01-29  
**Status**: Draft  
**Input**: Build a Python codebase that models the game of Domino as a discrete event simulation (DES) and evaluates fixed player strategies using Monte Carlo simulation.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Model Complete Domino Game State & Rules (Priority: P1)

A researcher needs to model a complete domino game with precise state tracking and rule enforcement so that strategy evaluation results are scientifically valid. The game state must capture tiles, hands, board layout, and scoring, advancing only through discrete events.

**Why this priority**: This is the foundation—all other stories depend on a correct, testable game model. Without accurate state and rules, strategy evaluations are meaningless.

**Independent Test**: Can be fully tested by:
1. Initializing a game with a fixed seed
2. Verifying initial state (shuffled tiles, dealt hands, empty board, correct scores)
3. Playing a deterministic sequence of moves
4. Validating state transitions match expected game rules (tile count conservation, valid moves only, score calculation)

**Acceptance Scenarios**:

1. **Given** a new game with fixed seed, **When** initialized, **Then** all 28 tiles are distributed (player hands + boneyard), board is empty, current player is known, scores are 0.
2. **Given** a game state with legal moves available, **When** a player plays a tile, **Then** tile is removed from hand, added to board layout, current player changes, state is valid.
3. **Given** a game state where a player has no legal plays, **When** player draws from boneyard, **Then** tile is added to hand, current player changes if draw succeeds, or pass occurs if boneyard is empty.
4. **Given** a pass event, **When** consecutive players cannot play, **Then** round ends and scores are calculated (pips in losing hand count as points for winner).
5. **Given** multiple rounds played sequentially, **When** a player reaches target score, **Then** game ends and final winner is determined.
6. **Given** any game sequence, **When** queried, **Then** all previous states are reproducible with the same seed.

---

### User Story 2 - Implement Pluggable Strategy Interface (Priority: P1)

A researcher needs to define strategy contracts so they can swap between different player strategies without modifying core simulation logic. Strategies should be pure functions of game state, enabling reproducible comparison.

**Why this priority**: Strategy pluggability is critical for comparing multiple strategies fairly. Without a clear interface, the codebase becomes tightly coupled and hard to extend.

**Independent Test**: Can be fully tested by:
1. Implementing 2-3 concrete strategies (e.g., greedy-highest-pip, random-legal-move)
2. Running the same game with different strategies using the same seed
3. Verifying each strategy produces different move choices but same game state validity

**Acceptance Scenarios**:

1. **Given** a Strategy interface defined, **When** implemented by concrete strategies, **Then** each strategy has method `choose_move(game_state, legal_moves) -> Move`.
2. **Given** a game state and list of legal moves, **When** strategy is called, **Then** returned move is always one of the legal moves.
3. **Given** two runs with same seed and same strategy, **When** executed, **Then** move choices are identical (determinism verified).
4. **Given** two runs with same seed but different strategies, **When** executed, **Then** move choices may differ but game state progression is valid in both cases.
5. **Given** a strategy implementation, **When** documented with docstring, **Then** assumptions and heuristic explanation are provided (e.g., "chooses highest pip sum to reduce hand size").

---

### User Story 3 - Run Single Deterministic Domino Game Simulation (Priority: P1)

A researcher needs a function to run one complete game between two strategies with a fixed seed so that individual game outcomes can be validated and paired comparisons are reproducible.

**Why this priority**: Single-game simulation is the atomic unit of Monte Carlo evaluation. Without reliable single-game execution, batch results are meaningless.

**Independent Test**: Can be fully tested by:
1. Running the same game 3 times with identical seed and strategies
2. Verifying identical winner, score differential, and turn count each time
3. Running with different seeds and verifying different outcomes (but all valid)

**Acceptance Scenarios**:

1. **Given** two strategies and a seed, **When** `simulate_game(strategy_a, strategy_b, seed)` is called, **Then** function returns outcome dict with winner, score_differential, turn_count.
2. **Given** the same seed and strategies, **When** function runs multiple times, **Then** returned outcomes are identical (reproducible).
3. **Given** different seeds with same strategies, **When** function runs, **Then** different outcomes are possible but all games are valid (correct rule enforcement).
4. **Given** a game outcome, **When** queried, **Then** outcome includes: winner (strategy name), score_differential (winner score - loser score), turn_count (number of moves made).
5. **Given** a simulation run, **When** logged, **Then** seed, strategy names, and full game trace are included for auditability.

---

### User Story 4 - Aggregate Monte Carlo Results Across Multiple Runs (Priority: P2)

A researcher needs to run many independent simulations with paired comparisons and compute statistics so they can compare strategy performance with confidence intervals.

**Why this priority**: Monte Carlo aggregation is the primary analysis tool; enables statistical validation of strategy differences.

**Independent Test**: Can be fully tested by:
1. Running 10-20 paired games with fixed seeds
2. Computing win rate, mean score differential, and variance
3. Verifying statistics are mathematically consistent (e.g., win counts sum to total runs)

**Acceptance Scenarios**:

1. **Given** a list of seeds and two strategies, **When** `monte_carlo_comparison(strategy_a, strategy_b, seeds)` is called, **Then** function runs each seed with both strategy pairs and returns aggregated results.
2. **Given** Monte Carlo results, **When** queried, **Then** results include: total_runs, win_count_a, win_count_b, win_rate_a, mean_score_diff_a, variance_score_diff_a, std_dev_score_diff_a.
3. **Given** results from 20+ runs, **When** statistics are computed, **Then** 95% confidence interval for win rate is calculated and included.
4. **Given** results object, **When** serialized, **Then** output is structured JSON or pandas DataFrame-compatible dict with all statistics and per-run details preserved.
5. **Given** paired seeds (same seed, swapped strategy positions), **When** comparison is run, **Then** results enable quantification of strategy-order effects or confirmation of strategy dominance.

---

### Edge Cases

- What happens when a boneyard is exhausted and a player has no legal plays? (Result: pass, and if all players pass, round ends)
- How does the system handle a game where a player's opening hand includes all doubles or all high pips? (Result: valid game, strategy must adapt)
- What if two strategies result in identical move choices? (Result: game proceeds normally; no special handling needed, outcome is deterministic per seed)
- What happens if a Monte Carlo batch runs with too few seeds (<5)? (Result: results are valid but confidence intervals are wide; user is warned in documentation)
- Can strategies access information about opponent's hand? (Result: No—strategies only see observable state: opponent hand size, board, boneyard size, scores)

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST support 28 standard domino tiles (double-0 through double-6, each with two faces showing 0-6 pips).
- **FR-002**: System MUST shuffle tiles deterministically using an injected RNG seeded with a provided integer seed.
- **FR-003**: System MUST deal tiles to 2 players (7 tiles each) and initialize boneyard (remaining 14 tiles) in a single deterministic deal operation.
- **FR-004**: System MUST validate all moves against current game state (tile ownership, legal board connections, tile availability).
- **FR-005**: System MUST enforce rule: a tile can only be played if it matches (by pip count) one end of the current board line.
- **FR-006**: System MUST track board layout as a sequence of tiles, with known endpoints for determining legal moves.
- **FR-007**: System MUST support draw operations from boneyard when a player has no legal plays.
- **FR-008**: System MUST detect round end: when no more plays possible and boneyard exhausted, or when first player reaches target score (target is configurable; default 100 or first to end with empty hand).
- **FR-009**: System MUST calculate round score: losing player's hand pip count goes to winner; multiple players: lowest hand score wins round.
- **FR-010**: System MUST support Strategy interface with signature `choose_move(game_state: GameState, legal_moves: List[Move]) -> Move`.
- **FR-011**: System MUST ensure all Strategy implementations are deterministic (same state → same move choice).
- **FR-012**: System MUST provide `simulate_game(strategy_a, strategy_b, seed)` function returning outcome with winner, score_differential, turn_count.
- **FR-013**: System MUST preserve reproducibility: identical seed + strategies → identical game outcome.
- **FR-014**: System MUST support Monte Carlo orchestration: accept list of seeds and run paired comparisons (A vs B, B vs A) with common random numbers.
- **FR-015**: System MUST aggregate results: win counts, win rates, score differentials, variance, and confidence intervals (95%).
- **FR-016**: System MUST serialize results to structured JSON with per-run details and aggregate statistics.
- **FR-017**: System MUST log game traces (event sequence, player moves, state snapshots) for debugging and result validation.
- **FR-018**: System MUST support multiple concrete strategy implementations (greedy, blocking, random) as examples.

### Key Entities

- **Tile**: Represents a domino with two faces (each 0-6 pips). Immutable. Identified by sorted tuple (pip_a, pip_b).
- **GameState**: Current game configuration including player hands (list of tiles), boneyard (list of tiles), board layout (ordered list of tiles), current player, scores, and round number. Immutable snapshot.
- **Move**: Represents a player action (play tile, draw, pass) with the action type and tile (if applicable).
- **Strategy**: Abstract interface defining `choose_move(state, legal_moves) -> Move`. Implementations are pure functions of observable game state.
- **GameOutcome**: Result of one simulation run: winner (strategy name), score_differential, turn_count, seed, game_trace (optional).
- **MonteCarloResult**: Aggregated results across multiple runs: total_runs, win_count_a, win_count_b, win_rate_a, mean_score_diff, variance, std_dev, ci_lower, ci_upper, per_run_outcomes.
- **GameTrace**: Sequence of events (deal, play_tile, draw, pass, end_round, end_game) with timestamps (event index) and state snapshots.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Single domino game simulation completes in under 1 second on standard hardware (deterministic reproducibility verified: same seed → identical outcome every run).
- **SC-002**: Monte Carlo batch of 10,000 paired games completes in under 60 seconds on standard hardware with less than 1GB memory footprint.
- **SC-003**: All game state transitions preserve tile conservation invariant: total tiles = 28 (player hands + board + boneyard) across all events.
- **SC-004**: Legal move validation achieves 100% accuracy: no invalid moves accepted, no valid moves rejected (verified via unit test suite covering board layout edge cases).
- **SC-005**: Strategy reproducibility: 100 repeated runs with same seed and strategy produce identical move sequences and game outcomes.
- **SC-006**: Monte Carlo results include 95% confidence intervals with width <= 15 percentage points for strategy win rate over 100+ runs.
- **SC-007**: 3+ concrete strategy implementations (greedy, blocking, random) are documented with clear docstrings explaining decision logic.
- **SC-008**: Game outcomes include seed, strategy names, and full trace enabling external reproduction of any game without code access (trace completeness).
- **SC-009**: Monte Carlo orchestration enables fair comparison: paired runs with common random numbers (same seed for A vs B and B vs A) to isolate strategy effect from luck.
- **SC-010**: Code is readable and modular with separation of concerns: <500 LOC per module (game state, rules, strategy, simulation, aggregation) and zero circular dependencies.
