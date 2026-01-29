"""RNG management for reproducible, seeded random number generation."""

from random import Random
from typing import Optional


class SeededRNG:
    """
    Seeded random number generator with explicit consumption tracking.
    
    Ensures reproducibility: same seed → same sequence of random values.
    """
    
    def __init__(self, seed: int) -> None:
        """Initialize with seed."""
        self.seed = seed
        self._rng = Random(seed)
        self._consumption_count = 0
    
    def random(self) -> float:
        """Generate random float [0.0, 1.0)."""
        self._consumption_count += 1
        return self._rng.random()
    
    def randint(self, a: int, b: int) -> int:
        """Generate random integer [a, b] inclusive."""
        self._consumption_count += 1
        return self._rng.randint(a, b)
    
    def choice(self, seq: list) -> any:  # type: ignore
        """Choose random element from sequence."""
        self._consumption_count += 1
        return self._rng.choice(seq)
    
    def shuffle(self, lst: list) -> None:
        """Shuffle list in place."""
        self._rng.shuffle(lst)
    
    @property
    def consumption_count(self) -> int:
        """Track how many random values consumed."""
        return self._consumption_count
