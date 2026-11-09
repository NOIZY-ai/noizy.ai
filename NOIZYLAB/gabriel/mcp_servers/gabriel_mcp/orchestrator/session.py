#!/usr/bin/env python3
"""
GABRIEL MCP v2 — Session Manager
==================================
Gabriel OWNS the session. Not Claude.

Session phases:
  initialized → characters_loaded → chamber_active → processing → synthesized → closed

Claude sees phase transitions. Gabriel holds the full state.
"""

from datetime import datetime
from typing import Optional

from ..state.store import StateStore


# Valid phase transitions
PHASE_TRANSITIONS = {
    "initialized": ["characters_loaded", "closed"],
    "characters_loaded": ["chamber_active", "closed"],
    "chamber_active": ["processing", "closed"],
    "processing": ["synthesized", "chamber_active", "closed"],
    "synthesized": ["chamber_active", "closed"],
    "closed": [],
}


class SessionManager:
    """
    Manages dream chamber session lifecycle.

    Enforces phase transitions. Delegates state persistence
    to StateStore. Returns only summaries across MCP wire.
    """

    def __init__(self, store: StateStore):
        self.store = store
        self._current_session_id: Optional[str] = None

    @property
    def current_session(self) -> Optional[str]:
        return self._current_session_id

    def start(self, metadata: Optional[dict] = None) -> dict:
        """Start a new chamber session."""
        session_id = f"chamber_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        summary = self.store.create_session(session_id, metadata)
        self._current_session_id = session_id
        return summary

    def advance_phase(self, session_id: str, new_phase: str) -> dict:
        """Advance session to next phase. Enforces valid transitions."""
        session = self.store.get_session(session_id)
        if not session:
            raise KeyError(f"Session not found: {session_id}")

        current_phase = session["phase"]
        valid_next = PHASE_TRANSITIONS.get(current_phase, [])

        if new_phase not in valid_next:
            raise ValueError(
                f"Invalid transition: {current_phase} → {new_phase}. "
                f"Valid: {valid_next}"
            )

        session["history"].append({
            "from": current_phase,
            "to": new_phase,
            "at": datetime.now().isoformat(),
        })

        return self.store.update_session(session_id, {"phase": new_phase})

    def load_characters(self, session_id: str, characters: dict[str, dict]) -> dict:
        """
        Load characters into session.

        Args:
            characters: {"morrison": {config}, "poet": {config}, ...}

        Gabriel holds full character configs locally.
        Claude gets: character names + ready status.
        """
        session = self.store.get_session(session_id)
        if not session:
            raise KeyError(f"Session not found: {session_id}")

        self.store.update_session(session_id, {"characters": characters})

        if session["phase"] == "initialized":
            self.advance_phase(session_id, "characters_loaded")

        return self.store.summarize(session_id)

    def get_status(self, session_id: Optional[str] = None) -> dict:
        """Get session status. Uses current session if none specified."""
        sid = session_id or self._current_session_id
        if not sid:
            return {"error": "No active session", "sessions": self.store.list_sessions(5)}
        return self.store.summarize(sid)

    def close(self, session_id: Optional[str] = None) -> dict:
        """Close a session."""
        sid = session_id or self._current_session_id
        if not sid:
            raise KeyError("No active session to close")

        summary = self.store.close_session(sid)
        if sid == self._current_session_id:
            self._current_session_id = None
        return summary

    def list_sessions(self, limit: int = 20) -> list[dict]:
        """List recent sessions."""
        return self.store.list_sessions(limit)
