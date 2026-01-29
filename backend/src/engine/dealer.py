"""Dealer for distributing tiles to players."""

from typing import List, Tuple
from src.models.tile import Tile


def deal_tiles(shuffled_tiles: List[Tile]) -> Tuple[List[Tile], List[Tile], List[Tile]]:
    """
    Deal tiles to two players and create boneyard.
    
    Distribution:
    - Player 0: 7 tiles
    - Player 1: 7 tiles  
    - Boneyard: remaining 14 tiles
    
    Args:
        shuffled_tiles: List of 28 shuffled tiles
    
    Returns:
        Tuple of (player_0_hand, player_1_hand, boneyard)
    """
    if len(shuffled_tiles) != 28:
        raise ValueError(f"Expected 28 tiles, got {len(shuffled_tiles)}")
    
    player_0_hand = shuffled_tiles[:7]
    player_1_hand = shuffled_tiles[7:14]
    boneyard = shuffled_tiles[14:28]
    
    return player_0_hand, player_1_hand, boneyard
