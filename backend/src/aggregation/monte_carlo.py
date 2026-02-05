"""Monte Carlo orchestration: batch strategy comparison with statistics."""

import statistics
from typing import List, Optional
from math import sqrt

from ..models.result import GameOutcome, MonteCarloResult
from ..simulation.runner import GameRunner
from ..strategy.base import Strategy

try:
    import matplotlib.pyplot as plt
    import numpy as np
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False


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
    
    def generate_visualization_data(
        self,
        num_games: int = 500,
        num_paths: int = 100,
    ) -> dict:
        """
        Generate Monte Carlo visualization data for frontend rendering.
        
        Returns data structure suitable for plotting convergence paths:
        - X-axis: game numbers (1 to num_games)
        - Y-axis: cumulative win rate for strategy A per path
        - Multiple independent paths demonstrate uncertainty/convergence
        
        Args:
            num_games: Number of games per simulation path
            num_paths: Number of independent paths to generate
        
        Returns:
            dict with keys:
                - strategy_a: str
                - strategy_b: str
                - total_games: int
                - num_paths: int
                - game_numbers: list[int]
                - paths: list[list[float]]  (cumulative win rates)
                - final_win_rate_a: float
                - final_win_rate_b: float
                - ci_lower: float
                - ci_upper: float
                - convergence_std: float
        """
        if num_paths < 10:
            raise ValueError(f"num_paths must be >= 10, got {num_paths}")
        if num_games < 50:
            raise ValueError(f"num_games must be >= 50, got {num_games}")
        
        paths = []
        final_rates = []
        
        for path_idx in range(num_paths):
            path_seed = self.base_seed + path_idx * 10000
            cumulative_wins = []
            wins = 0
            
            # Simulate a path
            for game_idx in range(num_games):
                run_seed = path_seed + game_idx
                
                if game_idx % 2 == 0:
                    runner = GameRunner(self.strategy_a, self.strategy_b, run_seed)
                else:
                    runner = GameRunner(self.strategy_b, self.strategy_a, run_seed)
                
                outcome = runner.run()
                
                if outcome.winner == self.strategy_a.name:
                    wins += 1
                
                # Calculate cumulative win rate
                cumulative_win_rate = wins / (game_idx + 1)
                cumulative_wins.append(cumulative_win_rate)
            
            paths.append(cumulative_wins)
            final_rates.append(cumulative_wins[-1])
        
        # Calculate statistics
        final_win_rate_a = statistics.mean(final_rates)
        final_win_rate_b = 1.0 - final_win_rate_a
        convergence_std = statistics.stdev(final_rates) if len(final_rates) > 1 else 0.0
        
        # 95% CI using standard error
        se = convergence_std / sqrt(num_paths) if convergence_std > 0 else 0.0
        ci_lower = final_win_rate_a - 1.96 * se
        ci_upper = final_win_rate_a + 1.96 * se
        
        return {
            "strategy_a": self.strategy_a.name,
            "strategy_b": self.strategy_b.name,
            "total_games": num_games,
            "num_paths": num_paths,
            "game_numbers": list(range(1, num_games + 1)),
            "paths": paths,
            "final_win_rate_a": final_win_rate_a,
            "final_win_rate_b": final_win_rate_b,
            "ci_lower": max(0.0, ci_lower),  # Clamp to valid range
            "ci_upper": min(1.0, ci_upper),
            "convergence_std": convergence_std,
        }
    
    def plot_monte_carlo_paths(
        self,
        result: MonteCarloResult,
        num_paths: int = 100,
        figsize: tuple = (12, 8),
        alpha: float = 0.3,
        save_path: Optional[str] = None,
    ) -> None:
        """
        Plot Monte Carlo simulation paths showing convergence and uncertainty.
        
        Similar to financial Monte Carlo visualization, this shows:
        - X-axis: Game number (replication)
        - Y-axis: Cumulative win rate for strategy A (0-1 scale)
        - Multiple paths from independent simulation runs
        
        This visualization demonstrates:
        1. Convergence: Paths narrow as more games are played
        2. Uncertainty: Wide spread early, tight spread later
        3. Final estimate: All paths converge toward true win rate
        
        Args:
            result: MonteCarloResult from run()
            num_paths: Number of simulation paths to plot (default 100)
            figsize: Figure size (width, height)
            alpha: Line transparency (0-1)
            save_path: Optional path to save figure (e.g., 'plot.png')
        
        Raises:
            ImportError: If matplotlib is not installed
            ValueError: If num_paths > total_runs
        """
        if not HAS_MATPLOTLIB:
            raise ImportError(
                "matplotlib is required for plotting. "
                "Install with: pip install matplotlib"
            )
        
        if num_paths > result.total_runs:
            raise ValueError(
                f"num_paths ({num_paths}) cannot exceed total_runs ({result.total_runs})"
            )
        
        # Generate multiple independent simulation paths
        paths = []
        for path_idx in range(num_paths):
            path_seed = self.base_seed + path_idx * 10000
            cumulative_wins = []
            wins = 0
            
            # Simulate a path
            for game_idx in range(result.total_runs):
                run_seed = path_seed + game_idx
                
                if game_idx % 2 == 0:
                    runner = GameRunner(self.strategy_a, self.strategy_b, run_seed)
                else:
                    runner = GameRunner(self.strategy_b, self.strategy_a, run_seed)
                
                outcome = runner.run()
                
                if outcome.winner == self.strategy_a.name:
                    wins += 1
                
                # Calculate cumulative win rate
                cumulative_win_rate = wins / (game_idx + 1)
                cumulative_wins.append(cumulative_win_rate)
            
            paths.append(cumulative_wins)
        
        # Create the plot
        fig, ax = plt.subplots(figsize=figsize)
        
        # Plot each path
        x = np.arange(1, result.total_runs + 1)
        for path in paths:
            ax.plot(x, path, alpha=alpha, linewidth=0.8)
        
        # Add reference line for final win rate
        ax.axhline(
            y=result.win_rate_a,
            color='red',
            linestyle='--',
            linewidth=2,
            label=f'Final Win Rate: {result.win_rate_a:.3f}',
            alpha=0.8
        )
        
        # Formatting
        ax.set_xlabel('Game Number (Replication)', fontsize=12)
        ax.set_ylabel(f'Cumulative Win Rate ({result.strategy_a})', fontsize=12)
        ax.set_title(
            f'Monte Carlo Paths: {result.strategy_a} vs {result.strategy_b}\n'
            f'{num_paths} paths, {result.total_runs} games each',
            fontsize=14,
            fontweight='bold'
        )
        ax.grid(True, alpha=0.3)
        ax.legend(loc='best', fontsize=10)
        ax.set_ylim(0, 1)
        
        # Add convergence annotation
        ax.text(
            0.02, 0.98,
            f'Convergence: {result.win_rate_a:.1%} ± {1.96 * np.std([p[-1] for p in paths]):.1%}',
            transform=ax.transAxes,
            fontsize=10,
            verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5)
        )
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Plot saved to: {save_path}")
        else:
            plt.show()

