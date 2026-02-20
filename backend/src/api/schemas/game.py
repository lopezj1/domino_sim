"""Pydantic schemas for game run and Monte Carlo compare API endpoints."""

from typing import Any, Dict, List
from pydantic import BaseModel, Field


class GameRunRequest(BaseModel):
    """Request to run a single game."""

    strategy_a: str = Field(..., description="First strategy name (greedy, random, blocking)")
    strategy_b: str = Field(..., description="Second strategy name (greedy, random, blocking)")
    seed: int = Field(default=42, description="RNG seed for reproducibility")
    include_trace: bool = Field(default=False, description="Include full event trace in response")


class EventSchema(BaseModel):
    """A discrete simulation event."""

    type: str
    timestamp: int
    data: Dict[str, Any]


class GameOutcomeSchema(BaseModel):
    """Result of a single game."""

    winner: str
    score_differential: int
    turns: int
    seed: int
    timestamp: str


class GameRunResponse(BaseModel):
    """Response for a single game run."""

    outcome: GameOutcomeSchema
    trace: List[EventSchema] = Field(default_factory=list)


class MonteCarloCompareRequest(BaseModel):
    """Request to compare two strategies via Monte Carlo simulation."""

    strategy_a: str = Field(..., description="First strategy name (greedy, random, blocking)")
    strategy_b: str = Field(..., description="Second strategy name (greedy, random, blocking)")
    num_runs: int = Field(
        default=100,
        ge=10,
        le=100000,
        description="Number of games to simulate (10–100000)",
    )
    start_seed: int = Field(default=1000, description="Base seed for reproducibility")


class MonteCarloResultSchema(BaseModel):
    """Aggregated Monte Carlo results."""

    strategy_a: str
    strategy_b: str
    total_runs: int
    runs_a_wins: int
    runs_b_wins: int
    win_rate_a: float
    win_rate_b: float
    mean_score_diff_a: float
    std_dev: float
    ci_lower: float
    ci_upper: float
    execution_time_seconds: float


class MonteCarloCompareResponse(BaseModel):
    """Response for Monte Carlo strategy comparison."""

    result: MonteCarloResultSchema
    per_run_outcomes: List[GameOutcomeSchema]
