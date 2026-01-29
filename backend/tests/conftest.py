"""Pytest configuration and shared fixtures."""

import pytest
from typing import List, Tuple

from src.models.tile import Tile
from src.models.game_state import GameState
from src.engine.rng import SeededRNG


@pytest.fixture
def standard_tile_set() -> List[Tile]:
    """
    Create the standard 28-domino tile set.
    
    All combinations of 0-6 pips on each face (double-0 through double-6).
    """
    tiles = []
    for a in range(7):
        for b in range(a, 7):  # b >= a to avoid duplicates
            tiles.append(Tile(a, b))
    return tiles


@pytest.fixture
def seeded_rng() -> SeededRNG:
    """Create seeded RNG for reproducible tests."""
    return SeededRNG(seed=12345)


def create_initial_game_state(
    player_0_hand: List[Tile],
    player_1_hand: List[Tile],
    boneyard: List[Tile],
) -> GameState:
    """
    Create game state with given hands and boneyard.
    
    Helper for test setup.
    """
    return GameState(
        players_hands=(tuple(player_0_hand), tuple(player_1_hand)),
        boneyard=tuple(boneyard),
        board=tuple(),
        current_player=0,
        scores=(0, 0),
        round_num=1,
    )


@pytest.fixture
def simple_game_state(standard_tile_set: List[Tile]) -> GameState:
    """
    Create simple game state for testing.
    
    Player 0: [6|6, 5|5]
    Player 1: [4|4, 3|3]
    Boneyard: remaining tiles
    """
    p0_hand = [Tile(6, 6), Tile(5, 5)]
    p1_hand = [Tile(4, 4), Tile(3, 3)]
    used_tiles = set(t.id for t in p0_hand + p1_hand)
    boneyard = [t for t in standard_tile_set if t.id not in used_tiles]
    
    return create_initial_game_state(p0_hand, p1_hand, boneyard)
