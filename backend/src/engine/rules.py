"""Game rules: move validation and scoring."""

from typing import List, Tuple
from src.models.tile import Tile
from src.models.game_state import GameState
from src.models.move import Move


def get_legal_plays_for_tile(tile: Tile, left_end: int, right_end: int) -> bool:
    """
    Check if a tile can be played given board endpoints.
    
    A tile can be played if either of its faces matches one of the endpoints.
    
    Args:
        tile: Tile to check
        left_end: Left endpoint pip count
        right_end: Right endpoint pip count
    
    Returns:
        True if tile can be played, False otherwise
    """
    return tile.pips_a in (left_end, right_end) or tile.pips_b in (left_end, right_end)


def validate_play_move(move: Move, state: GameState) -> bool:
    """
    Validate that a play move is legal.
    
    Args:
        move: Move to validate (must be action='play')
        state: Current game state
    
    Returns:
        True if move is legal, False otherwise
    """
    if move.action != "play" or move.tile is None:
        return False
    
    tile = move.tile
    player_hand = state.players_hands[state.current_player]
    
    # Tile must be in player's hand
    if tile not in player_hand:
        return False
    
    # If board is empty, any tile is playable
    if not state.board:
        return True
    
    # Check if tile matches board endpoints
    left_end = state.board[0].pips_a
    right_end = state.board[-1].pips_b
    
    return get_legal_plays_for_tile(tile, left_end, right_end)


def calculate_hand_pips(hand: Tuple[Tile, ...]) -> int:
    """Calculate total pips in a hand."""
    return sum(tile.total_pips for tile in hand)


def calculate_round_winner(hand_0: Tuple[Tile, ...], hand_1: Tuple[Tile, ...]) -> int:
    """
    Calculate round winner based on hand pip counts.
    
    Winner is player with lowest pip count.
    
    Args:
        hand_0: Player 0's remaining tiles
        hand_1: Player 1's remaining tiles
    
    Returns:
        0 or 1 (winning player index)
    """
    pips_0 = calculate_hand_pips(hand_0)
    pips_1 = calculate_hand_pips(hand_1)
    
    if pips_0 <= pips_1:
        return 0
    return 1


def calculate_round_score(winner: int, loser_hand: Tuple[Tile, ...]) -> int:
    """
    Calculate points awarded to winner in a round.
    
    Winner receives loser's hand pip count as points.
    
    Args:
        winner: Winner index (0 or 1)
        loser_hand: Loser's remaining tiles
    
    Returns:
        Points awarded to winner
    """
    return calculate_hand_pips(loser_hand)
