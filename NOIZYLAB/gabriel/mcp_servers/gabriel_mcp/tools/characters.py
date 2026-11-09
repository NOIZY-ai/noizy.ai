#!/usr/bin/env python3
"""
GABRIEL MCP v2 — Character Tools
==================================
Character registry and voice routing.

Characters are defined as JSON configs in CHARACTERS_DIR.
Each character has: name, voice_profile, cocoro_preset, personality, etc.

Gabriel holds full character definitions. Claude gets names and status.
"""

import json
from pathlib import Path
from typing import Any

from ..config import CHARACTERS_DIR


class CharacterTools:
    """Character management tools."""

    async def handle(self, action: str, args: dict[str, Any]) -> Any:
        """Dispatch character actions."""
        dispatch = {
            "list": self._list,
            "get": self._get,
            "create": self._create,
            "update": self._update,
            "delete": self._delete,
        }

        fn = dispatch.get(action)
        if not fn:
            return {"error": f"Unknown character action: {action}", "available": list(dispatch.keys())}
        return await fn(args)

    async def _list(self, args: dict) -> dict:
        """List all available character definitions."""
        CHARACTERS_DIR.mkdir(parents=True, exist_ok=True)

        characters = []
        for config_file in CHARACTERS_DIR.glob("*.json"):
            try:
                data = json.loads(config_file.read_text())
                characters.append({
                    "name": config_file.stem,
                    "voice_profile": data.get("voice_profile"),
                    "status": "ready",
                })
            except (json.JSONDecodeError, KeyError):
                characters.append({"name": config_file.stem, "status": "error"})

        return {"characters": characters, "count": len(characters)}

    async def _get(self, args: dict) -> dict:
        """Get a character's configuration summary (not full config)."""
        name = args.get("name")
        if not name:
            return {"error": "character name required"}

        config_path = CHARACTERS_DIR / f"{name}.json"
        if not config_path.exists():
            return {"error": f"Character not found: {name}"}

        try:
            data = json.loads(config_path.read_text())
            # Return summary, not full config — keep tokens low
            return {
                "name": name,
                "voice_profile": data.get("voice_profile"),
                "cocoro_preset": data.get("cocoro_preset"),
                "personality_summary": data.get("personality", "")[:200],
                "status": "ready",
            }
        except json.JSONDecodeError:
            return {"error": f"Invalid config for: {name}"}

    async def _create(self, args: dict) -> dict:
        """Create a new character definition."""
        name = args.get("name")
        if not name:
            return {"error": "character name required"}

        CHARACTERS_DIR.mkdir(parents=True, exist_ok=True)
        config_path = CHARACTERS_DIR / f"{name}.json"

        config = {
            "name": name,
            "voice_profile": args.get("voice_profile"),
            "cocoro_preset": args.get("cocoro_preset"),
            "fish_preset": args.get("fish_preset"),
            "personality": args.get("personality", ""),
            "audio_settings": args.get("audio_settings", {
                "sample_rate": 48000,
                "bit_depth": 24,
            }),
        }

        config_path.write_text(json.dumps(config, indent=2))
        return {"name": name, "status": "created", "path": str(config_path)}

    async def _update(self, args: dict) -> dict:
        """Update an existing character definition."""
        name = args.get("name")
        if not name:
            return {"error": "character name required"}

        config_path = CHARACTERS_DIR / f"{name}.json"
        if not config_path.exists():
            return {"error": f"Character not found: {name}"}

        try:
            config = json.loads(config_path.read_text())
        except json.JSONDecodeError:
            config = {}

        updates = {k: v for k, v in args.items() if k != "name" and v is not None}
        config.update(updates)
        config_path.write_text(json.dumps(config, indent=2))

        return {"name": name, "status": "updated", "fields_updated": list(updates.keys())}

    async def _delete(self, args: dict) -> dict:
        """Delete a character definition."""
        name = args.get("name")
        if not name:
            return {"error": "character name required"}

        config_path = CHARACTERS_DIR / f"{name}.json"
        if config_path.exists():
            config_path.unlink()
            return {"name": name, "status": "deleted"}
        return {"error": f"Character not found: {name}"}
