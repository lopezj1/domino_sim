"""GameState model representing immutable game snapshot."""

from dataclasses import dataclass
from typing import List, Tuple

from .move import Move
from .tile import Tile


@dataclass(frozen=True)
class GameState:
    """
    Immutable snapshot of current game state.
    
    Represents: player hands, boneyard, board layout, current player,
    scores, and round number.
    
    Invariant: Total of 28 tiles (hands + boneyard + board).
    """
    players_hands: Tuple[Tuple[Tile, ...], Tuple[Tile, ...]]
    boneyard: Tuple[Tile, ...]
    board: Tuple[Tile, ...]
    current_player: int  # 0 or 1
    scores: Tuple[int, int]  # (player_0_score, player_1_score)
    round_num: int
    
    def __post_init__(self) -> None:
        """Validate state invariants."""
        # Validate player index
        if self.current_player not in (0, 1):
            raise ValueError(f"current_player must be 0 or 1, got {self.current_player}")
        
        # Validate round number
        if self.round_num < 1:
            raise ValueError(f"round_num must be >= 1, got {self.round_num}")
        
        # Validate scores
        if any(s < 0 for s in self.scores):
            raise ValueError(f"scores must be non-negative, got {self.scores}")
        
        # Validate tile conservation (28 tiles total)
        total_tiles = (
            len(self.players_hands[0]) +
            len(self.players_hands[1]) +
            len(self.boneyard) +
            len(self.board)
        )
        if total_tiles > 28:
            raise ValueError(f"Total tiles {total_tiles} exceeds 28")
    
    def get_legal_moves(self) -> List[Move]:
        """
        Compute legal moves for current player.
        
        Returns list of legal moves in order:
        1. Play moves (tiles matching board endpoints)
        2. Draw move (if boneyard non-empty and no legal plays)
        3. Pass move (if no play or draw available)
        """
        legal_moves: List[Move] = []
        current_hand = self.players_hands[self.current_player]
        
        # If board is empty, any tile in hand is playable
        if not self.board:
            legal_moves = [Move(action="play", tile=tile) for tile in current_hand]
        else:
            # Board has tiles - find tiles that match endpoints
            left_end = self.board[0].pips_a
            right_end = self.board[-1].pips_b
            
            for tile in current_hand:
                # Tile matches if either face matches either endpoint
                if (tile.pips_a in (left_end, right_end) or 
                    tile.pips_b in (left_end, right_end)):
                    legal_moves.append(Move(action="play", tile=tile))
        
        # If no legal plays and boneyard has tiles, can draw
        if not legal_moves and self.boneyard:
            legal_moves.append(Move(action="draw", tile=None))
        
        # If no legal plays and no boneyard, must pass
        if not legal_moves:
            legal_moves.append(Move(action="pass", tile=None))
        
        return legal_moves
    
    @property
    def total_tiles_accounted(self) -> int:
        """Total tiles in play (for validation)."""
        return (
            len(self.players_hands[0]) +
            len(self.players_hands[1]) +
            len(self.boneyard) +
            len(self.board)
        )
