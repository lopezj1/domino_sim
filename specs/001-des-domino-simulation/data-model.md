# Data Model: DES Domino Simulation

**Feature**: 001-des-domino-simulation | **Date**: 2025-01-29

This document defines all core entities, their relationships, invariants, and state transitions.

---

## Core Entities

### 1. Tile

Represents a single domino tile with two faces.

```python
class Tile:
    pips_a: int       # 0-6
    pips_b: int       # 0-6
    
    @property
    def id(self) -> tuple[int, int]:
        """Canonical tile ID: (min, max)"""
        return (min(self.pips_a, self.pips_b), max(self.pips_a, self.pips_b))
    
    @property
    def total_pips(self) -> int:
        return self.pips_a + self.pips_b
```

**Invariants**:
- `0 <= pips_a <= 6`
- `0 <= pips_b <= 6`
- Total of 28 unique tiles in full set (0-0, 0-1, ..., 6-6)

**Immutable**: Yes

---

### 2. Move

Represents a player action.

```python
class Move:
    action: Literal["play", "draw", "pass"]
    tile: Tile | None
    
    # action="play" => tile must be provided
    # action="draw" => tile is None (drawn from boneyard)
    # action="pass" => tile is None
```

**Invariants**:
- `action="play"` ⟹ `tile is not None`
- `action="draw"` ⟹ `tile is None`
- `action="pass"` ⟹ `tile is None`

**Immutable**: Yes

---

### 3. GameState

Immutable snapshot of current game state.

```python
class GameState:
    players_hands: tuple[tuple[Tile, ...], tuple[Tile, ...]]
    boneyard: tuple[Tile, ...]
    board: tuple[Tile, ...]
    current_player: Literal[0, 1]
    scores: tuple[int, int]
    round_num: int
    
    @property
    def legal_moves(self) -> list[Move]:
        """Compute legal moves for current player."""
        # Play: any tile matching board endpoints
        # Draw: if boneyard non-empty and no legal plays
        # Pass: if boneyard empty and no legal plays
```

**Invariants**:
- `sum(len(h) + len(boneyard) + len(board) for h in players_hands) == 28`  ← Tile conservation
- `all(s >= 0 for s in scores)`
- `round_num >= 1`
- `board` is empty OR valid sequence (tiles match endpoints)

**Immutable**: Yes (all fields are tuples/immutable)

---

### 4. Event

Represents a discrete event in the simulation.

```python
class Event:
    type: Literal["deal", "play", "draw", "pass", "round_end", "game_end"]
    timestamp: int              # Event index (0, 1, 2, ...)
    data: dict
    
    # Example:
    # Event(type="play", timestamp=3, data={"player": 0, "tile": Tile(2, 5)})
    # Event(type="round_end", timestamp=15, data={"winner": 1, "score": 5})
```

**Invariants**:
- `timestamp >= 0`
- `data` contains event-specific fields (documented below)

**Immutable**: Yes

---

### 5. Strategy

Abstract interface for player strategies.

```python
class Strategy(ABC):
    @property
    def name(self) -> str:
        """Strategy name (e.g., "greedy", "random")."""
        ...
    
    @abstractmethod
    def choose_move(self, state: GameState, legal_moves: list[Move]) -> Move:
        """
        Deterministic decision function.
        
        Args:
            state: Current game state (observable only)
            legal_moves: List of legal moves available
        
        Returns:
            One of the legal_moves
        
        Invariant: Same state + legal_moves → same move returned
        """
        ...
```

**Invariants**:
- Strategy implementation is deterministic (pure function of state)
- Returned move is always in `legal_moves`
- Strategy only sees observable state (opponent hand size, not contents)

**Immutable**: Yes (strategies are stateless)

---

### 6. GameOutcome

Result of a single game simulation.

```python
class GameOutcome:
    winner: str                 # Strategy name of winner
    score_differential: int     # winner_score - loser_score
    turns: int                  # Number of player moves made
    seed: int                   # RNG seed used
    trace: list[Event]          # Full event sequence
    timestamp: str              # ISO 8601 timestamp of run
```

**Invariants**:
- `turns >= 1`
- `score_differential >= 0` (winner must have higher score)
- `trace[0].type == "deal"`
- `trace[-1].type == "game_end"`
- `len(trace) > 0`

**Immutable**: Yes

---

### 7. MonteCarloResult

Aggregated results from multiple runs.

```python
class MonteCarloResult:
    strategy_a: str
    strategy_b: str
    total_runs: int
    runs_a_wins: int            # Games where strategy A won
    runs_b_wins: int            # Games where strategy B won
    win_rate_a: float           # runs_a_wins / total_runs
    win_rate_b: float           # runs_b_wins / total_runs
    mean_score_diff_a: float    # Mean of score_differential for A
    std_dev_score_diff_a: float
    ci_lower: float             # 95% CI lower bound for win_rate_a
    ci_upper: float             # 95% CI upper bound for win_rate_a
    per_run_outcomes: list[GameOutcome]  # All individual game results
```

**Invariants**:
- `runs_a_wins + runs_b_wins == total_runs`
- `win_rate_a + win_rate_b == 1.0` (rounded)
- `ci_lower <= win_rate_a <= ci_upper`
- `ci_upper - ci_lower <= 0.15` (for 95% CI over 100+ runs)

**Immutable**: Yes (lists are tuples internally)

---

## State Transitions

### Game Lifecycle

```
[Start]
  ↓
[Deal] → Initial hands dealt, boneyard populated
  ↓
[Play/Draw/Pass loop]
  Play: Player plays tile matching board endpoint
  Draw: Player draws from boneyard
  Pass: Player cannot play or draw
  ↓ (Round continues until all players have empty hands or pass)
[Round End] → Scores calculated, new round begins
  ↓ (Repeat until a player reaches target score)
[Game End] → Winner declared
  ↓
[End]
```

### Event Sequence Example

```
Event 0: deal
         data: {players_hands: [7 tiles, 7 tiles], boneyard: 14 tiles}

Event 1: play
         data: {player: 0, tile: Tile(6, 5)}

Event 2: play
         data: {player: 1, tile: Tile(5, 3)}

Event 3: play
         data: {player: 0, tile: Tile(3, 2)}

...

Event N: round_end
         data: {winner: 0, points: 12}

Event N+1: play (new round)
...

Event M: game_end
         data: {winner: 0}
```

---

## Relationships

```
Tile
  (used in)
  ├── GameState.players_hands[]
  ├── GameState.boneyard[]
  ├── GameState.board[]
  └── Move.tile

GameState
  (immutable snapshot)
  ├── Event.data (for state-related events)
  └── Strategy.choose_move() (input)

Move
  ├── Strategy.choose_move() (output)
  └── Event.data (for play/draw/pass events)

Strategy
  └── GameOutcome.winner (strategy name)

Event
  └── GameOutcome.trace (sequence of events)

GameOutcome
  └── MonteCarloResult.per_run_outcomes (aggregated)
```

---

## Validation Rules

### Tile Shuffling
- Input: 28 tiles, seed (int)
- Output: Shuffled list of 28 tiles
- Process: Random.Random(seed).shuffle(tiles)
- Invariant: All 28 unique tiles present, same order given same seed

### Move Legality
- Play is legal if: tile in player's hand AND (board empty OR tile.pips match endpoint)
- Draw is legal if: boneyard non-empty AND no legal plays
- Pass is legal if: boneyard empty AND no legal plays

### Score Calculation (per round)
- Winner: player with lowest hand pip count (or first to empty hand)
- Points: loser's hand pip sum goes to winner
- New round: hands dealt from boneyard, board reset

### Game End
- Trigger: Player reaches target score (default 100)
- Winner: Player with highest score

---

## Type Definitions (Python)

```python
from dataclasses import dataclass
from typing import Literal, NewType

Pip = NewType('Pip', int)        # 0-6
PlayerId = NewType('PlayerId', int)  # 0 or 1

@dataclass(frozen=True)
class Tile:
    pips_a: Pip
    pips_b: Pip
    ...

@dataclass(frozen=True)
class Move:
    action: Literal["play", "draw", "pass"]
    tile: Tile | None
    ...

@dataclass(frozen=True)
class GameState:
    players_hands: tuple[tuple[Tile, ...], tuple[Tile, ...]]
    boneyard: tuple[Tile, ...]
    board: tuple[Tile, ...]
    current_player: PlayerId
    scores: tuple[int, int]
    round_num: int
    ...

@dataclass(frozen=True)
class Event:
    type: Literal["deal", "play", "draw", "pass", "round_end", "game_end"]
    timestamp: int
    data: dict
    ...

@dataclass(frozen=True)
class GameOutcome:
    winner: str
    score_differential: int
    turns: int
    seed: int
    trace: list[Event]
    timestamp: str
    ...

@dataclass(frozen=True)
class MonteCarloResult:
    strategy_a: str
    strategy_b: str
    total_runs: int
    runs_a_wins: int
    runs_b_wins: int
    win_rate_a: float
    win_rate_b: float
    mean_score_diff_a: float
    std_dev_score_diff_a: float
    ci_lower: float
    ci_upper: float
    per_run_outcomes: list[GameOutcome]
    ...
```

---

**Version**: 1.0.0 | **Status**: Design Phase 1
