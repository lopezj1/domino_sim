"""Event model representing discrete simulation events."""

from dataclasses import dataclass, field
from typing import Any, Dict, Literal


@dataclass(frozen=True)
class Event:
    """
    Immutable event in discrete event simulation.
    
    Represents: game events (deal, play, draw, pass, round_end, game_end)
    with timestamp (event index) and event-specific data.
    """
    type: Literal["deal", "play", "draw", "pass", "round_end", "game_end"]
    timestamp: int  # Event index (0, 1, 2, ...)
    data: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self) -> None:
        """Validate event invariants."""
        if self.timestamp < 0:
            raise ValueError(f"timestamp must be >= 0, got {self.timestamp}")
    
    def __repr__(self) -> str:
        """String representation."""
        return f"Event({self.type}@{self.timestamp})"
