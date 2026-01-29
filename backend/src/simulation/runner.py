"""GameRunner: orchestrates single-game simulation setup and execution."""

from typing import Tuple

from .game import Game
from ..models.game_state import GameState
from ..models.result import GameOutcome
from ..engine.rng import SeededRNG
from ..engine.tiles import create_standard_tile_set, shuffle_tiles
from ..engine.dealer import deal_tiles
from ..strategy.base import Strategy


class GameRunner:
    """
    Orchestrates a single game: setup (deal), execution, and result.
    
    Handles:
    - Tile creation and shuffling
    - Deal distribution
    - Game initialization and execution
    - Result capture
    """
    
    def __init__(
        self,
        player_0_strategy: Strategy,
        player_1_strategy: Strategy,
        seed: int,
    ):
        """
        Initialize game runner with strategies and seed.
        
        Args:
            player_0_strategy: Strategy for player 0
            player_1_strategy: Strategy for player 1
            seed: RNG seed for reproducibility
        """
        self.player_0_strategy = player_0_strategy
        self.player_1_strategy = player_1_strategy
        self.seed = seed
    
    def run(self) -> GameOutcome:
        """
        Execute a complete game simulation.
        
        Returns:
            GameOutcome with winner, score, trace, and seed
        """
        # Create seeded RNG
        rng = SeededRNG(seed=self.seed)
        
        # Create and shuffle tiles
        tiles = create_standard_tile_set()
        shuffled = shuffle_tiles(tiles, rng)
        
        # Deal tiles
        p0_hand, p1_hand, boneyard = deal_tiles(shuffled)
        
        # Create initial state (player 0 starts)
        initial_state = GameState(
            players_hands=(tuple(p0_hand), tuple(p1_hand)),
            boneyard=tuple(boneyard),
            board=tuple(),
            current_player=0,
            scores=(0, 0),
            round_num=1,
        )
        
        # Create game orchestrator
        game = Game(
            initial_state=initial_state,
            player_0_strategy=self.player_0_strategy,
            player_1_strategy=self.player_1_strategy,
            seed=self.seed,
        )
        
        # Play to completion
        outcome = game.play_game()
        
        return outcome
