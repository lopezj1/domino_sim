"""Tile set factory and shuffling utilities."""

from typing import List
from src.models.tile import Tile
from src.engine.rng import SeededRNG


def create_standard_tile_set() -> List[Tile]:
    """
    Create the standard 28-domino tile set.
    
    All combinations of pips 0-6 on each face:
    (0|0), (0|1), ..., (0|6), (1|1), (1|2), ..., (6|6)
    """
    tiles: List[Tile] = []
    for a in range(7):
        for b in range(a, 7):
            tiles.append(Tile(a, b))
    return tiles


def shuffle_tiles(tiles: List[Tile], rng: SeededRNG) -> List[Tile]:
    """
    Shuffle tile list using seeded RNG for reproducibility.
    
    Args:
        tiles: List of tiles to shuffle
        rng: Seeded random number generator
    
    Returns:
        Shuffled copy of tiles (original unchanged)
    """
    shuffled = tiles.copy()
    rng.shuffle(shuffled)
    return shuffled
