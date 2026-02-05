#!/usr/bin/env python3
"""
Example: Plot Monte Carlo simulation paths.

This demonstrates convergence and uncertainty visualization for strategy comparison.
Similar to financial Monte Carlo plots, shows how cumulative win rate converges.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.strategy.greedy import GreedyStrategy
from src.strategy.random import RandomStrategy
from src.strategy.blocking import BlockingStrategy
from src.engine.rng import SeededRNG
from src.aggregation.monte_carlo import MonteCarloRunner


def main():
    """Run Monte Carlo simulation and plot results."""
    
    print("=" * 70)
    print("Monte Carlo Simulation: Blocking vs Random")
    print("=" * 70)
    
    # Setup strategies
    blocking = BlockingStrategy()
    random_strat = RandomStrategy(SeededRNG(42))
    
    # Run Monte Carlo (more games = better convergence)
    print("\nRunning 500 games...")
    mc_runner = MonteCarloRunner(
        strategy_a=blocking,
        strategy_b=random_strat,
        num_runs=500,
        seed=12345
    )
    
    result = mc_runner.run()
    
    # Print summary
    print(f"\nResults:")
    print(f"  {result.strategy_a}: {result.runs_a_wins} wins ({result.win_rate_a:.1%})")
    print(f"  {result.strategy_b}: {result.runs_b_wins} wins ({result.win_rate_b:.1%})")
    print(f"  Mean score diff: {result.mean_score_diff_a:.2f} ± {result.std_dev_score_diff_a:.2f}")
    print(f"  95% CI: [{result.ci_lower:.2f}, {result.ci_upper:.2f}]")
    
    # Generate plot
    print("\nGenerating Monte Carlo paths plot...")
    print("  - X-axis: Game number (replication)")
    print("  - Y-axis: Cumulative win rate (0-1)")
    print("  - Shows convergence and uncertainty")
    
    try:
        mc_runner.plot_monte_carlo_paths(
            result=result,
            num_paths=100,  # 100 independent paths
            figsize=(12, 8),
            alpha=0.3,
            save_path="monte_carlo_paths.png"
        )
        print("\n✅ Plot saved to: monte_carlo_paths.png")
        print("   Open the file to see the visualization!")
        
    except ImportError as e:
        print(f"\n❌ Error: {e}")
        print("   Install matplotlib: pip install matplotlib numpy")
        return 1
    
    print("\n" + "=" * 70)
    print("Interpretation:")
    print("=" * 70)
    print("- Wide spread early: High uncertainty with few games")
    print("- Narrow spread later: Convergence to true win rate")
    print("- Red dashed line: Final estimated win rate")
    print("- More paths = better visualization of uncertainty")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
