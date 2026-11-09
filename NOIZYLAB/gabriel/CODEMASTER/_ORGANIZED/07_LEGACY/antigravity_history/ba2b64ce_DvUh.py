#!/usr/bin/env python3
"""
Gabriel Voice V1.0 - Text-to-Speech Engine
Local TTS (macOS say) with optional ElevenLabs integration and caching.
"""

import subprocess
import hashlib
import json
import asyncio
from pathlib import Path
from datetime import datetime
from typing import Optional

# Configuration
CACHE_DIR = Path.home() / "NOIZYLAB" / "cache" / "voice"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

# Voice profiles for macOS
MAC_VOICES = {
    "gabriel": "Daniel",  # Primary - British male
    "authority": "Alex",  # American male
    "calm": "Samantha",  # American female
    "british": "Daniel",
    "irish": "Moira",
}

# Default voice
DEFAULT_VOICE = "Daniel"


class GabrielVoice:
    """Text-to-Speech engine with caching."""

    def __init__(self, backend: str = "local"):
        self.backend = backend
        self.cache_stats = {"hits": 0, "misses": 0}
        self.voice = DEFAULT_VOICE

    def _hash(self, text: str, voice: str) -> str:
        """Generate cache key."""
        content = f"{text.strip()}:{voice}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]

    def _get_cache_path(self, text: str, voice: str) -> Path:
        """Get cache file path for text/voice combo."""
        key = self._hash(text, voice)
        return CACHE_DIR / f"{key}.aiff"

    def _cache_exists(self, text: str, voice: str) -> bool:
        """Check if text is already cached."""
        return self._get_cache_path(text, voice).exists()

    async def speak(
        self,
        text: str,
        voice: str = None,
        rate: int = 185,
        wait: bool = True,
    ) -> Optional[Path]:
        """
        Speak text using TTS.

        Args:
            text: Text to speak
            voice: Voice name (see MAC_VOICES)
            rate: Speech rate (words per minute)
            wait: Wait for speech to complete
        """
        if not text.strip():
            return None

        # Resolve voice
        voice = MAC_VOICES.get(voice, voice) or self.voice

        # Check cache
        cache_path = self._get_cache_path(text, voice)
        if cache_path.exists():
            self.cache_stats["hits"] += 1
            # Play cached audio
            cmd = ["afplay", str(cache_path)]
            if wait:
                subprocess.run(cmd, capture_output=True)
            else:
                subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return cache_path

        self.cache_stats["misses"] += 1

        # Generate and cache
        await self._generate_and_cache(text, voice, rate, cache_path)

        # Play
        cmd = ["afplay", str(cache_path)]
        if wait:
            subprocess.run(cmd, capture_output=True)
        else:
            subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        return cache_path

    async def _generate_and_cache(
        self,
        text: str,
        voice: str,
        rate: int,
        output_path: Path,
    ):
        """Generate audio file using macOS say."""
        cmd = [
            "say",
            "-v", voice,
            "-r", str(rate),
            "-o", str(output_path),
            text,
        ]
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.DEVNULL,
            stderr=asyncio.subprocess.DEVNULL,
        )
        await proc.wait()

    def say_sync(self, text: str, voice: str = None, rate: int = 185):
        """Synchronous speak (no caching, direct output)."""
        voice = MAC_VOICES.get(voice, voice) or self.voice
        cmd = ["say", "-v", voice, "-r", str(rate), text]
        subprocess.run(cmd)

    def get_available_voices(self) -> list[str]:
        """Get list of available macOS voices."""
        try:
            result = subprocess.run(
                ["say", "-v", "?"],
                capture_output=True,
                text=True,
            )
            voices = []
            for line in result.stdout.split("\n"):
                if line.strip():
                    parts = line.split()
                    if parts:
                        voices.append(parts[0])
            return voices
        except Exception:
            return list(MAC_VOICES.values())

    def get_stats(self) -> dict:
        """Get voice engine statistics."""
        cache_files = list(CACHE_DIR.glob("*.aiff"))
        cache_size = sum(f.stat().st_size for f in cache_files)

        return {
            "backend": self.backend,
            "default_voice": self.voice,
            "cache_hits": self.cache_stats["hits"],
            "cache_misses": self.cache_stats["misses"],
            "hit_rate": round(
                self.cache_stats["hits"]
                / max(1, self.cache_stats["hits"] + self.cache_stats["misses"])
                * 100,
                1,
            ),
            "cached_files": len(cache_files),
            "cache_size_mb": round(cache_size / (1024 * 1024), 2),
        }

    def clear_cache(self) -> int:
        """Clear voice cache. Returns number of files deleted."""
        count = 0
        for f in CACHE_DIR.glob("*.aiff"):
            try:
                f.unlink()
                count += 1
            except Exception:
                pass
        return count


# ============================================================================
# CLI
# ============================================================================

if __name__ == "__main__":
    import sys

    voice = GabrielVoice()

    if len(sys.argv) < 2:
        print("Gabriel Voice Engine V1.0")
        print("Usage: gabriel_voice.py <text> [--voice NAME] [--rate N]")
        print(f"\nAvailable voices: {', '.join(MAC_VOICES.keys())}")
        print(f"\nStats: {json.dumps(voice.get_stats(), indent=2)}")
        sys.exit(0)

    # Parse args
    text_parts = []
    voice_name = None
    rate = 185
    i = 1

    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == "--voice" and i + 1 < len(sys.argv):
            voice_name = sys.argv[i + 1]
            i += 2
        elif arg == "--rate" and i + 1 < len(sys.argv):
            rate = int(sys.argv[i + 1])
            i += 2
        elif arg == "--clear-cache":
            count = voice.clear_cache()
            print(f"Cleared {count} cached files.")
            sys.exit(0)
        elif arg == "--stats":
            print(json.dumps(voice.get_stats(), indent=2))
            sys.exit(0)
        else:
            text_parts.append(arg)
            i += 1

    text = " ".join(text_parts)

    if text:
        asyncio.run(voice.speak(text, voice=voice_name, rate=rate))
        print(f"✅ Spoke: \"{text[:50]}...\"" if len(text) > 50 else f"✅ Spoke: \"{text}\"")
