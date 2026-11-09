#!/usr/bin/env python3
"""
VAULT MCP SERVER
================
Provides access to GABRIEL's code vault and file system.
"""

import asyncio
import json
import os
import sys
from pathlib import Path
from datetime import datetime

try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    import mcp.types as types
except ImportError:
    print("Installing MCP SDK...", file=sys.stderr)
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "mcp"])
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    import mcp.types as types

# Configuration
GABRIEL_ROOT = Path(os.getenv("GABRIEL_ROOT", Path.home() / "NOIZYLAB" / "GABRIEL"))
VAULT_PATHS = [
    GABRIEL_ROOT,
    Path.home() / "NOIZYLAB",
    Path.home() / "Documents",
]

app = Server("vault")


def log(msg: str):
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {msg}", file=sys.stderr)


@app.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="vault.list",
            description="List files in a vault directory",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Directory path to list"},
                    "pattern": {"type": "string", "description": "Glob pattern (e.g., *.py)"}
                }
            }
        ),
        types.Tool(
            name="vault.search",
            description="Search for files by name",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"},
                    "max_results": {"type": "integer", "description": "Maximum results", "default": 20}
                },
                "required": ["query"]
            }
        ),
        types.Tool(
            name="vault.read",
            description="Read a file's contents",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "File path to read"}
                },
                "required": ["path"]
            }
        ),
        types.Tool(
            name="vault.stats",
            description="Get vault statistics",
            inputSchema={"type": "object", "properties": {}}
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    log(f"Tool call: {name} with {arguments}")

    if name == "vault.list":
        path = Path(arguments.get("path", str(GABRIEL_ROOT)))
        pattern = arguments.get("pattern", "*")

        if not path.exists():
            return [types.TextContent(type="text", text=f"Path not found: {path}")]

        files = list(path.glob(pattern))[:50]
        result = "\n".join([f"  {f.name}" for f in files])
        return [types.TextContent(type="text", text=f"Files in {path}:\n{result}")]

    elif name == "vault.search":
        query = arguments.get("query", "")
        max_results = arguments.get("max_results", 20)

        results = []
        for vault in VAULT_PATHS:
            if vault.exists():
                for f in vault.rglob(f"*{query}*"):
                    if len(results) >= max_results:
                        break
                    results.append(str(f))

        return [types.TextContent(type="text", text=f"Found {len(results)} files:\n" + "\n".join(results))]

    elif name == "vault.read":
        path = Path(arguments.get("path", ""))
        if not path.exists():
            return [types.TextContent(type="text", text=f"File not found: {path}")]

        try:
            content = path.read_text()[:5000]
            return [types.TextContent(type="text", text=content)]
        except Exception as e:
            return [types.TextContent(type="text", text=f"Error reading file: {e}")]

    elif name == "vault.stats":
        stats = {}
        for vault in VAULT_PATHS:
            if vault.exists():
                py_files = len(list(vault.rglob("*.py")))
                js_files = len(list(vault.rglob("*.js")))
                stats[str(vault)] = {"python": py_files, "javascript": js_files}

        return [types.TextContent(type="text", text=json.dumps(stats, indent=2))]

    return [types.TextContent(type="text", text=f"Unknown tool: {name}")]


async def main():
    log("Vault MCP Server starting...")
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
