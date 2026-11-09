#!/usr/bin/env python3
"""
⚡ TURBO MCP SERVER - GORUNFREE x1000
Maximum speed, parallel execution, zero latency
"""

import os
import sys
import json
import asyncio
import subprocess
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, List
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from collections import defaultdict
import threading

import mcp.types as types
from mcp.server import Server
from mcp.server.stdio import stdio_server

app = Server("turbo")

NOIZYLAB = Path("/Users/m2ultra/NOIZYLAB")
TURBO = NOIZYLAB / "TURBO"
CACHE = TURBO / "cache"
CORES = os.cpu_count() or 8

executor = ThreadPoolExecutor(max_workers=CORES)
process_pool = ProcessPoolExecutor(max_workers=CORES // 2)

CACHE.mkdir(parents=True, exist_ok=True)


def run_fast(cmd: str, cwd: str = None, timeout: int = 60) -> Dict:
    try:
        r = subprocess.run(
            cmd, shell=True, cwd=cwd, 
            capture_output=True, text=True, timeout=timeout
        )
        return {'out': r.stdout[:10000], 'err': r.stderr[:2000], 'code': r.returncode}
    except Exception as e:
        return {'error': str(e)}


def parallel_run(commands: List[str], cwd: str = None) -> List[Dict]:
    def run_one(cmd):
        return run_fast(cmd, cwd)
    
    with ThreadPoolExecutor(max_workers=min(len(commands), CORES)) as pool:
        return list(pool.map(run_one, commands))


def scan_parallel(path: Path, depth: int = 10) -> Dict:
    stats = {'files': 0, 'lines': 0, 'bytes': 0, 'langs': defaultdict(int)}
    skip = {'.git', 'node_modules', 'venv', '__pycache__', '.venv'}
    lang_map = {'.py': 'Python', '.js': 'JavaScript', '.ts': 'TypeScript', '.go': 'Go', '.rs': 'Rust', '.sh': 'Shell'}
    
    def process_file(fp):
        try:
            st = fp.stat()
            ext = fp.suffix.lower()
            lines = 0
            if ext in lang_map:
                lines = len(fp.read_text(errors='ignore').split('\n'))
            return {'size': st.st_size, 'lines': lines, 'lang': lang_map.get(ext)}
        except:
            return None
    
    files = []
    for root, dirs, filenames in os.walk(path):
        dirs[:] = [d for d in dirs if d not in skip]
        if str(root).count(os.sep) - str(path).count(os.sep) > depth:
            continue
        for f in filenames:
            if not f.startswith('.'):
                files.append(Path(root) / f)
    
    with ThreadPoolExecutor(max_workers=CORES) as pool:
        results = list(pool.map(process_file, files[:5000]))
    
    for r in results:
        if r:
            stats['files'] += 1
            stats['bytes'] += r['size']
            stats['lines'] += r['lines']
            if r['lang']:
                stats['langs'][r['lang']] += 1
    
    stats['langs'] = dict(stats['langs'])
    return stats


def grep_parallel(pattern: str, path: Path, limit: int = 100) -> List[Dict]:
    results = []
    skip = {'.git', 'node_modules', 'venv', '__pycache__'}
    exts = {'.py', '.js', '.ts', '.go', '.rs', '.sh', '.md', '.json'}
    p = pattern.lower()
    
    files = []
    for root, dirs, filenames in os.walk(path):
        dirs[:] = [d for d in dirs if d not in skip]
        for f in filenames:
            fp = Path(root) / f
            if fp.suffix.lower() in exts:
                files.append(fp)
    
    def search_file(fp):
        matches = []
        try:
            for i, line in enumerate(fp.read_text(errors='ignore').split('\n'), 1):
                if p in line.lower():
                    matches.append({'file': str(fp), 'line': i, 'text': line.strip()[:100]})
        except:
            pass
        return matches
    
    with ThreadPoolExecutor(max_workers=CORES) as pool:
        for file_matches in pool.map(search_file, files[:1000]):
            results.extend(file_matches)
            if len(results) >= limit:
                break
    
    return results[:limit]


@app.list_tools()
async def list_tools() -> List[types.Tool]:
    return [
        types.Tool(name="turbo_scan", description="⚡ Parallel codebase scan", inputSchema={
            "type": "object", "properties": {"path": {"type": "string"}, "depth": {"type": "integer", "default": 10}}
        }),
        types.Tool(name="turbo_grep", description="⚡ Parallel content search", inputSchema={
            "type": "object", "properties": {"pattern": {"type": "string"}, "path": {"type": "string"}}, "required": ["pattern"]
        }),
        types.Tool(name="turbo_run", description="⚡ Run command fast", inputSchema={
            "type": "object", "properties": {"command": {"type": "string"}, "cwd": {"type": "string"}}, "required": ["command"]
        }),
        types.Tool(name="turbo_parallel", description="⚡ Run multiple commands in parallel", inputSchema={
            "type": "object", "properties": {"commands": {"type": "array", "items": {"type": "string"}}, "cwd": {"type": "string"}}, "required": ["commands"]
        }),
        types.Tool(name="turbo_status", description="⚡ Full system status", inputSchema={"type": "object", "properties": {}}),
        types.Tool(name="turbo_start", description="⚡ Start all services", inputSchema={"type": "object", "properties": {}}),
        types.Tool(name="turbo_stop", description="⚡ Stop all services", inputSchema={"type": "object", "properties": {}}),
        types.Tool(name="turbo_glm", description="⚡ Start GLM-4.7 server", inputSchema={
            "type": "object", "properties": {"port": {"type": "integer", "default": 8080}}
        }),
        types.Tool(name="turbo_manus", description="⚡ Start OpenManus", inputSchema={"type": "object", "properties": {}}),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> List[types.TextContent]:
    def respond(data):
        if isinstance(data, str):
            return [types.TextContent(type="text", text=data)]
        return [types.TextContent(type="text", text=json.dumps(data, indent=2, default=str))]
    
    try:
        if name == "turbo_scan":
            path = Path(arguments.get("path", str(NOIZYLAB)))
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(executor, scan_parallel, path, arguments.get("depth", 10))
            return respond(result)
        
        elif name == "turbo_grep":
            path = Path(arguments.get("path", str(NOIZYLAB)))
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(executor, grep_parallel, arguments["pattern"], path, 100)
            return respond(result)
        
        elif name == "turbo_run":
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(executor, run_fast, arguments["command"], arguments.get("cwd"))
            return respond(result)
        
        elif name == "turbo_parallel":
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(executor, parallel_run, arguments["commands"], arguments.get("cwd"))
            return respond(result)
        
        elif name == "turbo_status":
            checks = [
                "pgrep -f 'dashboard/server.py' > /dev/null && echo 'dashboard:online' || echo 'dashboard:offline'",
                "pgrep -f 'gabriel_agent.py' > /dev/null && echo 'gabriel:online' || echo 'gabriel:offline'",
                "pgrep -f 'llama-server' > /dev/null && echo 'glm:online' || echo 'glm:offline'",
                f"echo 'cores:{CORES}'",
                "sysctl -n hw.memsize | awk '{printf \"ram:%.0fGB\", $1/1024/1024/1024}'",
            ]
            results = parallel_run(checks)
            status = {}
            for r in results:
                if r.get('out'):
                    for line in r['out'].strip().split('\n'):
                        if ':' in line:
                            k, v = line.split(':', 1)
                            status[k] = v
            return respond(status)
        
        elif name == "turbo_start":
            cmds = [
                f"cd {NOIZYLAB}/UNIFIED_MCP && python3 dashboard/server.py > /dev/null 2>&1 &",
                f"cd {NOIZYLAB}/GABRIEL && python3 gabriel_agent.py > /dev/null 2>&1 &",
            ]
            parallel_run(cmds)
            return respond({"status": "started", "services": ["dashboard", "gabriel"]})
        
        elif name == "turbo_stop":
            cmds = [
                "pkill -f 'dashboard/server.py'",
                "pkill -f 'gabriel_agent.py'",
                "pkill -f 'llama-server'",
            ]
            parallel_run(cmds)
            return respond({"status": "stopped"})
        
        elif name == "turbo_glm":
            port = arguments.get("port", 8080)
            glm_path = NOIZYLAB / "LOCAL_LLM" / "GLM-4.7"
            run_fast(f"nohup {glm_path}/server.sh {port} > /dev/null 2>&1 &", str(glm_path))
            return respond({"status": "starting", "port": port})
        
        elif name == "turbo_manus":
            manus_path = NOIZYLAB / "LOCAL_LLM" / "OpenManus"
            run_fast(f"cd {manus_path}/OpenManus && source .venv/bin/activate && python main.py &")
            return respond({"status": "starting"})
        
        else:
            return respond({"error": f"Unknown: {name}"})
    
    except Exception as e:
        return respond({"error": str(e)})


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
