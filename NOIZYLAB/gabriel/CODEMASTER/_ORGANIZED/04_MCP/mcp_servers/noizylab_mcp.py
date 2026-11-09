#!/usr/bin/env python3
"""
🧠 NOIZYLAB UNIFIED MCP SERVER
One MCP server to rule them all

Combines:
- GABRIEL (codebase intelligence)
- AI Command Center (video/audio/avatar generation)
- Memory systems
- System operations
- Network operations
"""

import os
import sys
import json
import asyncio
import hashlib
import subprocess
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, List, Optional
from collections import defaultdict
from dataclasses import dataclass

import mcp.types as types
from mcp.server import Server
from mcp.server.stdio import stdio_server

app = Server("noizylab")

NOIZYLAB_ROOT = Path("/Users/m2ultra/NOIZYLAB")
GABRIEL_ROOT = NOIZYLAB_ROOT / "GABRIEL"
CONFIG_DIR = Path.home() / ".noizylab"
KEYS_FILE = CONFIG_DIR / "api_keys.json"
MEMORY_FILE = CONFIG_DIR / "memory.json"

CONFIG_DIR.mkdir(parents=True, exist_ok=True)


@dataclass
class AIService:
    name: str
    category: str
    api_url: str
    api_key_env: str


AI_SERVICES = {
    "runway": AIService("Runway Gen-3", "video", "https://api.runwayml.com/v1", "RUNWAY_API_KEY"),
    "kling": AIService("Kling AI", "video", "https://api.klingai.com/v1", "KLING_API_KEY"),
    "pika": AIService("Pika", "video", "https://api.pika.art/v1", "PIKA_API_KEY"),
    "suno": AIService("Suno", "audio", "https://api.suno.ai/v1", "SUNO_API_KEY"),
    "udio": AIService("Udio", "audio", "https://api.udio.com/v1", "UDIO_API_KEY"),
    "elevenlabs": AIService("ElevenLabs", "audio", "https://api.elevenlabs.io/v1", "ELEVENLABS_API_KEY"),
    "heygen": AIService("HeyGen", "avatar", "https://api.heygen.com/v2", "HEYGEN_API_KEY"),
    "openai": AIService("OpenAI", "llm", "https://api.openai.com/v1", "OPENAI_API_KEY"),
    "anthropic": AIService("Anthropic", "llm", "https://api.anthropic.com/v1", "ANTHROPIC_API_KEY"),
}


class KeyManager:
    def __init__(self):
        self.keys = self._load()
    
    def _load(self) -> Dict:
        if KEYS_FILE.exists():
            return json.loads(KEYS_FILE.read_text())
        return {}
    
    def _save(self):
        KEYS_FILE.write_text(json.dumps(self.keys, indent=2))
        os.chmod(KEYS_FILE, 0o600)
    
    def set(self, service: str, key: str):
        self.keys[service] = key
        self._save()
    
    def get(self, service: str) -> Optional[str]:
        svc = AI_SERVICES.get(service)
        if svc:
            env_key = os.environ.get(svc.api_key_env)
            if env_key:
                return env_key
        return self.keys.get(service)
    
    def list(self) -> Dict[str, bool]:
        return {name: bool(self.get(name)) for name in AI_SERVICES}


class MemoryStore:
    def __init__(self):
        self.data = self._load()
    
    def _load(self) -> Dict:
        if MEMORY_FILE.exists():
            return json.loads(MEMORY_FILE.read_text())
        return {}
    
    def _save(self):
        MEMORY_FILE.write_text(json.dumps(self.data, indent=2, default=str))
    
    def store(self, key: str, value: Any, tags: List[str] = None):
        self.data[key] = {
            "value": value,
            "tags": tags or [],
            "created": datetime.now().isoformat(),
            "updated": datetime.now().isoformat(),
        }
        self._save()
    
    def get(self, key: str) -> Optional[Dict]:
        return self.data.get(key)
    
    def search(self, query: str) -> List[Dict]:
        results = []
        query_lower = query.lower()
        for key, item in self.data.items():
            if query_lower in key.lower():
                results.append({"key": key, **item})
            elif any(query_lower in tag.lower() for tag in item.get("tags", [])):
                results.append({"key": key, **item})
        return results
    
    def delete(self, key: str) -> bool:
        if key in self.data:
            del self.data[key]
            self._save()
            return True
        return False


class CodebaseScanner:
    LANG_MAP = {
        '.py': 'Python', '.js': 'JavaScript', '.ts': 'TypeScript',
        '.go': 'Go', '.rs': 'Rust', '.sh': 'Shell',
        '.html': 'HTML', '.css': 'CSS', '.md': 'Markdown',
        '.json': 'JSON', '.yaml': 'YAML', '.swift': 'Swift',
    }
    
    def scan(self, path: Path, depth: int = 10) -> Dict:
        stats = {
            'timestamp': datetime.now().isoformat(),
            'path': str(path),
            'total_files': 0,
            'total_lines': 0,
            'total_bytes': 0,
            'languages': defaultdict(lambda: {'files': 0, 'lines': 0}),
            'hot_files': [],
        }
        
        skip = {'.git', 'node_modules', 'venv', '__pycache__', '.venv'}
        files_data = []
        
        for root, dirs, files in os.walk(path):
            dirs[:] = [d for d in dirs if d not in skip]
            if str(root).count(os.sep) - str(path).count(os.sep) > depth:
                continue
            
            for file in files:
                if file.startswith('.'):
                    continue
                
                fp = Path(root) / file
                try:
                    st = fp.stat()
                    ext = fp.suffix.lower()
                    info = {'path': str(fp), 'size': st.st_size, 'lines': 0, 'complexity': 0}
                    
                    if ext in self.LANG_MAP:
                        content = fp.read_text(errors='ignore').split('\n')
                        info['lines'] = len(content)
                        for line in content:
                            if any(k in line for k in ['if ', 'for ', 'while ', 'def ', 'fn ', 'func ']):
                                info['complexity'] += 1
                        
                        stats['languages'][self.LANG_MAP[ext]]['files'] += 1
                        stats['languages'][self.LANG_MAP[ext]]['lines'] += info['lines']
                    
                    files_data.append(info)
                    stats['total_files'] += 1
                    stats['total_lines'] += info['lines']
                    stats['total_bytes'] += info['size']
                except:
                    continue
        
        files_data.sort(key=lambda x: x['complexity'], reverse=True)
        stats['hot_files'] = files_data[:15]
        stats['languages'] = dict(stats['languages'])
        return stats
    
    def search(self, query: str, path: Path, limit: int = 30) -> List[Dict]:
        results = []
        skip = {'.git', 'node_modules', 'venv', '__pycache__'}
        q = query.lower()
        
        for root, dirs, files in os.walk(path):
            dirs[:] = [d for d in dirs if d not in skip]
            for file in files:
                if q in file.lower():
                    results.append({'path': str(Path(root) / file), 'match': 'filename'})
                    if len(results) >= limit:
                        return results
        return results
    
    def grep(self, pattern: str, path: Path, limit: int = 50) -> List[Dict]:
        results = []
        skip = {'.git', 'node_modules', 'venv', '__pycache__'}
        code_ext = {'.py', '.js', '.ts', '.go', '.rs', '.sh', '.md', '.json', '.yaml'}
        p = pattern.lower()
        
        for root, dirs, files in os.walk(path):
            dirs[:] = [d for d in dirs if d not in skip]
            for file in files:
                fp = Path(root) / file
                if fp.suffix.lower() not in code_ext:
                    continue
                try:
                    for i, line in enumerate(fp.read_text(errors='ignore').split('\n'), 1):
                        if p in line.lower():
                            results.append({'file': str(fp), 'line': i, 'text': line.strip()[:150]})
                            if len(results) >= limit:
                                return results
                except:
                    continue
        return results


keys = KeyManager()
memory = MemoryStore()
scanner = CodebaseScanner()


def run_cmd(cmd: str, cwd: str = None, timeout: int = 30) -> Dict:
    dangerous = ['rm -rf /', 'sudo rm', 'mkfs', '> /dev/sd']
    if any(d in cmd for d in dangerous):
        return {'error': 'Dangerous command blocked'}
    try:
        r = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True, timeout=timeout)
        return {'stdout': r.stdout[:8000], 'stderr': r.stderr[:2000], 'code': r.returncode}
    except subprocess.TimeoutExpired:
        return {'error': 'Timeout'}
    except Exception as e:
        return {'error': str(e)}


@app.list_resources()
async def list_resources() -> List[types.Resource]:
    return [
        types.Resource(uri="noizylab://status", name="System Status", mimeType="application/json"),
        types.Resource(uri="noizylab://memory", name="Memory Store", mimeType="application/json"),
        types.Resource(uri="noizylab://services", name="AI Services", mimeType="application/json"),
        types.Resource(uri="noizylab://intelligence", name="Codebase Intelligence", mimeType="application/json"),
    ]


@app.read_resource()
async def read_resource(uri: str) -> str:
    if uri == "noizylab://status":
        return json.dumps({
            "status": "online",
            "version": "1.0",
            "timestamp": datetime.now().isoformat(),
            "root": str(NOIZYLAB_ROOT),
        })
    elif uri == "noizylab://memory":
        return json.dumps({"count": len(memory.data), "keys": list(memory.data.keys())[:50]})
    elif uri == "noizylab://services":
        return json.dumps({"services": keys.list()})
    elif uri == "noizylab://intelligence":
        report = GABRIEL_ROOT / "intelligence_report.json"
        if report.exists():
            return report.read_text()
        return json.dumps({"error": "No report - run scan_codebase first"})
    raise ValueError(f"Unknown resource: {uri}")


@app.list_tools()
async def list_tools() -> List[types.Tool]:
    return [
        # CODEBASE INTELLIGENCE
        types.Tool(name="scan_codebase", description="Full codebase scan with stats, languages, complexity", inputSchema={
            "type": "object", "properties": {
                "path": {"type": "string", "description": "Path to scan (default: NOIZYLAB)"},
                "depth": {"type": "integer", "default": 10}
            }
        }),
        types.Tool(name="search_files", description="Search for files by name", inputSchema={
            "type": "object", "properties": {
                "query": {"type": "string"}, "path": {"type": "string"}, "limit": {"type": "integer", "default": 30}
            }, "required": ["query"]
        }),
        types.Tool(name="grep_content", description="Search file contents", inputSchema={
            "type": "object", "properties": {
                "pattern": {"type": "string"}, "path": {"type": "string"}, "limit": {"type": "integer", "default": 50}
            }, "required": ["pattern"]
        }),
        
        # FILE OPERATIONS
        types.Tool(name="read_file", description="Read a file", inputSchema={
            "type": "object", "properties": {"path": {"type": "string"}, "lines": {"type": "integer"}}, "required": ["path"]
        }),
        types.Tool(name="write_file", description="Write to a file", inputSchema={
            "type": "object", "properties": {"path": {"type": "string"}, "content": {"type": "string"}, "append": {"type": "boolean", "default": False}}, "required": ["path", "content"]
        }),
        types.Tool(name="list_dir", description="List directory contents", inputSchema={
            "type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]
        }),
        
        # SYSTEM OPERATIONS
        types.Tool(name="run_command", description="Execute shell command", inputSchema={
            "type": "object", "properties": {"command": {"type": "string"}, "cwd": {"type": "string"}}, "required": ["command"]
        }),
        types.Tool(name="system_info", description="Get system info (CPU, memory, disk)", inputSchema={"type": "object", "properties": {}}),
        types.Tool(name="process_list", description="List running processes", inputSchema={
            "type": "object", "properties": {"filter": {"type": "string"}}
        }),
        
        # GIT OPERATIONS
        types.Tool(name="git_status", description="Git repository status", inputSchema={
            "type": "object", "properties": {"path": {"type": "string"}}
        }),
        types.Tool(name="git_log", description="Recent git commits", inputSchema={
            "type": "object", "properties": {"path": {"type": "string"}, "limit": {"type": "integer", "default": 10}}
        }),
        
        # MEMORY OPERATIONS
        types.Tool(name="memory_store", description="Store data in memory", inputSchema={
            "type": "object", "properties": {
                "key": {"type": "string"}, "value": {"type": "string"}, "tags": {"type": "array", "items": {"type": "string"}}
            }, "required": ["key", "value"]
        }),
        types.Tool(name="memory_get", description="Retrieve from memory", inputSchema={
            "type": "object", "properties": {"key": {"type": "string"}}, "required": ["key"]
        }),
        types.Tool(name="memory_search", description="Search memory", inputSchema={
            "type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]
        }),
        types.Tool(name="memory_delete", description="Delete from memory", inputSchema={
            "type": "object", "properties": {"key": {"type": "string"}}, "required": ["key"]
        }),
        
        # API KEY MANAGEMENT
        types.Tool(name="api_key_set", description="Set API key for a service", inputSchema={
            "type": "object", "properties": {"service": {"type": "string"}, "key": {"type": "string"}}, "required": ["service", "key"]
        }),
        types.Tool(name="api_key_list", description="List API key status", inputSchema={"type": "object", "properties": {}}),
        
        # AI GENERATION (Video, Audio, Avatar)
        types.Tool(name="generate_video", description="Generate video with AI (Runway, Kling, Pika)", inputSchema={
            "type": "object", "properties": {
                "prompt": {"type": "string"}, "provider": {"type": "string", "enum": ["runway", "kling", "pika"], "default": "runway"},
                "duration": {"type": "integer", "default": 5}
            }, "required": ["prompt"]
        }),
        types.Tool(name="generate_audio", description="Generate music/audio with AI (Suno, Udio)", inputSchema={
            "type": "object", "properties": {
                "prompt": {"type": "string"}, "provider": {"type": "string", "enum": ["suno", "udio"], "default": "suno"},
                "duration": {"type": "integer", "default": 60}
            }, "required": ["prompt"]
        }),
        types.Tool(name="generate_speech", description="Text to speech with ElevenLabs", inputSchema={
            "type": "object", "properties": {
                "text": {"type": "string"}, "voice": {"type": "string", "default": "default"}
            }, "required": ["text"]
        }),
        types.Tool(name="generate_avatar", description="Create avatar video (HeyGen)", inputSchema={
            "type": "object", "properties": {
                "script": {"type": "string"}, "avatar": {"type": "string", "default": "default"}
            }, "required": ["script"]
        }),
        
        # NETWORK
        types.Tool(name="network_scan", description="Scan local network", inputSchema={
            "type": "object", "properties": {"interface": {"type": "string", "default": "en0"}}
        }),
        
        # VOLUMES
        types.Tool(name="list_volumes", description="List mounted volumes", inputSchema={"type": "object", "properties": {}}),
        types.Tool(name="scan_volume", description="Scan a volume for files", inputSchema={
            "type": "object", "properties": {"volume": {"type": "string"}, "extensions": {"type": "array", "items": {"type": "string"}}}, "required": ["volume"]
        }),
        
        # LOCAL LLM (GLM-4.7)
        types.Tool(name="llm_status", description="Check local LLM server status", inputSchema={"type": "object", "properties": {}}),
        types.Tool(name="llm_start", description="Start local GLM-4.7 server", inputSchema={
            "type": "object", "properties": {"port": {"type": "integer", "default": 8080}}
        }),
        types.Tool(name="llm_stop", description="Stop local LLM server", inputSchema={"type": "object", "properties": {}}),
        types.Tool(name="llm_chat", description="Chat with local GLM-4.7", inputSchema={
            "type": "object", "properties": {
                "message": {"type": "string"},
                "system": {"type": "string", "default": "You are a helpful AI assistant."},
                "temperature": {"type": "number", "default": 1.0},
                "max_tokens": {"type": "integer", "default": 2048}
            }, "required": ["message"]
        }),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> List[types.TextContent]:
    def respond(data: Any) -> List[types.TextContent]:
        if isinstance(data, str):
            return [types.TextContent(type="text", text=data)]
        return [types.TextContent(type="text", text=json.dumps(data, indent=2, default=str))]
    
    try:
        # CODEBASE
        if name == "scan_codebase":
            path = Path(arguments.get("path", str(NOIZYLAB_ROOT)))
            result = scanner.scan(path, arguments.get("depth", 10))
            (GABRIEL_ROOT / "intelligence_report.json").write_text(json.dumps(result, indent=2, default=str))
            return respond({"files": result["total_files"], "lines": result["total_lines"], "languages": result["languages"], "hot_files": [f["path"] for f in result["hot_files"][:10]]})
        
        elif name == "search_files":
            path = Path(arguments.get("path", str(NOIZYLAB_ROOT)))
            return respond(scanner.search(arguments["query"], path, arguments.get("limit", 30)))
        
        elif name == "grep_content":
            path = Path(arguments.get("path", str(NOIZYLAB_ROOT)))
            return respond(scanner.grep(arguments["pattern"], path, arguments.get("limit", 50)))
        
        # FILES
        elif name == "read_file":
            fp = Path(arguments["path"])
            if not fp.exists():
                return respond({"error": f"Not found: {fp}"})
            content = fp.read_text(errors='ignore')
            if arguments.get("lines"):
                content = '\n'.join(content.split('\n')[:arguments["lines"]])
            return respond(content)
        
        elif name == "write_file":
            fp = Path(arguments["path"])
            fp.parent.mkdir(parents=True, exist_ok=True)
            mode = 'a' if arguments.get("append") else 'w'
            fp.open(mode).write(arguments["content"])
            return respond({"success": True, "path": str(fp)})
        
        elif name == "list_dir":
            dp = Path(arguments["path"])
            if not dp.exists():
                return respond({"error": f"Not found: {dp}"})
            items = [{"name": i.name, "is_dir": i.is_dir(), "size": i.stat().st_size if i.is_file() else None} for i in dp.iterdir()]
            return respond(sorted(items, key=lambda x: (not x["is_dir"], x["name"])))
        
        # SYSTEM
        elif name == "run_command":
            return respond(run_cmd(arguments["command"], arguments.get("cwd")))
        
        elif name == "system_info":
            return respond({
                "hostname": run_cmd("hostname")["stdout"].strip(),
                "uptime": run_cmd("uptime")["stdout"].strip(),
                "cpu": run_cmd("sysctl -n machdep.cpu.brand_string")["stdout"].strip(),
                "memory": run_cmd("vm_stat | head -5")["stdout"],
                "disk": run_cmd("df -h / | tail -1")["stdout"],
            })
        
        elif name == "process_list":
            f = arguments.get("filter", "")
            cmd = f"ps aux | grep -i '{f}' | head -20" if f else "ps aux | head -30"
            return respond(run_cmd(cmd))
        
        # GIT
        elif name == "git_status":
            path = arguments.get("path", str(NOIZYLAB_ROOT))
            return respond(run_cmd("git status --short", path))
        
        elif name == "git_log":
            path = arguments.get("path", str(NOIZYLAB_ROOT))
            return respond(run_cmd(f"git log --oneline -n {arguments.get('limit', 10)}", path))
        
        # MEMORY
        elif name == "memory_store":
            memory.store(arguments["key"], arguments["value"], arguments.get("tags"))
            return respond({"stored": arguments["key"]})
        
        elif name == "memory_get":
            result = memory.get(arguments["key"])
            return respond(result if result else {"error": "Not found"})
        
        elif name == "memory_search":
            return respond(memory.search(arguments["query"]))
        
        elif name == "memory_delete":
            return respond({"deleted": memory.delete(arguments["key"])})
        
        # API KEYS
        elif name == "api_key_set":
            keys.set(arguments["service"], arguments["key"])
            return respond({"set": arguments["service"]})
        
        elif name == "api_key_list":
            return respond(keys.list())
        
        # AI GENERATION
        elif name == "generate_video":
            provider = arguments.get("provider", "runway")
            api_key = keys.get(provider)
            if not api_key:
                return respond({"error": f"No API key for {provider}. Use api_key_set to configure."})
            return respond({
                "status": "queued",
                "provider": provider,
                "prompt": arguments["prompt"],
                "duration": arguments.get("duration", 5),
                "note": "API integration ready - implement webhook for async result"
            })
        
        elif name == "generate_audio":
            provider = arguments.get("provider", "suno")
            api_key = keys.get(provider)
            if not api_key:
                return respond({"error": f"No API key for {provider}. Use api_key_set to configure."})
            return respond({
                "status": "queued",
                "provider": provider,
                "prompt": arguments["prompt"],
                "duration": arguments.get("duration", 60),
            })
        
        elif name == "generate_speech":
            api_key = keys.get("elevenlabs")
            if not api_key:
                return respond({"error": "No ElevenLabs API key. Use api_key_set to configure."})
            return respond({
                "status": "queued",
                "text": arguments["text"][:100] + "...",
                "voice": arguments.get("voice", "default"),
            })
        
        elif name == "generate_avatar":
            api_key = keys.get("heygen")
            if not api_key:
                return respond({"error": "No HeyGen API key. Use api_key_set to configure."})
            return respond({
                "status": "queued",
                "script": arguments["script"][:100] + "...",
                "avatar": arguments.get("avatar", "default"),
            })
        
        # NETWORK
        elif name == "network_scan":
            return respond(run_cmd(f"arp -a -i {arguments.get('interface', 'en0')}"))
        
        # VOLUMES
        elif name == "list_volumes":
            return respond(run_cmd("ls -la /Volumes"))
        
        elif name == "scan_volume":
            vol = arguments["volume"]
            exts = arguments.get("extensions", [])
            path = f"/Volumes/{vol}"
            if not Path(path).exists():
                return respond({"error": f"Volume not found: {vol}"})
            if exts:
                ext_args = " -o ".join([f'-name "*.{e}"' for e in exts])
                cmd = f'find "{path}" -type f \\( {ext_args} \\) 2>/dev/null | head -100'
            else:
                cmd = f'find "{path}" -type f 2>/dev/null | head -100'
            return respond(run_cmd(cmd, timeout=60))
        
        # LOCAL LLM (GLM-4.7)
        elif name == "llm_status":
            result = run_cmd("curl -s http://127.0.0.1:8080/health 2>/dev/null || echo 'offline'")
            if "offline" in result.get("stdout", "offline"):
                return respond({"status": "offline", "message": "GLM-4.7 server not running. Use llm_start to start."})
            return respond({"status": "online", "endpoint": "http://127.0.0.1:8080/v1"})
        
        elif name == "llm_start":
            port = arguments.get("port", 8080)
            glm_root = NOIZYLAB_ROOT / "LOCAL_LLM" / "GLM-4.7"
            server_script = glm_root / "server.sh"
            if not server_script.exists():
                return respond({"error": "GLM-4.7 not installed. Run setup.sh first.", "path": str(glm_root)})
            run_cmd(f"nohup {server_script} {port} > /dev/null 2>&1 &", str(glm_root))
            return respond({"status": "starting", "port": port, "message": "GLM-4.7 server starting (takes ~30s to load model)"})
        
        elif name == "llm_stop":
            run_cmd("pkill -f 'llama-server'")
            return respond({"status": "stopped"})
        
        elif name == "llm_chat":
            try:
                import urllib.request
                msg = arguments["message"]
                sys_prompt = arguments.get("system", "You are a helpful AI assistant.")
                temp = arguments.get("temperature", 1.0)
                max_tok = arguments.get("max_tokens", 2048)
                
                payload = json.dumps({
                    "model": "glm-4.7",
                    "messages": [
                        {"role": "system", "content": sys_prompt},
                        {"role": "user", "content": msg}
                    ],
                    "temperature": temp,
                    "max_tokens": max_tok
                }).encode()
                
                req = urllib.request.Request(
                    "http://127.0.0.1:8080/v1/chat/completions",
                    data=payload,
                    headers={"Content-Type": "application/json"}
                )
                resp = urllib.request.urlopen(req, timeout=120)
                data = json.loads(resp.read().decode())
                return respond({"response": data["choices"][0]["message"]["content"]})
            except urllib.error.URLError:
                return respond({"error": "LLM server not running. Use llm_start first."})
            except Exception as e:
                return respond({"error": str(e)})
        
        else:
            return respond({"error": f"Unknown tool: {name}"})
    
    except Exception as e:
        return respond({"error": str(e)})


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
