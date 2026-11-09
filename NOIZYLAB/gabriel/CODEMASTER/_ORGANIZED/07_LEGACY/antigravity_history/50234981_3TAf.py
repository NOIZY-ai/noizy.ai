#!/usr/bin/env python3
"""
Gabriel CLI V1.0 - Unified Command Center
Start, stop, interact, and manage all Gabriel services.
"""

import subprocess
import sys
import os
import json
import asyncio
import signal
from pathlib import Path
from datetime import datetime

# Paths
GABRIEL_DIR = Path(__file__).parent.parent
CORE_DIR = GABRIEL_DIR / "core"
SCRIPTS_DIR = GABRIEL_DIR / "scripts"
PID_FILE = GABRIEL_DIR / ".gabriel.pid"

# Add core to path
sys.path.insert(0, str(CORE_DIR))


def print_banner():
    """Print Gabriel banner."""
    print("""
╔═══════════════════════════════════════════════════════════════╗
║                    🧠 GABRIEL CLI V1.0                        ║
║           Global Autonomous Binary Reality Interface          ║
╚═══════════════════════════════════════════════════════════════╝
""")


def cmd_start(port: int = 8000, background: bool = True):
    """Start Gabriel server."""
    print("🚀 Starting Gabriel Server...")

    if PID_FILE.exists():
        pid = PID_FILE.read_text().strip()
        print(f"⚠️  Gabriel may already be running (PID: {pid})")
        print("   Run 'gabriel stop' first, or 'gabriel status' to check.")
        return

    server_path = CORE_DIR / "gabriel_server.py"

    if background:
        # Start in background
        proc = subprocess.Popen(
            [sys.executable, str(server_path)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            cwd=str(CORE_DIR),
            start_new_session=True,
        )
        PID_FILE.write_text(str(proc.pid))
        print(f"✅ Gabriel started (PID: {proc.pid})")
        print(f"🌐 API: http://localhost:{port}")
        print(f"📡 WebSocket: ws://localhost:{port}/ws")
        print(f"🎭 Avatar: http://localhost:{port}/avatar")
    else:
        # Run in foreground
        os.chdir(str(CORE_DIR))
        subprocess.run([sys.executable, str(server_path)])


def cmd_stop():
    """Stop Gabriel server."""
    if not PID_FILE.exists():
        print("⚠️  Gabriel is not running (no PID file found)")
        return

    pid = PID_FILE.read_text().strip()
    try:
        os.kill(int(pid), signal.SIGTERM)
        print(f"✅ Sent SIGTERM to Gabriel (PID: {pid})")
        PID_FILE.unlink()
    except ProcessLookupError:
        print(f"⚠️  Process {pid} not found (already stopped?)")
        PID_FILE.unlink()
    except Exception as e:
        print(f"❌ Error stopping Gabriel: {e}")


def cmd_status():
    """Check Gabriel status."""
    import httpx

    print("🔍 Checking Gabriel status...")

    # Check PID file
    if PID_FILE.exists():
        pid = PID_FILE.read_text().strip()
        try:
            os.kill(int(pid), 0)
            print(f"✅ Gabriel process running (PID: {pid})")
        except ProcessLookupError:
            print(f"⚠️  PID file exists but process {pid} not found")
            PID_FILE.unlink()
    else:
        print("⚠️  No PID file (Gabriel may not be running)")

    # Check API
    try:
        with httpx.Client(timeout=2.0) as client:
            resp = client.get("http://localhost:8000/status")
            if resp.status_code == 200:
                data = resp.json()
                print(f"\n📊 API Status:")
                print(f"   Name: {data.get('name', 'N/A')}")
                print(f"   Version: {data.get('version', 'N/A')}")
                print(f"   Status: {data.get('status', 'N/A')}")
                print(f"   Mode: {data.get('mode', 'N/A')}")
                print(f"   LLM: {'✅' if data.get('llm_available') else '❌'}")
                print(f"   Uptime: {data.get('uptime_seconds', 0):.0f}s")
                print(f"   Requests: {data.get('requests_processed', 0)}")
                print(f"   Cache Hit Rate: {data.get('cache_hit_rate', 0)}%")
    except Exception as e:
        print(f"❌ API not responding: {e}")


def cmd_chat(message: str):
    """Send a chat message to Gabriel."""
    import httpx

    try:
        with httpx.Client(timeout=30.0) as client:
            resp = client.post(
                "http://localhost:8000/interact",
                json={"text": message},
            )
            if resp.status_code == 200:
                data = resp.json()
                print(f"\n🧠 Gabriel: {data.get('response', 'No response')}")
                meta = data.get("meta", {})
                print(f"   [Latency: {meta.get('latency_ms', 'N/A')}ms, "
                      f"Source: {meta.get('source', 'N/A')}, "
                      f"Intent: {meta.get('intent', 'N/A')}]")
            else:
                print(f"❌ Error: {resp.status_code}")
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print("   Is Gabriel running? Try: gabriel start")


def cmd_voice(text: str):
    """Speak text using Gabriel voice."""
    voice_path = CORE_DIR / "gabriel_voice.py"
    subprocess.run([sys.executable, str(voice_path), text])


def cmd_doctor():
    """Run Gabriel Doctor for code hygiene."""
    doctor_path = SCRIPTS_DIR / "gabriel_doctor.py"
    if doctor_path.exists():
        subprocess.run([
            sys.executable, str(doctor_path),
            "--root", str(GABRIEL_DIR),
            "--fix-python",
            "--delete-empty",
            "--manifest",
        ])
    else:
        print(f"❌ gabriel_doctor.py not found at {doctor_path}")


def cmd_memory():
    """Show memory status."""
    memory_path = CORE_DIR / "memory_engine.py"
    subprocess.run([sys.executable, str(memory_path), "recall"])


def cmd_help():
    """Show help."""
    print_banner()
    print("""
USAGE: gabriel <command> [args]

COMMANDS:
  start [--foreground]  Start Gabriel server
  stop                  Stop Gabriel server
  status                Check system status
  chat <message>        Send a message to Gabriel
  voice <text>          Speak text using TTS
  memory                Show memory status
  doctor                Run code hygiene checks
  help                  Show this help

EXAMPLES:
  gabriel start
  gabriel chat "What is your status?"
  gabriel voice "Hello, I am Gabriel."
  gabriel stop
""")


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        cmd_help()
        return

    command = sys.argv[1].lower()
    args = sys.argv[2:]

    if command == "start":
        foreground = "--foreground" in args or "-f" in args
        cmd_start(background=not foreground)

    elif command == "stop":
        cmd_stop()

    elif command == "status":
        cmd_status()

    elif command == "chat":
        if args:
            cmd_chat(" ".join(args))
        else:
            print("Usage: gabriel chat <message>")

    elif command == "voice":
        if args:
            cmd_voice(" ".join(args))
        else:
            print("Usage: gabriel voice <text>")

    elif command == "memory":
        cmd_memory()

    elif command == "doctor":
        cmd_doctor()

    elif command in ["help", "-h", "--help"]:
        cmd_help()

    else:
        print(f"Unknown command: {command}")
        cmd_help()


if __name__ == "__main__":
    main()
