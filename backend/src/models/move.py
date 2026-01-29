"""Move model representing a player action in the game."""

from dataclasses import dataclass
from typing import Literal, Optional

from .tile import Tile


@dataclass(frozen=True)
class Move:
    """
    Immutable player move/action.
    
    A move can be:
    - play: Place a tile on the board
    - draw: Draw a tile from the boneyard
    - pass: Cannot play or draw
    """
    action: Literal["play", "draw", "pass"]
    tile: Optional[Tile] = None
    
    def __post_init__(self) -> None:
        """Validate move invariants."""
        if self.action == "play" and self.tile is None:
            raise ValueError("play action requires a tile")
        if self.action in ("draw", "pass") and self.tile is not None:
            raise ValueError(f"{self.action} action does not accept a tile")
    
    def __repr__(self) -> str:
        """String representation."""
        if self.tile:
            return f"Move({self.action}({self.tile}))"
        return f"Move({self.action})"
