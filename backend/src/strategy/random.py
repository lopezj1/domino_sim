"""Random strategy: choose uniformly at random from legal moves."""

from typing import List

from .base import Strategy
from ..models.game_state import GameState
from ..models.move import Move
from ..engine.rng import SeededRNG


class RandomStrategy(Strategy):
    """
    Random strategy: pick uniformly at random from legal moves.
    
    Requires seeded RNG for reproducibility.
    Uses only observable game state (not random within choose_move).
    """
    
    def __init__(self, rng: SeededRNG):
        """
        Initialize with seeded RNG.
        
        Args:
            rng: Seeded random number generator
        """
        self.rng = rng
    
    @property
    def name(self) -> str:
        """Strategy identifier."""
        return "random"
    
    def choose_move(self, state: GameState, legal_moves: List[Move]) -> Move:
        """
        Choose move uniformly at random from legal options.
        
        Deterministic: same RNG state → same move
        """
        return self.rng.choice(legal_moves)
