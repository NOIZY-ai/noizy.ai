"""
GABRIEL Utilities Module
MC96DIGIUNIVERSE AI LIFELUV
"""

import subprocess
import os
import sys
from pathlib import Path
from typing import Optional, Tuple, List
from datetime import datetime
import json
import hashlib


def run_command(
    command: str,
    timeout: int = 30,
    capture: bool = True
) -> Tuple[bool, str]:
    """Run a shell command safely"""
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=capture,
            text=True,
            timeout=timeout
        )
        output = result.stdout + result.stderr if capture else ""
        return result.returncode == 0, output
    except subprocess.TimeoutExpired:
        return False, "Command timed out"
    except Exception as e:
        return False, str(e)


def speak(text: str, voice: str = "Oliver", wait: bool = True) -> bool:
    """Speak text using macOS TTS"""
    try:
        if wait:
            subprocess.run(["say", "-v", voice, text], check=True)
        else:
            subprocess.Popen(["say", "-v", voice, text])
        return True
    except Exception:
        return False


def get_timestamp() -> str:
    """Get current ISO timestamp"""
    return datetime.now().isoformat()


def ensure_dir(path: Path) -> Path:
    """Ensure directory exists"""
    path.mkdir(parents=True, exist_ok=True)
    return path


def hash_content(content: str) -> str:
    """Generate SHA-256 hash of content"""
    return hashlib.sha256(content.encode()).hexdigest()


def find_files(
    root: Path,
    pattern: str = "*",
    recursive: bool = True
) -> List[Path]:
    """Find files matching pattern"""
    if recursive:
        return list(root.rglob(pattern))
    return list(root.glob(pattern))


def load_json(path: Path) -> dict:
    """Load JSON file"""
    with open(path) as f:
        return json.load(f)


def save_json(path: Path, data: dict, indent: int = 2) -> None:
    """Save data to JSON file"""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w') as f:
        json.dump(data, f, indent=indent)


def print_banner(title: str, width: int = 68) -> None:
    """Print a formatted banner"""
    print("╔" + "═" * width + "╗")
    print("║" + title.center(width) + "║")
    print("╚" + "═" * width + "╝")


def print_status(name: str, status: str, ok: bool = True) -> None:
    """Print a status line"""
    icon = "✅" if ok else "❌"
    print(f"  {icon} {name}: {status}")


class Timer:
    """Simple context manager timer"""

    def __init__(self, name: str = "Operation"):
        self.name = name
        self.start_time: Optional[float] = None
        self.end_time: Optional[float] = None

    def __enter__(self):
        import time
        self.start_time = time.time()
        return self

    def __exit__(self, *args):
        import time
        self.end_time = time.time()

    @property
    def elapsed(self) -> float:
        if self.start_time is None:
            return 0.0
        end = self.end_time or __import__('time').time()
        return end - self.start_time

    def __str__(self) -> str:
        return f"{self.name}: {self.elapsed:.3f}s"
