"""Unit tests for Event model."""

import pytest
from src.models.events import Event


class TestEvent:
    """Test suite for Event model."""
    
    def test_event_deal(self) -> None:
        """Test deal event creation."""
        event = Event(type="deal", timestamp=0, data={"tiles_dealt": 14})
        
        assert event.type == "deal"
        assert event.timestamp == 0
        assert event.data == {"tiles_dealt": 14}
    
    def test_event_play(self) -> None:
        """Test play event creation."""
        event = Event(
            type="play",
            timestamp=1,
            data={"player": 0, "tile": "Tile(3|5)"}
        )
        
        assert event.type == "play"
        assert event.timestamp == 1
        assert event.data["player"] == 0
    
    def test_event_pass(self) -> None:
        """Test pass event creation."""
        event = Event(type="pass", timestamp=5, data={"player": 1})
        
        assert event.type == "pass"
        assert event.timestamp == 5
    
    def test_event_invalid_timestamp(self) -> None:
        """Test that negative timestamp raises error."""
        with pytest.raises(ValueError, match="timestamp must be >= 0"):
            Event(type="deal", timestamp=-1)
    
    def test_event_frozen(self) -> None:
        """Test that event is immutable (frozen)."""
        event = Event(type="deal", timestamp=0)
        with pytest.raises(AttributeError):
            event.timestamp = 1  # type: ignore
    
    def test_event_default_data(self) -> None:
        """Test that data defaults to empty dict."""
        event = Event(type="draw", timestamp=3)
        assert event.data == {}
