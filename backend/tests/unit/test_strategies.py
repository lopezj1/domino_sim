"""Tests for strategy implementations."""

import pytest

from src.strategy.greedy import GreedyStrategy
from src.strategy.random import RandomStrategy
from src.strategy.blocking import BlockingStrategy
from src.engine.rng import SeededRNG
from src.models.game_state import GameState
from src.models.move import Move
from src.models.tile import Tile


@pytest.fixture
def simple_state_with_plays():
    """Create simple game state with multiple legal play moves."""
    board = (Tile(3, 3),)
    p0_hand = (Tile(3, 4), Tile(3, 5), Tile(6, 6))
    p1_hand = (Tile(1, 1),)
    boneyard = tuple()
    
    return GameState(
        players_hands=(p0_hand, p1_hand),
        board=board,
        boneyard=boneyard,
        current_player=0,
        scores=(0, 0),
        round_num=1,
    )


@pytest.fixture
def state_no_plays_has_draw():
    """Game state where current player has no legal plays but boneyard exists."""
    board = (Tile(1, 1),)
    p0_hand = (Tile(4, 5), Tile(5, 6))
    p1_hand = (Tile(2, 2),)
    boneyard = (Tile(3, 4), Tile(6, 6))
    
    return GameState(
        players_hands=(p0_hand, p1_hand),
        board=board,
        boneyard=boneyard,
        current_player=0,
        scores=(0, 0),
        round_num=1,
    )


@pytest.fixture
def state_no_plays_no_draw():
    """Game state where current player must pass."""
    board = (Tile(1, 1),)
    p0_hand = (Tile(4, 5), Tile(5, 6))
    p1_hand = (Tile(2, 2),)
    boneyard = tuple()
    
    return GameState(
        players_hands=(p0_hand, p1_hand),
        board=board,
        boneyard=boneyard,
        current_player=0,
        scores=(0, 0),
        round_num=1,
    )


class TestGreedyStrategy:
    """Tests for GreedyStrategy."""
    
    def test_greedy_name(self):
        """Test strategy name."""
        strategy = GreedyStrategy()
        assert strategy.name == "greedy"
    
    def test_greedy_chooses_highest_pip_tile(self, simple_state_with_plays):
        """Test greedy chooses tile with highest pips."""
        strategy = GreedyStrategy()
        legal_moves = simple_state_with_plays.get_legal_moves()
        
        # Should have play moves: (3|4) and (3|5)
        assert len(legal_moves) > 0
        assert all(m.action == "play" for m in legal_moves)
        
        chosen = strategy.choose_move(simple_state_with_plays, legal_moves)
        assert chosen.action == "play"
        # (3|5) has 8 pips, (3|4) has 7, so should choose (3|5)
        assert chosen.tile.pips_a == 3 and chosen.tile.pips_b == 5
    
    def test_greedy_draws_when_no_plays(self, state_no_plays_has_draw):
        """Test greedy draws when no legal plays."""
        strategy = GreedyStrategy()
        legal_moves = state_no_plays_has_draw.get_legal_moves()
        
        chosen = strategy.choose_move(state_no_plays_has_draw, legal_moves)
        assert chosen.action == "draw"
    
    def test_greedy_passes_when_no_plays_no_draw(self, state_no_plays_no_draw):
        """Test greedy passes when can't play or draw."""
        strategy = GreedyStrategy()
        legal_moves = state_no_plays_no_draw.get_legal_moves()
        
        chosen = strategy.choose_move(state_no_plays_no_draw, legal_moves)
        assert chosen.action == "pass"


class TestRandomStrategy:
    """Tests for RandomStrategy."""
    
    def test_random_name(self):
        """Test strategy name."""
        rng = SeededRNG(seed=42)
        strategy = RandomStrategy(rng)
        assert strategy.name == "random"
    
    def test_random_chooses_from_legal_moves(self, simple_state_with_plays):
        """Test random strategy chooses from legal moves."""
        rng = SeededRNG(seed=42)
        strategy = RandomStrategy(rng)
        legal_moves = simple_state_with_plays.get_legal_moves()
        
        chosen = strategy.choose_move(simple_state_with_plays, legal_moves)
        assert chosen in legal_moves
    
    def test_random_reproducible_same_seed(self, simple_state_with_plays):
        """Test random strategy is reproducible with same seed."""
        rng1 = SeededRNG(seed=100)
        strategy1 = RandomStrategy(rng1)
        
        rng2 = SeededRNG(seed=100)
        strategy2 = RandomStrategy(rng2)
        
        legal_moves = simple_state_with_plays.get_legal_moves()
        
        choice1 = strategy1.choose_move(simple_state_with_plays, legal_moves)
        choice2 = strategy2.choose_move(simple_state_with_plays, legal_moves)
        
        assert choice1 == choice2


class TestBlockingStrategy:
    """Tests for BlockingStrategy."""
    
    def test_blocking_name(self):
        """Test strategy name."""
        strategy = BlockingStrategy()
        assert strategy.name == "blocking"
    
    def test_blocking_plays_when_available(self, simple_state_with_plays):
        """Test blocking prioritizes plays over draw/pass."""
        strategy = BlockingStrategy()
        legal_moves = simple_state_with_plays.get_legal_moves()
        
        chosen = strategy.choose_move(simple_state_with_plays, legal_moves)
        assert chosen.action == "play"
    
    def test_blocking_draws_when_no_plays(self, state_no_plays_has_draw):
        """Test blocking draws when no legal plays."""
        strategy = BlockingStrategy()
        legal_moves = state_no_plays_has_draw.get_legal_moves()
        
        chosen = strategy.choose_move(state_no_plays_has_draw, legal_moves)
        assert chosen.action == "draw"
    
    def test_blocking_passes_when_no_plays_no_draw(self, state_no_plays_no_draw):
        """Test blocking passes when can't play or draw."""
        strategy = BlockingStrategy()
        legal_moves = state_no_plays_no_draw.get_legal_moves()
        
        chosen = strategy.choose_move(state_no_plays_no_draw, legal_moves)
        assert chosen.action == "pass"
