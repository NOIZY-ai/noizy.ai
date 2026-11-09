#!/usr/bin/env python3
"""
GABRIEL MCP v2 — Audio Processor
==================================
Main orchestrator for the audio pipeline.
Coordinates Cocoro, Fish, effects, and rendering.

Pipeline flow:
  Text → Character Selection → Engine Selection → Synthesis → Effects → Render

The processor owns the full pipeline. Individual engines (Cocoro, Fish)
handle their domain. This layer coordinates.
"""

import asyncio
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

from .cocoro import CocoroEngine
from .fish import FishEngine
from ..config import AUDIO_OUTPUT_DIR, CHARACTERS_DIR


class AudioProcessor:
    """
    Central audio processing orchestrator.

    Manages:
    - Engine selection based on character config
    - Pipeline routing (Cocoro → Fish → Effects → Render)
    - Job tracking and state
    - Batch processing for multi-character scenes
    """

    def __init__(self):
        self.cocoro = CocoroEngine()
        self.fish = FishEngine()
        self._jobs: dict[str, dict] = {}
        self._pipeline_state = "idle"

    @property
    def status(self) -> dict:
        """Current processor status."""
        return {
            "state": self._pipeline_state,
            "cocoro_available": self.cocoro.available,
            "fish_available": self.fish.available,
            "active_jobs": len([j for j in self._jobs.values() if j.get("status") == "processing"]),
            "total_jobs": len(self._jobs),
        }

    async def process(
        self,
        text: str,
        character: str,
        options: Optional[dict] = None,
    ) -> dict:
        """
        Process text through the full pipeline for a character.

        Automatically selects engine based on character config:
        - voice_profile.type == "fish_speech" → Fish first, Cocoro for emotion
        - voice_profile.type == "cocoro" → Cocoro only
        - No type specified → Cocoro default

        Args:
            text: Text to synthesize
            character: Character name
            options: Processing options (override presets, output path, etc.)

        Returns:
            Job result with final output path
        """
        job_id = f"proc_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
        options = options or {}

        # Load character config
        char_config = self._load_character_config(character)
        voice_profile = char_config.get("voice_profile", {})
        voice_type = voice_profile.get("type", "cocoro")

        output_path = options.get("output_path") or AUDIO_OUTPUT_DIR / f"{job_id}_final.wav"

        job = {
            "id": job_id,
            "character": character,
            "text_length": len(text),
            "voice_type": voice_type,
            "stages": [],
            "output_path": str(output_path),
            "started_at": datetime.now().isoformat(),
            "status": "processing",
        }
        self._jobs[job_id] = job
        self._pipeline_state = "processing"

        try:
            if voice_type == "fish_speech":
                # Fish Speech pipeline: clone voice, then optionally enhance with Cocoro
                fish_result = await self.fish.clone_voice(text, character)
                job["stages"].append({"engine": "fish", "result": fish_result})

                # Optional Cocoro post-processing for emotional enhancement
                if options.get("cocoro_enhance", False):
                    cocoro_result = await self.cocoro.synthesize(
                        text, character,
                        output_path=output_path,
                    )
                    job["stages"].append({"engine": "cocoro_enhance", "result": cocoro_result})
            else:
                # Cocoro pipeline
                cocoro_result = await self.cocoro.synthesize(
                    text, character,
                    output_path=output_path,
                )
                job["stages"].append({"engine": "cocoro", "result": cocoro_result})

            job["status"] = "complete"

        except Exception as e:
            job["status"] = "error"
            job["error"] = str(e)

        job["completed_at"] = datetime.now().isoformat()
        self._pipeline_state = "idle"
        return job

    async def process_scene(
        self,
        lines: list[dict],
        output_dir: Optional[Path] = None,
    ) -> dict:
        """
        Process a multi-character scene.

        Args:
            lines: List of {"character": str, "text": str, "options": dict}
            output_dir: Directory for outputs (auto-created if None)

        Returns:
            Scene result with all line outputs
        """
        scene_id = f"scene_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        output_dir = output_dir or AUDIO_OUTPUT_DIR / scene_id
        output_dir.mkdir(parents=True, exist_ok=True)

        scene = {
            "id": scene_id,
            "line_count": len(lines),
            "output_dir": str(output_dir),
            "started_at": datetime.now().isoformat(),
            "status": "processing",
            "lines": [],
        }

        self._pipeline_state = "processing_scene"

        for i, line in enumerate(lines):
            options = line.get("options", {})
            options["output_path"] = output_dir / f"{i:03d}_{line['character']}.wav"

            result = await self.process(
                text=line["text"],
                character=line["character"],
                options=options,
            )
            scene["lines"].append({
                "index": i,
                "character": line["character"],
                "result": result,
            })

        scene["status"] = "complete"
        scene["completed_at"] = datetime.now().isoformat()
        self._pipeline_state = "idle"

        return scene

    async def process_chamber_session(
        self,
        session_data: dict,
    ) -> dict:
        """
        Process a full dream chamber session.

        This is the top-level entry point for chamber audio processing.
        Takes session data from the orchestrator and runs the full pipeline.

        Args:
            session_data: Session state from ChamberOrchestrator

        Returns:
            Processing results for the session
        """
        session_id = session_data.get("id", "unknown")
        characters = session_data.get("characters", {})
        audio_queue = session_data.get("audio_pipeline", {}).get("queue", [])

        result = {
            "session_id": session_id,
            "processed_jobs": [],
            "started_at": datetime.now().isoformat(),
        }

        self._pipeline_state = "processing_chamber"

        for job_spec in audio_queue:
            character = job_spec.get("character")
            action = job_spec.get("action")
            params = job_spec.get("params", {})

            if action in ("process_cocoro", "process_fish", "render"):
                text = params.get("text", "")
                if text:
                    job_result = await self.process(text, character)
                    result["processed_jobs"].append(job_result)

        result["completed_at"] = datetime.now().isoformat()
        result["job_count"] = len(result["processed_jobs"])
        self._pipeline_state = "idle"

        return result

    def _load_character_config(self, character: str) -> dict:
        """Load character configuration."""
        config_path = CHARACTERS_DIR / f"{character}.json"
        if config_path.exists():
            try:
                return json.loads(config_path.read_text())
            except json.JSONDecodeError:
                pass
        return {}

    def get_job(self, job_id: str) -> Optional[dict]:
        """Get job by ID."""
        return self._jobs.get(job_id)

    def list_jobs(self, limit: int = 20) -> list[dict]:
        """List recent processing jobs."""
        jobs = list(self._jobs.values())
        return sorted(jobs, key=lambda j: j.get("started_at", ""), reverse=True)[:limit]

    def clear_completed(self) -> int:
        """Clear completed jobs from memory. Returns count cleared."""
        completed = [jid for jid, j in self._jobs.items() if j.get("status") in ("complete", "error")]
        for jid in completed:
            del self._jobs[jid]
        return len(completed)
