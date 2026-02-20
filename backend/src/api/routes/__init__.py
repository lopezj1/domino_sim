"""__init__.py for routes package."""

from .game import router as game_router
from .visualization import router as visualization_router

__all__ = ["visualization_router", "game_router"]
