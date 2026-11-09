#!/usr/bin/env python3
"""
GOD BRAIN - Gabriel Orchestration & Direction
MC96DIGIUNIVERSE AI LIFELUV INFINITE ENERGY
GORUNFREEX1000 SUPREME INTEGRATION

The central nervous system of the GABRIEL ecosystem.
Handles voice output, system coordination, and AI integration.
"""

import subprocess
import sys
import os
from pathlib import Path
from typing import Optional
import json
from datetime import datetime

class GodBrain:
    """Gabriel's Central Intelligence System"""

    def __init__(self):
        self.home = Path.home()
        self.gabriel_root = self.home / "GABRIEL_UNIFIED"
        self.voice = "Oliver"  # macOS voice
        self.energy_level = "∞ INFINITE"
        self.active = True
        self.log_file = self.gabriel_root / "logs" / "god_brain.log"
        self._ensure_directories()

    def _ensure_directories(self):
        """Ensure required directories exist"""
        dirs = ["logs", "data", "config", "scripts"]
        for d in dirs:
            (self.gabriel_root / d).mkdir(parents=True, exist_ok=True)

    def speak(self, text: str, voice: Optional[str] = None) -> bool:
        """
        Speaks text using macOS text-to-speech.
        Returns True if successful.
        """
        v = voice or self.voice
        try:
            print(f"🗣️  GOD BRAIN [{v}]: {text}")
            subprocess.run(["say", "-v", v, text], check=True, capture_output=True)
            self._log(f"SPEAK: {text}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Speech error: {e}")
            return False
        except FileNotFoundError:
            print("❌ 'say' command not found (macOS only)")
            return False

    def speak_async(self, text: str, voice: Optional[str] = None) -> subprocess.Popen:
        """Non-blocking speech - returns process handle"""
        v = voice or self.voice
        print(f"🗣️  GOD BRAIN [{v}]: {text}")
        return subprocess.Popen(["say", "-v", v, text])

    def execute_command(self, command: str, timeout: int = 30) -> tuple:
        """Execute a shell command safely"""
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            output = result.stdout + result.stderr
            self._log(f"EXEC: {command} -> {result.returncode}")
            return result.returncode == 0, output
        except subprocess.TimeoutExpired:
            return False, "Command timed out"
        except Exception as e:
            return False, str(e)

    def activate_dreamchamber(self) -> bool:
        """Activate the DreamChamber subsystem"""
        dreamchamber = self.gabriel_root / "core" / "dreamchamber.py"
        if dreamchamber.exists():
            self.speak("Activating DreamChamber")
            success, output = self.execute_command(f"python3 {dreamchamber}")
            return success
        else:
            self.speak("DreamChamber not found")
            return False

    def get_system_status(self) -> dict:
        """Get current system status"""
        status = {
            "active": self.active,
            "energy_level": self.energy_level,
            "timestamp": datetime.now().isoformat(),
            "voice": self.voice,
            "components": {}
        }

        # Check component status
        components = {
            "dreamchamber": self.gabriel_root / "core" / "dreamchamber.py",
            "visual_scanner": self.gabriel_root / "core" / "visual_scanner.py",
            "mc96_server": self.gabriel_root / "core" / "mc96_server_x1000.py",
            "launcher": self.gabriel_root / "GORUNFREEX1000.py"
        }

        for name, path in components.items():
            status["components"][name] = "READY" if path.exists() else "MISSING"

        return status

    def broadcast(self, message: str) -> None:
        """Broadcast a message to all systems"""
        print(f"""
╔══════════════════════════════════════════════════════════════════╗
║  GOD BRAIN BROADCAST
╠══════════════════════════════════════════════════════════════════╣
║  {message[:60]:<60} ║
╚══════════════════════════════════════════════════════════════════╝
""")
        self.speak(message)
        self._log(f"BROADCAST: {message}")

    def _log(self, message: str) -> None:
        """Log message to file"""
        try:
            self.log_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.log_file, "a") as f:
                timestamp = datetime.now().isoformat()
                f.write(f"[{timestamp}] {message}\n")
        except Exception:
            pass  # Silent fail for logging

    def awaken(self) -> None:
        """Awaken the God Brain"""
        self.broadcast("The DreamChamber is open. Gabriel, awaken.")
        status = self.get_system_status()
        print(f"\n📊 System Status: {json.dumps(status, indent=2)}")


# Legacy compatibility function
def speak_to_portal(text: str) -> None:
    """Legacy function for backward compatibility"""
    brain = GodBrain()
    brain.speak(text)


# Quick activation function
def awaken():
    """Quick awaken function"""
    brain = GodBrain()
    brain.awaken()
    return brain


# Main entry point
if __name__ == "__main__":
    brain = awaken()
