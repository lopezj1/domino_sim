"""Unit tests for GameState model."""

import pytest
from src.models.tile import Tile
from src.models.game_state import GameState
from src.models.move import Move


class TestGameState:
    """Test suite for GameState model."""
    
    def test_game_state_creation(self, simple_game_state: GameState) -> None:
        """Test game state creation."""
        assert simple_game_state.current_player == 0
        assert simple_game_state.scores == (0, 0)
        assert simple_game_state.round_num == 1
        assert len(simple_game_state.players_hands[0]) == 2
        assert len(simple_game_state.players_hands[1]) == 2
    
    def test_game_state_tile_conservation(self, simple_game_state: GameState) -> None:
        """Test that total tiles equals 28."""
        assert simple_game_state.total_tiles_accounted == 28
    
    def test_game_state_invalid_player(self) -> None:
        """Test that invalid current_player raises error."""
        with pytest.raises(ValueError, match="current_player must be 0 or 1"):
            GameState(
                players_hands=(tuple(), tuple()),
                boneyard=tuple(),
                board=tuple(),
                current_player=2,
                scores=(0, 0),
                round_num=1,
            )
    
    def test_game_state_invalid_round(self) -> None:
        """Test that invalid round_num raises error."""
        with pytest.raises(ValueError, match="round_num must be >= 1"):
            GameState(
                players_hands=(tuple(), tuple()),
                boneyard=tuple(),
                board=tuple(),
                current_player=0,
                scores=(0, 0),
                round_num=0,
            )
    
    def test_game_state_invalid_scores(self) -> None:
        """Test that negative scores raise error."""
        with pytest.raises(ValueError, match="scores must be non-negative"):
            GameState(
                players_hands=(tuple(), tuple()),
                boneyard=tuple(),
                board=tuple(),
                current_player=0,
                scores=(-1, 0),
                round_num=1,
            )
    
    def test_game_state_legal_moves_empty_board(self, simple_game_state: GameState) -> None:
        """Test legal moves when board is empty (any tile playable)."""
        moves = simple_game_state.get_legal_moves()
        
        # All tiles in player 0's hand should be playable
        assert len(moves) == 2
        assert all(m.action == "play" for m in moves)
        assert moves[0].tile == Tile(6, 6)
        assert moves[1].tile == Tile(5, 5)
    
    def test_game_state_frozen(self, simple_game_state: GameState) -> None:
        """Test that game state is immutable (frozen)."""
        with pytest.raises(AttributeError):
            simple_game_state.current_player = 1  # type: ignore
