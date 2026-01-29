"""Unit tests for Tile model."""

import pytest
from src.models.tile import Tile


class TestTile:
    """Test suite for Tile model."""
    
    def test_tile_creation(self) -> None:
        """Test basic tile creation."""
        tile = Tile(3, 5)
        assert tile.pips_a == 3
        assert tile.pips_b == 5
    
    def test_tile_id_property(self) -> None:
        """Test that tile ID is always sorted (min, max)."""
        tile1 = Tile(3, 5)
        tile2 = Tile(5, 3)  # Swapped
        
        # Both should have same canonical ID
        assert tile1.id == (3, 5)
        assert tile2.id == (3, 5)
    
    def test_tile_total_pips(self) -> None:
        """Test total pip calculation."""
        tile = Tile(4, 5)
        assert tile.total_pips == 9
    
    def test_tile_double(self) -> None:
        """Test double tile (same pips on both sides)."""
        double = Tile(6, 6)
        assert double.pips_a == 6
        assert double.pips_b == 6
        assert double.total_pips == 12
        assert double.id == (6, 6)
    
    def test_tile_blank(self) -> None:
        """Test blank-blank tile (0|0)."""
        blank = Tile(0, 0)
        assert blank.total_pips == 0
        assert blank.id == (0, 0)
    
    def test_tile_equality(self) -> None:
        """Test tile equality (based on ID, not order)."""
        tile1 = Tile(2, 4)
        tile2 = Tile(4, 2)  # Swapped
        tile3 = Tile(2, 5)  # Different
        
        assert tile1 == tile2  # Same ID
        assert tile1 != tile3  # Different ID
    
    def test_tile_hashable(self) -> None:
        """Test that tiles can be hashed (use in sets/dicts)."""
        tile1 = Tile(2, 4)
        tile2 = Tile(4, 2)  # Swapped
        
        tile_set = {tile1, tile2}
        assert len(tile_set) == 1  # Should be one unique tile
    
    def test_tile_invalid_pips_a(self) -> None:
        """Test that invalid pips_a raises error."""
        with pytest.raises(ValueError, match="pips_a must be 0-6"):
            Tile(7, 3)
    
    def test_tile_invalid_pips_b(self) -> None:
        """Test that invalid pips_b raises error."""
        with pytest.raises(ValueError, match="pips_b must be 0-6"):
            Tile(3, -1)
    
    def test_tile_frozen(self) -> None:
        """Test that tile is immutable (frozen)."""
        tile = Tile(3, 5)
        with pytest.raises(AttributeError):
            tile.pips_a = 4  # type: ignore
