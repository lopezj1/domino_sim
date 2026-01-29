"""Unit tests for Move model."""

import pytest
from src.models.move import Move
from src.models.tile import Tile


class TestMove:
    """Test suite for Move model."""
    
    def test_move_play(self) -> None:
        """Test play move creation."""
        tile = Tile(3, 5)
        move = Move(action="play", tile=tile)
        
        assert move.action == "play"
        assert move.tile == tile
    
    def test_move_draw(self) -> None:
        """Test draw move creation."""
        move = Move(action="draw")
        
        assert move.action == "draw"
        assert move.tile is None
    
    def test_move_pass(self) -> None:
        """Test pass move creation."""
        move = Move(action="pass")
        
        assert move.action == "pass"
        assert move.tile is None
    
    def test_move_play_without_tile(self) -> None:
        """Test that play without tile raises error."""
        with pytest.raises(ValueError, match="play action requires a tile"):
            Move(action="play", tile=None)
    
    def test_move_draw_with_tile(self) -> None:
        """Test that draw with tile raises error."""
        tile = Tile(3, 5)
        with pytest.raises(ValueError, match="draw action does not accept a tile"):
            Move(action="draw", tile=tile)
    
    def test_move_pass_with_tile(self) -> None:
        """Test that pass with tile raises error."""
        tile = Tile(3, 5)
        with pytest.raises(ValueError, match="pass action does not accept a tile"):
            Move(action="pass", tile=tile)
    
    def test_move_frozen(self) -> None:
        """Test that move is immutable (frozen)."""
        move = Move(action="draw")
        with pytest.raises(AttributeError):
            move.action = "pass"  # type: ignore
