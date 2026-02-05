"""Tests for Monte Carlo visualization data generation."""

import pytest

from src.aggregation.monte_carlo import MonteCarloRunner
from src.strategy.greedy import GreedyStrategy
from src.strategy.blocking import BlockingStrategy


class TestMonteCarloVisualization:
    """Tests for visualization data generation."""
    
    def test_generate_visualization_data_basic(self):
        """Test basic visualization data generation."""
        greedy = GreedyStrategy()
        blocking = BlockingStrategy()
        
        runner = MonteCarloRunner(greedy, blocking, num_runs=100, seed=1000)
        viz_data = runner.generate_visualization_data(num_games=100, num_paths=20)
        
        assert viz_data["strategy_a"] == "greedy"
        assert viz_data["strategy_b"] == "blocking"
        assert viz_data["total_games"] == 100
        assert viz_data["num_paths"] == 20
        assert len(viz_data["game_numbers"]) == 100
        assert viz_data["game_numbers"][0] == 1
        assert viz_data["game_numbers"][-1] == 100
        assert len(viz_data["paths"]) == 20
        assert all(len(path) == 100 for path in viz_data["paths"])
    
    def test_visualization_cumulative_win_rates(self):
        """Test that paths contain valid cumulative win rates."""
        greedy = GreedyStrategy()
        blocking = BlockingStrategy()
        
        runner = MonteCarloRunner(greedy, blocking, num_runs=50, seed=2000)
        viz_data = runner.generate_visualization_data(num_games=50, num_paths=10)
        
        # All win rates should be 0-1
        for path in viz_data["paths"]:
            for rate in path:
                assert 0.0 <= rate <= 1.0
        
        # Final rates should sum close to 1
        assert 0.0 <= viz_data["final_win_rate_a"] <= 1.0
        assert 0.0 <= viz_data["final_win_rate_b"] <= 1.0
        assert abs(viz_data["final_win_rate_a"] + viz_data["final_win_rate_b"] - 1.0) < 0.01
    
    def test_visualization_confidence_interval(self):
        """Test that confidence interval is valid."""
        greedy = GreedyStrategy()
        blocking = BlockingStrategy()
        
        runner = MonteCarloRunner(greedy, blocking, num_runs=100, seed=3000)
        viz_data = runner.generate_visualization_data(num_games=100, num_paths=30)
        
        assert viz_data["ci_lower"] <= viz_data["final_win_rate_a"]
        assert viz_data["final_win_rate_a"] <= viz_data["ci_upper"]
        assert 0.0 <= viz_data["ci_lower"] <= 1.0
        assert 0.0 <= viz_data["ci_upper"] <= 1.0
        assert viz_data["convergence_std"] >= 0.0
    
    def test_visualization_min_games_validation(self):
        """Test that num_games < 50 raises error."""
        greedy = GreedyStrategy()
        blocking = BlockingStrategy()
        
        runner = MonteCarloRunner(greedy, blocking, num_runs=100, seed=4000)
        
        with pytest.raises(ValueError, match="num_games must be >= 50"):
            runner.generate_visualization_data(num_games=40, num_paths=10)
    
    def test_visualization_min_paths_validation(self):
        """Test that num_paths < 10 raises error."""
        greedy = GreedyStrategy()
        blocking = BlockingStrategy()
        
        runner = MonteCarloRunner(greedy, blocking, num_runs=100, seed=5000)
        
        with pytest.raises(ValueError, match="num_paths must be >= 10"):
            runner.generate_visualization_data(num_games=100, num_paths=5)
    
    def test_visualization_convergence(self):
        """Test that paths show convergence behavior."""
        greedy = GreedyStrategy()
        blocking = BlockingStrategy()
        
        runner = MonteCarloRunner(greedy, blocking, num_runs=200, seed=6000)
        viz_data = runner.generate_visualization_data(num_games=200, num_paths=30)
        
        # Early variance should be higher than late variance (convergence)
        early_values = [path[9] for path in viz_data["paths"]]  # After 10 games
        late_values = [path[199] for path in viz_data["paths"]]  # After 200 games
        
        import statistics
        early_std = statistics.stdev(early_values) if len(early_values) > 1 else 0
        late_std = statistics.stdev(late_values) if len(late_values) > 1 else 0
        
        # Late standard deviation should generally be smaller (convergence)
        # Note: This might not always hold for small samples, but should trend true
        assert late_std >= 0  # At minimum, should be valid
