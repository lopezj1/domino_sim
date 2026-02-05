"""Tests for Monte Carlo batch orchestration."""

import pytest

from src.aggregation.monte_carlo import MonteCarloRunner
from src.strategy.greedy import GreedyStrategy
from src.strategy.random import RandomStrategy
from src.strategy.blocking import BlockingStrategy
from src.engine.rng import SeededRNG


class TestMonteCarloRunner:
    """Tests for Monte Carlo strategy comparison."""
    
    def test_monte_carlo_basic(self):
        """Test basic Monte Carlo run with 10 games."""
        greedy = GreedyStrategy()
        rng = SeededRNG(seed=42)
        random_strat = RandomStrategy(rng)
        
        runner = MonteCarloRunner(greedy, random_strat, num_runs=10, seed=1000)
        result = runner.run()
        
        assert result.strategy_a == "greedy"
        assert result.strategy_b == "random"
        assert result.total_runs == 10
        assert result.runs_a_wins + result.runs_b_wins == 10
        assert 0 <= result.win_rate_a <= 1
        assert 0 <= result.win_rate_b <= 1
        assert abs((result.win_rate_a + result.win_rate_b) - 1.0) < 0.01
        assert len(result.per_run_outcomes) == 10
    
    def test_monte_carlo_reproducibility(self):
        """Test that same seed produces reproducible results."""
        greedy = GreedyStrategy()
        
        rng1 = SeededRNG(seed=100)
        rng2 = SeededRNG(seed=100)
        random1 = RandomStrategy(rng1)
        random2 = RandomStrategy(rng2)
        
        runner1 = MonteCarloRunner(greedy, random1, num_runs=10, seed=5000)
        result1 = runner1.run()
        
        runner2 = MonteCarloRunner(greedy, random2, num_runs=10, seed=5000)
        result2 = runner2.run()
        
        assert result1.runs_a_wins == result2.runs_a_wins
        assert result1.runs_b_wins == result2.runs_b_wins
        assert result1.win_rate_a == result2.win_rate_a
    
    def test_monte_carlo_min_runs_validation(self):
        """Test that num_runs < 10 raises error."""
        greedy = GreedyStrategy()
        blocking = BlockingStrategy()
        
        with pytest.raises(ValueError, match="num_runs must be >= 10"):
            MonteCarloRunner(greedy, blocking, num_runs=9)
    
    def test_monte_carlo_different_strategies(self):
        """Test Monte Carlo with different strategy pairs."""
        greedy = GreedyStrategy()
        blocking = BlockingStrategy()
        
        runner = MonteCarloRunner(greedy, blocking, num_runs=10, seed=3000)
        result = runner.run()
        
        assert result.strategy_a == "greedy"
        assert result.strategy_b == "blocking"
        assert result.total_runs == 10
        assert len(result.per_run_outcomes) == 10
    
    def test_monte_carlo_confidence_interval(self):
        """Test that confidence interval is calculated."""
        greedy = GreedyStrategy()
        rng = SeededRNG(seed=55)
        random_strat = RandomStrategy(rng)
        
        runner = MonteCarloRunner(greedy, random_strat, num_runs=20, seed=4000)
        result = runner.run()
        
        # CI should be valid
        assert result.ci_lower <= result.ci_upper
        assert result.std_dev_score_diff_a >= 0
    
    def test_plot_monte_carlo_paths_validation(self):
        """Test plotting validation without actually rendering."""
        greedy = GreedyStrategy()
        rng = SeededRNG(seed=77)
        random_strat = RandomStrategy(rng)
        
        runner = MonteCarloRunner(greedy, random_strat, num_runs=10, seed=6000)
        result = runner.run()
        
        # Test that num_paths > total_runs raises error
        with pytest.raises(ValueError, match="num_paths.*cannot exceed total_runs"):
            runner.plot_monte_carlo_paths(result, num_paths=20)
    
    def test_plot_monte_carlo_paths_no_matplotlib(self, monkeypatch):
        """Test graceful failure when matplotlib is not installed."""
        greedy = GreedyStrategy()
        rng = SeededRNG(seed=88)
        random_strat = RandomStrategy(rng)
        
        runner = MonteCarloRunner(greedy, random_strat, num_runs=10, seed=7000)
        result = runner.run()
        
        # Mock matplotlib as unavailable
        import src.aggregation.monte_carlo as mc_module
        monkeypatch.setattr(mc_module, 'HAS_MATPLOTLIB', False)
        
        with pytest.raises(ImportError, match="matplotlib is required"):
            runner.plot_monte_carlo_paths(result, num_paths=5)
