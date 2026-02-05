#!/usr/bin/env python3
"""
Compare all three strategies with Monte Carlo visualizations.

Generates three plots:
1. Greedy vs Random
2. Greedy vs Blocking
3. Random vs Blocking
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.strategy.greedy import GreedyStrategy
from src.strategy.random import RandomStrategy
from src.strategy.blocking import BlockingStrategy
from src.engine.rng import SeededRNG
from src.aggregation.monte_carlo import MonteCarloRunner


def run_comparison(name, strategy_a, strategy_b, seed, num_runs=500, num_paths=100):
    """Run a single comparison and generate plot."""
    print(f"\n{'='*70}")
    print(f"Comparison: {strategy_a.name.upper()} vs {strategy_b.name.upper()}")
    print(f"{'='*70}")
    
    runner = MonteCarloRunner(strategy_a, strategy_b, num_runs=num_runs, seed=seed)
    result = runner.run()
    
    print(f"\nResults after {num_runs} games:")
    print(f"  {result.strategy_a}: {result.runs_a_wins} wins ({result.win_rate_a:.1%})")
    print(f"  {result.strategy_b}: {result.runs_b_wins} wins ({result.win_rate_b:.1%})")
    print(f"  Mean score diff: {result.mean_score_diff_a:.2f} ± {result.std_dev_score_diff_a:.2f}")
    print(f"  95% CI: [{result.ci_lower:.2f}, {result.ci_upper:.2f}]")
    
    filename = f"{name}.png"
    print(f"\nGenerating plot: {filename}")
    
    runner.plot_monte_carlo_paths(
        result=result,
        num_paths=num_paths,
        figsize=(12, 8),
        alpha=0.25,
        save_path=filename
    )
    
    return result


def main():
    """Run all comparisons."""
    print("\n" + "="*70)
    print("COMPLETE STRATEGY COMPARISON SUITE")
    print("="*70)
    print("\nThis will run 1500 total games (3 matchups × 500 games)")
    print("Estimated time: 10-20 seconds")
    
    # Initialize strategies
    greedy = GreedyStrategy()
    blocking = BlockingStrategy()
    random_strat = RandomStrategy(SeededRNG(42))
    
    results = []
    
    # Run all three matchups
    results.append(run_comparison(
        "greedy_vs_random",
        greedy,
        RandomStrategy(SeededRNG(100)),
        seed=1000
    ))
    
    results.append(run_comparison(
        "greedy_vs_blocking",
        greedy,
        blocking,
        seed=2000
    ))
    
    results.append(run_comparison(
        "random_vs_blocking",
        RandomStrategy(SeededRNG(200)),
        BlockingStrategy(),
        seed=3000
    ))
    
    # Summary
    print("\n" + "="*70)
    print("OVERALL SUMMARY")
    print("="*70)
    
    print("\nWin Rates:")
    for i, (name, r) in enumerate(zip(
        ["Greedy vs Random", "Greedy vs Blocking", "Random vs Blocking"],
        results
    ), 1):
        print(f"{i}. {name}:")
        print(f"   {r.strategy_a}: {r.win_rate_a:.1%}")
        print(f"   {r.strategy_b}: {r.win_rate_b:.1%}")
    
    # Determine ranking
    print("\n" + "="*70)
    print("STRATEGY RANKING")
    print("="*70)
    
    greedy_wins = results[0].runs_a_wins  # vs random
    greedy_total = 1000  # 500 vs random + 500 vs blocking
    
    blocking_wins = (
        results[1].runs_b_wins +  # vs greedy
        results[2].runs_b_wins    # vs random
    )
    blocking_total = 1000
    
    random_wins = (
        results[0].runs_b_wins +  # vs greedy
        results[2].runs_a_wins    # vs blocking
    )
    random_total = 1000
    
    ranking = [
        ("Blocking", blocking_wins / blocking_total),
        ("Greedy", greedy_wins / greedy_total),
        ("Random", random_wins / random_total),
    ]
    ranking.sort(key=lambda x: x[1], reverse=True)
    
    for i, (name, win_rate) in enumerate(ranking, 1):
        medal = ["🥇", "🥈", "🥉"][i-1]
        print(f"{medal} {i}. {name}: {win_rate:.1%} overall win rate")
    
    print("\n" + "="*70)
    print("FILES GENERATED")
    print("="*70)
    print("  1. greedy_vs_random.png")
    print("  2. greedy_vs_blocking.png")
    print("  3. random_vs_blocking.png")
    print("\nOpen these files to see convergence visualizations!")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
