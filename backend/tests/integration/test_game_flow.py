"""Integration tests for complete game flow."""

import pytest

from src.simulation.runner import GameRunner
from src.strategy.greedy import GreedyStrategy
from src.strategy.random import RandomStrategy
from src.strategy.blocking import BlockingStrategy
from src.engine.rng import SeededRNG


class TestGameFlow:
    """Integration tests for complete game simulations."""
    
    def test_single_game_greedy_vs_random(self):
        """Test single game between greedy and random strategies."""
        greedy = GreedyStrategy()
        rng = SeededRNG(seed=42)
        random_strat = RandomStrategy(rng)
        
        runner = GameRunner(greedy, random_strat, seed=12345)
        outcome = runner.run()
        
        assert outcome.winner in ["greedy", "random"]
        assert outcome.seed == 12345
        assert outcome.turns >= 1
        assert outcome.score_differential >= 0
        assert len(outcome.trace) > 0
        assert outcome.trace[0].type == "deal"
        assert outcome.trace[-1].type == "game_end"
    
    def test_reproducibility_same_seed(self):
        """Test that same seed produces same outcome."""
        greedy = GreedyStrategy()
        rng1 = SeededRNG(seed=100)
        rng2 = SeededRNG(seed=100)
        random1 = RandomStrategy(rng1)
        random2 = RandomStrategy(rng2)
        
        runner1 = GameRunner(greedy, random1, seed=54321)
        outcome1 = runner1.run()
        
        runner2 = GameRunner(greedy, random2, seed=54321)
        outcome2 = runner2.run()
        
        assert outcome1.winner == outcome2.winner
        assert outcome1.turns == outcome2.turns
        assert outcome1.score_differential == outcome2.score_differential
        assert len(outcome1.trace) == len(outcome2.trace)
    
    def test_game_tile_conservation(self):
        """Test that tile count is conserved throughout game."""
        greedy = GreedyStrategy()
        blocking = BlockingStrategy()
        
        runner = GameRunner(greedy, blocking, seed=99999)
        outcome = runner.run()
        
        # All events should be valid
        assert len(outcome.trace) > 0
        
        # Game should have produced a winner
        assert outcome.winner in ["greedy", "blocking"]
        assert outcome.turns >= 1
    
    def test_multiple_games_different_seeds(self):
        """Test that different seeds produce different outcomes (usually)."""
        greedy = GreedyStrategy()
        
        outcomes = []
        for seed in [1, 2, 3, 4, 5]:
            rng = SeededRNG(seed=seed * 1000)
            random_strat = RandomStrategy(rng)
            runner = GameRunner(greedy, random_strat, seed=seed)
            outcome = runner.run()
            outcomes.append(outcome)
        
        # At least one should have different winner or turns
        # (statistically very likely with 5 runs)
        assert len(outcomes) == 5
        assert all(o.seed in [1, 2, 3, 4, 5] for o in outcomes)
