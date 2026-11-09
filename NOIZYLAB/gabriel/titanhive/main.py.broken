#!/usr/bin/env python3
"""
GABRIEL COMMAND CENTER (TitanHive)
==================================
Textual TUI + MCP + Ollama + Voice Inbox
The Autonomous AI Hive for M2 Ultra (192GB)
"""

from __future__ import annotations

import asyncio
import json
import os
import socket
import subprocess
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

import httpx
import psutil
from dotenv import load_dotenv

try:
    from fastmcp import Client
except ImportError:
    Client = None  # Will work without MCP

from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Header, Footer, Static, Input, RichLog
from textual import work

# -----------------------------
# Config
# -----------------------------

load_dotenv()

GABRIEL_ROOT = Path(os.getenv("GABRIEL_ROOT", Path.home() / "NOIZYLAB" / "GABRIEL"))
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:latest")
OMEN_HOST = os.getenv("OMEN_HOST", "10.0.0.160")
OMEN_USER = os.getenv("OMEN_USER", "admin")

# GABRIEL Voice Configuration (Oliver - British Male Premium)
GABRIEL_VOICE = os.getenv("GABRIEL_VOICE", "Oliver")
GABRIEL_VOICE_RATE = int(os.getenv("GABRIEL_VOICE_RATE", "180"))
GABRIEL_VOICE_ENABLED = os.getenv("GABRIEL_VOICE_ENABLED", "true").lower() == "true"

MCP_CONFIG_PATH = Path(os.getenv("MCP_CONFIG", GABRIEL_ROOT / "titanhive" / "configs" / "mcp.json"))
VOICE_INBOX_DIR = Path(os.getenv("VOICE_INBOX_DIR", Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/TitanHive/inbox"))
VOICE_POLL_SECONDS = float(os.getenv("VOICE_POLL_SECONDS", "1.5"))

# Safety: explicit allowlist for command execution
ALLOWED_COMMANDS = {
    "help",
    "tools",
    "ping",
    "status",
    "scan",
    "speak",
    "ai",
    "models",
    "omen",
    "wake",
    "sync",
    "clear",
    "race",      # Multi-model race
    "use",       # Switch Ollama model
    "gpu",       # GPU memory commands
    "bench",     # Benchmark
    "archive",   # Archive voice files
    "thermal",   # Thermal monitoring
    "speed",     # Network speed test
    "guardian",  # Guardian agent status
    "index",     # Index files (librarian)
    "find",      # Find files
    "top",       # Top processes
    "optimize",  # Memory optimization suggestions
    # MCP tool commands
    "vault.list",
    "vault.search",
    "omen.status",
    "omen.gpu",
    "net.ping",
}

# Try to import agents
try:
    from agents import GuardianAgent, LibrarianAgent, SysAdminAgent
    AGENTS_AVAILABLE = True
except ImportError:
    AGENTS_AVAILABLE = False


# -----------------------------
# Utility Functions
# -----------------------------

def check_ollama() -> tuple[bool, list[str]]:
    """Check if Ollama is running and get available models."""
    try:
        import urllib.request
        with urllib.request.urlopen(f"{OLLAMA_URL}/api/tags", timeout=2) as resp:
            data = json.loads(resp.read())
            models = [m["name"] for m in data.get("models", [])]
            return True, models
    except Exception:
        return False, []


def check_host_reachable(host: str, port: int = 22, timeout: float = 1.0) -> bool:
    """Check if a host is reachable."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((host, port))
        sock.close()
        return True
    except Exception:
        return False


def send_wol(mac_address: str, broadcast: str = "255.255.255.255") -> bool:
    """Send Wake-on-LAN magic packet."""
    try:
        mac_bytes = bytes.fromhex(mac_address.replace(":", "").replace("-", ""))
        magic_packet = b'\xff' * 6 + mac_bytes * 16
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.sendto(magic_packet, (broadcast, 9))
        sock.close()
        return True
    except Exception:
        return False


def gabriel_speak(text: str, voice: str = None, rate: int = None, wait: bool = False) -> bool:
    """
    GABRIEL speaks using Oliver (British Male Premium) voice.

    Args:
        text: Text to speak
        voice: Voice to use (default: Oliver)
        rate: Speech rate in words per minute (default: 180)
        wait: If True, wait for speech to complete

    Returns:
        True if successful
    """
    if not GABRIEL_VOICE_ENABLED:
        return False

    voice = voice or GABRIEL_VOICE
    rate = rate or GABRIEL_VOICE_RATE

    try:
        cmd = ["say", "-v", voice, "-r", str(rate), text]
        if wait:
            subprocess.run(cmd, check=True)
        else:
            subprocess.Popen(cmd)
        return True
    except Exception:
        return False


def gabriel_announce(message: str) -> bool:
    """Quick announcement with GABRIEL's voice."""
    return gabriel_speak(message, wait=False)


# Voice phrases for different events
GABRIEL_PHRASES = {
    "startup": "Gabriel Hive online. All systems operational.",
    "shutdown": "Gabriel Hive shutting down. Goodbye.",
    "error": "An error has occurred.",
    "success": "Task completed successfully.",
    "alert": "Attention. Important notification.",
    "memory_low": "Warning. Memory resources are running low.",
    "omen_online": "HP Omen is now online.",
    "omen_offline": "HP Omen has gone offline.",
    "model_ready": "AI model is ready.",
    "thinking": "Processing your request.",
}


def get_gpu_memory_info() -> dict:
    """Get GPU/Metal memory info on macOS."""
    info = {"wired_mb": 0, "total_mb": 0, "available_mb": 0}
    try:
        # Get total memory
        mem = psutil.virtual_memory()
        info["total_mb"] = int(mem.total / (1024 * 1024))
        info["available_mb"] = int(mem.available / (1024 * 1024))
        info["wired_mb"] = int((mem.total - mem.available) / (1024 * 1024))

        # Try to get Metal GPU info via system_profiler
        result = subprocess.run(
            ["system_profiler", "SPDisplaysDataType", "-json"],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            data = json.loads(result.stdout)
            displays = data.get("SPDisplaysDataType", [])
            for d in displays:
                if "sppci_model" in d:
                    info["gpu_name"] = d.get("sppci_model", "Unknown")
                    break
    except Exception:
        pass
    return info


async def ollama_generate_stream(prompt: str, model: str, callback) -> str:
    """Stream Ollama response, calling callback for each chunk."""
    sys_prompt = (
        "You are GABRIEL, an AI assistant running on a 192GB M2 Ultra Mac Studio. "
        "Be brief, technical, and action-oriented. Suggest commands when appropriate."
    )

    payload = {
        "model": model,
        "prompt": f"SYSTEM: {sys_prompt}\nUSER: {prompt}\n",
        "stream": True,
    }

    full_response = ""
    try:
        async with httpx.AsyncClient(timeout=120) as client:
            async with client.stream(
                "POST",
                f"{OLLAMA_URL.rstrip('/')}/api/generate",
                json=payload
            ) as response:
                async for line in response.aiter_lines():
                    if line:
                        try:
                            chunk = json.loads(line)
                            text = chunk.get("response", "")
                            if text:
                                full_response += text
                                callback(text)
                            if chunk.get("done"):
                                break
                        except json.JSONDecodeError:
                            pass
    except Exception as e:
        callback(f"\n[Error: {e}]")

    return full_response


async def race_models(prompt: str, models: list[str]) -> dict[str, tuple[str, float]]:
    """Race multiple models, return {model: (response, time_ms)}."""
    results = {}

    async def query_model(model: str) -> tuple[str, float]:
        start = asyncio.get_event_loop().time()
        try:
            async with httpx.AsyncClient(timeout=60) as client:
                r = await client.post(
                    f"{OLLAMA_URL.rstrip('/')}/api/generate",
                    json={"model": model, "prompt": prompt, "stream": False}
                )
                data = r.json()
                elapsed = (asyncio.get_event_loop().time() - start) * 1000
                return data.get("response", "")[:200], elapsed
        except Exception as e:
            return f"Error: {e}", 0

    tasks = [query_model(m) for m in models]
    responses = await asyncio.gather(*tasks)

    for model, (resp, time_ms) in zip(models, responses):
        results[model] = (resp, time_ms)

    return results


@dataclass
class McpState:
    client: Optional[Any] = None
    ready: bool = False
    tools: list[str] = field(default_factory=list)


# -----------------------------
# App
# -----------------------------

class GabrielHive(App):
    """GABRIEL Command Center (Textual + Ollama + FastMCP + Voice Inbox)."""

    TITLE = "GABRIEL HIVE"
    SUB_TITLE = "Autonomous AI Command Center"

    CSS = """
    Screen { background: #0a0a0a; }
    #stats-pane { width: 32%; background: #0d1117; border: solid #00ff88; padding: 1; color: #00ff88; }
    #chat-pane  { width: 68%; border: solid #00ff88; padding: 1; }
    #chat-history { height: 1fr; background: #0a0a0a; }
    #cmd { dock: bottom; background: #1a1a2e; }
    .title { text-style: bold; color: #00ffff; }
    .online { color: #00ff00; }
    .offline { color: #ff4444; }
    """

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("c", "clear", "Clear"),
        ("m", "show_models", "Models"),
        ("s", "show_status", "Status"),
    ]

    def __init__(self) -> None:
        super().__init__()
        self.mcp = McpState()
        self._stop = asyncio.Event()
        self._seen_voice_files: set[Path] = set()
        self._ollama_ok = False
        self._ollama_models: list[str] = []
        self._omen_online = False

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Horizontal():
            with Vertical(id="stats-pane"):
                yield Static("[b]GABRIEL HIVE[/b]", classes="title")
                yield Static("─" * 26)
                yield Static(id="ram-usage", content="RAM: ...")
                yield Static(id="gpu-vram", content="VRAM: ...")
                yield Static(id="cpu-usage", content="CPU: ...")
                yield Static(id="cores", content="CORES: ...")
                yield Static("─" * 26)
                yield Static(id="ollama-status", content="OLLAMA: ...")
                yield Static(id="ollama-model", content="MODEL: ...")
                yield Static(id="model-count", content="MODELS: ...")
                yield Static("─" * 26)
                yield Static(id="mcp-status", content="MCP: [b]OFF[/b]")
                yield Static(id="node-omen", content="OMEN: [b]?[/b]")
                yield Static(id="voice-status", content="VOICE: ...")
                yield Static("─" * 26)
                yield Static(id="timestamp", content="...")
            with Vertical(id="chat-pane"):
                yield RichLog(id="chat-history", highlight=True, markup=True)
                yield Input(id="cmd", placeholder="Command or question...")
        yield Footer()

    def on_mount(self) -> None:
        self.set_interval(1.0, self.update_stats)
        self.set_interval(VOICE_POLL_SECONDS, self.poll_voice_inbox)

        # Connect MCP in background
        if Client is not None:
            self.connect_mcp()

        self._log("[b][GABRIEL][/b]: Autonomous AI Hive Online.")
        self._log("[b][GABRIEL][/b]: Type [b]help[/b] for commands or ask naturally.")

    # -----------------------------
    # Actions
    # -----------------------------

    def action_show_models(self) -> None:
        """Show available Ollama models."""
        if self._ollama_models:
            self._log(f"[b][MODELS][/b]: {', '.join(self._ollama_models)}")
        else:
            self._log("[b][MODELS][/b]: Ollama not connected or no models available.")

    def action_show_status(self) -> None:
        """Show full system status."""
        mem = psutil.virtual_memory()
        self._log(f"[b][STATUS][/b]: RAM {mem.used/(1024**3):.0f}GB/{mem.total/(1024**3):.0f}GB | "
                  f"CPU {psutil.cpu_percent()}% | "
                  f"Ollama {'OK' if self._ollama_ok else 'OFF'} | "
                  f"MCP {'OK' if self.mcp.ready else 'OFF'} | "
                  f"Omen {'OK' if self._omen_online else 'OFF'}")

    # -----------------------------
    # UI helpers
    # -----------------------------

    def _log(self, msg: str) -> None:
        self.query_one("#chat-history", RichLog).write(msg)

    def action_clear(self) -> None:
        self.query_one("#chat-history", RichLog).clear()

    # -----------------------------
    # Stats
    # -----------------------------

    def update_stats(self) -> None:
        mem = psutil.virtual_memory()
        cpu = psutil.cpu_percent()
        cores = psutil.cpu_count()

        used_gb = mem.used / (1024**3)
        total_gb = mem.total / (1024**3)
        available_gb = mem.available / (1024**3)

        # RAM display optimized for 192GB system
        self.query_one("#ram-usage", Static).update(
            f"RAM: [b]{used_gb:.0f}GB[/b]/{total_gb:.0f}GB"
        )

        # VRAM (on M2 Ultra, unified memory = GPU memory)
        # Show available memory that could be used for AI models
        vram_available = available_gb
        vram_status = "[b]OK[/b]" if vram_available > 50 else "[yellow]LOW[/yellow]"
        self.query_one("#gpu-vram", Static).update(
            f"VRAM: [b]{vram_available:.0f}GB[/b] free {vram_status}"
        )

        self.query_one("#cpu-usage", Static).update(f"CPU: [b]{cpu:.0f}%[/b]")
        self.query_one("#cores", Static).update(f"CORES: [b]{cores}[/b] (M2 Ultra)")

        # Ollama status (check every 5 seconds via counter)
        if not hasattr(self, "_stat_counter"):
            self._stat_counter = 0
        self._stat_counter += 1
        if self._stat_counter % 5 == 0:
            self._ollama_ok, self._ollama_models = check_ollama()
            self._omen_online = check_host_reachable(OMEN_HOST)

        ollama_txt = "[b]ONLINE[/b]" if self._ollama_ok else "[dim]OFFLINE[/dim]"
        self.query_one("#ollama-status", Static).update(f"OLLAMA: {ollama_txt}")

        model_txt = OLLAMA_MODEL.split(":")[0] if self._ollama_ok else "N/A"
        self.query_one("#ollama-model", Static).update(f"MODEL: [b]{model_txt}[/b]")

        model_count = len(self._ollama_models)
        self.query_one("#model-count", Static).update(f"MODELS: [b]{model_count}[/b] available")

        # MCP status
        mcp_txt = "[b]CONNECTED[/b]" if self.mcp.ready else "[dim]OFF[/dim]"
        self.query_one("#mcp-status", Static).update(f"MCP: {mcp_txt}")

        # Omen status
        omen_txt = "[b]ONLINE[/b]" if self._omen_online else "[dim]OFFLINE[/dim]"
        self.query_one("#node-omen", Static).update(f"OMEN: {omen_txt}")

        # Voice inbox status
        inbox_ok = VOICE_INBOX_DIR.exists()
        inbox_count = len(list(VOICE_INBOX_DIR.glob("*.txt"))) if inbox_ok else 0
        self.query_one("#voice-status", Static).update(
            f"VOICE: {'[b]OK[/b]' if inbox_ok else '[dim]MISSING[/dim]'} ({inbox_count})"
        )

        # Timestamp
        self.query_one("#timestamp", Static).update(
            f"[dim]{datetime.now().strftime('%H:%M:%S')}[/dim]"
        )

    # -----------------------------
    # MCP
    # -----------------------------

    @work(exclusive=True)
    async def connect_mcp(self) -> None:
        """Connect to MCP servers using config file."""
        if not MCP_CONFIG_PATH.exists():
            self._log("[b][GABRIEL][/b]: MCP config not found. Running without MCP.")
            return

        if Client is None:
            self._log("[b][GABRIEL][/b]: FastMCP not installed. pip install fastmcp")
            return

        try:
            config = json.loads(MCP_CONFIG_PATH.read_text(encoding="utf-8"))
            client = Client(config)
        except Exception as e:
            self._log(f"[b][GABRIEL][/b]: MCP config error: {e}")
            return

        self.mcp.client = client
        try:
            async with client:
                await client.ping()
                tools = await client.list_tools()
                self.mcp.tools = [t.name for t in tools]
                self.mcp.ready = True
                self._log(f"[b][GABRIEL][/b]: MCP connected. Tools: {len(self.mcp.tools)}")
                await self._stop.wait()
        except Exception as e:
            self.mcp.ready = False
            self._log(f"[b][GABRIEL][/b]: MCP connection failed: {e}")

    async def mcp_call(self, tool_name: str, args: dict[str, Any]) -> Any:
        if not (self.mcp.ready and self.mcp.client):
            raise RuntimeError("MCP not connected.")
        return await self.mcp.client.call_tool(tool_name, args)

    # -----------------------------
    # Voice inbox
    # -----------------------------

    def poll_voice_inbox(self) -> None:
        """
        Voice Memo bridge:
        - iPhone Shortcut writes .txt files to VOICE_INBOX_DIR
        - This app ingests new .txt files and executes them as commands
        """
        if not VOICE_INBOX_DIR.exists():
            return

        for p in sorted(VOICE_INBOX_DIR.glob("*.txt")):
            if p in self._seen_voice_files:
                continue

            try:
                text = p.read_text(encoding="utf-8").strip()
            except Exception:
                continue

            self._seen_voice_files.add(p)
            if text:
                asyncio.create_task(self.handle_query(text, source="VOICE"))

    # -----------------------------
    # Input / command routing
    # -----------------------------

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        text = event.value.strip()
        if not text:
            return
        self.query_one("#cmd", Input).value = ""
        await self.handle_query(text, source="YOU")

    async def handle_query(self, text: str, source: str = "YOU") -> None:
        self._log(f"[b][{source}][/b]: {text}")

        # Command mode (first token)
        cmd = text.split()[0].lower()

        if cmd in ALLOWED_COMMANDS:
            await self.run_command(text)
            return

        # Otherwise: ask the brain (Ollama)
        await self.ask_ollama(text)

    async def run_command(self, text: str) -> None:
        parts = text.split()
        cmd = parts[0].lower()
        args = parts[1:] if len(parts) > 1 else []

        if cmd == "help":
            self._log("[b]═══ GABRIEL HIVE COMMANDS ═══[/b]")
            self._log("[b]AI & Models:[/b]")
            self._log("  models   - List Ollama models")
            self._log("  use <m>  - Switch model")
            self._log("  race <p> - Race all models")
            self._log("  bench    - Benchmark current model")
            self._log("[b]System:[/b]")
            self._log("  status   - Full status")
            self._log("  gpu      - GPU/VRAM info")
            self._log("  top      - Top memory processes")
            self._log("  thermal  - CPU/GPU temps")
            self._log("  optimize - Memory suggestions")
            self._log("  guardian - Health check")
            self._log("[b]Network:[/b]")
            self._log("  ping     - Test connectivity")
            self._log("  scan     - Scan all nodes")
            self._log("  speed    - Latency test")
            self._log("  omen     - HP Omen status")
            self._log("  wake     - Wake Omen (WoL)")
            self._log("[b]Files:[/b]")
            self._log("  index    - Index all files")
            self._log("  find <q> - Search files")
            self._log("  sync     - Sync to vault")
            self._log("  archive  - Archive voice")
            self._log("[b]Other:[/b]")
            self._log("  speak <t> - Text to speech")
            self._log("  tools    - MCP tools")
            self._log("  clear    - Clear chat")
            self._log("[b][KEYS][/b]: q=quit c=clear m=models s=status")
            return

        if cmd == "clear":
            self.action_clear()
            return

        if cmd == "tools":
            if self.mcp.ready:
                self._log(f"[b][MCP][/b]: {len(self.mcp.tools)} tools: " + ", ".join(self.mcp.tools))
            else:
                self._log("[b][MCP][/b]: Not connected.")
            return

        if cmd == "models":
            self.action_show_models()
            return

        if cmd == "ping":
            self._log("[b][PING][/b]: pong")
            # Check Ollama
            ok, _ = check_ollama()
            self._log(f"  Ollama: {'OK' if ok else 'OFFLINE'}")
            # Check Omen
            omen_ok = check_host_reachable(OMEN_HOST)
            self._log(f"  Omen ({OMEN_HOST}): {'OK' if omen_ok else 'OFFLINE'}")
            # Check MCP
            if self.mcp.ready and self.mcp.client:
                try:
                    await self.mcp.client.ping()
                    self._log("  MCP: OK")
                except Exception:
                    self._log("  MCP: ERROR")
            else:
                self._log("  MCP: OFF")
            return

        if cmd == "status":
            self.action_show_status()
            return

        if cmd == "omen":
            self._log(f"[b][OMEN][/b]: Checking {OMEN_HOST}...")
            if check_host_reachable(OMEN_HOST):
                self._log(f"[b][OMEN][/b]: ONLINE at {OMEN_HOST}")
                # Try to get uptime via SSH if possible
                try:
                    result = subprocess.run(
                        ["ssh", "-o", "ConnectTimeout=2", f"{OMEN_USER}@{OMEN_HOST}", "uptime"],
                        capture_output=True, text=True, timeout=5
                    )
                    if result.returncode == 0:
                        self._log(f"[b][OMEN][/b]: {result.stdout.strip()}")
                except Exception:
                    pass
            else:
                self._log(f"[b][OMEN][/b]: OFFLINE")
            return

        if cmd == "wake":
            # Wake-on-LAN for Omen (you'd need to set the MAC address)
            omen_mac = os.getenv("OMEN_MAC", "")
            if omen_mac:
                self._log(f"[b][WAKE][/b]: Sending WoL to {omen_mac}...")
                if send_wol(omen_mac):
                    self._log("[b][WAKE][/b]: Magic packet sent. Omen should boot in ~30s.")
                else:
                    self._log("[b][WAKE][/b]: Failed to send WoL packet.")
            else:
                self._log("[b][WAKE][/b]: Set OMEN_MAC in .env to enable Wake-on-LAN")
            return

        if cmd == "speak":
            msg = " ".join(args) if args else "Hello from Gabriel Hive"
            subprocess.Popen(["say", "-v", "Oliver", msg])
            self._log(f"[b][SPEAK][/b]: {msg}")
            return

        if cmd == "scan":
            self._log("[b][SCAN][/b]: Scanning network nodes...")
            nodes = [
                ("Mac Studio", "localhost", 22),
                ("HP Omen", OMEN_HOST, 22),
                ("Ollama", "localhost", 11434),
            ]
            for name, host, port in nodes:
                ok = check_host_reachable(host, port, timeout=1.0)
                status = "[b]ONLINE[/b]" if ok else "[dim]OFFLINE[/dim]"
                self._log(f"  {name}: {status}")
            return

        if cmd == "use":
            # Switch active Ollama model
            if not args:
                self._log("[b][USE][/b]: Specify a model. Available:")
                for m in self._ollama_models:
                    marker = " [active]" if m == OLLAMA_MODEL else ""
                    self._log(f"  {m}{marker}")
                return
            new_model = args[0]
            if new_model in self._ollama_models or ":" in new_model:
                global OLLAMA_MODEL
                OLLAMA_MODEL = new_model
                self._log(f"[b][USE][/b]: Switched to [b]{new_model}[/b]")
            else:
                self._log(f"[b][USE][/b]: Model '{new_model}' not found")
            return

        if cmd == "race":
            # Race multiple models with same prompt
            if not args:
                self._log("[b][RACE][/b]: Usage: race <prompt>")
                return
            prompt = " ".join(args)
            if len(self._ollama_models) < 2:
                self._log("[b][RACE][/b]: Need 2+ models to race")
                return
            self._log(f"[b][RACE][/b]: Racing {len(self._ollama_models)} models...")
            self.run_race(prompt)
            return

        if cmd == "gpu":
            # Show GPU/VRAM info
            info = get_gpu_memory_info()
            mem = psutil.virtual_memory()
            self._log("[b][GPU][/b]: M2 Ultra Unified Memory")
            self._log(f"  Total: [b]{mem.total/(1024**3):.0f}GB[/b]")
            self._log(f"  Available: [b]{mem.available/(1024**3):.0f}GB[/b]")
            self._log(f"  For AI: ~{mem.available/(1024**3):.0f}GB (unified)")
            if "gpu_name" in info:
                self._log(f"  GPU: {info['gpu_name']}")
            self._log("[b][TIP][/b]: Run 'sudo sysctl iogpu.wired_limit_mb=172032'")
            self._log("  to allocate 168GB for GPU/AI workloads")
            return

        if cmd == "bench":
            # Quick benchmark
            self._log("[b][BENCH][/b]: Running quick benchmark...")
            self.run_benchmark()
            return

        if cmd == "sync":
            # Sync command
            vault_path = os.getenv("VAULT_PATH", "")
            if not vault_path:
                self._log("[b][SYNC][/b]: Set VAULT_PATH in .env")
                self._log("[b][SYNC][/b]: Example: VAULT_PATH=/Volumes/MacProVault")
                return
            self._log(f"[b][SYNC][/b]: Would sync to {vault_path}")
            self._log("[b][SYNC][/b]: Use rsync manually for now:")
            self._log(f"  rsync -avz ~/Projects/ {vault_path}/Backups/")
            return

        if cmd == "archive":
            # Archive processed voice files
            if not VOICE_INBOX_DIR.exists():
                self._log("[b][ARCHIVE][/b]: Voice inbox not found")
                return
            archive_dir = VOICE_INBOX_DIR.parent / "archive"
            archive_dir.mkdir(exist_ok=True)
            files = list(VOICE_INBOX_DIR.glob("*.txt"))
            if not files:
                self._log("[b][ARCHIVE][/b]: No files to archive")
                return
            for f in files:
                dest = archive_dir / f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{f.name}"
                f.rename(dest)
            self._seen_voice_files.clear()
            self._log(f"[b][ARCHIVE][/b]: Archived {len(files)} voice files")
            return

        if cmd == "thermal":
            # Show thermal info
            self._log("[b][THERMAL][/b]: Checking system thermals...")
            try:
                # Try powermetrics (may need sudo)
                result = subprocess.run(
                    ["sudo", "powermetrics", "--samplers", "smc", "-i1", "-n1"],
                    capture_output=True, text=True, timeout=10
                )
                if result.returncode == 0:
                    for line in result.stdout.split('\n'):
                        if 'temperature' in line.lower() or 'fan' in line.lower():
                            self._log(f"  {line.strip()}")
                else:
                    self._log("[b][THERMAL][/b]: Run with sudo for thermal data")
                    self._log("  Or install: brew install osx-cpu-temp")
            except Exception as e:
                self._log(f"[b][THERMAL][/b]: {e}")
            return

        if cmd == "speed":
            # Network speed test
            self._log("[b][SPEED][/b]: Testing network latency...")
            import time
            nodes = [
                ("Ollama", "localhost", 11434),
                ("HP Omen", OMEN_HOST, 22),
                ("Internet", "8.8.8.8", 53),
            ]
            for name, host, port in nodes:
                start = time.perf_counter()
                ok = check_host_reachable(host, port, timeout=2.0)
                latency = (time.perf_counter() - start) * 1000
                if ok:
                    self._log(f"  {name}: [b]{latency:.1f}ms[/b]")
                else:
                    self._log(f"  {name}: [dim]OFFLINE[/dim]")
            return

        if cmd == "guardian":
            # Guardian agent status
            if not AGENTS_AVAILABLE:
                self._log("[b][GUARDIAN][/b]: Agents not available")
                return
            guardian = GuardianAgent()
            self._log("[b][GUARDIAN][/b]: System Health Check")
            health = guardian.get_health()
            self._log(f"  Memory: {health.memory_used_gb:.0f}GB / 192GB")
            self._log(f"  Available: [b]{health.memory_available_gb:.0f}GB[/b]")
            self._log(f"  Pressure: {health.memory_pressure}")
            self._log(f"  CPU: {health.cpu_percent:.1f}%")
            self._log(f"  Processes: {health.process_count}")
            if health.swap_used_gb > 0:
                self._log(f"  [yellow]Swap: {health.swap_used_gb:.1f}GB[/yellow]")
            # Suggestions
            suggestions = guardian.get_optimization_suggestions()
            if suggestions:
                self._log("[b][TIPS][/b]:")
                for s in suggestions[:3]:
                    self._log(f"  - {s}")
            return

        if cmd == "top":
            # Top memory processes
            self._log("[b][TOP][/b]: Memory-hungry processes")
            procs = []
            for proc in psutil.process_iter(['name', 'memory_info']):
                try:
                    mem = proc.info['memory_info']
                    if mem:
                        gb = mem.rss / (1024**3)
                        if gb > 0.1:
                            procs.append((proc.info['name'], gb))
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            procs.sort(key=lambda x: x[1], reverse=True)
            for name, gb in procs[:10]:
                bar = "█" * int(gb * 2)
                self._log(f"  {name[:20]:<20} {gb:>5.1f}GB {bar}")
            return

        if cmd == "optimize":
            # Memory optimization suggestions
            self._log("[b][OPTIMIZE][/b]: Checking for optimizations...")
            mem = psutil.virtual_memory()
            available_gb = mem.available / (1024**3)

            if available_gb > 150:
                self._log("  [b]EXCELLENT[/b]: You have 150GB+ free for AI")
                self._log("  Consider running llama3.1:70b or qwen2.5:72b")
            elif available_gb > 100:
                self._log("  [b]GOOD[/b]: 100GB+ available")
                self._log("  All standard models should run fine")
            elif available_gb > 50:
                self._log("  [yellow]MODERATE[/yellow]: 50-100GB available")
                self._log("  Stick to 7B-13B models for speed")
            else:
                self._log("  [red]LOW[/red]: Less than 50GB available")
                self._log("  Consider closing apps")

            # Check for memory hogs
            procs = []
            for proc in psutil.process_iter(['name', 'memory_info']):
                try:
                    mem_info = proc.info['memory_info']
                    if mem_info and mem_info.rss > 5 * (1024**3):  # > 5GB
                        procs.append((proc.info['name'], mem_info.rss / (1024**3)))
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass

            if procs:
                self._log("[b][MEMORY HOGS][/b]:")
                for name, gb in sorted(procs, key=lambda x: -x[1])[:5]:
                    self._log(f"  {name}: {gb:.1f}GB")
            return

        if cmd == "index":
            # Index files with librarian
            if not AGENTS_AVAILABLE:
                self._log("[b][INDEX][/b]: Agents not available")
                return
            self._log("[b][INDEX][/b]: Indexing files...")
            librarian = LibrarianAgent()
            count = librarian.index_all()
            self._log(f"[b][INDEX][/b]: Indexed {count:,} files")
            stats = librarian.get_stats()
            for ftype, data in stats.get("by_type", {}).items():
                self._log(f"  {ftype}: {data['count']:,} files ({data['size_mb']/1024:.1f}GB)")
            return

        if cmd == "find":
            # Find files
            if not args:
                self._log("[b][FIND][/b]: Usage: find <query>")
                return
            query = " ".join(args)
            if not AGENTS_AVAILABLE:
                # Fallback to basic find
                self._log(f"[b][FIND][/b]: Searching for '{query}'...")
                try:
                    result = subprocess.run(
                        ["find", str(GABRIEL_ROOT), "-name", f"*{query}*", "-type", "f"],
                        capture_output=True, text=True, timeout=30
                    )
                    files = result.stdout.strip().split('\n')[:10]
                    for f in files:
                        if f:
                            self._log(f"  {Path(f).name}")
                except Exception as e:
                    self._log(f"[b][FIND][/b]: Error: {e}")
            else:
                librarian = LibrarianAgent()
                librarian.index_all()
                results = librarian.search(query)
                self._log(f"[b][FIND][/b]: Found {len(results)} files")
                for info in results[:10]:
                    self._log(f"  {info.name} ({info.size_mb:.1f}MB)")
            return

        # MCP tool calls (e.g., vault.list, omen.status)
        if "." in cmd and self.mcp.ready:
            try:
                result = await self.mcp_call(cmd, {})
                self._log(f"[b][MCP][/b]: {cmd} -> {result}")
            except Exception as e:
                self._log(f"[b][MCP][/b]: Error: {e}")
            return

        self._log(f"[b][GABRIEL][/b]: Unknown command: {cmd}. Type 'help'.")

    # -----------------------------
    # Ollama
    # -----------------------------

    @work(exclusive=False)
    async def ask_ollama(self, prompt: str) -> None:
        """Streaming Ollama call via /api/generate."""
        self._log(f"[b][GABRIEL][/b]: [dim]thinking...[/dim]")

        # Use streaming for better UX
        response_parts = []

        def on_chunk(text: str):
            response_parts.append(text)

        try:
            await ollama_generate_stream(prompt, OLLAMA_MODEL, on_chunk)
            full_response = "".join(response_parts).strip()
            if full_response:
                # Clear the "thinking" and show response
                self._log(f"[b][GABRIEL][/b]: {full_response[:500]}")
                if len(full_response) > 500:
                    self._log(f"[dim]... ({len(full_response)} chars total)[/dim]")
            else:
                self._log("[b][GABRIEL][/b]: (no response)")
        except Exception as e:
            self._log(f"[b][GABRIEL][/b]: Ollama error: {e}")

    @work(exclusive=False)
    async def run_race(self, prompt: str) -> None:
        """Race multiple models with the same prompt."""
        models = self._ollama_models[:4]  # Max 4 models
        self._log(f"[b][RACE][/b]: Starting race with {len(models)} models...")

        results = await race_models(prompt, models)

        # Sort by time
        sorted_results = sorted(results.items(), key=lambda x: x[1][1] if x[1][1] > 0 else float('inf'))

        self._log("[b][RACE RESULTS][/b]:")
        for i, (model, (response, time_ms)) in enumerate(sorted_results):
            medal = ["1st", "2nd", "3rd", "4th"][i] if i < 4 else f"{i+1}th"
            model_short = model.split(":")[0]
            self._log(f"  {medal}: [b]{model_short}[/b] - {time_ms:.0f}ms")
            if response and not response.startswith("Error"):
                self._log(f"    [dim]{response[:100]}...[/dim]")

    @work(exclusive=False)
    async def run_benchmark(self) -> None:
        """Quick benchmark of current model."""
        import time

        self._log(f"[b][BENCH][/b]: Testing {OLLAMA_MODEL}...")

        prompts = [
            "What is 2+2?",
            "Write a haiku about code.",
            "Explain Python in one sentence.",
        ]

        total_time = 0
        total_tokens = 0

        for i, prompt in enumerate(prompts):
            start = time.perf_counter()
            try:
                async with httpx.AsyncClient(timeout=30) as client:
                    r = await client.post(
                        f"{OLLAMA_URL.rstrip('/')}/api/generate",
                        json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False}
                    )
                    data = r.json()
                    elapsed = (time.perf_counter() - start) * 1000
                    tokens = data.get("eval_count", 0)
                    total_time += elapsed
                    total_tokens += tokens
                    self._log(f"  Test {i+1}: {elapsed:.0f}ms ({tokens} tokens)")
            except Exception as e:
                self._log(f"  Test {i+1}: Error - {e}")

        if total_time > 0:
            avg_time = total_time / len(prompts)
            tokens_per_sec = (total_tokens / total_time) * 1000 if total_time > 0 else 0
            self._log(f"[b][BENCH][/b]: Avg: {avg_time:.0f}ms | {tokens_per_sec:.1f} tok/s")

    async def on_shutdown_request(self) -> None:
        self._stop.set()


if __name__ == "__main__":
    GabrielHive().run()
