"""Strategy base class for player decision logic."""

from abc import ABC, abstractmethod
from typing import List

from ..models.game_state import GameState
from ..models.move import Move


class Strategy(ABC):
    """
    Abstract base class for player strategies.
    
    All strategies are deterministic: same game state → same move choice.
    Strategies only see observable game state (no hidden information).
    """
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Strategy name (e.g., 'greedy', 'random')."""
        pass
    
    @abstractmethod
    def choose_move(self, state: GameState, legal_moves: List[Move]) -> Move:
        """
        Choose a move given game state and legal options.
        
        Args:
            state: Current game state (observable information only)
            legal_moves: List of legal moves available
        
        Returns:
            One of the legal_moves
        
        Invariant: Returned move must be in legal_moves
        Invariant: Same state + legal_moves → same move (deterministic)
        """
        pass
