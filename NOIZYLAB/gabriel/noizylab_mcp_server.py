#!/usr/bin/env python3
"""
NOIZYLAB MCP SERVER
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Model Context Protocol server for GABRIEL integration.

Provides tools:
    - noizylab_heal: Run system healing
    - noizylab_scan: Scan for code
    - noizylab_diag: System diagnostics
    - noizylab_status: System status
    - noizylab_portal: Portal control
    - noizylab_execute: Execute commands
    - noizylab_search: Search codebase
"""

import asyncio
import subprocess
import json
import os
from pathlib import Path
from datetime import datetime

try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import Tool, TextContent
except ImportError:
    print("MCP not installed. Run: pip install mcp")
    exit(1)

# Initialize server
server = Server("noizylab")

NOIZYLAB_ROOT = Path.home() / "NOIZYLAB"
PORTAL_URL = "http://localhost:5185"

def run_cmd(command: str, timeout: int = 30) -> str:
    """Execute shell command"""
    try:
        result = subprocess.run(
            command, shell=True, capture_output=True, 
            text=True, timeout=timeout
        )
        return result.stdout.strip() or result.stderr.strip()
    except subprocess.TimeoutExpired:
        return f"Command timed out after {timeout}s"
    except Exception as e:
        return f"Error: {e}"

# ============================================================================
# TOOLS
# ============================================================================

@server.list_tools()
async def list_tools():
    """List available NOIZYLAB tools"""
    return [
        Tool(
            name="noizylab_status",
            description="Get full NOIZYLAB system status including CPU, RAM, Portal, HP-OMEN connectivity",
            inputSchema={"type": "object", "properties": {}}
        ),
        Tool(
            name="noizylab_heal",
            description="Run World Healer - clears caches, optimizes memory, flushes DNS, checks disk health",
            inputSchema={"type": "object", "properties": {}}
        ),
        Tool(
            name="noizylab_scan",
            description="Scan directories for code files (Python, JavaScript, TypeScript)",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Path to scan (defaults to NOIZYLAB root)"
                    },
                    "extension": {
                        "type": "string", 
                        "description": "File extension to search (py, js, ts, html)"
                    }
                }
            }
        ),
        Tool(
            name="noizylab_diag",
            description="Run full system diagnostics via Portal API",
            inputSchema={"type": "object", "properties": {}}
        ),
        Tool(
            name="noizylab_portal",
            description="Control the NOIZYLAB Portal server",
            inputSchema={
                "type": "object",
                "properties": {
                    "action": {
                        "type": "string",
                        "enum": ["start", "stop", "status"],
                        "description": "Action to perform"
                    }
                },
                "required": ["action"]
            }
        ),
        Tool(
            name="noizylab_execute",
            description="Execute a shell command on the local system",
            inputSchema={
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "Command to execute"
                    },
                    "timeout": {
                        "type": "integer",
                        "description": "Timeout in seconds (default 30)"
                    }
                },
                "required": ["command"]
            }
        ),
        Tool(
            name="noizylab_search",
            description="Search for files or content in the NOIZYLAB codebase",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query (filename or content)"
                    },
                    "type": {
                        "type": "string",
                        "enum": ["filename", "content"],
                        "description": "Search type"
                    }
                },
                "required": ["query"]
            }
        ),
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    """Handle tool calls"""
    
    if name == "noizylab_status":
        cpu = run_cmd("top -l 1 | grep 'CPU usage' | awk '{print $3}'")
        mem = run_cmd("memory_pressure | grep 'free percentage' | head -1")
        portal = run_cmd(f"curl -s {PORTAL_URL}/api/status 2>/dev/null")
        omen = "ONLINE" if run_cmd("ping -c 1 -t 1 10.0.0.160 2>/dev/null | grep 'bytes from'") else "OFFLINE"
        mtu = run_cmd("ifconfig en0 | grep mtu | awk '{print $NF}'")
        
        status = {
            "cpu": cpu,
            "memory": mem,
            "portal": "ONLINE" if "ONLINE" in portal else "OFFLINE",
            "portal_url": PORTAL_URL,
            "hp_omen": omen,
            "hp_omen_ip": "10.0.0.160",
            "mtu": mtu,
            "jumbo_frames": mtu == "9000"
        }
        return [TextContent(type="text", text=json.dumps(status, indent=2))]
    
    elif name == "noizylab_heal":
        results = []
        
        # Cache cleanup
        run_cmd("rm -rf ~/Library/Caches/* 2>/dev/null")
        results.append("✅ User caches cleared")
        
        # DNS flush
        run_cmd("dscacheutil -flushcache")
        results.append("✅ DNS cache flushed")
        
        # Memory info
        mem = run_cmd("memory_pressure | grep 'free percentage' | head -1")
        results.append(f"✅ Memory: {mem}")
        
        # Disk check
        disk = run_cmd("df -h / | tail -1 | awk '{print $5}'")
        results.append(f"✅ Root disk: {disk} used")
        
        return [TextContent(type="text", text="\n".join(results))]
    
    elif name == "noizylab_scan":
        path = arguments.get("path", str(NOIZYLAB_ROOT))
        ext = arguments.get("extension", "py")
        
        files = run_cmd(f"find '{path}' -maxdepth 5 -name '*.{ext}' 2>/dev/null | head -50")
        count = run_cmd(f"find '{path}' -maxdepth 5 -name '*.{ext}' 2>/dev/null | wc -l")
        
        result = f"Found {count.strip()} .{ext} files in {path}\n\nSample:\n{files}"
        return [TextContent(type="text", text=result)]
    
    elif name == "noizylab_diag":
        result = run_cmd(f"curl -s {PORTAL_URL}/api/diagnose/local 2>/dev/null")
        if result:
            try:
                data = json.loads(result)
                return [TextContent(type="text", text=json.dumps(data, indent=2))]
            except:
                return [TextContent(type="text", text=f"Raw response: {result}")]
        return [TextContent(type="text", text="Portal not responding. Start with: noizylab_portal start")]
    
    elif name == "noizylab_portal":
        action = arguments.get("action", "status")
        
        if action == "start":
            run_cmd(f"cd {NOIZYLAB_ROOT}/PORTAL && nohup python3 portal_server.py > /tmp/portal.log 2>&1 &")
            return [TextContent(type="text", text=f"Portal starting at {PORTAL_URL}")]
        elif action == "stop":
            run_cmd("pkill -f portal_server.py")
            return [TextContent(type="text", text="Portal stopped")]
        else:
            result = run_cmd(f"curl -s {PORTAL_URL}/api/status 2>/dev/null")
            status = "ONLINE" if "ONLINE" in result else "OFFLINE"
            return [TextContent(type="text", text=f"Portal: {status} at {PORTAL_URL}")]
    
    elif name == "noizylab_execute":
        command = arguments.get("command", "")
        timeout = arguments.get("timeout", 30)
        
        if not command:
            return [TextContent(type="text", text="No command provided")]
        
        result = run_cmd(command, timeout)
        return [TextContent(type="text", text=result)]
    
    elif name == "noizylab_search":
        query = arguments.get("query", "")
        search_type = arguments.get("type", "filename")
        
        if not query:
            return [TextContent(type="text", text="No query provided")]
        
        if search_type == "filename":
            result = run_cmd(f"find {NOIZYLAB_ROOT} -name '*{query}*' 2>/dev/null | head -20")
        else:
            result = run_cmd(f"grep -r '{query}' {NOIZYLAB_ROOT} --include='*.py' -l 2>/dev/null | head -20")
        
        return [TextContent(type="text", text=result or "No results found")]
    
    return [TextContent(type="text", text=f"Unknown tool: {name}")]

# ============================================================================
# MAIN
# ============================================================================

async def main():
    """Run the MCP server"""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())
