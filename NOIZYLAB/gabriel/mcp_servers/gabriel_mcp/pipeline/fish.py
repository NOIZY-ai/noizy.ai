#!/usr/bin/env python3
"""
GABRIEL MCP v2 — Fish Speech Integration
==========================================
Voice cloning via Fish Speech.
Runs locally on M2 Ultra. Zero cloud.

Fish Speech excels at voice cloning from short reference audio.
Combined with Cocoro for emotional control, creates the
character voice pipeline.
"""

import asyncio
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

from ..config import AUDIO_OUTPUT_DIR, CHARACTERS_DIR


class FishEngine:
    """
    Fish Speech voice cloning engine.

    On M2 Ultra with Fish Speech installed: runs real cloning.
    Otherwise: returns job tracking stubs for pipeline testing.
    """

    def __init__(self):
        self._available = self._check_availability()
        self._jobs: dict[str, dict] = {}
        self._voice_cache: dict[str, Any] = {}

    def _check_availability(self) -> bool:
        """Check if Fish Speech is available."""
        try:
            # Try importing Fish Speech
            # from fish_speech import FishSpeech
            # self._engine = FishSpeech()
            # return True
            return False  # Stub until Fish is wired
        except ImportError:
            return False

    @property
    def available(self) -> bool:
        return self._available

    async def clone_voice(
        self,
        text: str,
        character: str,
        reference_audio: Optional[Path] = None,
        preset: Optional[dict] = None,
        output_path: Optional[Path] = None,
    ) -> dict:
        """
        Clone voice from reference and synthesize text.

        Args:
            text: Text to synthesize
            character: Character name (loads config)
            reference_audio: Path to reference audio (loaded from config if None)
            preset: Fish preset overrides
            output_path: Where to save output

        Returns:
            Job result with output path
        """
        job_id = f"fish_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"

        # Load character config
        char_config = self._load_character_config(character)
        if preset is None:
            preset = char_config.get("fish_preset", {})

        # Resolve reference audio
        if reference_audio is None:
            voice_profile = char_config.get("voice_profile", {})
            ref_filename = voice_profile.get("reference_audio")
            if ref_filename:
                reference_audio = CHARACTERS_DIR / "audio" / ref_filename

        output_path = output_path or AUDIO_OUTPUT_DIR / f"{job_id}.wav"

        job = {
            "id": job_id,
            "engine": "fish_speech",
            "character": character,
            "text_length": len(text),
            "reference_audio": str(reference_audio) if reference_audio else None,
            "preset": preset,
            "output_path": str(output_path),
            "started_at": datetime.now().isoformat(),
            "status": "processing",
        }
        self._jobs[job_id] = job

        if self._available:
            result = await self._process_real(text, reference_audio, preset, output_path)
            job.update(result)
        else:
            await asyncio.sleep(0.1)
            job["status"] = "stub_complete"
            job["stub"] = True
            job["estimated_duration_sec"] = len(text) * 0.06

        job["completed_at"] = datetime.now().isoformat()
        return job

    async def _process_real(
        self,
        text: str,
        reference_audio: Optional[Path],
        preset: dict,
        output_path: Path,
    ) -> dict:
        """
        Real Fish Speech processing.

        Wire when Fish Speech is installed:
        - Load or cache voice embedding from reference audio
        - Run inference with preset params
        - Write output
        """
        # TODO: Wire real Fish Speech inference
        # speaker_embedding = self._get_or_create_embedding(reference_audio)
        # self._engine.synthesize(
        #     text=text,
        #     speaker=speaker_embedding,
        #     temperature=preset.get("temperature", 0.8),
        #     top_p=preset.get("top_p", 0.9),
        #     output_path=output_path,
        # )
        return {
            "status": "complete",
            "duration_sec": None,
        }

    def _load_character_config(self, character: str) -> dict:
        """Load full character config."""
        config_path = CHARACTERS_DIR / f"{character}.json"
        if config_path.exists():
            try:
                return json.loads(config_path.read_text())
            except json.JSONDecodeError:
                pass
        return {}

    async def create_voice_embedding(
        self,
        character: str,
        reference_audio: Path,
    ) -> dict:
        """
        Pre-compute voice embedding from reference audio.
        Caches for faster synthesis.
        """
        job_id = f"embedding_{character}_{datetime.now().strftime('%H%M%S')}"

        if self._available:
            # TODO: Real embedding creation
            # embedding = self._engine.create_embedding(reference_audio)
            # self._voice_cache[character] = embedding
            pass

        return {
            "id": job_id,
            "character": character,
            "reference_audio": str(reference_audio),
            "cached": character in self._voice_cache,
            "status": "complete" if self._available else "stub",
        }

    async def batch_synthesize(
        self,
        items: list[dict],
    ) -> list[dict]:
        """
        Batch synthesize with voice cloning.

        Args:
            items: List of {"text": str, "character": str}

        Returns:
            List of job results
        """
        tasks = [
            self.clone_voice(
                text=item["text"],
                character=item.get("character", "default"),
                preset=item.get("preset"),
            )
            for item in items
        ]
        return await asyncio.gather(*tasks)

    def get_job(self, job_id: str) -> Optional[dict]:
        return self._jobs.get(job_id)

    def list_jobs(self, limit: int = 20) -> list[dict]:
        jobs = list(self._jobs.values())
        return sorted(jobs, key=lambda j: j.get("started_at", ""), reverse=True)[:limit]
