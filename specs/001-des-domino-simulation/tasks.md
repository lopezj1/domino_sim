---
description: "Task list for DES Domino Simulation feature implementation"
---

# Tasks: Discrete Event Simulation (DES) for Domino Game with Monte Carlo Strategy Evaluation

**Input**: Design documents from `/specs/001-des-domino-simulation/`  
**Prerequisites**: plan.md (required), spec.md (required), data-model.md, contracts/, quickstart.md

**Note**: Tests are MANDATORY for this project per constitution (Test-First principle). Each user story includes unit, integration, and contract tests. See acceptance scenarios in spec.md for test requirements.

---

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies on incomplete tasks)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create backend project structure per plan.md in `backend/` directory
- [ ] T002 Create frontend project structure per plan.md in `frontend/` directory
- [ ] T003 [P] Initialize Python project: `backend/pyproject.toml` with dependencies (fastapi, uvicorn, pytest, dataclasses-json)
- [ ] T004 [P] Initialize Python venv and requirements file: `backend/requirements.txt` with pinned versions
- [ ] T005 [P] Create pytest configuration: `backend/pytest.ini` with test discovery and markers
- [ ] T006 [P] Initialize Node.js project: `frontend/package.json` with React, TypeScript, Vite, Vitest, Recharts dependencies
- [ ] T007 [P] Create TypeScript configuration: `frontend/tsconfig.json` with strict mode enabled
- [ ] T008 [P] Create Vite configuration: `frontend/vite.config.ts` for dev server and build
- [ ] T009 Create `.gitignore` at repository root (ignore venv/, node_modules/, __pycache__/, dist/, build/, .pytest_cache/)
- [ ] T010 Create root `Dockerfile` for backend containerization (Python 3.11 base, FastAPI setup)
- [ ] T011 Create root `docker-compose.yml` for local dev environment (backend service + frontend service)

**Checkpoint**: Backend and frontend directories exist with all dependencies installed. Commands work: `python -m pytest --version` and `npm --version`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### 2a. Core Data Models

- [ ] T012 [P] Create Tile model in `backend/src/models/tile.py` with immutable dataclass (pips_a, pips_b, id property, total_pips property)
- [ ] T013 [P] Create Move model in `backend/src/models/move.py` with immutable dataclass (action: play/draw/pass, tile: optional)
- [ ] T014 [P] Create GameState model in `backend/src/models/game_state.py` with immutable dataclass (players_hands, boneyard, board, current_player, scores, round_num, legal_moves property)
- [ ] T015 [P] Create Event model in `backend/src/models/events.py` with immutable dataclass (type: deal/play/draw/pass/round_end/game_end, timestamp, data dict)
- [ ] T016 [P] Create GameOutcome model in `backend/src/models/result.py` with immutable dataclass (winner, score_differential, turns, seed, trace, timestamp)
- [ ] T017 [P] Create MonteCarloResult model in `backend/src/models/result.py` (strategy_a, strategy_b, total_runs, win counts, rates, mean_score_diff, std_dev, ci bounds, per_run_outcomes list)

### 2b. RNG & Reproducibility Infrastructure

- [ ] T018 Create RNG manager in `backend/src/engine/rng.py` with seeded Random instance and explicit consumption tracking

### 2c. Test Fixtures & Helpers

- [ ] T019 Create test fixtures in `backend/tests/conftest.py` (fixture for standard 28-tile set, fixture for GameState factory, fixture for seed generator)
- [ ] T020 Create helper utilities in `backend/tests/helpers.py` (tile creation helpers, game state builders, assertion utilities)

### 2d. Backend API Scaffolding

- [ ] T021 Create FastAPI app in `backend/src/api/main.py` with CORS enabled and health check endpoint
- [ ] T022 [P] Create API schemas in `backend/src/api/schemas/game.py` (GameRunRequest, GameRunResponse Pydantic models)
- [ ] T023 [P] Create API schemas in `backend/src/api/schemas/monte_carlo.py` (MonteCarloRequest, MonteCarloResponse Pydantic models)
- [ ] T024 Create API routes directory structure `backend/src/api/routes/__init__.py`

### 2e. Frontend Scaffolding

- [ ] T025 Create React App structure: `frontend/src/App.tsx` with router setup and navigation
- [ ] T026 Create API client service: `frontend/src/services/api.ts` with Axios instance and typed methods
- [ ] T027 Create TypeScript types mirror: `frontend/src/services/types.ts` matching backend Pydantic schemas
- [ ] T028 Create custom hook: `frontend/src/hooks/useAPI.ts` for API calls with error handling
- [ ] T029 Create CSS foundation: `frontend/src/styles/globals.css` with Tailwind/base styles

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Model Complete Domino Game State & Rules (Priority: P1) 🎯 MVP

**Goal**: Implement complete game mechanics with state tracking, rule enforcement, and reproducibility

**Independent Test**: Verify by:
1. Initializing game with fixed seed
2. Asserting initial state (28 tiles distributed, board empty, scores 0)
3. Playing sequence of valid moves
4. Asserting state transitions preserve tile conservation
5. Re-running with same seed produces identical trace

### Tests for User Story 1 ⚠️ MANDATORY

- [ ] T030 [P] [US1] Contract test for Game initialization in `backend/tests/contract/test_game_initialization.py` (verify all 28 tiles distributed)
- [ ] T031 [P] [US1] Contract test for Move validation in `backend/tests/contract/test_move_validation.py` (verify only legal moves accepted)
- [ ] T032 [P] [US1] Contract test for State transitions in `backend/tests/contract/test_state_transitions.py` (verify state invariants after each event)
- [ ] T033 [P] [US1] Unit test for Tile model in `backend/tests/unit/test_tile.py` (creation, properties, id)
- [ ] T034 [P] [US1] Unit test for GameState model in `backend/tests/unit/test_game_state.py` (creation, legal moves computation, immutability)
- [ ] T035 [P] [US1] Unit test for Move model in `backend/tests/unit/test_move.py` (creation, validation)
- [ ] T036 [P] [US1] Unit test for Event model in `backend/tests/unit/test_events.py` (creation, type validation)
- [ ] T037 [US1] Integration test for Full game flow in `backend/tests/integration/test_full_game.py` (deal → play/draw → pass → round_end → game_end)
- [ ] T038 [US1] Integration test for Reproducibility in `backend/tests/integration/test_reproducibility.py` (same seed → identical trace 10 times)
- [ ] T039 [US1] Integration test for Tile conservation in `backend/tests/integration/test_tile_conservation.py` (invariant holds across 100 moves)

### Implementation for User Story 1

- [ ] T040 [P] [US1] Create Tile set factory in `backend/src/engine/tiles.py` (all 28 standard domino tiles)
- [ ] T041 [P] [US1] Create Tile shuffler in `backend/src/engine/tiles.py` with seeded RNG (verify same seed = same shuffle)
- [ ] T042 [P] [US1] Create Dealer in `backend/src/engine/dealer.py` (distribute 7 tiles to each player, 14 to boneyard)
- [ ] T043 [US1] Create Rules engine in `backend/src/engine/rules.py` with:
  - `is_legal_move(move, state) -> bool`
  - `get_legal_moves(state) -> List[Move]`
  - `apply_move(move, state) -> GameState` (immutable transition)
- [ ] T044 [US1] Create Scoring engine in `backend/src/engine/rules.py`:
  - `calculate_round_winner(hands) -> int` (lowest pip count)
  - `calculate_round_score(winner_idx, loser_hand) -> int` (loser's pip sum)
- [ ] T045 [US1] Create Game class in `backend/src/engine/game.py` with:
  - Event loop (authoritative control flow)
  - State immutability enforcement
  - Event sequence tracking
- [ ] T046 [US1] Implement game initialization in `backend/src/engine/game.py` (deal, set board empty, current_player=0)
- [ ] T047 [US1] Implement play move logic in `backend/src/engine/game.py` (validate, update board, change player)
- [ ] T048 [US1] Implement draw move logic in `backend/src/engine/game.py` (draw from boneyard, add to hand, change player or pass)
- [ ] T049 [US1] Implement pass logic in `backend/src/engine/game.py` (detect consecutive passes, trigger round end)
- [ ] T050 [US1] Implement round scoring logic in `backend/src/engine/game.py` (calculate scores, trigger game end if threshold reached)
- [ ] T051 [US1] Implement game end detection in `backend/src/engine/game.py` (first player to 100+ points wins)
- [ ] T052 [US1] Add validation assertions in `backend/src/engine/game.py` (tile conservation, legal move enforcement, score validity)
- [ ] T053 [US1] Add logging to game events in `backend/src/engine/game.py` (structured JSON for reproducibility)

**Checkpoint**: At this point, User Story 1 should be fully functional and independently testable. Verify: `pytest tests/ -k "US1 or test_game" -v`

---

## Phase 4: User Story 2 - Implement Pluggable Strategy Interface (Priority: P1)

**Goal**: Create strategy abstraction with 3+ concrete implementations enabling pluggable player logic

**Independent Test**: Verify by:
1. Creating abstract Strategy class
2. Implementing 3 concrete strategies (greedy, random, blocking)
3. Running same game with different strategies using same seed
4. Asserting different move choices, same game state validity

### Tests for User Story 2 ⚠️ MANDATORY

- [ ] T054 [P] [US2] Contract test for Strategy interface in `backend/tests/contract/test_strategy_interface.py` (verify all strategies implement choose_move signature)
- [ ] T055 [P] [US2] Contract test for Strategy determinism in `backend/tests/contract/test_strategy_determinism.py` (same state → same move 10 times)
- [ ] T056 [P] [US2] Unit test for GreedyStrategy in `backend/tests/unit/test_greedy_strategy.py` (highest pip logic)
- [ ] T057 [P] [US2] Unit test for RandomStrategy in `backend/tests/unit/test_random_strategy.py` (distribution of choices)
- [ ] T058 [P] [US2] Unit test for BlockingStrategy in `backend/tests/unit/test_blocking_strategy.py` (blocks opponent logic)
- [ ] T059 [US2] Integration test for Strategy substitution in `backend/tests/integration/test_strategy_substitution.py` (same game, different strategies, different outcomes valid)

### Implementation for User Story 2

- [ ] T060 [P] [US2] Create Strategy base class in `backend/src/strategy/base.py` with abstract `choose_move(state, legal_moves) -> Move`
- [ ] T061 [P] [US2] Create GreedyStrategy in `backend/src/strategy/greedy.py` (plays highest pip tile to reduce hand)
- [ ] T062 [P] [US2] Create RandomStrategy in `backend/src/strategy/random.py` (plays random legal move, uses seeded RNG)
- [ ] T063 [P] [US2] Create BlockingStrategy in `backend/src/strategy/blocking.py` (plays largest pip tile to block opponent)
- [ ] T064 [US2] Add strategy registry in `backend/src/strategy/__init__.py` mapping names to implementations
- [ ] T065 [US2] Add docstrings to all strategies in `backend/src/strategy/*.py` (explain heuristic, assumptions, limitations)

**Checkpoint**: At this point, User Story 2 should be fully functional. Verify: `pytest tests/ -k "US2 or test_strategy" -v`

---

## Phase 5: User Story 3 - Run Single Deterministic Domino Game Simulation (Priority: P1)

**Goal**: Create simulation runner with reproducible game outcomes and full result logging

**Independent Test**: Verify by:
1. Running same game 3 times with identical seed and strategies
2. Asserting identical winner, score_differential, turn_count each run
3. Running with different seeds, verifying all outcomes valid

### Tests for User Story 3 ⚠️ MANDATORY

- [ ] T066 [P] [US3] Contract test for simulate_game API in `backend/tests/contract/test_simulate_game_api.py` (correct signature and return type)
- [ ] T067 [P] [US3] Contract test for Reproducibility in `backend/tests/contract/test_reproducibility.py` (same seed → identical outcome 10x)
- [ ] T068 [P] [US3] Unit test for GameRunner in `backend/tests/unit/test_runner.py` (trace construction, outcome extraction)
- [ ] T069 [US3] Integration test for Seed variation in `backend/tests/integration/test_seed_variation.py` (different seeds → different valid outcomes)
- [ ] T070 [US3] Integration test for Trace completeness in `backend/tests/integration/test_trace_completeness.py` (trace has all events, timestamps, data)

### Implementation for User Story 3

- [ ] T071 [P] [US3] Create GameRunner in `backend/src/simulation/runner.py` with:
  - `simulate_game(strategy_a, strategy_b, seed) -> GameOutcome`
  - Event loop execution with logging
  - Outcome extraction (winner, score_diff, turns)
- [ ] T072 [US3] Implement trace building in `backend/src/simulation/runner.py` (log each event with timestamp and data)
- [ ] T073 [US3] Implement seed logging in `backend/src/simulation/runner.py` (store seed in GameOutcome)
- [ ] T074 [US3] Create outcome serialization in `backend/src/models/result.py` (GameOutcome → dict for JSON export)

**Checkpoint**: At this point, User Story 3 should be fully functional. Verify: `pytest tests/ -k "US3 or test_runner or test_reproducibility" -v`

---

## Phase 6: User Story 4 - Aggregate Monte Carlo Results Across Multiple Runs (Priority: P2)

**Goal**: Implement batch simulation orchestration with statistical aggregation and result visualization

**Independent Test**: Verify by:
1. Running 50-100 paired games
2. Computing statistics (win rate, mean score diff, std dev, 95% CI)
3. Validating math (win counts sum, rate = count/total, CI width ≤ 0.15)

### Tests for User Story 4 ⚠️ MANDATORY

- [ ] T075 [P] [US4] Contract test for monte_carlo_compare API in `backend/tests/contract/test_monte_carlo_api.py` (correct signature, return type)
- [ ] T076 [P] [US4] Contract test for Statistics computation in `backend/tests/contract/test_stats_contract.py` (math validation)
- [ ] T077 [P] [US4] Unit test for MonteCarloRunner in `backend/tests/unit/test_monte_carlo.py` (batch orchestration, seed iteration)
- [ ] T078 [P] [US4] Unit test for Statistics in `backend/tests/unit/test_stats.py` (mean, std dev, CI calculation)
- [ ] T079 [US4] Integration test for Batch comparison in `backend/tests/integration/test_batch_comparison.py` (100 runs, validate all stats)
- [ ] T080 [US4] Integration test for Result serialization in `backend/tests/integration/test_result_serialization.py` (MonteCarloResult → JSON → back)

### Implementation for User Story 4

- [ ] T081 [P] [US4] Create MonteCarloRunner in `backend/src/simulation/monte_carlo.py` with:
  - `monte_carlo_compare(strategy_a, strategy_b, num_runs, start_seed) -> MonteCarloResult`
  - Paired comparison (A vs B, B vs A) with common RNG
  - Per-run outcome collection
- [ ] T082 [P] [US4] Create Statistics aggregator in `backend/src/aggregation/stats.py` with:
  - `compute_win_rate(outcomes_a, outcomes_b) -> float`
  - `compute_mean_score_diff(outcomes) -> float`
  - `compute_std_dev(outcomes) -> float`
  - `compute_confidence_interval(win_rate, n) -> (lower, upper)` (95% CI using binomial approx)
- [ ] T083 [US4] Implement result aggregation in `backend/src/simulation/monte_carlo.py` (collect outcomes, compute stats, build MonteCarloResult)
- [ ] T084 [US4] Create result export in `backend/src/simulation/monte_carlo.py` (MonteCarloResult → JSON dict)

**Checkpoint**: At this point, all 4 user stories are complete and independently testable. Verify: `pytest tests/ -v`

---

## Phase 7: API Endpoints & Backend Integration

**Purpose**: Expose simulation logic via REST API for frontend consumption

### Contract Tests for API Endpoints ⚠️ MANDATORY

- [ ] T085 [P] Contract test for GET /api/health in `backend/tests/contract/test_health_endpoint.py`
- [ ] T086 [P] Contract test for GET /api/strategies in `backend/tests/contract/test_strategies_endpoint.py`
- [ ] T087 [P] Contract test for POST /api/game/run in `backend/tests/contract/test_game_endpoint.py`
- [ ] T088 [P] Contract test for POST /api/monte-carlo/compare in `backend/tests/contract/test_monte_carlo_endpoint.py`

### API Implementation

- [ ] T089 [US3] Implement health endpoint in `backend/src/api/routes/health.py` (GET /api/health → {status, version})
- [ ] T090 [US2] Implement strategies endpoint in `backend/src/api/routes/strategies.py` (GET /api/strategies → list of available)
- [ ] T091 [US3] Implement game run endpoint in `backend/src/api/routes/game.py` (POST /api/game/run → GameOutcome)
- [ ] T092 [US4] Implement monte carlo endpoint in `backend/src/api/routes/monte_carlo.py` (POST /api/monte-carlo/compare → MonteCarloResult)
- [ ] T093 Register routes in `backend/src/api/main.py` (include all route modules)

---

## Phase 8: Frontend Components & Pages

**Purpose**: Create interactive UI for simulation showcase

### Frontend Tests ⚠️ MANDATORY (Component tests)

- [ ] T094 [P] [US3] Component test for GameSimulator in `frontend/tests/unit/GameSimulator.test.tsx` (renders controls, handles input)
- [ ] T095 [P] [US2] Component test for StrategySelector in `frontend/tests/unit/StrategySelector.test.tsx` (dropdown, selection)
- [ ] T096 [P] [US3] Component test for GameViewer in `frontend/tests/unit/GameViewer.test.tsx` (board visualization, move display)
- [ ] T097 [P] [US4] Component test for ResultsChart in `frontend/tests/unit/ResultsChart.test.tsx` (chart rendering)
- [ ] T098 E2E test for Single Game flow in `frontend/tests/integration/single-game-flow.test.ts` (select strategies → run → see results)
- [ ] T099 E2E test for Monte Carlo flow in `frontend/tests/integration/monte-carlo-flow.test.ts` (select strategies → run batch → see stats)

### Frontend Implementation

- [ ] T100 [P] [US3] Create GameSimulator component in `frontend/src/components/GameSimulator.tsx` (layout, controls, state management)
- [ ] T101 [P] [US2] Create StrategySelector component in `frontend/src/components/StrategySelector.tsx` (dropdown, on-change handler)
- [ ] T102 [P] [US3] Create GameViewer component in `frontend/src/components/GameViewer.tsx` (SVG board layout, tile rendering)
- [ ] T103 [P] [US3] Create TraceViewer component in `frontend/src/components/TraceViewer.tsx` (move history table, event details)
- [ ] T104 [P] [US4] Create MonteCarloRunner component in `frontend/src/components/MonteCarloRunner.tsx` (num_runs slider, progress bar)
- [ ] T105 [P] [US4] Create ResultsChart component in `frontend/src/components/ResultsChart.tsx` (Recharts: win rate, score diff, CI)
- [ ] T106 [P] [US4] Create ConfidenceInterval component in `frontend/src/components/ConfidenceInterval.tsx` (CI display with bounds)
- [ ] T107 [P] [US4] Create ExportButton component in `frontend/src/components/ExportButton.tsx` (JSON/CSV export)
- [ ] T108 [US3] Create SingleGame page in `frontend/src/pages/SingleGame.tsx` (orchestrate components, handle game run)
- [ ] T109 [US4] Create MonteCarlo page in `frontend/src/pages/MonteCarlo.tsx` (orchestrate components, handle batch run)
- [ ] T110 [US4] Create Results page in `frontend/src/pages/Results.tsx` (upload/display results)
- [ ] T111 Create Home page in `frontend/src/pages/Home.tsx` (landing page, navigation links)
- [ ] T112 [P] Create useGameSimulation hook in `frontend/src/hooks/useGameSimulation.ts` (state + logic for single game)
- [ ] T113 [P] Create useMonteCarloComparison hook in `frontend/src/hooks/useMonteCarloComparison.ts` (state + logic for batch runs)
- [ ] T114 Update App router in `frontend/src/App.tsx` (routes: /, /single, /compare, /results)

---

## Phase 9: Integration & Cross-Component Testing

**Purpose**: Verify backend + frontend work together end-to-end

- [ ] T115 Backend integration test suite in `backend/tests/integration/` (all user stories together)
- [ ] T116 Frontend + Backend API integration test in `frontend/tests/integration/api-integration.test.ts` (mock API calls)
- [ ] T117 E2E test: Full single game flow in `frontend/tests/integration/full-single-game.test.ts` (UI → API → results)
- [ ] T118 E2E test: Full Monte Carlo flow in `frontend/tests/integration/full-monte-carlo.test.ts` (UI → API batch → charts)
- [ ] T119 Performance test: Game simulation <1s in `backend/tests/performance/test_game_performance.py` (100 runs averaged)
- [ ] T120 Performance test: Monte Carlo <60s/10k in `backend/tests/performance/test_monte_carlo_performance.py` (measure batch time)
- [ ] T121 Memory test: <1GB per 10k runs in `backend/tests/performance/test_memory_usage.py` (track peak memory)

---

## Phase 10: Documentation & Polish

**Purpose**: Final improvements, documentation, and deployment readiness

### Documentation

- [ ] T122 [P] Write backend API documentation in `docs/API.md` (OpenAPI/Swagger format, endpoint details, examples)
- [ ] T123 [P] Write architecture documentation in `docs/ARCHITECTURE.md` (system design, data flow, DES pattern explanation)
- [ ] T124 [P] Write deployment guide in `docs/DEPLOYMENT.md` (Docker, cloud hosting, environment setup)
- [ ] T125 Create/update `backend/README.md` (setup, testing, development workflow)
- [ ] T126 Create/update `frontend/README.md` (setup, testing, development workflow)
- [ ] T127 Create/update root `README.md` (project overview, features, quick start, live demo link)

### Code Quality & Cleanup

- [ ] T128 [P] Add type hints to all backend modules (enforce mypy --strict)
- [ ] T129 [P] Add docstrings to all functions in `backend/src/` (Google style, 100% coverage)
- [ ] T130 [P] Format Python code with Black in `backend/` (run: black --check .)
- [ ] T131 [P] Lint Python code with flake8 in `backend/` (run: flake8 src/)
- [ ] T132 [P] Format TypeScript code with Prettier in `frontend/` (run: prettier --check .)
- [ ] T133 [P] Lint TypeScript code with ESLint in `frontend/` (run: eslint src/)
- [ ] T134 Run full test suite: `pytest tests/ -v --cov=src` (expect 100% coverage in engine, strategy, simulation modules)
- [ ] T135 Run frontend tests: `npm test` (expect all components tested)

### Final Validation

- [ ] T136 Verify spec compliance in `backend/tests/acceptance/` (each acceptance scenario has a test)
- [ ] T137 Validate performance metrics (game <1s, 10k runs <60s, memory <1GB)
- [ ] T138 Validate tile conservation invariant across 1000 games in `backend/tests/invariants/test_tile_conservation.py`
- [ ] T139 Validate reproducibility: export 10 game results, re-import, re-run, verify identical outcomes
- [ ] T140 Manual testing checklist: UI works, API responds, results export/import works

### Optional Enhancements

- [ ] T141 Setup GitHub Actions for CI/CD (pytest on push, build Docker image)
- [ ] T142 Deploy backend Docker image (optional: Heroku, AWS, or local)
- [ ] T143 Deploy frontend (optional: Vercel, Netlify, or local static server)
- [ ] T144 Create demo video showing game simulator and strategy comparison
- [ ] T145 Add support for additional strategies (e.g., machine-learning-based, minimax)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: No dependencies - can start immediately
- **Phase 2 (Foundational)**: Depends on Phase 1 completion - BLOCKS all user stories
- **Phase 3 (US1)**: Depends on Phase 2 completion - Can start immediately after
- **Phase 4 (US2)**: Depends on Phase 2 completion - Can run in parallel with US1
- **Phase 5 (US3)**: Depends on Phase 2 + US1 + US2 - Combines both into simulation
- **Phase 6 (US4)**: Depends on Phase 2 + US3 - Aggregates US3 results
- **Phase 7 (API)**: Depends on Phase 2 + all user stories (3, 4, 2) - Exposes logic via REST
- **Phase 8 (Frontend)**: Depends on Phase 7 - Consumes API
- **Phase 9 (Integration)**: Depends on Phase 8 - End-to-end testing
- **Phase 10 (Polish)**: Depends on Phase 9 - Final touches

### User Story Dependencies

- **User Story 1 (US1)**: Independent - foundation for all others
- **User Story 2 (US2)**: Independent of US1 in testing, but US3 depends on both
- **User Story 3 (US3)**: Depends on US1 + US2 - combines them into simulator
- **User Story 4 (US4)**: Depends on US3 - aggregates results

### Parallel Opportunities

- **All Phase 1 tasks marked [P]** can run in parallel
- **All Phase 2 tasks marked [P]** can run in parallel (within Phase 2)
- **Phase 3 (US1) and Phase 4 (US2)**: Can run in parallel (after Phase 2)
  - Different files, no cross-story dependencies
- **All tests marked [P]** within a story can run in parallel
- **All model creation [P]** tasks can run in parallel
- **Frontend components [P]** can be built in parallel (after API scaffolding)

---

## Parallel Example: User Story 1 (US1)

```bash
# Launch all unit tests for US1 together (all marked [P]):
Task T033: Unit test for Tile model
Task T034: Unit test for GameState model
Task T035: Unit test for Move model
Task T036: Unit test for Event model

# Launch all implementation model tasks together (all marked [P]):
Task T040: Create Tile set factory
Task T041: Create Tile shuffler
Task T042: Create Dealer

# All above tasks complete in parallel, then sequential:
Task T043: Rules engine (depends on models from T040-T042)
Task T044: Scoring engine (depends on models)
Task T045+: Game class and event loop (depends on all above)
```

---

## Implementation Strategy

### MVP First (User Stories 1-3 Only)

Complete in this order:

1. **Phase 1**: Setup (infrastructure) — ~1-2 hours
2. **Phase 2**: Foundational (blocking prerequisites) — ~2-3 hours
3. **Phase 3**: User Story 1 (game mechanics) — ~4-6 hours
4. **Phase 4**: User Story 2 (strategies) — ~2-3 hours
5. **Phase 5**: User Story 3 (simulation runner) — ~2-3 hours

**Checkpoint**: At this point, you have a fully functional backend with game simulation, 3 strategies, and reproducibility. Total: ~11-17 hours.

**MVP Demo Capability**: 
```bash
from backend.src.simulation.runner import simulate_game
from backend.src.strategy.greedy import GreedyStrategy
from backend.src.strategy.random import RandomStrategy

outcome = simulate_game(GreedyStrategy(), RandomStrategy(), seed=42)
print(f"Winner: {outcome.winner}, Score: {outcome.score_differential}, Moves: {outcome.turns}")
```

### Incremental Delivery (Add User Story 4)

6. **Phase 6**: User Story 4 (Monte Carlo batch) — ~2-3 hours

**Checkpoint**: Now you can compare strategies statistically.

### Full Stack (Add Frontend)

7. **Phase 7**: API Endpoints — ~2 hours
8. **Phase 8**: Frontend Components — ~6-8 hours
9. **Phase 9**: Integration & Testing — ~2-3 hours
10. **Phase 10**: Polish & Documentation — ~2-3 hours

**Total**: ~25-35 hours for complete MVP with webapp

### Parallel Team Strategy

With multiple developers:

1. Developer A starts Phase 1 + Phase 2 (infrastructure)
2. After Phase 2 complete:
   - Developer A: Phase 3 (US1 - game mechanics)
   - Developer B: Phase 4 (US2 - strategies)
   - Developer C: Frontend scaffolding (partial Phase 8)
3. After US1 + US2 complete:
   - Developer A: Phase 5 (US3 - simulation)
   - Developer B: Phase 6 (US4 - Monte Carlo)
   - Developer C: Phase 7 (API) + Phase 8 (Frontend)
4. All: Phase 9 (Integration) and Phase 10 (Polish) together

---

## Notes

- **[P] tasks**: Different files, no dependencies - safe to run in parallel
- **[Story] labels**: Map task to specific user story for traceability
- **Tests marked ⚠️ MANDATORY**: These are NON-OPTIONAL per constitution (Test-First principle)
- **Each user story** should be independently completable and testable
- **Verify tests fail** before implementing (TDD)
- **Commit after each task** or logical group
- **Stop at any checkpoint** (after US1, US2, US3, or US4) to validate story independently
- **Performance targets**: Game <1s, 10k runs <60s, memory <1GB
- **Avoid**: Vague tasks, same-file conflicts between parallel tasks, cross-story dependencies that break independence

---

**Version**: 1.0.0 | **Created**: 2025-01-29 | **Status**: Ready for Implementation
