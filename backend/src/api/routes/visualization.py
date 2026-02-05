"""API routes for Monte Carlo visualization."""

from fastapi import APIRouter, HTTPException

from ...aggregation.monte_carlo import MonteCarloRunner
from ...strategy.greedy import GreedyStrategy
from ...strategy.random import RandomStrategy
from ...strategy.blocking import BlockingStrategy
from ...engine.rng import SeededRNG
from ..schemas.visualization import (
    MonteCarloVisualizationRequest,
    MonteCarloVisualizationResponse,
)

router = APIRouter(prefix="/visualization", tags=["visualization"])


def _get_strategy(name: str, seed: int = 42):
    """Get strategy instance by name."""
    name = name.lower()
    if name == "greedy":
        return GreedyStrategy()
    elif name == "random":
        return RandomStrategy(SeededRNG(seed))
    elif name == "blocking":
        return BlockingStrategy()
    else:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown strategy: {name}. Available: greedy, random, blocking"
        )


@router.post("/monte-carlo-paths", response_model=MonteCarloVisualizationResponse)
async def generate_monte_carlo_visualization(
    request: MonteCarloVisualizationRequest
) -> MonteCarloVisualizationResponse:
    """
    Generate Monte Carlo visualization data for convergence plotting.
    
    Returns multiple independent simulation paths showing how cumulative win rate
    converges over time. Each path demonstrates uncertainty quantification.
    
    **Usage**:
    - X-axis: game_numbers (1 to num_games)
    - Y-axis: paths (cumulative win rates, 0.0 to 1.0)
    - Multiple paths show convergence and uncertainty
    
    **Example**:
    ```json
    {
      "strategy_a": "blocking",
      "strategy_b": "random",
      "num_games": 500,
      "num_paths": 100,
      "seed": 12345
    }
    ```
    """
    try:
        # Get strategies
        strategy_a = _get_strategy(request.strategy_a, request.seed)
        strategy_b = _get_strategy(request.strategy_b, request.seed + 1)
        
        # Create Monte Carlo runner
        mc_runner = MonteCarloRunner(
            strategy_a=strategy_a,
            strategy_b=strategy_b,
            num_runs=request.num_games,
            seed=request.seed
        )
        
        # Generate visualization data
        viz_data = mc_runner.generate_visualization_data(
            num_games=request.num_games,
            num_paths=request.num_paths
        )
        
        return MonteCarloVisualizationResponse(**viz_data)
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@router.get("/strategies", response_model=dict)
async def list_available_strategies() -> dict:
    """
    List all available strategies for visualization.
    
    Returns:
        dict: Strategy names and descriptions
    """
    return {
        "strategies": [
            {
                "name": "greedy",
                "description": "Plays highest pip tiles to reduce hand score"
            },
            {
                "name": "random",
                "description": "Randomly selects from legal moves"
            },
            {
                "name": "blocking",
                "description": "Strategically blocks opponent tiles"
            }
        ]
    }
