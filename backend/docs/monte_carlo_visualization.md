# Monte Carlo Visualization Guide

## Overview

The `MonteCarloRunner` now includes a `plot_monte_carlo_paths()` method that visualizes uncertainty and convergence in strategy comparison simulations, similar to financial Monte Carlo analysis.

## What the Plot Shows

**X-Axis**: Game number (replication) from 1 to N  
**Y-Axis**: Cumulative win rate for Strategy A (0 to 1 scale)

Each colored line represents an independent simulation path showing how the cumulative win rate evolves as more games are played.

## Key Insights

### 1. **Uncertainty Visualization**
- **Early games**: Wide spread between paths indicates high uncertainty
- **Later games**: Narrow convergence shows increasing confidence in the true win rate

### 2. **Convergence Demonstration**
- All paths converge toward the true win rate as sample size increases
- Red dashed line shows the final estimated win rate
- Annotation box displays convergence statistics with confidence interval

### 3. **Statistical Significance**
- Wider final spread: Strategies are close in performance
- Tight final spread: Clear winner with high confidence

## Usage Example

```python
from src.strategy.blocking import BlockingStrategy
from src.strategy.random import RandomStrategy
from src.engine.rng import SeededRNG
from src.aggregation.monte_carlo import MonteCarloRunner

# Setup strategies
blocking = BlockingStrategy()
random_strat = RandomStrategy(SeededRNG(42))

# Run Monte Carlo
mc_runner = MonteCarloRunner(
    strategy_a=blocking,
    strategy_b=random_strat,
    num_runs=500,
    seed=12345
)

result = mc_runner.run()

# Generate visualization
mc_runner.plot_monte_carlo_paths(
    result=result,
    num_paths=100,        # Number of independent paths to plot
    figsize=(12, 8),      # Figure size
    alpha=0.3,            # Line transparency
    save_path="monte_carlo_paths.png"  # Optional: save to file
)
```

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `result` | `MonteCarloResult` | - | Result from `run()` method |
| `num_paths` | `int` | 100 | Number of simulation paths (max = total_runs) |
| `figsize` | `tuple` | (12, 8) | Figure size (width, height) in inches |
| `alpha` | `float` | 0.3 | Line transparency (0=invisible, 1=opaque) |
| `save_path` | `str` | None | Path to save figure (e.g., 'plot.png') |

## Interpretation Guide

### Pattern 1: Quick Convergence
```
All paths quickly narrow → Dominant strategy, high confidence
```

### Pattern 2: Late Convergence
```
Wide spread persists → Close matchup, needs more games
```

### Pattern 3: Oscillating Paths
```
Paths cross frequently → Strategies are evenly matched
```

### Pattern 4: Early Separation
```
Paths diverge early → Strong strategy advantage
```

## Comparison to Screenshot

The provided screenshot shows asset prices in financial Monte Carlo simulation. Our domino implementation adapts this to show:

| Financial MC | Domino MC |
|-------------|-----------|
| Asset prices | Cumulative win rate |
| Time steps | Game number |
| Price uncertainty | Win rate uncertainty |
| Risk analysis | Strategy strength |

## Dependencies

Requires `matplotlib` and `numpy`:

```bash
uv pip install matplotlib numpy
# or
pip install matplotlib numpy
```

## Running the Example

```bash
cd backend
python examples/plot_monte_carlo.py
```

This generates `monte_carlo_paths.png` with 100 paths over 500 games.

## Technical Details

### Path Generation
Each path uses an independent seed (`base_seed + path_idx * 10000`) to ensure true independence between visualized paths.

### Cumulative Win Rate Calculation
For each game in a path:
```python
cumulative_win_rate = total_wins / games_played_so_far
```

### Convergence Metric
The annotation shows:
```
final_win_rate ± 1.96 * std(final_win_rates_across_paths)
```

This represents the 95% confidence interval for the convergence point.

## Performance Notes

- Generating plots is **computational**: Each path reruns simulations
- For `num_paths=100` and `num_runs=500`: ~50,000 total games simulated
- Typical time: 5-15 seconds depending on hardware
- Consider reducing `num_paths` for faster iteration during development

## Example Output

```
======================================================================
Monte Carlo Simulation: Blocking vs Random
======================================================================

Running 500 games...

Results:
  blocking: 289 wins (57.8%)
  random: 211 wins (42.2%)
  Mean score diff: 17.53 ± 19.88
  95% CI: [15.79, 19.27]

Generating Monte Carlo paths plot...
✅ Plot saved to: monte_carlo_paths.png

Interpretation:
- Wide spread early: High uncertainty with few games
- Narrow spread later: Convergence to true win rate
- Red dashed line: Final estimated win rate
```

## Next Steps

1. **Experiment with parameters**: Try different `num_paths` and `num_runs`
2. **Compare strategies**: Test all strategy pairs
3. **Analyze convergence**: Determine minimum games needed for confidence
4. **Export results**: Use plots in presentations/papers

## References

- Monte Carlo methods: [Wikipedia](https://en.wikipedia.org/wiki/Monte_Carlo_method)
- Convergence visualization: Standard practice in quantitative finance
- Law of Large Numbers: Mathematical foundation for convergence
