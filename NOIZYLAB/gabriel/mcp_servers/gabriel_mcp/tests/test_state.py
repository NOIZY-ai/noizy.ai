#!/usr/bin/env python3
"""Tests for state persistence layer."""

import pytest
import tempfile
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from state.store import StateStore


@pytest.fixture
def store():
    """Create a StateStore with a temp directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield StateStore(Path(tmpdir))


class TestStateStore:
    def test_create_session(self, store):
        """Test session creation."""
        result = store.create_session("test_001", {"test": True})
        assert result["session_id"] == "test_001"
        assert result["phase"] == "initialized"

    def test_get_session(self, store):
        """Test session retrieval."""
        store.create_session("test_002")
        session = store.get_session("test_002")
        assert session is not None
        assert session["id"] == "test_002"

    def test_update_session(self, store):
        """Test session updates."""
        store.create_session("test_003")
        result = store.update_session("test_003", {"phase": "processing"})
        assert result["phase"] == "processing"

    def test_close_session(self, store):
        """Test session closing."""
        store.create_session("test_004")
        result = store.close_session("test_004")
        assert result["phase"] == "closed"

    def test_summarize_is_lightweight(self, store):
        """Verify summary doesn't include heavy data."""
        store.create_session("test_005")
        store.update_session("test_005", {
            "characters": {
                "morrison": {"full_config": "lots of data here"},
                "poet": {"full_config": "more heavy data"},
            }
        })
        summary = store.summarize("test_005")

        # Summary should only have names, not full configs
        assert "characters_loaded" in summary
        assert isinstance(summary["characters_loaded"], list)
        assert "full_config" not in str(summary)

    def test_list_sessions(self, store):
        """Test session listing."""
        store.create_session("list_001")
        store.create_session("list_002")
        sessions = store.list_sessions()
        assert len(sessions) >= 2


class TestSessionPersistence:
    def test_persistence_to_disk(self, store):
        """Test that sessions persist to disk."""
        store.create_session("persist_001")
        session_file = store.state_dir / "session_persist_001.json"
        assert session_file.exists()

    def test_reload_from_disk(self):
        """Test session reload after store recreation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir)

            # Create session with first store
            store1 = StateStore(path)
            store1.create_session("reload_001")
            store1.update_session("reload_001", {"phase": "processing"})

            # Clear memory cache
            store1._active_sessions.clear()

            # Create new store, should load from disk
            store2 = StateStore(path)
            session = store2.get_session("reload_001")
            assert session is not None
            assert session["phase"] == "processing"
