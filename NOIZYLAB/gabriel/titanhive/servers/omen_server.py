#!/usr/bin/env python3
"""
OMEN MCP SERVER
================
Remote control and monitoring for HP Omen 25L via SSH/Tailscale.
"""

import asyncio
import json
import os
import sys
import subprocess
from datetime import datetime
from pathlib import Path

try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    import mcp.types as types
except ImportError:
    print("Installing MCP SDK...", file=sys.stderr)
    subprocess.check_call([sys.executable, "-m", "pip", "install", "mcp"])
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    import mcp.types as types

# Configuration
OMEN_HOST = os.getenv("OMEN_HOST", "10.0.0.160")  # HP Omen IP or Tailscale IP
OMEN_USER = os.getenv("OMEN_USER", "admin")
TAILSCALE_ENABLED = os.getenv("TAILSCALE_ENABLED", "false").lower() == "true"

app = Server("omen")


def log(msg: str):
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {msg}", file=sys.stderr)


def run_ssh_command(command: str) -> tuple[str, str, int]:
    """Execute command on Omen via SSH."""
    ssh_cmd = ["ssh", f"{OMEN_USER}@{OMEN_HOST}", command]
    try:
        result = subprocess.run(ssh_cmd, capture_output=True, text=True, timeout=30)
        return result.stdout, result.stderr, result.returncode
    except subprocess.TimeoutExpired:
        return "", "Command timed out", 1
    except Exception as e:
        return "", str(e), 1


def ping_host(host: str) -> bool:
    """Check if host is reachable."""
    try:
        result = subprocess.run(
            ["ping", "-c", "1", "-W", "2", host],
            capture_output=True, timeout=5
        )
        return result.returncode == 0
    except:
        return False


@app.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="omen.status",
            description="Check if HP Omen is online and get basic status",
            inputSchema={"type": "object", "properties": {}}
        ),
        types.Tool(
            name="omen.gpu",
            description="Get GPU temperature and stats from Omen",
            inputSchema={"type": "object", "properties": {}}
        ),
        types.Tool(
            name="omen.game_mode",
            description="Set Omen to high performance gaming mode",
            inputSchema={"type": "object", "properties": {}}
        ),
        types.Tool(
            name="omen.run",
            description="Execute a command on Omen via SSH",
            inputSchema={
                "type": "object",
                "properties": {
                    "command": {"type": "string", "description": "Command to execute"}
                },
                "required": ["command"]
            }
        ),
        types.Tool(
            name="omen.wake",
            description="Wake up Omen via Wake-on-LAN",
            inputSchema={
                "type": "object",
                "properties": {
                    "mac": {"type": "string", "description": "MAC address (optional)"}
                }
            }
        ),
        types.Tool(
            name="net.ping",
            description="Ping a host to check connectivity",
            inputSchema={
                "type": "object",
                "properties": {
                    "host": {"type": "string", "description": "Host to ping"}
                },
                "required": ["host"]
            }
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    log(f"Tool call: {name} with {arguments}")

    if name == "omen.status":
        online = ping_host(OMEN_HOST)
        if online:
            stdout, stderr, code = run_ssh_command("hostname && uptime")
            if code == 0:
                return [types.TextContent(type="text", text=f"OMEN ONLINE:\n{stdout}")]
            return [types.TextContent(type="text", text=f"OMEN reachable but SSH failed: {stderr}")]
        return [types.TextContent(type="text", text=f"OMEN OFFLINE (no response from {OMEN_HOST})")]

    elif name == "omen.gpu":
        # Try nvidia-smi on Windows
        stdout, stderr, code = run_ssh_command("nvidia-smi --query-gpu=temperature.gpu,utilization.gpu,memory.used --format=csv,noheader")
        if code == 0:
            return [types.TextContent(type="text", text=f"GPU Stats:\n{stdout}")]
        return [types.TextContent(type="text", text=f"Could not get GPU stats: {stderr}")]

    elif name == "omen.game_mode":
        # Set Windows to high performance power plan
        stdout, stderr, code = run_ssh_command("powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c")
        if code == 0:
            return [types.TextContent(type="text", text="OMEN set to High Performance mode")]
        return [types.TextContent(type="text", text=f"Failed to set game mode: {stderr}")]

    elif name == "omen.run":
        command = arguments.get("command", "")
        if not command:
            return [types.TextContent(type="text", text="No command specified")]

        # Safety check for dangerous commands
        dangerous = ["rm ", "del ", "format", "shutdown", "restart"]
        if any(d in command.lower() for d in dangerous):
            return [types.TextContent(type="text", text="Command blocked for safety")]

        stdout, stderr, code = run_ssh_command(command)
        if code == 0:
            return [types.TextContent(type="text", text=stdout or "Command executed successfully")]
        return [types.TextContent(type="text", text=f"Error: {stderr}")]

    elif name == "omen.wake":
        mac = arguments.get("mac", "")
        if mac:
            # Use wakeonlan command if available
            try:
                subprocess.run(["wakeonlan", mac], capture_output=True, timeout=5)
                return [types.TextContent(type="text", text=f"Wake-on-LAN sent to {mac}")]
            except:
                return [types.TextContent(type="text", text="wakeonlan command not found. Install with: brew install wakeonlan")]
        return [types.TextContent(type="text", text="No MAC address provided for Wake-on-LAN")]

    elif name == "net.ping":
        host = arguments.get("host", "")
        if not host:
            return [types.TextContent(type="text", text="No host specified")]

        online = ping_host(host)
        return [types.TextContent(type="text", text=f"{host}: {'ONLINE' if online else 'OFFLINE'}")]

    return [types.TextContent(type="text", text=f"Unknown tool: {name}")]


async def main():
    log("Omen MCP Server starting...")
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
