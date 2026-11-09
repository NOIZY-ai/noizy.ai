#!/usr/bin/env python3
"""
GABRIEL MCP v2 — State Store
=============================
Local state persistence. Gabriel owns all session state.
Claude gets lightweight summaries. Full state stays here.

Supports JSON files now, swappable to SQLite later without
changing the interface.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Optional


class StateStore:
    """
    Persistent local state for Gabriel MCP.

    Responsibilities:
    - Session lifecycle (create, update, close)
    - Character state per session
    - Audio pipeline state per session
    - Never sends raw state to Claude — only summaries
    """

    def __init__(self, state_dir: Path):
        self.state_dir = state_dir
        self.state_dir.mkdir(parents=True, exist_ok=True)
        self._active_sessions: dict[str, dict] = {}

    # ── Session Lifecycle ───────────────────────────────────────────

    def create_session(self, session_id: str, metadata: Optional[dict] = None) -> dict:
        """Create a new chamber session. Returns session summary (Claude-safe)."""
        session = {
            "id": session_id,
            "phase": "initialized",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "characters": {},
            "audio_pipeline": {"state": "idle", "queue": []},
            "metadata": metadata or {},
            "history": [],
        }
        self._active_sessions[session_id] = session
        self._persist(session_id)
        return self.summarize(session_id)

    def get_session(self, session_id: str) -> Optional[dict]:
        """Get full session state (internal use only)."""
        if session_id in self._active_sessions:
            return self._active_sessions[session_id]
        return self._load(session_id)

    def update_session(self, session_id: str, updates: dict) -> dict:
        """Apply updates to session state. Returns summary."""
        session = self.get_session(session_id)
        if not session:
            raise KeyError(f"Session not found: {session_id}")

        for key, value in updates.items():
            if key in session and isinstance(session[key], dict) and isinstance(value, dict):
                session[key].update(value)
            else:
                session[key] = value

        session["updated_at"] = datetime.now().isoformat()
        self._active_sessions[session_id] = session
        self._persist(session_id)
        return self.summarize(session_id)

    def close_session(self, session_id: str) -> dict:
        """Close a session. Persists final state, removes from active."""
        session = self.get_session(session_id)
        if not session:
            raise KeyError(f"Session not found: {session_id}")

        session["phase"] = "closed"
        session["closed_at"] = datetime.now().isoformat()
        self._persist(session_id)
        self._active_sessions.pop(session_id, None)
        return self.summarize(session_id)

    def list_sessions(self, limit: int = 20) -> list[dict]:
        """List recent sessions (summaries only)."""
        session_files = sorted(
            self.state_dir.glob("session_*.json"),
            key=lambda p: p.stat().st_mtime,
            reverse=True,
        )[:limit]

        summaries = []
        for f in session_files:
            try:
                data = json.loads(f.read_text())
                summaries.append({
                    "id": data["id"],
                    "phase": data["phase"],
                    "created_at": data["created_at"],
                    "character_count": len(data.get("characters", {})),
                })
            except (json.JSONDecodeError, KeyError):
                continue
        return summaries

    # ── Summary (Claude-safe output) ────────────────────────────────

    def summarize(self, session_id: str) -> dict:
        """
        Return a lightweight summary suitable for Claude.
        This is the TOKEN BOUNDARY — full state stays on Gabriel,
        only this crosses the MCP wire.
        """
        session = self.get_session(session_id)
        if not session:
            return {"error": f"Session not found: {session_id}"}

        return {
            "session_id": session["id"],
            "phase": session["phase"],
            "characters_loaded": list(session.get("characters", {}).keys()),
            "character_count": len(session.get("characters", {})),
            "audio_state": session.get("audio_pipeline", {}).get("state", "unknown"),
            "audio_queue_depth": len(session.get("audio_pipeline", {}).get("queue", [])),
            "updated_at": session.get("updated_at"),
        }

    # ── Persistence ─────────────────────────────────────────────────

    def _session_path(self, session_id: str) -> Path:
        return self.state_dir / f"session_{session_id}.json"

    def _persist(self, session_id: str):
        """Write session state to disk."""
        session = self._active_sessions.get(session_id)
        if session:
            self._session_path(session_id).write_text(
                json.dumps(session, indent=2, default=str)
            )

    def _load(self, session_id: str) -> Optional[dict]:
        """Load session from disk."""
        path = self._session_path(session_id)
        if path.exists():
            try:
                data = json.loads(path.read_text())
                self._active_sessions[session_id] = data
                return data
            except json.JSONDecodeError:
                return None
        return None
