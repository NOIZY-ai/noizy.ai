#!/usr/bin/env python3
"""Tests for chamber orchestration."""

import pytest
import tempfile
from pathlib import Path
import os

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

# Set up test environment
os.environ["GABRIEL_STATE_DIR"] = tempfile.mkdtemp()

from orchestrator.chamber import ChamberOrchestrator


@pytest.fixture
def chamber():
    """Create a ChamberOrchestrator with temp state."""
    with tempfile.TemporaryDirectory() as tmpdir:
        os.environ["GABRIEL_STATE_DIR"] = tmpdir
        yield ChamberOrchestrator()


class TestChamberOrchestrator:
    def test_start_session_empty(self, chamber):
        """Test starting session without characters."""
        result = chamber.start_session()
        assert "session_id" in result
        assert result["phase"] == "initialized"

    def test_start_session_with_characters(self, chamber):
        """Test starting session with character list."""
        result = chamber.start_session(characters=["morrison", "poet"])
        assert result["character_count"] == 2
        assert result["phase"] == "characters_loaded"

    def test_activate_chamber(self, chamber):
        """Test chamber activation."""
        chamber.start_session(characters=["morrison"])
        result = chamber.activate_chamber()
        assert result["phase"] == "chamber_active"

    def test_queue_audio(self, chamber):
        """Test audio job queuing."""
        chamber.start_session(characters=["morrison"])

        result = chamber.queue_audio(
            character="morrison",
            action="process_cocoro",
            params={"text": "test text"},
        )

        assert "job_id" in result
        assert result["queue_depth"] == 1

    def test_audio_status(self, chamber):
        """Test audio status retrieval."""
        chamber.start_session(characters=["morrison"])
        chamber.queue_audio("morrison", "process_cocoro")
        chamber.queue_audio("morrison", "render")

        status = chamber.get_audio_status()
        assert status["queue_depth"] == 2

    def test_full_session_flow(self, chamber):
        """Test complete session lifecycle."""
        # Start
        start = chamber.start_session(characters=["morrison", "poet"])
        assert start["phase"] == "characters_loaded"

        # Activate
        chamber.activate_chamber()

        # Process
        chamber.begin_processing()

        # Queue work
        chamber.queue_audio("morrison", "process_cocoro", {"text": "Break on through"})

        # Complete
        complete = chamber.complete_processing(results={"duration": 5.5})
        assert complete["phase"] == "synthesized"

        # Close
        close = chamber.close_session()
        assert close["phase"] == "closed"


class TestCharacterManagement:
    def test_add_character(self, chamber):
        """Test adding character to session."""
        chamber.start_session()
        result = chamber.add_character("oracle")
        assert "oracle" in result["characters_loaded"]

    def test_remove_character(self, chamber):
        """Test removing character from session."""
        chamber.start_session(characters=["morrison", "poet"])
        result = chamber.remove_character("morrison")
        assert "morrison" not in result["characters_loaded"]
        assert "poet" in result["characters_loaded"]

    def test_list_characters(self, chamber):
        """Test character listing."""
        chamber.start_session(characters=["morrison"])
        result = chamber.list_characters()
        assert "loaded" in result
        assert "available" in result
