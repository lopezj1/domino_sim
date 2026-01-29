"""Greedy strategy: play highest pip tiles first."""

from typing import List

from .base import Strategy
from ..models.game_state import GameState
from ..models.move import Move


class GreedyStrategy(Strategy):
    """
    Greedy strategy: prioritizes playing tiles with highest total pips.
    
    Logic:
    1. If can play, choose tile with highest pip total
    2. If can't play but can draw, draw
    3. If can't draw, pass
    """
    
    @property
    def name(self) -> str:
        """Strategy identifier."""
        return "greedy"
    
    def choose_move(self, state: GameState, legal_moves: List[Move]) -> Move:
        """
        Choose move by prioritizing highest pip tiles.
        
        Deterministic: same state → same move
        """
        # Separate move types
        play_moves = [m for m in legal_moves if m.action == "play"]
        draw_moves = [m for m in legal_moves if m.action == "draw"]
        pass_moves = [m for m in legal_moves if m.action == "pass"]
        
        if play_moves:
            # Sort by tile pip count descending, pick first (highest)
            return max(play_moves, key=lambda m: m.tile.total_pips if m.tile else 0)
        elif draw_moves:
            return draw_moves[0]
        else:
            return pass_moves[0]
