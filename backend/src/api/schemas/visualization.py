"""Pydantic schemas for Monte Carlo visualization API."""

from typing import List
from pydantic import BaseModel, Field


class MonteCarloVisualizationRequest(BaseModel):
    """Request for Monte Carlo visualization data."""
    
    strategy_a: str = Field(
        ...,
        description="First strategy name (greedy, random, blocking)",
        example="blocking"
    )
    strategy_b: str = Field(
        ...,
        description="Second strategy name (greedy, random, blocking)",
        example="random"
    )
    num_games: int = Field(
        default=500,
        ge=50,
        le=10000,
        description="Number of games per simulation path"
    )
    num_paths: int = Field(
        default=100,
        ge=10,
        le=500,
        description="Number of independent simulation paths to generate"
    )
    seed: int = Field(
        default=42,
        description="Base seed for reproducibility"
    )


class MonteCarloVisualizationResponse(BaseModel):
    """Response containing Monte Carlo visualization data."""
    
    strategy_a: str
    strategy_b: str
    total_games: int
    num_paths: int
    game_numbers: List[int] = Field(
        ...,
        description="X-axis values: [1, 2, 3, ..., total_games]"
    )
    paths: List[List[float]] = Field(
        ...,
        description="Y-axis values: num_paths lists of cumulative win rates"
    )
    final_win_rate_a: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Final win rate for strategy A"
    )
    final_win_rate_b: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Final win rate for strategy B"
    )
    ci_lower: float = Field(
        ...,
        description="95% confidence interval lower bound"
    )
    ci_upper: float = Field(
        ...,
        description="95% confidence interval upper bound"
    )
    convergence_std: float = Field(
        ...,
        description="Standard deviation of final path values"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "strategy_a": "blocking",
                "strategy_b": "random",
                "total_games": 500,
                "num_paths": 100,
                "game_numbers": [1, 2, 3, "..."],
                "paths": [[0.0, 0.5, 0.67, "..."], ["..."]],
                "final_win_rate_a": 0.578,
                "final_win_rate_b": 0.422,
                "ci_lower": 0.52,
                "ci_upper": 0.64,
                "convergence_std": 0.045
            }
        }
