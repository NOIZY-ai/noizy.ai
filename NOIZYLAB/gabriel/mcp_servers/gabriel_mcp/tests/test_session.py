#!/usr/bin/env python3
"""Tests for session state machine."""

import pytest
import tempfile
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from state.store import StateStore
from orchestrator.session import SessionManager, PHASE_TRANSITIONS


@pytest.fixture
def manager():
    """Create a SessionManager with temp state."""
    with tempfile.TemporaryDirectory() as tmpdir:
        store = StateStore(Path(tmpdir))
        yield SessionManager(store)


class TestSessionManager:
    def test_start_session(self, manager):
        """Test session start."""
        result = manager.start()
        assert "session_id" in result
        assert result["phase"] == "initialized"
        assert manager.current_session is not None

    def test_advance_phase_valid(self, manager):
        """Test valid phase transition."""
        summary = manager.start()
        session_id = summary["session_id"]

        # Load characters first (required transition)
        manager.load_characters(session_id, {"test_char": {}})

        result = manager.advance_phase(session_id, "chamber_active")
        assert result["phase"] == "chamber_active"

    def test_advance_phase_invalid(self, manager):
        """Test invalid phase transition raises error."""
        summary = manager.start()
        session_id = summary["session_id"]

        # Can't jump directly to processing from initialized
        with pytest.raises(ValueError) as exc:
            manager.advance_phase(session_id, "processing")
        assert "Invalid transition" in str(exc.value)

    def test_load_characters(self, manager):
        """Test character loading."""
        summary = manager.start()
        session_id = summary["session_id"]

        result = manager.load_characters(session_id, {
            "morrison": {"voice": "intense"},
            "poet": {"voice": "gentle"},
        })

        assert result["character_count"] == 2
        assert result["phase"] == "characters_loaded"

    def test_close_session(self, manager):
        """Test session closing."""
        summary = manager.start()
        session_id = summary["session_id"]

        result = manager.close(session_id)
        assert result["phase"] == "closed"
        assert manager.current_session is None


class TestPhaseTransitions:
    def test_all_phases_have_transitions(self):
        """Every phase should have defined transitions."""
        required_phases = [
            "initialized", "characters_loaded", "chamber_active",
            "processing", "synthesized", "closed"
        ]
        for phase in required_phases:
            assert phase in PHASE_TRANSITIONS

    def test_closed_is_terminal(self):
        """Closed should have no valid next transitions."""
        assert PHASE_TRANSITIONS["closed"] == []

    def test_can_always_close(self):
        """Should be able to close from any non-closed phase."""
        for phase, transitions in PHASE_TRANSITIONS.items():
            if phase != "closed":
                assert "closed" in transitions, f"Phase {phase} should allow closing"
