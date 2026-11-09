#!/usr/bin/env python3
"""
GABRIEL MCP v2 — System Tools
================================
System info, shell commands. Extracted from v1 monolith.
"""

import asyncio
import subprocess
from typing import Any


class SystemTools:
    """System interaction tools."""

    # Commands that are never allowed
    _BLOCKED = ["rm -rf /", "mkfs", "dd if=", "> /dev/", ":(){ :|:& };:"]

    async def handle(self, action: str, args: dict[str, Any]) -> Any:
        dispatch = {
            "info": self._info,
            "run": self._run,
        }

        fn = dispatch.get(action)
        if not fn:
            return {"error": f"Unknown system action: {action}", "available": list(dispatch.keys())}
        return await fn(args)

    async def _info(self, args: dict) -> dict:
        info = {}

        # Disk
        try:
            result = subprocess.run(["df", "-h", "/"], capture_output=True, text=True, timeout=5)
            info["disk"] = result.stdout.strip()
        except (subprocess.TimeoutExpired, OSError):
            info["disk"] = "unavailable"

        # Uptime
        try:
            result = subprocess.run(["uptime"], capture_output=True, text=True, timeout=5)
            info["uptime"] = result.stdout.strip()
        except (subprocess.TimeoutExpired, OSError):
            info["uptime"] = "unavailable"

        return info

    async def _run(self, args: dict) -> dict:
        command = args.get("command", "")
        cwd = args.get("cwd")
        timeout = args.get("timeout", 30)

        if any(d in command for d in self._BLOCKED):
            return {"error": "Command blocked for safety"}

        try:
            proc = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=cwd,
            )
            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=timeout)

            output = stdout.decode()
            if stderr:
                output += f"\n[stderr]\n{stderr.decode()}"

            return {"command": command, "output": output or "(no output)", "exit_code": proc.returncode}
        except asyncio.TimeoutError:
            return {"error": f"Command timed out after {timeout}s"}
        except Exception as e:
            return {"error": str(e)}
