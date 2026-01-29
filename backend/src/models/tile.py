"""Tile model representing a domino tile with two faces."""

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class Tile:
    """
    Immutable domino tile with two faces.
    
    Each face shows 0-6 pips. Tiles are uniquely identified by their
    sorted tuple (min_pips, max_pips) for canonical representation.
    """
    pips_a: int
    pips_b: int
    
    def __post_init__(self) -> None:
        """Validate pip counts."""
        if not (0 <= self.pips_a <= 6):
            raise ValueError(f"pips_a must be 0-6, got {self.pips_a}")
        if not (0 <= self.pips_b <= 6):
            raise ValueError(f"pips_b must be 0-6, got {self.pips_b}")
    
    @property
    def id(self) -> Tuple[int, int]:
        """Canonical tile ID: (min_pips, max_pips)."""
        return (min(self.pips_a, self.pips_b), max(self.pips_a, self.pips_b))
    
    @property
    def total_pips(self) -> int:
        """Total pips on the tile."""
        return self.pips_a + self.pips_b
    
    def __repr__(self) -> str:
        """String representation: Tile(a|b)."""
        return f"Tile({self.pips_a}|{self.pips_b})"
    
    def __eq__(self, other: object) -> bool:
        """Tiles are equal if they have the same ID."""
        if not isinstance(other, Tile):
            return NotImplemented
        return self.id == other.id
    
    def __hash__(self) -> int:
        """Hash based on canonical ID."""
        return hash(self.id)
