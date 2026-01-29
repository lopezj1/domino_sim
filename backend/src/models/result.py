"""Result models for game outcomes and Monte Carlo aggregation."""

from dataclasses import dataclass, field
from typing import Any, Dict, List

from .events import Event


@dataclass(frozen=True)
class GameOutcome:
    """
    Result of a single game simulation.
    
    Contains: winner, score differential, turn count, seed, and optional trace.
    """
    winner: str  # Strategy name of winner
    score_differential: int  # winner_score - loser_score
    turns: int  # Number of player moves
    seed: int  # RNG seed for reproducibility
    trace: List[Event] = field(default_factory=list)
    timestamp: str = ""  # ISO 8601 timestamp
    
    def __post_init__(self) -> None:
        """Validate outcome invariants."""
        if self.turns < 1:
            raise ValueError(f"turns must be >= 1, got {self.turns}")
        if self.score_differential < 0:
            raise ValueError(f"score_differential must be >= 0, got {self.score_differential}")
        if self.trace and self.trace[0].type != "deal":
            raise ValueError("Trace must start with 'deal' event")
        if self.trace and self.trace[-1].type != "game_end":
            raise ValueError("Trace must end with 'game_end' event")


@dataclass(frozen=True)
class MonteCarloResult:
    """
    Aggregated results from multiple game simulations.
    
    Contains statistics: win rates, score differentials, confidence intervals.
    """
    strategy_a: str
    strategy_b: str
    total_runs: int
    runs_a_wins: int
    runs_b_wins: int
    win_rate_a: float
    win_rate_b: float
    mean_score_diff_a: float
    std_dev_score_diff_a: float
    ci_lower: float  # 95% confidence interval lower bound
    ci_upper: float  # 95% confidence interval upper bound
    per_run_outcomes: List[GameOutcome] = field(default_factory=list)
    
    def __post_init__(self) -> None:
        """Validate result invariants."""
        if self.total_runs < 10:
            raise ValueError(f"total_runs must be >= 10, got {self.total_runs}")
        if self.runs_a_wins + self.runs_b_wins != self.total_runs:
            raise ValueError(
                f"wins must sum to total_runs: {self.runs_a_wins} + {self.runs_b_wins} != {self.total_runs}"
            )
        if not (0 <= self.win_rate_a <= 1):
            raise ValueError(f"win_rate_a must be 0-1, got {self.win_rate_a}")
        if not (0 <= self.ci_lower <= self.ci_upper <= 1):
            raise ValueError(f"CI bounds invalid: {self.ci_lower} > {self.ci_upper}")
