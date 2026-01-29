"""Monte Carlo orchestration: batch strategy comparison with statistics."""

import statistics
from typing import List
from math import sqrt

from ..models.result import GameOutcome, MonteCarloResult
from ..simulation.runner import GameRunner
from ..strategy.base import Strategy


class MonteCarloRunner:
    """
    Orchestrates Monte Carlo batch simulations for strategy comparison.
    
    Runs multiple games between two strategies and aggregates statistics:
    - Win rates
    - Score differentials
    - Confidence intervals
    """
    
    def __init__(
        self,
        strategy_a: Strategy,
        strategy_b: Strategy,
        num_runs: int = 100,
        seed: int = 42,
    ):
        """
        Initialize Monte Carlo runner.
        
        Args:
            strategy_a: First strategy
            strategy_b: Second strategy
            num_runs: Number of games to run (must be >= 10)
            seed: Base seed for reproducible runs
        """
        if num_runs < 10:
            raise ValueError(f"num_runs must be >= 10, got {num_runs}")
        
        self.strategy_a = strategy_a
        self.strategy_b = strategy_b
        self.num_runs = num_runs
        self.base_seed = seed
    
    def run(self) -> MonteCarloResult:
        """
        Run Monte Carlo batch of games and aggregate statistics.
        
        Returns:
            MonteCarloResult with aggregated stats and per-run outcomes
        """
        outcomes: List[GameOutcome] = []
        a_wins = 0
        b_wins = 0
        score_diffs = []
        
        for run_idx in range(self.num_runs):
            # Derive unique seed for each run
            run_seed = self.base_seed + run_idx
            
            # Alternate which strategy goes first for fairness
            if run_idx % 2 == 0:
                runner = GameRunner(self.strategy_a, self.strategy_b, run_seed)
            else:
                runner = GameRunner(self.strategy_b, self.strategy_a, run_seed)
            
            outcome = runner.run()
            outcomes.append(outcome)
            
            # Track winners and score differentials
            if outcome.winner == self.strategy_a.name:
                a_wins += 1
            else:
                b_wins += 1
            
            score_diffs.append(outcome.score_differential)
        
        # Calculate statistics
        win_rate_a = a_wins / self.num_runs
        win_rate_b = b_wins / self.num_runs
        mean_score_diff = statistics.mean(score_diffs) if score_diffs else 0.0
        std_dev = statistics.stdev(score_diffs) if len(score_diffs) > 1 else 0.0
        
        # Calculate 95% confidence interval (using normal approximation)
        se = std_dev / sqrt(self.num_runs) if std_dev > 0 else 0.0
        ci_lower = mean_score_diff - 1.96 * se
        ci_upper = mean_score_diff + 1.96 * se
        
        return MonteCarloResult(
            strategy_a=self.strategy_a.name,
            strategy_b=self.strategy_b.name,
            total_runs=self.num_runs,
            runs_a_wins=a_wins,
            runs_b_wins=b_wins,
            win_rate_a=win_rate_a,
            win_rate_b=win_rate_b,
            mean_score_diff_a=mean_score_diff,
            std_dev_score_diff_a=std_dev,
            ci_lower=ci_lower,
            ci_upper=ci_upper,
            per_run_outcomes=outcomes,
        )
