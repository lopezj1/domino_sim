"""API routes for game run and Monte Carlo compare."""

import time
from datetime import datetime, timezone
from typing import Any, Dict

from fastapi import APIRouter, HTTPException

from ...aggregation.monte_carlo import MonteCarloRunner
from ...simulation.runner import GameRunner
from ..schemas.game import (
    EventSchema,
    GameOutcomeSchema,
    GameRunRequest,
    GameRunResponse,
    MonteCarloCompareRequest,
    MonteCarloCompareResponse,
    MonteCarloResultSchema,
)
from .visualization import _get_strategy

router = APIRouter(tags=["game"])


def _serialize_event_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Shallow-convert tuples to lists so the dict is JSON-serializable."""
    result: Dict[str, Any] = {}
    for key, value in data.items():
        if isinstance(value, tuple):
            result[key] = list(value)
        elif isinstance(value, dict):
            result[key] = _serialize_event_data(value)
        else:
            result[key] = value
    return result


@router.post("/game/run", response_model=GameRunResponse)
async def run_game(request: GameRunRequest) -> GameRunResponse:
    """
    Run a single domino game between two strategies.

    Returns the outcome and, optionally, the full event trace.
    """
    try:
        strategy_a = _get_strategy(request.strategy_a, request.seed)
        strategy_b = _get_strategy(request.strategy_b, request.seed + 1)

        game_runner = GameRunner(
            player_0_strategy=strategy_a,
            player_1_strategy=strategy_b,
            seed=request.seed,
        )
        outcome = game_runner.run()

        outcome_schema = GameOutcomeSchema(
            winner=outcome.winner,
            score_differential=outcome.score_differential,
            turns=outcome.turns,
            seed=outcome.seed,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )

        trace: list[EventSchema] = []
        if request.include_trace:
            trace = [
                EventSchema(
                    type=event.type,
                    timestamp=event.timestamp,
                    data=_serialize_event_data(event.data),
                )
                for event in outcome.trace
            ]

        return GameRunResponse(outcome=outcome_schema, trace=trace)

    except HTTPException:
        raise
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Internal error: {exc}") from exc


@router.post("/monte-carlo/compare", response_model=MonteCarloCompareResponse)
async def compare_strategies(request: MonteCarloCompareRequest) -> MonteCarloCompareResponse:
    """
    Compare two strategies using Monte Carlo simulation.

    Returns aggregated statistics and per-run outcomes.
    """
    try:
        strategy_a = _get_strategy(request.strategy_a, request.start_seed)
        strategy_b = _get_strategy(request.strategy_b, request.start_seed + 1)

        mc_runner = MonteCarloRunner(
            strategy_a=strategy_a,
            strategy_b=strategy_b,
            num_runs=request.num_runs,
            seed=request.start_seed,
        )

        t_start = time.monotonic()
        mc_result = mc_runner.run()
        execution_time = time.monotonic() - t_start

        result_schema = MonteCarloResultSchema(
            strategy_a=mc_result.strategy_a,
            strategy_b=mc_result.strategy_b,
            total_runs=mc_result.total_runs,
            runs_a_wins=mc_result.runs_a_wins,
            runs_b_wins=mc_result.runs_b_wins,
            win_rate_a=mc_result.win_rate_a,
            win_rate_b=mc_result.win_rate_b,
            mean_score_diff_a=mc_result.mean_score_diff_a,
            std_dev=mc_result.std_dev_score_diff_a,
            ci_lower=mc_result.ci_lower,
            ci_upper=mc_result.ci_upper,
            execution_time_seconds=execution_time,
        )

        per_run_outcomes = [
            GameOutcomeSchema(
                winner=o.winner,
                score_differential=o.score_differential,
                turns=o.turns,
                seed=o.seed,
                timestamp=o.timestamp,
            )
            for o in mc_result.per_run_outcomes
        ]

        return MonteCarloCompareResponse(
            result=result_schema,
            per_run_outcomes=per_run_outcomes,
        )

    except HTTPException:
        raise
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Internal error: {exc}") from exc
