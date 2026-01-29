"""Blocking strategy: prioritize blocking opponent's tiles."""

from typing import List

from .base import Strategy
from ..models.game_state import GameState
from ..models.move import Move


class BlockingStrategy(Strategy):
    """
    Blocking strategy: try to play tiles that opponent can't match.
    
    Logic:
    1. If can play, choose tile that blocks opponent (highest pips at endpoints)
    2. Fall back to greedy (highest pips) if blocking not applicable
    3. Draw if can't play
    4. Pass if can't draw
    """
    
    @property
    def name(self) -> str:
        """Strategy identifier."""
        return "blocking"
    
    def choose_move(self, state: GameState, legal_moves: List[Move]) -> Move:
        """
        Choose move prioritizing tiles that block opponent.
        
        Deterministic: same state → same move
        """
        play_moves = [m for m in legal_moves if m.action == "play"]
        draw_moves = [m for m in legal_moves if m.action == "draw"]
        pass_moves = [m for m in legal_moves if m.action == "pass"]
        
        if play_moves:
            # For each play move, count how many of opponent's tiles could match
            opponent_id = 1 - state.current_player
            opponent_hand = state.players_hands[opponent_id]
            
            # Find tiles that opponent has the fewest matches for
            best_move = None
            min_opponent_matches = float('inf')
            
            for move in play_moves:
                if move.tile is None:
                    continue
                
                # Count how many tiles in opponent's hand could match this tile
                tile = move.tile
                matches = sum(
                    1 for t in opponent_hand
                    if (t.pips_a in (tile.pips_a, tile.pips_b) or
                        t.pips_b in (tile.pips_a, tile.pips_b))
                )
                
                if matches < min_opponent_matches:
                    min_opponent_matches = matches
                    best_move = move
            
            if best_move:
                return best_move
            
            # Fallback to greedy if no blocking advantage
            return max(play_moves, key=lambda m: m.tile.total_pips if m.tile else 0)
        
        elif draw_moves:
            return draw_moves[0]
        else:
            return pass_moves[0]
