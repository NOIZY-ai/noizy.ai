#!/usr/bin/env python3
"""
🧠 GABRIEL MCP SERVER v2.0
Complete Model Context Protocol server for GABRIEL

Exposes all GABRIEL capabilities as MCP tools:
- Codebase intelligence
- File operations
- Agent management
- System monitoring
- Network operations
"""

import os
import sys
import json
import asyncio
import hashlib
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, List, Optional
from collections import defaultdict

import mcp.types as types
from mcp.server import Server
from mcp.server.stdio import stdio_server

# Import NOIZY Collective
try:
    from noizy_collective import get_knowledge, NOIZYCollective, Qwen3Client
    COLLECTIVE_AVAILABLE = True
except ImportError:
    COLLECTIVE_AVAILABLE = False

app = Server("gabriel")

GABRIEL_ROOT = Path("/Users/m2ultra/NOIZYLAB/GABRIEL")
NOIZYLAB_ROOT = Path("/Users/m2ultra/NOIZYLAB")
INDEX_FILE = GABRIEL_ROOT / "gabriel_index.json"
BRAIN_FILE = GABRIEL_ROOT / "memcell_data" / "brain.json"
INTELLIGENCE_REPORT = GABRIEL_ROOT / "intelligence_report.json"


class GabrielCore:
    """Core GABRIEL functionality"""
    
    def __init__(self):
        self.file_hashes = {}
        self.stats = {}
        self.lang_map = {
            '.py': 'Python', '.js': 'JavaScript', '.ts': 'TypeScript',
            '.go': 'Go', '.rs': 'Rust', '.sh': 'Shell',
            '.html': 'HTML', '.css': 'CSS', '.md': 'Markdown',
            '.json': 'JSON', '.yaml': 'YAML', '.toml': 'TOML',
        }
    
    def scan_codebase(self, path: Path, depth: int = 10) -> Dict:
        """Full codebase intelligence scan"""
        stats = {
            'timestamp': datetime.now().isoformat(),
            'path': str(path),
            'total_files': 0,
            'total_lines': 0,
            'total_bytes': 0,
            'languages': defaultdict(lambda: {'files': 0, 'lines': 0, 'bytes': 0}),
            'files': [],
            'hot_files': [],
        }
        
        skip_dirs = {'.git', 'node_modules', 'venv', '__pycache__', '.venv', 'dist', 'build'}
        
        for root, dirs, files in os.walk(path):
            dirs[:] = [d for d in dirs if d not in skip_dirs]
            
            current_depth = str(root).count(os.sep) - str(path).count(os.sep)
            if current_depth > depth:
                continue
            
            for file in files:
                if file.startswith('.'):
                    continue
                
                filepath = Path(root) / file
                try:
                    stat = filepath.stat()
                    ext = filepath.suffix.lower()
                    
                    file_info = {
                        'path': str(filepath),
                        'name': file,
                        'ext': ext,
                        'size': stat.st_size,
                        'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                        'lines': 0,
                        'complexity': 0,
                    }
                    
                    if ext in self.lang_map:
                        try:
                            content = filepath.read_text(errors='ignore')
                            lines = content.split('\n')
                            file_info['lines'] = len(lines)
                            
                            for line in lines:
                                if any(kw in line for kw in ['if ', 'for ', 'while ', 'match ']):
                                    file_info['complexity'] += 1
                                if any(kw in line for kw in ['def ', 'fn ', 'func ', 'class ', 'struct ']):
                                    file_info['complexity'] += 2
                        except:
                            pass
                        
                        lang = self.lang_map[ext]
                        stats['languages'][lang]['files'] += 1
                        stats['languages'][lang]['lines'] += file_info['lines']
                        stats['languages'][lang]['bytes'] += file_info['size']
                    
                    stats['files'].append(file_info)
                    stats['total_files'] += 1
                    stats['total_lines'] += file_info['lines']
                    stats['total_bytes'] += file_info['size']
                    
                except Exception:
                    continue
        
        stats['files'].sort(key=lambda x: x['complexity'], reverse=True)
        stats['hot_files'] = stats['files'][:20]
        stats['languages'] = dict(stats['languages'])
        
        return stats
    
    def search_files(self, query: str, path: Path, limit: int = 20) -> List[Dict]:
        """Search files by name or content"""
        results = []
        query_lower = query.lower()
        
        skip_dirs = {'.git', 'node_modules', 'venv', '__pycache__'}
        
        for root, dirs, files in os.walk(path):
            dirs[:] = [d for d in dirs if d not in skip_dirs]
            
            for file in files:
                if query_lower in file.lower():
                    filepath = Path(root) / file
                    results.append({
                        'path': str(filepath),
                        'name': file,
                        'match_type': 'filename',
                    })
                    if len(results) >= limit:
                        return results
        
        return results
    
    def grep_content(self, pattern: str, path: Path, limit: int = 50) -> List[Dict]:
        """Search file contents"""
        results = []
        pattern_lower = pattern.lower()
        
        skip_dirs = {'.git', 'node_modules', 'venv', '__pycache__'}
        code_exts = {'.py', '.js', '.ts', '.go', '.rs', '.sh', '.md', '.json', '.yaml'}
        
        for root, dirs, files in os.walk(path):
            dirs[:] = [d for d in dirs if d not in skip_dirs]
            
            for file in files:
                filepath = Path(root) / file
                if filepath.suffix.lower() not in code_exts:
                    continue
                
                try:
                    content = filepath.read_text(errors='ignore')
                    lines = content.split('\n')
                    
                    for i, line in enumerate(lines, 1):
                        if pattern_lower in line.lower():
                            results.append({
                                'file': str(filepath),
                                'line_num': i,
                                'line': line.strip()[:200],
                            })
                            if len(results) >= limit:
                                return results
                except:
                    continue
        
        return results
    
    def get_file_info(self, filepath: str) -> Dict:
        """Get detailed file information"""
        path = Path(filepath)
        if not path.exists():
            return {'error': f'File not found: {filepath}'}
        
        stat = path.stat()
        info = {
            'path': str(path),
            'name': path.name,
            'ext': path.suffix,
            'size': stat.st_size,
            'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
            'is_file': path.is_file(),
            'is_dir': path.is_dir(),
        }
        
        if path.is_file() and path.suffix in self.lang_map:
            try:
                content = path.read_text(errors='ignore')
                info['lines'] = len(content.split('\n'))
                info['language'] = self.lang_map[path.suffix]
            except:
                pass
        
        return info
    
    def run_command(self, cmd: str, cwd: str = None) -> Dict:
        """Execute shell command safely"""
        dangerous = ['rm -rf', 'sudo', 'mkfs', 'dd if=', '> /dev']
        if any(d in cmd for d in dangerous):
            return {'error': 'Dangerous command blocked', 'cmd': cmd}
        
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                cwd=cwd or str(GABRIEL_ROOT),
                capture_output=True,
                text=True,
                timeout=30
            )
            return {
                'stdout': result.stdout[:10000],
                'stderr': result.stderr[:2000],
                'returncode': result.returncode,
            }
        except subprocess.TimeoutExpired:
            return {'error': 'Command timed out', 'cmd': cmd}
        except Exception as e:
            return {'error': str(e), 'cmd': cmd}


gabriel = GabrielCore()


@app.list_resources()
async def list_resources() -> List[types.Resource]:
    """List available GABRIEL resources"""
    return [
        types.Resource(
            uri="gabriel://index",
            name="Codebase Index",
            description="Full index of NOIZYLAB codebase",
            mimeType="application/json",
        ),
        types.Resource(
            uri="gabriel://brain",
            name="GABRIEL Brain",
            description="Knowledge graph and memory",
            mimeType="application/json",
        ),
        types.Resource(
            uri="gabriel://intelligence",
            name="Intelligence Report",
            description="Latest codebase analysis",
            mimeType="application/json",
        ),
        types.Resource(
            uri="gabriel://status",
            name="System Status",
            description="GABRIEL system status",
            mimeType="application/json",
        ),
    ]


@app.read_resource()
async def read_resource(uri: str) -> str:
    """Read a GABRIEL resource"""
    if uri == "gabriel://index":
        if INDEX_FILE.exists():
            return INDEX_FILE.read_text()
        return json.dumps({"error": "Index not built"})
    
    elif uri == "gabriel://brain":
        if BRAIN_FILE.exists():
            return BRAIN_FILE.read_text()
        return json.dumps({"nodes": [], "edges": []})
    
    elif uri == "gabriel://intelligence":
        if INTELLIGENCE_REPORT.exists():
            return INTELLIGENCE_REPORT.read_text()
        return json.dumps({"error": "No report available"})
    
    elif uri == "gabriel://status":
        return json.dumps({
            "status": "online",
            "timestamp": datetime.now().isoformat(),
            "version": "2.0",
            "root": str(GABRIEL_ROOT),
        })
    
    raise ValueError(f"Unknown resource: {uri}")


@app.list_tools()
async def list_tools() -> List[types.Tool]:
    """List all GABRIEL tools"""
    return [
        types.Tool(
            name="scan_codebase",
            description="Perform full codebase intelligence scan. Returns file stats, language breakdown, complexity analysis.",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Path to scan (default: NOIZYLAB)"},
                    "depth": {"type": "integer", "description": "Max directory depth", "default": 10},
                },
            }
        ),
        types.Tool(
            name="search_files",
            description="Search for files by name pattern",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"},
                    "path": {"type": "string", "description": "Path to search"},
                    "limit": {"type": "integer", "default": 20},
                },
                "required": ["query"]
            }
        ),
        types.Tool(
            name="grep_content",
            description="Search file contents (like grep)",
            inputSchema={
                "type": "object",
                "properties": {
                    "pattern": {"type": "string", "description": "Pattern to search"},
                    "path": {"type": "string", "description": "Path to search"},
                    "limit": {"type": "integer", "default": 50},
                },
                "required": ["pattern"]
            }
        ),
        types.Tool(
            name="read_file",
            description="Read contents of a file",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "File path"},
                    "lines": {"type": "integer", "description": "Max lines to read"},
                },
                "required": ["path"]
            }
        ),
        types.Tool(
            name="write_file",
            description="Write content to a file",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "File path"},
                    "content": {"type": "string", "description": "Content to write"},
                    "append": {"type": "boolean", "default": False},
                },
                "required": ["path", "content"]
            }
        ),
        types.Tool(
            name="file_info",
            description="Get detailed information about a file",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "File path"},
                },
                "required": ["path"]
            }
        ),
        types.Tool(
            name="list_directory",
            description="List contents of a directory",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Directory path"},
                    "recursive": {"type": "boolean", "default": False},
                },
                "required": ["path"]
            }
        ),
        types.Tool(
            name="run_command",
            description="Execute a shell command (safe commands only)",
            inputSchema={
                "type": "object",
                "properties": {
                    "command": {"type": "string", "description": "Command to run"},
                    "cwd": {"type": "string", "description": "Working directory"},
                },
                "required": ["command"]
            }
        ),
        types.Tool(
            name="git_status",
            description="Get git status for a repository",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Repository path"},
                },
            }
        ),
        types.Tool(
            name="git_log",
            description="Get recent git commits",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Repository path"},
                    "limit": {"type": "integer", "default": 10},
                },
            }
        ),
        types.Tool(
            name="process_list",
            description="List running processes",
            inputSchema={
                "type": "object",
                "properties": {
                    "filter": {"type": "string", "description": "Filter pattern"},
                },
            }
        ),
        types.Tool(
            name="system_info",
            description="Get system information (CPU, memory, disk)",
            inputSchema={"type": "object", "properties": {}}
        ),
        types.Tool(
            name="network_scan",
            description="Scan local network for devices",
            inputSchema={
                "type": "object",
                "properties": {
                    "interface": {"type": "string", "description": "Network interface"},
                },
            }
        ),
        types.Tool(
            name="memory_store",
            description="Store data in GABRIEL's memory",
            inputSchema={
                "type": "object",
                "properties": {
                    "key": {"type": "string", "description": "Memory key"},
                    "value": {"type": "string", "description": "Value to store"},
                },
                "required": ["key", "value"]
            }
        ),
        types.Tool(
            name="memory_retrieve",
            description="Retrieve data from GABRIEL's memory",
            inputSchema={
                "type": "object",
                "properties": {
                    "key": {"type": "string", "description": "Memory key"},
                },
                "required": ["key"]
            }
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> List[types.TextContent]:
    """Execute a GABRIEL tool"""
    
    def respond(data: Any) -> List[types.TextContent]:
        if isinstance(data, str):
            return [types.TextContent(type="text", text=data)]
        return [types.TextContent(type="text", text=json.dumps(data, indent=2, default=str))]
    
    try:
        if name == "scan_codebase":
            path = Path(arguments.get("path", str(NOIZYLAB_ROOT)))
            depth = arguments.get("depth", 10)
            result = gabriel.scan_codebase(path, depth)
            
            INTELLIGENCE_REPORT.write_text(json.dumps(result, indent=2, default=str))
            
            summary = {
                "total_files": result["total_files"],
                "total_lines": result["total_lines"],
                "total_bytes": result["total_bytes"],
                "languages": result["languages"],
                "hot_files": [f["path"] for f in result["hot_files"][:10]],
            }
            return respond(summary)
        
        elif name == "search_files":
            query = arguments["query"]
            path = Path(arguments.get("path", str(NOIZYLAB_ROOT)))
            limit = arguments.get("limit", 20)
            return respond(gabriel.search_files(query, path, limit))
        
        elif name == "grep_content":
            pattern = arguments["pattern"]
            path = Path(arguments.get("path", str(NOIZYLAB_ROOT)))
            limit = arguments.get("limit", 50)
            return respond(gabriel.grep_content(pattern, path, limit))
        
        elif name == "read_file":
            filepath = Path(arguments["path"])
            if not filepath.exists():
                return respond({"error": f"File not found: {filepath}"})
            
            content = filepath.read_text(errors='ignore')
            max_lines = arguments.get("lines")
            if max_lines:
                content = '\n'.join(content.split('\n')[:max_lines])
            return respond(content)
        
        elif name == "write_file":
            filepath = Path(arguments["path"])
            content = arguments["content"]
            mode = 'a' if arguments.get("append") else 'w'
            
            filepath.parent.mkdir(parents=True, exist_ok=True)
            with open(filepath, mode) as f:
                f.write(content)
            
            return respond({"success": True, "path": str(filepath)})
        
        elif name == "file_info":
            return respond(gabriel.get_file_info(arguments["path"]))
        
        elif name == "list_directory":
            dirpath = Path(arguments["path"])
            if not dirpath.exists():
                return respond({"error": f"Directory not found: {dirpath}"})
            
            items = []
            for item in dirpath.iterdir():
                items.append({
                    "name": item.name,
                    "is_dir": item.is_dir(),
                    "size": item.stat().st_size if item.is_file() else None,
                })
            return respond(sorted(items, key=lambda x: (not x["is_dir"], x["name"])))
        
        elif name == "run_command":
            return respond(gabriel.run_command(
                arguments["command"],
                arguments.get("cwd")
            ))
        
        elif name == "git_status":
            path = arguments.get("path", str(NOIZYLAB_ROOT))
            return respond(gabriel.run_command("git status --short", path))
        
        elif name == "git_log":
            path = arguments.get("path", str(NOIZYLAB_ROOT))
            limit = arguments.get("limit", 10)
            return respond(gabriel.run_command(
                f"git log --oneline -n {limit}",
                path
            ))
        
        elif name == "process_list":
            pattern = arguments.get("filter", "")
            cmd = f"ps aux | head -50"
            if pattern:
                cmd = f"ps aux | grep -i '{pattern}' | head -20"
            return respond(gabriel.run_command(cmd))
        
        elif name == "system_info":
            info = {
                "hostname": gabriel.run_command("hostname")["stdout"].strip(),
                "uptime": gabriel.run_command("uptime")["stdout"].strip(),
                "memory": gabriel.run_command("vm_stat | head -10")["stdout"],
                "disk": gabriel.run_command("df -h / | tail -1")["stdout"],
                "cpu": gabriel.run_command("sysctl -n machdep.cpu.brand_string")["stdout"].strip(),
            }
            return respond(info)
        
        elif name == "network_scan":
            interface = arguments.get("interface", "en0")
            result = gabriel.run_command(f"arp -a -i {interface}")
            return respond(result)
        
        elif name == "memory_store":
            key = arguments["key"]
            value = arguments["value"]
            
            memory_file = GABRIEL_ROOT / "memcell_data" / "memory.json"
            memory_file.parent.mkdir(parents=True, exist_ok=True)
            
            memory = {}
            if memory_file.exists():
                memory = json.loads(memory_file.read_text())
            
            memory[key] = {
                "value": value,
                "timestamp": datetime.now().isoformat(),
            }
            memory_file.write_text(json.dumps(memory, indent=2))
            
            return respond({"stored": key})
        
        elif name == "memory_retrieve":
            key = arguments["key"]
            
            memory_file = GABRIEL_ROOT / "memcell_data" / "memory.json"
            if not memory_file.exists():
                return respond({"error": "Memory empty"})
            
            memory = json.loads(memory_file.read_text())
            if key in memory:
                return respond(memory[key])
            return respond({"error": f"Key not found: {key}"})
        
        else:
            return respond({"error": f"Unknown tool: {name}"})
    
    except Exception as e:
        return respond({"error": str(e)})


async def main():
    """Run the GABRIEL MCP server"""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
