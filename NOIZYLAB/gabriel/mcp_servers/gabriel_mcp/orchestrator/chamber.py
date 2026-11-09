#!/usr/bin/env python3
"""
GABRIEL MCP v2 — Chamber Orchestrator
=======================================
The dream chamber controller. Gabriel owns the flow.
Claude handles reasoning. Token stays low.

This is the conductor. It coordinates:
- Session lifecycle via SessionManager
- Character loading and voice routing
- Audio pipeline triggers
- Phase advancement through the chamber experience

Everything heavy stays local. Only summaries cross the wire.
"""

from datetime import datetime
from typing import Optional

from .session import SessionManager
from ..state.store import StateStore
from ..config import STATE_DIR, CHARACTERS_DIR, AUDIO_OUTPUT_DIR


class ChamberOrchestrator:
    """
    Dream Chamber Orchestration Controller.

    North Star: Gabriel owns the flow, Claude handles reasoning,
    token stays low because you're not passing massive context around.
    """

    def __init__(self):
        self.store = StateStore(STATE_DIR)
        self.sessions = SessionManager(self.store)

    # ── Chamber Lifecycle ───────────────────────────────────────────

    def start_session(
        self,
        characters: Optional[list[str]] = None,
        metadata: Optional[dict] = None,
    ) -> dict:
        """
        Start a new dream chamber session.

        Claude sends:  chamber.start(characters=["morrison", "poet"])
        Gabriel does:  loads configs, inits pipeline, sets up state
        Claude gets:   { session_id, characters_loaded: 2, status: "ready" }
        """
        session_summary = self.sessions.start(metadata)
        session_id = session_summary["session_id"]

        if characters:
            char_configs = self._load_character_configs(characters)
            self.sessions.load_characters(session_id, char_configs)
            session_summary = self.sessions.get_status(session_id)

        return session_summary

    def activate_chamber(self, session_id: Optional[str] = None) -> dict:
        """Move chamber to active state. Characters are in, ready to flow."""
        sid = session_id or self.sessions.current_session
        if not sid:
            raise KeyError("No active session")

        return self.sessions.advance_phase(sid, "chamber_active")

    def begin_processing(self, session_id: Optional[str] = None) -> dict:
        """Trigger audio processing pipeline."""
        sid = session_id or self.sessions.current_session
        if not sid:
            raise KeyError("No active session")

        # Update audio pipeline state
        self.store.update_session(sid, {
            "audio_pipeline": {
                "state": "processing",
                "started_at": datetime.now().isoformat(),
                "queue": [],
            }
        })

        return self.sessions.advance_phase(sid, "processing")

    def complete_processing(self, session_id: Optional[str] = None, results: Optional[dict] = None) -> dict:
        """Mark processing complete. Store results locally, return summary."""
        sid = session_id or self.sessions.current_session
        if not sid:
            raise KeyError("No active session")

        updates = {
            "audio_pipeline": {
                "state": "complete",
                "completed_at": datetime.now().isoformat(),
            }
        }

        if results:
            # Full results stay on Gabriel
            updates["processing_results"] = results

        self.store.update_session(sid, updates)
        return self.sessions.advance_phase(sid, "synthesized")

    def close_session(self, session_id: Optional[str] = None) -> dict:
        """Close the chamber session."""
        return self.sessions.close(session_id)

    # ── Character Management ────────────────────────────────────────

    def add_character(self, character_name: str, session_id: Optional[str] = None) -> dict:
        """Add a character to an active session."""
        sid = session_id or self.sessions.current_session
        if not sid:
            raise KeyError("No active session")

        session = self.store.get_session(sid)
        if not session:
            raise KeyError(f"Session not found: {sid}")

        config = self._load_single_character(character_name)
        session["characters"][character_name] = config
        self.store.update_session(sid, {"characters": session["characters"]})

        return self.store.summarize(sid)

    def remove_character(self, character_name: str, session_id: Optional[str] = None) -> dict:
        """Remove a character from session."""
        sid = session_id or self.sessions.current_session
        if not sid:
            raise KeyError("No active session")

        session = self.store.get_session(sid)
        if not session:
            raise KeyError(f"Session not found: {sid}")

        session["characters"].pop(character_name, None)
        self.store.update_session(sid, {"characters": session["characters"]})

        return self.store.summarize(sid)

    def list_characters(self, session_id: Optional[str] = None) -> dict:
        """List characters in current session."""
        sid = session_id or self.sessions.current_session
        if not sid:
            return {"characters": [], "available": self._list_available_characters()}

        session = self.store.get_session(sid)
        return {
            "session_id": sid,
            "loaded": list(session.get("characters", {}).keys()) if session else [],
            "available": self._list_available_characters(),
        }

    # ── Audio Pipeline ──────────────────────────────────────────────

    def queue_audio(
        self,
        character: str,
        action: str,
        params: Optional[dict] = None,
        session_id: Optional[str] = None,
    ) -> dict:
        """
        Queue an audio processing job. Stays on Gabriel.
        Claude just gets confirmation it's queued.

        Actions: "record", "process_cocoro", "process_fish", "render", "export"
        """
        sid = session_id or self.sessions.current_session
        if not sid:
            raise KeyError("No active session")

        session = self.store.get_session(sid)
        if not session:
            raise KeyError(f"Session not found: {sid}")

        job = {
            "id": f"audio_{datetime.now().strftime('%H%M%S')}",
            "character": character,
            "action": action,
            "params": params or {},
            "queued_at": datetime.now().isoformat(),
            "status": "queued",
        }

        pipeline = session.get("audio_pipeline", {"state": "idle", "queue": []})
        pipeline["queue"].append(job)
        pipeline["state"] = "has_work"
        self.store.update_session(sid, {"audio_pipeline": pipeline})

        # Return just the job ID and queue depth — not the full payload
        return {
            "job_id": job["id"],
            "character": character,
            "action": action,
            "queue_depth": len(pipeline["queue"]),
        }

    def get_audio_status(self, session_id: Optional[str] = None) -> dict:
        """Get audio pipeline status (summary only)."""
        sid = session_id or self.sessions.current_session
        if not sid:
            return {"error": "No active session"}

        session = self.store.get_session(sid)
        if not session:
            return {"error": f"Session not found: {sid}"}

        pipeline = session.get("audio_pipeline", {})
        queue = pipeline.get("queue", [])

        return {
            "state": pipeline.get("state", "idle"),
            "queue_depth": len(queue),
            "jobs": [
                {"id": j["id"], "character": j["character"], "action": j["action"], "status": j["status"]}
                for j in queue
            ],
        }

    # ── Status ──────────────────────────────────────────────────────

    def status(self, session_id: Optional[str] = None) -> dict:
        """Full chamber status — still lightweight for Claude."""
        sid = session_id or self.sessions.current_session

        result = {
            "has_active_session": sid is not None,
            "server_version": "2.0.0",
        }

        if sid:
            result["session"] = self.store.summarize(sid)
            result["audio"] = self.get_audio_status(sid)

        result["recent_sessions"] = self.sessions.list_sessions(5)
        return result

    # ── Internal Helpers ────────────────────────────────────────────

    def _load_character_configs(self, names: list[str]) -> dict[str, dict]:
        """Load character configurations from disk."""
        configs = {}
        for name in names:
            configs[name] = self._load_single_character(name)
        return configs

    def _load_single_character(self, name: str) -> dict:
        """
        Load a single character config.
        Returns a placeholder if config file doesn't exist yet.
        Wire your real character definitions into CHARACTERS_DIR.
        """
        import json

        config_path = CHARACTERS_DIR / f"{name}.json"
        if config_path.exists():
            try:
                return json.loads(config_path.read_text())
            except json.JSONDecodeError:
                pass

        # Placeholder until real configs are created on M2 Ultra
        return {
            "name": name,
            "status": "loaded",
            "voice_profile": None,
            "cocoro_preset": None,
            "loaded_at": datetime.now().isoformat(),
        }

    def _list_available_characters(self) -> list[str]:
        """List character configs available on disk."""
        if not CHARACTERS_DIR.exists():
            return []
        return [
            p.stem for p in CHARACTERS_DIR.glob("*.json")
        ]
