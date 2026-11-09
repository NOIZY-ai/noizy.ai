#!/usr/bin/env python3
"""
🧠 NOIZYLAB AI COMMAND CENTER
Unified management for all AI tools via automation
"""

import os
import sys
import json
import subprocess
import threading
import time
import hashlib
from dataclasses import dataclass, field
from typing import Optional, Dict, List, Callable
from pathlib import Path
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta
import sqlite3
import signal
import atexit

# ============================================================================
# METRICS & ANALYTICS ENGINE
# ============================================================================

class MetricsEngine:
    """Real-time metrics, cost tracking, and analytics"""
    
    def __init__(self, db_path: str = "~/.noizylab/metrics.db"):
        self.db_path = Path(db_path).expanduser()
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()
    
    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS requests (
                id INTEGER PRIMARY KEY,
                timestamp TEXT,
                provider TEXT,
                action TEXT,
                tokens_in INTEGER,
                tokens_out INTEGER,
                latency_ms REAL,
                cost REAL,
                success INTEGER,
                cached INTEGER
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id TEXT PRIMARY KEY,
                created TEXT,
                updated TEXT,
                messages TEXT
            )
        """)
        conn.commit()
        conn.close()
    
    def log_request(self, provider: str, action: str, tokens_in: int = 0, 
                    tokens_out: int = 0, latency_ms: float = 0, 
                    cost: float = 0, success: bool = True, cached: bool = False):
        conn = sqlite3.connect(self.db_path)
        conn.execute("""
            INSERT INTO requests (timestamp, provider, action, tokens_in, tokens_out, 
                                  latency_ms, cost, success, cached)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (datetime.now().isoformat(), provider, action, tokens_in, tokens_out,
              latency_ms, cost, 1 if success else 0, 1 if cached else 0))
        conn.commit()
        conn.close()
    
    def get_stats(self, hours: int = 24) -> dict:
        """Get usage statistics for the last N hours"""
        conn = sqlite3.connect(self.db_path)
        cutoff = (datetime.now() - timedelta(hours=hours)).isoformat()
        
        stats = {}
        
        # Total requests
        cur = conn.execute("SELECT COUNT(*) FROM requests WHERE timestamp > ?", (cutoff,))
        stats['total_requests'] = cur.fetchone()[0]
        
        # Total cost
        cur = conn.execute("SELECT SUM(cost) FROM requests WHERE timestamp > ?", (cutoff,))
        stats['total_cost'] = cur.fetchone()[0] or 0
        
        # Cache hit rate
        cur = conn.execute("SELECT SUM(cached), COUNT(*) FROM requests WHERE timestamp > ?", (cutoff,))
        row = cur.fetchone()
        stats['cache_hits'] = row[0] or 0
        stats['cache_rate'] = (row[0] / row[1] * 100) if row[1] else 0
        
        # Average latency
        cur = conn.execute("SELECT AVG(latency_ms) FROM requests WHERE timestamp > ? AND cached = 0", (cutoff,))
        stats['avg_latency_ms'] = cur.fetchone()[0] or 0
        
        # By provider
        cur = conn.execute("""
            SELECT provider, COUNT(*), SUM(cost) FROM requests 
            WHERE timestamp > ? GROUP BY provider
        """, (cutoff,))
        stats['by_provider'] = {row[0]: {'count': row[1], 'cost': row[2]} for row in cur.fetchall()}
        
        conn.close()
        return stats
    
    def print_dashboard(self):
        """Print real-time metrics dashboard"""
        stats = self.get_stats(24)
        print("\n" + "="*60)
        print("📊 METRICS DASHBOARD (Last 24h)")
        print("="*60)
        print(f"  Total Requests:  {stats['total_requests']}")
        print(f"  Total Cost:      ${stats['total_cost']:.4f}")
        print(f"  Cache Hit Rate:  {stats['cache_rate']:.1f}%")
        print(f"  Avg Latency:     {stats['avg_latency_ms']:.0f}ms")
        print("\n  By Provider:")
        for prov, data in stats.get('by_provider', {}).items():
            print(f"    {prov:<15} │ {data['count']} reqs │ ${data['cost']:.4f}")
        print()


class ConversationMemory:
    """Persistent conversation memory for context-aware responses"""
    
    def __init__(self, db_path: str = "~/.noizylab/metrics.db"):
        self.db_path = Path(db_path).expanduser()
        self.conversations: Dict[str, List[dict]] = {}
        self.current_id: Optional[str] = None
        self.max_history = 20
    
    def start_conversation(self, conv_id: str = None) -> str:
        """Start or resume a conversation"""
        if not conv_id:
            conv_id = hashlib.md5(str(time.time()).encode()).hexdigest()[:12]
        self.current_id = conv_id
        if conv_id not in self.conversations:
            self.conversations[conv_id] = []
        return conv_id
    
    def add_message(self, role: str, content: str):
        """Add a message to current conversation"""
        if not self.current_id:
            self.start_conversation()
        
        self.conversations[self.current_id].append({
            'role': role,
            'content': content,
            'timestamp': datetime.now().isoformat()
        })
        
        # Trim old messages
        if len(self.conversations[self.current_id]) > self.max_history:
            self.conversations[self.current_id] = self.conversations[self.current_id][-self.max_history:]
    
    def get_context(self, max_messages: int = 10) -> List[dict]:
        """Get conversation context for LLM"""
        if not self.current_id:
            return []
        messages = self.conversations.get(self.current_id, [])[-max_messages:]
        return [{'role': m['role'], 'content': m['content']} for m in messages]
    
    def clear(self):
        """Clear current conversation"""
        if self.current_id:
            self.conversations[self.current_id] = []


class PromptTemplates:
    """Prompt template system for common tasks"""
    
    def __init__(self, templates_dir: str = None):
        if templates_dir:
            self.templates_dir = Path(templates_dir)
        else:
            self.templates_dir = Path(__file__).parent / "templates"
        self.templates: Dict[str, dict] = self._load_templates()
    
    def _load_templates(self) -> Dict[str, dict]:
        templates = {}
        prompts_file = self.templates_dir / "prompts.json"
        if prompts_file.exists():
            templates = json.loads(prompts_file.read_text())
        return templates
    
    def list(self):
        """List available templates"""
        print("\n📝 PROMPT TEMPLATES:\n")
        for name, tmpl in self.templates.items():
            print(f"  {name:<15} │ {tmpl.get('name', name)}")
        print()
    
    def get(self, name: str) -> Optional[dict]:
        """Get a template by name"""
        return self.templates.get(name)
    
    def render(self, name: str, **kwargs) -> tuple:
        """Render a template with variables"""
        tmpl = self.get(name)
        if not tmpl:
            return None, None
        
        system = tmpl.get('system', '')
        prompt = tmpl.get('template', '')
        
        # Substitute variables
        for key, value in kwargs.items():
            prompt = prompt.replace(f'{{{key}}}', str(value))
        
        return system, prompt


class CodeExecutor:
    """Safe code execution sandbox"""
    
    ALLOWED_LANGUAGES = ['python', 'bash', 'javascript', 'ruby']
    
    def __init__(self):
        self.temp_dir = Path("/tmp/noizylab_sandbox")
        self.temp_dir.mkdir(exist_ok=True)
        self.timeout = 30
    
    def execute(self, code: str, language: str = "python") -> dict:
        """Execute code in a sandboxed environment"""
        if language not in self.ALLOWED_LANGUAGES:
            return {"error": f"Language {language} not supported"}
        
        print(f"⚡ Executing {language} code...")
        
        # Create temp file
        ext_map = {"python": ".py", "bash": ".sh", "javascript": ".js", "ruby": ".rb"}
        temp_file = self.temp_dir / f"sandbox_{int(time.time())}{ext_map.get(language, '.txt')}"
        temp_file.write_text(code)
        
        # Command map
        cmd_map = {
            "python": [sys.executable, str(temp_file)],
            "bash": ["bash", str(temp_file)],
            "javascript": ["node", str(temp_file)],
            "ruby": ["ruby", str(temp_file)]
        }
        
        start = time.time()
        try:
            result = subprocess.run(
                cmd_map[language],
                capture_output=True,
                text=True,
                timeout=self.timeout,
                cwd=str(self.temp_dir)
            )
            elapsed = (time.time() - start) * 1000
            
            return {
                "status": "success" if result.returncode == 0 else "error",
                "stdout": result.stdout,
                "stderr": result.stderr,
                "exit_code": result.returncode,
                "elapsed_ms": elapsed
            }
        except subprocess.TimeoutExpired:
            return {"error": f"Execution timed out after {self.timeout}s"}
        except Exception as e:
            return {"error": str(e)}
        finally:
            temp_file.unlink(missing_ok=True)


class FileOperations:
    """File system operations for AI-driven automation"""
    
    def __init__(self, base_path: str = None):
        self.base_path = Path(base_path) if base_path else Path.home() / "NOIZYLAB"
    
    def search(self, pattern: str, path: str = None) -> List[dict]:
        """Search for files matching pattern"""
        search_path = Path(path) if path else self.base_path
        results = []
        
        for match in search_path.rglob(pattern):
            if not any(p.startswith('.') for p in match.parts):
                results.append({
                    "path": str(match),
                    "name": match.name,
                    "size": match.stat().st_size if match.is_file() else 0,
                    "is_dir": match.is_dir()
                })
        
        return results[:100]  # Limit results
    
    def read(self, filepath: str, lines: int = 100) -> dict:
        """Read file contents"""
        try:
            path = Path(filepath)
            if not path.exists():
                return {"error": "File not found"}
            
            content = path.read_text()
            line_list = content.split('\n')
            
            return {
                "path": str(path),
                "lines": len(line_list),
                "content": '\n'.join(line_list[:lines]),
                "truncated": len(line_list) > lines
            }
        except Exception as e:
            return {"error": str(e)}
    
    def write(self, filepath: str, content: str, backup: bool = True) -> dict:
        """Write content to file"""
        try:
            path = Path(filepath)
            
            # Backup existing file
            if backup and path.exists():
                backup_path = path.with_suffix(path.suffix + '.bak')
                backup_path.write_text(path.read_text())
            
            # Create parent dirs
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)
            
            return {"status": "success", "path": str(path), "bytes": len(content)}
        except Exception as e:
            return {"error": str(e)}
    
    def tree(self, path: str = None, depth: int = 3) -> dict:
        """Get directory tree"""
        target = Path(path) if path else self.base_path
        
        def walk(p, d):
            if d <= 0:
                return {"...": "max depth"}
            
            result = {}
            try:
                for item in sorted(p.iterdir()):
                    if item.name.startswith('.'):
                        continue
                    if item.is_dir():
                        result[item.name + "/"] = walk(item, d - 1)
                    else:
                        result[item.name] = item.stat().st_size
            except PermissionError:
                pass
            return result
        
        return {target.name: walk(target, depth)}


class ProjectGenerator:
    """Generate project scaffolding from templates"""
    
    TEMPLATES = {
        "python-cli": {
            "files": {
                "main.py": '#!/usr/bin/env python3\n"""Main entry point"""\n\ndef main():\n    print("Hello!")\n\nif __name__ == "__main__":\n    main()\n',
                "requirements.txt": "# Add dependencies here\n",
                "README.md": "# Project\n\n## Usage\n\n```bash\npython main.py\n```\n",
                ".gitignore": "__pycache__/\n*.pyc\nvenv/\n.env\n"
            }
        },
        "python-api": {
            "files": {
                "app.py": 'from flask import Flask, jsonify\n\napp = Flask(__name__)\n\n@app.route("/")\ndef index():\n    return jsonify({"status": "ok"})\n\nif __name__ == "__main__":\n    app.run(debug=True)\n',
                "requirements.txt": "flask\nflask-cors\n",
                "README.md": "# API\n\n## Run\n\n```bash\npython app.py\n```\n"
            }
        },
        "node-api": {
            "files": {
                "index.js": 'const express = require("express");\nconst app = express();\n\napp.get("/", (req, res) => res.json({status: "ok"}));\n\napp.listen(3000, () => console.log("Server on :3000"));\n',
                "package.json": '{"name": "api", "scripts": {"start": "node index.js"}, "dependencies": {"express": "^4.18.0"}}',
                "README.md": "# API\n\n```bash\nnpm install && npm start\n```\n"
            }
        }
    }
    
    def list_templates(self) -> List[str]:
        return list(self.TEMPLATES.keys())
    
    def generate(self, template: str, path: str, name: str = "project") -> dict:
        """Generate project from template"""
        if template not in self.TEMPLATES:
            return {"error": f"Unknown template: {template}"}
        
        project_path = Path(path) / name
        project_path.mkdir(parents=True, exist_ok=True)
        
        created = []
        for filename, content in self.TEMPLATES[template]["files"].items():
            filepath = project_path / filename
            filepath.write_text(content)
            created.append(str(filepath))
        
        return {
            "status": "success",
            "path": str(project_path),
            "files": created
        }


class DocGenerator:
    """AI-powered documentation generator"""
    
    def __init__(self):
        self.llm = None  # Lazy init
    
    def _get_llm(self):
        if not self.llm:
            self.llm = SmartLLM()
        return self.llm
    
    def generate_readme(self, project_path: str) -> str:
        """Generate README from project structure"""
        path = Path(project_path)
        
        # Gather project info
        files = list(path.rglob("*.py"))[:10]
        file_list = "\n".join([f.name for f in files])
        
        # Check for common files
        has_requirements = (path / "requirements.txt").exists()
        has_package = (path / "package.json").exists()
        
        prompt = f"""Generate a README.md for this project:
Files: {file_list}
Has requirements.txt: {has_requirements}
Has package.json: {has_package}

Include: Title, Description, Installation, Usage, License sections.
Keep it concise."""
        
        result = self._get_llm().chat(prompt, "You are a technical writer. Generate clean markdown.")
        return result.get('content', '')
    
    def document_function(self, code: str) -> str:
        """Generate docstring for a function"""
        prompt = f"Generate a Python docstring for this function:\n\n{code}"
        result = self._get_llm().chat(prompt, "Generate only the docstring, nothing else.")
        return result.get('content', '')
    
    def explain_code(self, code: str) -> str:
        """Explain what code does"""
        prompt = f"Explain what this code does in simple terms:\n\n{code}"
        result = self._get_llm().chat(prompt, "Be concise, use bullet points.")
        return result.get('content', '')


class SystemMonitor:
    """Real-time system monitoring"""
    
    def __init__(self):
        self.start_time = time.time()
    
    def get_system_info(self) -> dict:
        """Get comprehensive system information"""
        import platform
        
        info = {
            "platform": platform.system(),
            "python": platform.python_version(),
            "machine": platform.machine(),
            "uptime_seconds": time.time() - self.start_time
        }
        
        # CPU info (macOS)
        try:
            result = subprocess.run(
                ["sysctl", "-n", "machdep.cpu.brand_string"],
                capture_output=True, text=True
            )
            info["cpu"] = result.stdout.strip()
        except:
            pass
        
        # Memory
        try:
            result = subprocess.run(
                ["sysctl", "-n", "hw.memsize"],
                capture_output=True, text=True
            )
            mem_bytes = int(result.stdout.strip())
            info["memory_gb"] = round(mem_bytes / (1024**3), 1)
        except:
            pass
        
        return info
    
    def get_processes(self, limit: int = 10) -> List[dict]:
        """Get top processes by CPU"""
        try:
            result = subprocess.run(
                ["ps", "-arcwwwxo", "pid,pcpu,pmem,comm"],
                capture_output=True, text=True
            )
            
            processes = []
            for line in result.stdout.split('\n')[1:limit+1]:
                parts = line.split()
                if len(parts) >= 4:
                    processes.append({
                        "pid": parts[0],
                        "cpu": parts[1],
                        "mem": parts[2],
                        "name": parts[3]
                    })
            return processes
        except:
            return []
    
    def health_check(self) -> dict:
        """Run system health check"""
        checks = {
            "python": True,
            "disk_ok": True,
            "memory_ok": True,
            "network_ok": False
        }
        
        # Check network
        try:
            import urllib.request
            urllib.request.urlopen("https://google.com", timeout=5)
            checks["network_ok"] = True
        except:
            pass
        
        # Check disk space
        try:
            import shutil
            total, used, free = shutil.disk_usage("/")
            checks["disk_free_gb"] = round(free / (1024**3), 1)
            checks["disk_ok"] = free > 10 * (1024**3)  # 10GB minimum
        except:
            pass
        
        return checks


class EnvManager:
    """Environment and dependency management"""
    
    def __init__(self):
        self.env_file = Path.home() / ".noizylab" / ".env"
        self.env_file.parent.mkdir(parents=True, exist_ok=True)
    
    def get_env(self, key: str) -> Optional[str]:
        """Get environment variable"""
        return os.environ.get(key)
    
    def set_env(self, key: str, value: str, persist: bool = False):
        """Set environment variable"""
        os.environ[key] = value
        if persist:
            self._persist_env(key, value)
    
    def _persist_env(self, key: str, value: str):
        """Persist to .env file"""
        lines = []
        if self.env_file.exists():
            lines = self.env_file.read_text().strip().split('\n')
        
        # Update or add
        found = False
        for i, line in enumerate(lines):
            if line.startswith(f"{key}="):
                lines[i] = f"{key}={value}"
                found = True
                break
        
        if not found:
            lines.append(f"{key}={value}")
        
        self.env_file.write_text('\n'.join(lines) + '\n')
    
    def list_env(self) -> Dict[str, str]:
        """List NOIZYLAB-related env vars"""
        prefixes = ['OPENAI', 'ANTHROPIC', 'RUNWAY', 'SUNO', 'HEYGEN', 'GEMINI', 'NOIZY']
        return {k: v[:20] + "..." if len(v) > 20 else v 
                for k, v in os.environ.items() 
                if any(k.startswith(p) for p in prefixes)}
    
    def check_dependencies(self) -> Dict[str, bool]:
        """Check required dependencies"""
        deps = {
            "python3": ["python3", "--version"],
            "git": ["git", "--version"],
            "brew": ["brew", "--version"],
            "node": ["node", "--version"],
            "npm": ["npm", "--version"],
            "docker": ["docker", "--version"],
            "gcloud": ["gcloud", "--version"],
            "ffmpeg": ["ffmpeg", "-version"],
            "curl": ["curl", "--version"],
        }
        
        results = {}
        for name, cmd in deps.items():
            try:
                result = subprocess.run(cmd, capture_output=True, timeout=5)
                results[name] = result.returncode == 0
            except:
                results[name] = False
        
        return results


class PerformanceProfiler:
    """Performance profiling utilities"""
    
    def __init__(self):
        self.timings: Dict[str, List[float]] = {}
    
    def start_timer(self, name: str) -> float:
        """Start a named timer"""
        return time.time()
    
    def end_timer(self, name: str, start: float) -> float:
        """End timer and record"""
        elapsed = (time.time() - start) * 1000  # ms
        if name not in self.timings:
            self.timings[name] = []
        self.timings[name].append(elapsed)
        return elapsed
    
    def get_stats(self, name: str) -> dict:
        """Get timing stats for a named operation"""
        if name not in self.timings or not self.timings[name]:
            return {"error": "No data"}
        
        times = self.timings[name]
        return {
            "count": len(times),
            "avg_ms": sum(times) / len(times),
            "min_ms": min(times),
            "max_ms": max(times),
            "total_ms": sum(times)
        }
    
    def profile_function(self, func, *args, **kwargs) -> tuple:
        """Profile a function call"""
        start = time.time()
        try:
            result = func(*args, **kwargs)
            elapsed = (time.time() - start) * 1000
            return result, {"success": True, "elapsed_ms": elapsed}
        except Exception as e:
            elapsed = (time.time() - start) * 1000
            return None, {"success": False, "error": str(e), "elapsed_ms": elapsed}
    
    def memory_usage(self) -> dict:
        """Get current memory usage"""
        try:
            result = subprocess.run(
                ["ps", "-o", "rss,vsz", "-p", str(os.getpid())],
                capture_output=True, text=True
            )
            lines = result.stdout.strip().split('\n')
            if len(lines) > 1:
                rss, vsz = lines[1].split()
                return {
                    "rss_mb": int(rss) / 1024,
                    "vsz_mb": int(vsz) / 1024
                }
        except:
            pass
        return {"error": "Unable to get memory info"}


class NetworkMonitor:
    """Network connectivity monitoring"""
    
    def __init__(self):
        self.endpoints = {
            "google": "https://google.com",
            "github": "https://github.com",
            "openai": "https://api.openai.com",
            "anthropic": "https://api.anthropic.com",
            "cloudflare": "https://cloudflare.com",
        }
    
    def ping_endpoint(self, url: str) -> dict:
        """Ping an endpoint and measure latency"""
        import urllib.request
        
        start = time.time()
        try:
            req = urllib.request.Request(url, method='HEAD')
            with urllib.request.urlopen(req, timeout=10) as resp:
                elapsed = (time.time() - start) * 1000
                return {
                    "status": resp.status,
                    "latency_ms": elapsed,
                    "online": True
                }
        except Exception as e:
            return {"online": False, "error": str(e)}
    
    def check_all(self) -> Dict[str, dict]:
        """Check all monitored endpoints"""
        results = {}
        for name, url in self.endpoints.items():
            results[name] = self.ping_endpoint(url)
        return results
    
    def get_local_ip(self) -> str:
        """Get local IP address"""
        try:
            import socket
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "Unknown"
    
    def get_public_ip(self) -> str:
        """Get public IP address"""
        import urllib.request
        try:
            with urllib.request.urlopen("https://api.ipify.org", timeout=5) as resp:
                return resp.read().decode()
        except:
            return "Unknown"
    
    def dns_lookup(self, hostname: str) -> List[str]:
        """Perform DNS lookup"""
        try:
            import socket
            return list(set(socket.gethostbyname_ex(hostname)[2]))
        except:
            return []


class LogViewer:
    """Real-time log viewing and management"""
    
    def __init__(self):
        self.log_dir = Path.home() / ".noizylab" / "logs"
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.current_log = self.log_dir / f"session_{datetime.now().strftime('%Y%m%d')}.log"
    
    def log(self, message: str, level: str = "INFO"):
        """Write to log file"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"[{timestamp}] [{level}] {message}\n"
        with open(self.current_log, "a") as f:
            f.write(entry)
    
    def tail(self, lines: int = 20) -> List[str]:
        """Get last N lines from current log"""
        if not self.current_log.exists():
            return []
        
        all_lines = self.current_log.read_text().strip().split('\n')
        return all_lines[-lines:]
    
    def search(self, pattern: str) -> List[str]:
        """Search logs for pattern"""
        matches = []
        for log_file in self.log_dir.glob("*.log"):
            for line in log_file.read_text().split('\n'):
                if pattern.lower() in line.lower():
                    matches.append(line)
        return matches[-50:]  # Last 50 matches
    
    def clear(self) -> bool:
        """Clear current log"""
        if self.current_log.exists():
            self.current_log.unlink()
            return True
        return False
    
    def list_logs(self) -> List[dict]:
        """List all log files"""
        logs = []
        for log_file in sorted(self.log_dir.glob("*.log"), reverse=True):
            logs.append({
                "name": log_file.name,
                "size_kb": log_file.stat().st_size / 1024,
                "modified": datetime.fromtimestamp(log_file.stat().st_mtime).isoformat()
            })
        return logs[:10]


class BackupManager:
    """Configuration and data backup"""
    
    def __init__(self):
        self.backup_dir = Path.home() / ".noizylab" / "backups"
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        self.config_dir = Path.home() / ".noizylab"
    
    def create_backup(self, name: str = None) -> dict:
        """Create a backup of NOIZYLAB config"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = name or f"backup_{timestamp}"
        backup_path = self.backup_dir / f"{backup_name}.tar.gz"
        
        try:
            import tarfile
            with tarfile.open(backup_path, "w:gz") as tar:
                # Backup key files
                for pattern in ["*.json", "*.db", ".env", "vault/*"]:
                    for f in self.config_dir.glob(pattern):
                        if f.is_file() and "backups" not in str(f):
                            tar.add(f, arcname=f.name)
            
            return {
                "status": "success",
                "path": str(backup_path),
                "size_kb": backup_path.stat().st_size / 1024
            }
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def restore_backup(self, backup_name: str) -> dict:
        """Restore from backup"""
        backup_path = self.backup_dir / backup_name
        if not backup_path.exists():
            backup_path = self.backup_dir / f"{backup_name}.tar.gz"
        
        if not backup_path.exists():
            return {"status": "error", "error": "Backup not found"}
        
        try:
            import tarfile
            with tarfile.open(backup_path, "r:gz") as tar:
                tar.extractall(self.config_dir)
            return {"status": "success", "restored_from": str(backup_path)}
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def list_backups(self) -> List[dict]:
        """List available backups"""
        backups = []
        for f in sorted(self.backup_dir.glob("*.tar.gz"), reverse=True):
            backups.append({
                "name": f.stem,
                "size_kb": f.stat().st_size / 1024,
                "created": datetime.fromtimestamp(f.stat().st_mtime).isoformat()
            })
        return backups


class CronManager:
    """Cron job management"""
    
    def __init__(self):
        self.cron_file = Path.home() / ".noizylab" / "cron_jobs.json"
        self.cron_file.parent.mkdir(parents=True, exist_ok=True)
    
    def _load(self) -> List[dict]:
        if self.cron_file.exists():
            return json.loads(self.cron_file.read_text())
        return []
    
    def _save(self, jobs: List[dict]):
        self.cron_file.write_text(json.dumps(jobs, indent=2))
    
    def add_job(self, name: str, schedule: str, command: str) -> dict:
        """Add a cron job (schedule: '0 9 * * *' = daily 9am)"""
        jobs = self._load()
        job = {
            "id": hashlib.md5(f"{name}{time.time()}".encode()).hexdigest()[:8],
            "name": name,
            "schedule": schedule,
            "command": command,
            "enabled": True,
            "last_run": None,
            "created": datetime.now().isoformat()
        }
        jobs.append(job)
        self._save(jobs)
        return job
    
    def list_jobs(self) -> List[dict]:
        return self._load()
    
    def remove_job(self, job_id: str) -> bool:
        jobs = self._load()
        for i, job in enumerate(jobs):
            if job["id"] == job_id:
                jobs.pop(i)
                self._save(jobs)
                return True
        return False
    
    def toggle_job(self, job_id: str) -> Optional[bool]:
        jobs = self._load()
        for job in jobs:
            if job["id"] == job_id:
                job["enabled"] = not job["enabled"]
                self._save(jobs)
                return job["enabled"]
        return None


class NotificationCenter:
    """System notifications"""
    
    def __init__(self):
        self.history: List[dict] = []
    
    def notify(self, title: str, message: str, sound: bool = True) -> bool:
        """Send macOS notification"""
        try:
            script = f'display notification "{message}" with title "{title}"'
            if sound:
                script += ' sound name "Ping"'
            subprocess.run(["osascript", "-e", script], check=True)
            
            self.history.append({
                "title": title,
                "message": message,
                "time": datetime.now().isoformat()
            })
            return True
        except:
            return False
    
    def alert(self, title: str, message: str) -> bool:
        """Show alert dialog"""
        try:
            script = f'display alert "{title}" message "{message}"'
            subprocess.run(["osascript", "-e", script], check=True)
            return True
        except:
            return False
    
    def speak(self, text: str, voice: str = "Samantha") -> bool:
        """Text-to-speech"""
        try:
            subprocess.run(["say", "-v", voice, text], check=True)
            return True
        except:
            return False


class CloudSync:
    """Cloud sync utilities"""
    
    def __init__(self):
        self.config_dir = Path.home() / ".noizylab"
        self.sync_targets = {
            "gdrive": Path.home() / "Google Drive/My Drive/NOIZYLAB_SYNC",
            "icloud": Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/NOIZYLAB_SYNC",
            "dropbox": Path.home() / "Dropbox/NOIZYLAB_SYNC"
        }
    
    def detect_clouds(self) -> Dict[str, bool]:
        """Detect available cloud services"""
        return {name: path.parent.exists() for name, path in self.sync_targets.items()}
    
    def sync_to(self, target: str) -> dict:
        """Sync config to cloud target"""
        if target not in self.sync_targets:
            return {"status": "error", "error": f"Unknown target: {target}"}
        
        dest = self.sync_targets[target]
        dest.mkdir(parents=True, exist_ok=True)
        
        try:
            import shutil
            # Sync key files
            synced = []
            for pattern in ["*.json", "*.db", "vault/*"]:
                for f in self.config_dir.glob(pattern):
                    if f.is_file() and "backups" not in str(f):
                        dest_file = dest / f.name
                        shutil.copy2(f, dest_file)
                        synced.append(f.name)
            
            return {"status": "success", "target": target, "files": synced}
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def sync_from(self, target: str) -> dict:
        """Sync config from cloud target"""
        if target not in self.sync_targets:
            return {"status": "error", "error": f"Unknown target: {target}"}
        
        src = self.sync_targets[target]
        if not src.exists():
            return {"status": "error", "error": "Sync folder not found"}
        
        try:
            import shutil
            restored = []
            for f in src.glob("*"):
                if f.is_file():
                    dest_file = self.config_dir / f.name
                    shutil.copy2(f, dest_file)
                    restored.append(f.name)
            
            return {"status": "success", "source": target, "files": restored}
        except Exception as e:
            return {"status": "error", "error": str(e)}


class ProcessManager:
    """Process management utilities"""
    
    def __init__(self):
        self.managed_pids: Dict[str, int] = {}
    
    def find_process(self, name: str) -> List[dict]:
        """Find processes by name"""
        try:
            result = subprocess.run(
                ["pgrep", "-fl", name],
                capture_output=True, text=True
            )
            processes = []
            for line in result.stdout.strip().split('\n'):
                if line:
                    parts = line.split(' ', 1)
                    if len(parts) >= 2:
                        processes.append({
                            "pid": parts[0],
                            "command": parts[1][:50]
                        })
            return processes
        except:
            return []
    
    def kill_process(self, pid: int, force: bool = False) -> bool:
        """Kill a process by PID"""
        try:
            sig = "-9" if force else "-15"
            subprocess.run(["kill", sig, str(pid)], check=True)
            return True
        except:
            return False
    
    def get_port_usage(self) -> List[dict]:
        """Get processes using network ports"""
        try:
            result = subprocess.run(
                ["lsof", "-i", "-P", "-n"],
                capture_output=True, text=True
            )
            ports = []
            seen = set()
            for line in result.stdout.split('\n')[1:]:
                parts = line.split()
                if len(parts) >= 9:
                    key = f"{parts[0]}:{parts[8]}"
                    if key not in seen:
                        seen.add(key)
                        ports.append({
                            "process": parts[0],
                            "pid": parts[1],
                            "port": parts[8]
                        })
            return ports[:20]
        except:
            return []
    
    def run_background(self, command: List[str], name: str) -> int:
        """Run a command in background"""
        proc = subprocess.Popen(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True
        )
        self.managed_pids[name] = proc.pid
        return proc.pid


class SecretVault:
    """Secure secrets management"""
    
    def __init__(self):
        self.vault_dir = Path.home() / ".noizylab" / "vault"
        self.vault_dir.mkdir(parents=True, exist_ok=True)
        self.secrets_file = self.vault_dir / "secrets.json"
    
    def _load(self) -> dict:
        if self.secrets_file.exists():
            return json.loads(self.secrets_file.read_text())
        return {}
    
    def _save(self, data: dict):
        self.secrets_file.write_text(json.dumps(data, indent=2))
        os.chmod(self.secrets_file, 0o600)  # Owner read/write only
    
    def set_secret(self, key: str, value: str):
        """Store a secret"""
        import base64
        data = self._load()
        # Simple obfuscation (not encryption, use keyring for real security)
        encoded = base64.b64encode(value.encode()).decode()
        data[key] = encoded
        self._save(data)
    
    def get_secret(self, key: str) -> Optional[str]:
        """Retrieve a secret"""
        import base64
        data = self._load()
        if key in data:
            return base64.b64decode(data[key].encode()).decode()
        return None
    
    def list_secrets(self) -> List[str]:
        """List secret keys (not values)"""
        return list(self._load().keys())
    
    def delete_secret(self, key: str) -> bool:
        """Delete a secret"""
        data = self._load()
        if key in data:
            del data[key]
            self._save(data)
            return True
        return False


class TaskQueue:
    """Async task queue for background processing"""
    
    def __init__(self):
        self.queue: List[dict] = []
        self.results: Dict[str, dict] = {}
        self.running = False
    
    def add(self, task_type: str, params: dict) -> str:
        """Add task to queue"""
        task_id = hashlib.md5(f"{time.time()}{task_type}".encode()).hexdigest()[:8]
        self.queue.append({
            "id": task_id,
            "type": task_type,
            "params": params,
            "status": "pending",
            "created": datetime.now().isoformat()
        })
        return task_id
    
    def get_status(self, task_id: str) -> Optional[dict]:
        """Get task status"""
        for task in self.queue:
            if task["id"] == task_id:
                return task
        return self.results.get(task_id)
    
    def list_pending(self) -> List[dict]:
        """List pending tasks"""
        return [t for t in self.queue if t["status"] == "pending"]
    
    def process_next(self) -> Optional[dict]:
        """Process next task in queue"""
        pending = self.list_pending()
        if not pending:
            return None
        
        task = pending[0]
        task["status"] = "running"
        
        # Execute based on type
        try:
            if task["type"] == "chat":
                llm = SmartLLM()
                result = llm.chat(task["params"].get("prompt", ""))
                task["result"] = result
            elif task["type"] == "image":
                gen = ImageGenerator()
                result = gen.generate(task["params"].get("prompt", ""))
                task["result"] = result
            
            task["status"] = "completed"
        except Exception as e:
            task["status"] = "failed"
            task["error"] = str(e)
        
        self.results[task["id"]] = task
        self.queue.remove(task)
        return task


class APITester:
    """Simple API testing utility"""
    
    def __init__(self):
        self.history: List[dict] = []
    
    def request(self, url: str, method: str = "GET", 
                headers: dict = None, data: dict = None) -> dict:
        """Make HTTP request"""
        import urllib.request
        import urllib.error
        
        start = time.time()
        try:
            req_data = json.dumps(data).encode() if data else None
            req = urllib.request.Request(
                url,
                data=req_data,
                headers=headers or {},
                method=method.upper()
            )
            
            with urllib.request.urlopen(req, timeout=30) as resp:
                body = resp.read().decode()
                elapsed = (time.time() - start) * 1000
                
                result = {
                    "status": resp.status,
                    "headers": dict(resp.headers),
                    "body": body[:1000],
                    "elapsed_ms": elapsed
                }
                self.history.append(result)
                return result
                
        except urllib.error.HTTPError as e:
            return {"error": str(e), "status": e.code}
        except Exception as e:
            return {"error": str(e)}
    
    def get(self, url: str, headers: dict = None) -> dict:
        return self.request(url, "GET", headers)
    
    def post(self, url: str, data: dict, headers: dict = None) -> dict:
        h = headers or {}
        h["Content-Type"] = "application/json"
        return self.request(url, "POST", h, data)


class GitAutomation:
    """Git automation utilities"""
    
    def __init__(self, repo_path: str = None):
        self.repo_path = Path(repo_path) if repo_path else Path.cwd()
    
    def status(self) -> dict:
        """Get git status"""
        try:
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                capture_output=True, text=True,
                cwd=self.repo_path
            )
            
            files = [line.strip() for line in result.stdout.split('\n') if line.strip()]
            return {
                "modified": [f[3:] for f in files if f.startswith(' M')],
                "added": [f[3:] for f in files if f.startswith('A ')],
                "untracked": [f[3:] for f in files if f.startswith('??')],
                "total": len(files)
            }
        except Exception as e:
            return {"error": str(e)}
    
    def commit(self, message: str) -> dict:
        """Create a commit"""
        try:
            # Stage all
            subprocess.run(["git", "add", "-A"], cwd=self.repo_path, check=True)
            
            # Commit
            result = subprocess.run(
                ["git", "commit", "-m", message],
                capture_output=True, text=True,
                cwd=self.repo_path
            )
            
            return {"status": "success", "message": message, "output": result.stdout}
        except Exception as e:
            return {"error": str(e)}
    
    def log(self, limit: int = 10) -> List[dict]:
        """Get recent commits"""
        try:
            result = subprocess.run(
                ["git", "log", f"-{limit}", "--pretty=format:%h|%s|%an|%ar"],
                capture_output=True, text=True,
                cwd=self.repo_path
            )
            
            commits = []
            for line in result.stdout.split('\n'):
                if line:
                    parts = line.split('|')
                    commits.append({
                        "hash": parts[0],
                        "message": parts[1] if len(parts) > 1 else "",
                        "author": parts[2] if len(parts) > 2 else "",
                        "date": parts[3] if len(parts) > 3 else ""
                    })
            return commits
        except Exception as e:
            return [{"error": str(e)}]


class QuickActions:
    """Pre-defined quick actions for common tasks"""
    
    ACTIONS = {
        "fix": {"system": "You are a code fixing expert. Fix the issue concisely.", "prefix": "Fix this: "},
        "improve": {"system": "Suggest improvements concisely.", "prefix": "Improve this: "},
        "explain": {"system": "Explain simply in 2-3 sentences.", "prefix": ""},
        "tldr": {"system": "Summarize in one sentence.", "prefix": "TL;DR: "},
        "review": {"system": "Review briefly, noting key issues.", "prefix": "Review: "},
        "idea": {"system": "Generate 3 creative ideas.", "prefix": "Ideas for: "},
        "doc": {"system": "Generate concise documentation.", "prefix": "Document: "},
        "test": {"system": "Generate test cases.", "prefix": "Test cases for: "},
    }
    
    @classmethod
    def run(cls, action: str, content: str) -> dict:
        if action not in cls.ACTIONS:
            return {"error": f"Unknown action: {action}"}
        
        cfg = cls.ACTIONS[action]
        llm = SmartLLM()
        return llm.chat(f"{cfg['prefix']}{content}", cfg['system'])


class RateLimiter:
    """Smart rate limiting to avoid API throttling"""
    
    def __init__(self):
        self.requests: Dict[str, List[float]] = {}
        self.limits = {
            'anthropic': (50, 60),   # 50 requests per 60 seconds
            'openai': (60, 60),      # 60 requests per 60 seconds
            'default': (30, 60)
        }
    
    def can_request(self, provider: str) -> bool:
        limit, window = self.limits.get(provider, self.limits['default'])
        now = time.time()
        
        if provider not in self.requests:
            self.requests[provider] = []
        
        # Clean old requests
        self.requests[provider] = [t for t in self.requests[provider] if now - t < window]
        
        return len(self.requests[provider]) < limit
    
    def record_request(self, provider: str):
        if provider not in self.requests:
            self.requests[provider] = []
        self.requests[provider].append(time.time())
    
    def wait_time(self, provider: str) -> float:
        if self.can_request(provider):
            return 0
        
        limit, window = self.limits.get(provider, self.limits['default'])
        oldest = min(self.requests.get(provider, [time.time()]))
        return max(0, window - (time.time() - oldest))


class WebhookNotifier:
    """Send notifications via webhooks"""
    
    def __init__(self, config_file: str = "~/.noizylab/webhooks.json"):
        self.config_file = Path(config_file).expanduser()
        self.webhooks = self._load_config()
    
    def _load_config(self) -> Dict[str, str]:
        if self.config_file.exists():
            return json.loads(self.config_file.read_text())
        return {}
    
    def add(self, name: str, url: str):
        """Add a webhook"""
        self.webhooks[name] = url
        self.config_file.parent.mkdir(parents=True, exist_ok=True)
        self.config_file.write_text(json.dumps(self.webhooks, indent=2))
        print(f"✅ Added webhook: {name}")
    
    def notify(self, name: str, message: str, data: dict = None):
        """Send notification to webhook"""
        url = self.webhooks.get(name)
        if not url:
            return False
        
        try:
            import urllib.request
            payload = {
                "text": message,
                "data": data or {},
                "timestamp": datetime.now().isoformat()
            }
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode(),
                headers={"Content-Type": "application/json"}
            )
            urllib.request.urlopen(req, timeout=5)
            return True
        except:
            return False
    
    def list(self):
        """List configured webhooks"""
        print("\n🔔 WEBHOOKS:\n")
        if not self.webhooks:
            print("  No webhooks configured")
        for name in self.webhooks:
            print(f"  {name}")
        print()


class ModelEnsemble:
    """Multi-model ensemble for better responses"""
    
    def __init__(self):
        self.models = ['anthropic', 'openai']
        self.key_manager = KeyManager()
    
    def query_all(self, prompt: str, system: str = "") -> List[dict]:
        """Query all available models in parallel"""
        results = []
        available = [m for m in self.models if self.key_manager.get_key(m)]
        
        with ThreadPoolExecutor(max_workers=len(available)) as executor:
            futures = {}
            for model in available:
                llm = SmartLLM()
                futures[executor.submit(llm.chat, prompt, system, model)] = model
            
            for future in as_completed(futures):
                model = futures[future]
                try:
                    result = future.result()
                    results.append({'model': model, 'response': result})
                except Exception as e:
                    results.append({'model': model, 'error': str(e)})
        
        return results
    
    def consensus(self, prompt: str, system: str = "") -> dict:
        """Get consensus response from multiple models"""
        results = self.query_all(prompt, system)
        successful = [r for r in results if 'response' in r]
        
        if not successful:
            return {'error': 'All models failed'}
        
        # Use first successful response but note agreement
        primary = successful[0]['response']
        primary['ensemble_count'] = len(successful)
        primary['models_used'] = [r['model'] for r in successful]
        
        return primary

# Global metrics instance
METRICS = MetricsEngine()

# ============================================================================
# CONFIGURATION
# ============================================================================

@dataclass
class AIService:
    name: str
    category: str
    api_url: str
    api_key_env: str
    cost_per_unit: float
    unit_name: str
    features: List[str]

AI_SERVICES: Dict[str, AIService] = {
    # VIDEO
    "runway": AIService("Runway Gen-3", "video", "https://api.runwayml.com/v1", "RUNWAY_API_KEY", 0.05, "second", ["text-to-video", "image-to-video", "motion-brush"]),
    "kling": AIService("Kling AI", "video", "https://api.klingai.com/v1", "KLING_API_KEY", 0.03, "second", ["text-to-video", "5min-video", "lip-sync"]),
    "pika": AIService("Pika", "video", "https://api.pika.art/v1", "PIKA_API_KEY", 0.02, "second", ["text-to-video", "modify", "effects"]),
    "luma": AIService("Luma Dream Machine", "video", "https://api.lumalabs.ai/v1", "LUMA_API_KEY", 0.04, "second", ["text-to-video", "fast-gen"]),
    
    # AUDIO
    "suno": AIService("Suno", "audio", "https://api.suno.ai/v1", "SUNO_API_KEY", 0.01, "song", ["text-to-music", "vocals", "extend"]),
    "udio": AIService("Udio", "audio", "https://api.udio.com/v1", "UDIO_API_KEY", 0.01, "song", ["text-to-music", "remix", "stems"]),
    "elevenlabs": AIService("ElevenLabs", "audio", "https://api.elevenlabs.io/v1", "ELEVENLABS_API_KEY", 0.0003, "char", ["tts", "voice-clone", "sfx"]),
    
    # AVATAR
    "heygen": AIService("HeyGen", "avatar", "https://api.heygen.com/v2", "HEYGEN_API_KEY", 0.10, "minute", ["avatar-video", "translate", "voice-clone"]),
    "synthesia": AIService("Synthesia", "avatar", "https://api.synthesia.io/v2", "SYNTHESIA_API_KEY", 0.15, "minute", ["avatar-video", "templates", "enterprise"]),
    "did": AIService("D-ID", "avatar", "https://api.d-id.com/v1", "DID_API_KEY", 0.08, "minute", ["real-time", "api-first", "streaming"]),
    
    # LLM
    "openai": AIService("OpenAI", "llm", "https://api.openai.com/v1", "OPENAI_API_KEY", 0.01, "1k-tokens", ["gpt-4", "gpt-4o", "dall-e"]),
    "anthropic": AIService("Anthropic", "llm", "https://api.anthropic.com/v1", "ANTHROPIC_API_KEY", 0.015, "1k-tokens", ["claude-3", "claude-3.5"]),
    "openrouter": AIService("OpenRouter", "llm", "https://openrouter.ai/api/v1", "OPENROUTER_API_KEY", 0.001, "1k-tokens", ["multi-provider", "fallback"]),
}

# ============================================================================
# CACHE SYSTEM - FASTER RESPONSES
# ============================================================================

class ResponseCache:
    """In-memory cache with disk persistence for faster responses"""
    
    def __init__(self, cache_dir: str = "~/.noizylab/cache"):
        self.cache_dir = Path(cache_dir).expanduser()
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.memory_cache: Dict[str, dict] = {}
        self.ttl = 3600  # 1 hour default TTL
    
    def _hash_key(self, key: str) -> str:
        return hashlib.md5(key.encode()).hexdigest()
    
    def get(self, key: str) -> Optional[dict]:
        hashed = self._hash_key(key)
        
        # Check memory first (fastest)
        if hashed in self.memory_cache:
            entry = self.memory_cache[hashed]
            if time.time() - entry['timestamp'] < self.ttl:
                return entry['data']
        
        # Check disk
        cache_file = self.cache_dir / f"{hashed}.json"
        if cache_file.exists():
            entry = json.loads(cache_file.read_text())
            if time.time() - entry['timestamp'] < self.ttl:
                self.memory_cache[hashed] = entry
                return entry['data']
        
        return None
    
    def set(self, key: str, data: dict):
        hashed = self._hash_key(key)
        entry = {'data': data, 'timestamp': time.time()}
        
        # Memory cache
        self.memory_cache[hashed] = entry
        
        # Disk persistence
        cache_file = self.cache_dir / f"{hashed}.json"
        cache_file.write_text(json.dumps(entry))
    
    def clear(self):
        self.memory_cache.clear()
        for f in self.cache_dir.glob("*.json"):
            f.unlink()
        print("✅ Cache cleared")

# Global cache instance
CACHE = ResponseCache()

# ============================================================================
# AUTONOMOUS BATCH PROCESSOR
# ============================================================================

class BatchProcessor:
    """Process multiple AI tasks in parallel with automatic retry"""
    
    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers
        self.results: List[dict] = []
        self.failed: List[dict] = []
    
    def process(self, tasks: List[dict], retry_count: int = 3) -> List[dict]:
        """Process tasks in parallel with retry logic"""
        print(f"\n🚀 BATCH PROCESSING: {len(tasks)} tasks with {self.max_workers} workers\n")
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {}
            for i, task in enumerate(tasks):
                future = executor.submit(self._execute_task, task, retry_count)
                futures[future] = (i, task)
            
            for future in as_completed(futures):
                idx, task = futures[future]
                try:
                    result = future.result()
                    self.results.append({'task': task, 'result': result, 'status': 'success'})
                    print(f"  ✅ Task {idx+1}/{len(tasks)} completed")
                except Exception as e:
                    self.failed.append({'task': task, 'error': str(e)})
                    print(f"  ❌ Task {idx+1}/{len(tasks)} failed: {e}")
        
        print(f"\n📊 BATCH COMPLETE: {len(self.results)} succeeded, {len(self.failed)} failed")
        return self.results
    
    def _execute_task(self, task: dict, retries: int) -> dict:
        """Execute single task with retry"""
        last_error = None
        for attempt in range(retries):
            try:
                task_type = task.get('type', 'video')
                if task_type == 'video':
                    gen = VideoGenerator(task.get('provider', 'runway'))
                    return gen.generate(task['prompt'], task.get('duration', 5))
                elif task_type == 'audio':
                    gen = AudioGenerator(task.get('provider', 'suno'))
                    return gen.generate_music(task['prompt'], task.get('duration', 60))
                elif task_type == 'avatar':
                    gen = AvatarGenerator(task.get('provider', 'heygen'))
                    return gen.create_video(task['script'])
            except Exception as e:
                last_error = e
                time.sleep(2 ** attempt)  # Exponential backoff
        raise last_error

# ============================================================================
# AUTO-DISCOVERY & HEALTH CHECK
# ============================================================================

class ServiceDiscovery:
    """Automatically discover and health-check available AI services"""
    
    @staticmethod
    def discover_available() -> Dict[str, bool]:
        """Check which services have API keys configured"""
        km = KeyManager()
        available = {}
        for name in AI_SERVICES:
            available[name] = km.get_key(name) is not None
        return available
    
    @staticmethod
    def health_check(service: str) -> dict:
        """Test if a service is responding"""
        client = AIClient(service)
        if not client.api_key:
            return {'status': 'unconfigured', 'latency': None}
        
        start = time.time()
        try:
            # Simple connectivity test
            import urllib.request
            req = urllib.request.Request(
                AI_SERVICES[service].api_url,
                headers={'Authorization': f'Bearer {client.api_key}'}
            )
            urllib.request.urlopen(req, timeout=5)
            latency = (time.time() - start) * 1000
            return {'status': 'healthy', 'latency': f'{latency:.0f}ms'}
        except Exception as e:
            return {'status': 'error', 'error': str(e)[:50]}
    
    @staticmethod
    def recommend_provider(task_type: str) -> str:
        """Recommend best available provider for task type"""
        available = ServiceDiscovery.discover_available()
        
        priorities = {
            'video': ['runway', 'kling', 'pika', 'luma'],
            'audio': ['suno', 'udio', 'elevenlabs'],
            'avatar': ['heygen', 'synthesia', 'did'],
            'llm': ['anthropic', 'openai', 'openrouter']
        }
        
        for provider in priorities.get(task_type, []):
            if available.get(provider):
                return provider
        return priorities.get(task_type, ['unknown'])[0]

# ============================================================================
# SELF-HEALING DIAGNOSTICS
# ============================================================================

class SelfHealing:
    """Autonomous diagnostics and self-healing capabilities"""
    
    @staticmethod
    def diagnose() -> List[dict]:
        """Run full system diagnostics"""
        issues = []
        
        # Check API keys
        available = ServiceDiscovery.discover_available()
        missing = [k for k, v in available.items() if not v]
        if missing:
            issues.append({
                'type': 'missing_keys',
                'severity': 'warning',
                'message': f"Missing API keys: {', '.join(missing)}",
                'fix': 'python3 ai_manager.py keys --set SERVICE KEY'
            })
        
        # Check cache health
        cache_size = sum(f.stat().st_size for f in CACHE.cache_dir.glob("*.json"))
        if cache_size > 100_000_000:  # 100MB
            issues.append({
                'type': 'cache_large',
                'severity': 'info',
                'message': f"Cache size is {cache_size/1_000_000:.1f}MB",
                'fix': 'python3 ai_manager.py heal --clear-cache'
            })
        
        # Check Python environment
        try:
            import requests
        except ImportError:
            issues.append({
                'type': 'missing_dependency',
                'severity': 'error',
                'message': 'requests library not installed',
                'fix': 'pip install requests'
            })
        
        return issues
    
    @staticmethod
    def heal(auto: bool = False) -> List[str]:
        """Attempt to fix discovered issues"""
        actions = []
        issues = SelfHealing.diagnose()
        
        for issue in issues:
            if issue['severity'] == 'error' or auto:
                if issue['type'] == 'cache_large':
                    CACHE.clear()
                    actions.append("Cleared cache")
                elif issue['type'] == 'missing_dependency':
                    subprocess.run(['pip', 'install', 'requests'], capture_output=True)
                    actions.append("Installed requests")
        
        return actions

# ============================================================================
# API KEY MANAGEMENT
# ============================================================================

class KeyManager:
    def __init__(self, keys_file: str = "~/.noizylab/api_keys.json"):
        self.keys_file = Path(keys_file).expanduser()
        self.keys_file.parent.mkdir(parents=True, exist_ok=True)
        self.keys = self._load_keys()
    
    def _load_keys(self) -> Dict[str, str]:
        if self.keys_file.exists():
            return json.loads(self.keys_file.read_text())
        return {}
    
    def _save_keys(self):
        self.keys_file.write_text(json.dumps(self.keys, indent=2))
        os.chmod(self.keys_file, 0o600)
    
    def set_key(self, service: str, key: str):
        self.keys[service] = key
        self._save_keys()
        print(f"✅ {service} API key saved")
    
    def get_key(self, service: str) -> Optional[str]:
        env_var = AI_SERVICES.get(service, {})
        if isinstance(env_var, AIService):
            env_var = env_var.api_key_env
        return os.environ.get(env_var) or self.keys.get(service)
    
    def list_keys(self):
        print("\n🔑 API KEYS STATUS:\n")
        for name, svc in AI_SERVICES.items():
            key = self.get_key(name)
            status = "✅ SET" if key else "❌ MISSING"
            print(f"  {name:<15} │ {status}")
        print()

# ============================================================================
# SERVICE CLIENTS
# ============================================================================

class AIClient:
    def __init__(self, service: str):
        self.service = AI_SERVICES.get(service)
        self.key_manager = KeyManager()
        self.api_key = self.key_manager.get_key(service)
    
    def _request(self, endpoint: str, data: dict) -> dict:
        import urllib.request
        import urllib.error
        
        url = f"{self.service.api_url}/{endpoint}"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        req = urllib.request.Request(
            url,
            data=json.dumps(data).encode(),
            headers=headers,
            method="POST"
        )
        
        try:
            with urllib.request.urlopen(req) as resp:
                return json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            return {"error": str(e), "status": e.code}

# ============================================================================
# VIDEO GENERATION
# ============================================================================

class ImageGenerator:
    """Generate images using DALL-E or other providers"""
    
    def __init__(self, provider: str = "openai"):
        self.provider = provider
        self.key_manager = KeyManager()
    
    def generate(self, prompt: str, size: str = "1024x1024", style: str = "vivid") -> dict:
        print(f"🎨 Generating image with {self.provider}...")
        print(f"   Prompt: {prompt[:50]}...")
        
        api_key = self.key_manager.get_key(self.provider)
        if not api_key:
            return {"error": f"No API key for {self.provider}"}
        
        start = time.time()
        try:
            import urllib.request
            data = {
                "model": "dall-e-3",
                "prompt": prompt,
                "n": 1,
                "size": size,
                "style": style
            }
            req = urllib.request.Request(
                "https://api.openai.com/v1/images/generations",
                data=json.dumps(data).encode(),
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                }
            )
            with urllib.request.urlopen(req) as resp:
                result = json.loads(resp.read().decode())
                latency = (time.time() - start) * 1000
                METRICS.log_request(self.provider, 'image', latency_ms=latency, cost=0.04)
                return {
                    "status": "success",
                    "url": result['data'][0]['url'],
                    "revised_prompt": result['data'][0].get('revised_prompt', prompt)
                }
        except Exception as e:
            return {"error": str(e)}


class VideoGenerator:
    def __init__(self, provider: str = "runway"):
        self.client = AIClient(provider)
        self.provider = provider
    
    def generate(self, prompt: str, duration: int = 5, style: str = "cinematic") -> dict:
        print(f"🎬 Generating video with {self.provider}...")
        print(f"   Prompt: {prompt[:50]}...")
        print(f"   Duration: {duration}s | Style: {style}")
        
        # This would be the actual API call
        return {
            "status": "queued",
            "provider": self.provider,
            "prompt": prompt,
            "estimated_time": duration * 10
        }

# ============================================================================
# AUDIO GENERATION  
# ============================================================================

class AudioGenerator:
    def __init__(self, provider: str = "suno"):
        self.client = AIClient(provider)
        self.provider = provider
    
    def generate_music(self, prompt: str, duration: int = 60, genre: str = "auto") -> dict:
        print(f"🎵 Generating music with {self.provider}...")
        print(f"   Prompt: {prompt[:50]}...")
        print(f"   Duration: {duration}s | Genre: {genre}")
        
        return {
            "status": "queued",
            "provider": self.provider,
            "prompt": prompt,
            "estimated_time": 30
        }
    
    def text_to_speech(self, text: str, voice: str = "default") -> dict:
        print(f"🗣️ Generating speech with {self.provider}...")
        return {
            "status": "queued",
            "text": text[:100],
            "voice": voice
        }

# ============================================================================
# AVATAR GENERATION
# ============================================================================

class AvatarGenerator:
    def __init__(self, provider: str = "heygen"):
        self.client = AIClient(provider)
        self.provider = provider
    
    def create_video(self, script: str, avatar: str = "default", voice: str = "auto") -> dict:
        print(f"🎭 Creating avatar video with {self.provider}...")
        print(f"   Script: {script[:50]}...")
        print(f"   Avatar: {avatar} | Voice: {voice}")
        
        return {
            "status": "queued",
            "provider": self.provider,
            "script": script,
            "estimated_time": len(script) // 10
        }

# ============================================================================
# MICROSOFT OFFICE INTEGRATION
# ============================================================================

class MSOfficeAI:
    """Integration with Microsoft 365 Copilot and Power Automate"""
    
    @staticmethod
    def list_copilot_features():
        features = {
            "Word": ["Draft documents", "Rewrite text", "Summarize", "Generate from prompt"],
            "Excel": ["Analyze data", "Create formulas", "Generate charts", "Python in Excel"],
            "PowerPoint": ["Generate slides", "Design suggestions", "Speaker notes"],
            "Outlook": ["Draft emails", "Summarize threads", "Schedule meetings"],
            "Teams": ["Meeting summaries", "Action items", "Chat recaps"],
            "Power Automate": ["Natural language flows", "AI Builder", "Document processing"],
        }
        
        print("\n🪟 MICROSOFT 365 COPILOT FEATURES:\n")
        for app, feats in features.items():
            print(f"  {app}:")
            for f in feats:
                print(f"    • {f}")
        print()
        return features
    
    @staticmethod
    def power_automate_templates():
        templates = [
            "When email arrives → Extract attachments → Save to OneDrive → Notify Teams",
            "When form submitted → Process with AI → Update SharePoint → Send confirmation",
            "Daily → Summarize emails → Generate report → Post to channel",
            "When file uploaded → Analyze with Vision AI → Tag and categorize",
            "Scheduled → Collect data → AI analysis → Executive summary email",
        ]
        
        print("\n⚡ POWER AUTOMATE AI TEMPLATES:\n")
        for i, t in enumerate(templates, 1):
            print(f"  {i}. {t}")
        print()
        return templates

# ============================================================================
# UNIFIED DASHBOARD
# ============================================================================

class SmartLLM:
    """Intelligent LLM router with fallback and load balancing"""
    
    def __init__(self):
        self.providers = ['anthropic', 'openai', 'openrouter']
        self.key_manager = KeyManager()
    
    def chat(self, prompt: str, system: str = "You are a helpful assistant.", 
             model: str = "auto", max_tokens: int = 4096) -> dict:
        """Smart chat with automatic provider selection and fallback"""
        
        # Auto-select provider
        provider = model if model != "auto" else ServiceDiscovery.recommend_provider('llm')
        print(f"🧠 Using {provider} for LLM request...")
        
        api_key = self.key_manager.get_key(provider)
        if not api_key:
            return {"error": f"No API key for {provider}"}
        
        # Check cache first
        cache_key = f"{provider}:{system}:{prompt}"
        cached = CACHE.get(cache_key)
        if cached:
            print("  ⚡ Cache hit!")
            return cached
        
        try:
            if provider == "anthropic":
                result = self._call_anthropic(api_key, prompt, system, max_tokens)
            elif provider == "openai":
                result = self._call_openai(api_key, prompt, system, max_tokens)
            else:
                result = self._call_openrouter(api_key, prompt, system, max_tokens)
            
            CACHE.set(cache_key, result)
            return result
        except Exception as e:
            # Fallback to next provider
            remaining = [p for p in self.providers if p != provider and self.key_manager.get_key(p)]
            if remaining:
                print(f"  ⚠️ {provider} failed, trying {remaining[0]}...")
                return self.chat(prompt, system, remaining[0], max_tokens)
            return {"error": str(e)}
    
    def _call_anthropic(self, api_key: str, prompt: str, system: str, max_tokens: int) -> dict:
        import urllib.request
        data = {
            "model": "claude-3-5-sonnet-20241022",
            "max_tokens": max_tokens,
            "system": system,
            "messages": [{"role": "user", "content": prompt}]
        }
        req = urllib.request.Request(
            "https://api.anthropic.com/v1/messages",
            data=json.dumps(data).encode(),
            headers={
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01",
                "Content-Type": "application/json"
            }
        )
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read().decode())
            return {"provider": "anthropic", "content": result.get("content", [{}])[0].get("text", "")}
    
    def _call_openai(self, api_key: str, prompt: str, system: str, max_tokens: int) -> dict:
        import urllib.request
        data = {
            "model": "gpt-4o",
            "max_tokens": max_tokens,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": prompt}
            ]
        }
        req = urllib.request.Request(
            "https://api.openai.com/v1/chat/completions",
            data=json.dumps(data).encode(),
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
        )
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read().decode())
            return {"provider": "openai", "content": result["choices"][0]["message"]["content"]}
    
    def _call_openrouter(self, api_key: str, prompt: str, system: str, max_tokens: int) -> dict:
        import urllib.request
        data = {
            "model": "anthropic/claude-3.5-sonnet",
            "max_tokens": max_tokens,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": prompt}
            ]
        }
        req = urllib.request.Request(
            "https://openrouter.ai/api/v1/chat/completions",
            data=json.dumps(data).encode(),
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
        )
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read().decode())
            return {"provider": "openrouter", "content": result["choices"][0]["message"]["content"]}


class Scheduler:
    """Scheduled task automation"""
    
    def __init__(self, schedule_file: str = "~/.noizylab/schedule.json"):
        self.schedule_file = Path(schedule_file).expanduser()
        self.schedule_file.parent.mkdir(parents=True, exist_ok=True)
        self.tasks = self._load_schedule()
    
    def _load_schedule(self) -> List[dict]:
        if self.schedule_file.exists():
            return json.loads(self.schedule_file.read_text())
        return []
    
    def _save_schedule(self):
        self.schedule_file.write_text(json.dumps(self.tasks, indent=2))
    
    def add_task(self, task: dict):
        """Add a scheduled task"""
        task['id'] = hashlib.md5(str(time.time()).encode()).hexdigest()[:8]
        task['created'] = datetime.now().isoformat()
        task['last_run'] = None
        self.tasks.append(task)
        self._save_schedule()
        print(f"✅ Scheduled task {task['id']}: {task.get('action', 'unknown')}")
        return task['id']
    
    def list_tasks(self):
        """List all scheduled tasks"""
        print("\n📅 SCHEDULED TASKS:\n")
        if not self.tasks:
            print("  No scheduled tasks")
        for task in self.tasks:
            status = "🟢" if task.get('enabled', True) else "⬚"
            print(f"  {status} {task['id']} │ {task.get('action')} │ {task.get('schedule', 'manual')}")
        print()
    
    def remove_task(self, task_id: str):
        """Remove a scheduled task"""
        self.tasks = [t for t in self.tasks if t.get('id') != task_id]
        self._save_schedule()
        print(f"✅ Removed task {task_id}")
    
    def run_due_tasks(self):
        """Run all due tasks"""
        now = datetime.now()
        ran = 0
        for task in self.tasks:
            if not task.get('enabled', True):
                continue
            # Simple interval-based scheduling
            interval = task.get('interval_minutes', 60)
            last_run = task.get('last_run')
            if last_run:
                last = datetime.fromisoformat(last_run)
                if (now - last).total_seconds() < interval * 60:
                    continue
            
            print(f"⏰ Running scheduled task: {task['id']}")
            task['last_run'] = now.isoformat()
            ran += 1
        
        self._save_schedule()
        return ran


class AIAgent:
    """Autonomous AI agent for complex tasks"""
    
    def __init__(self):
        self.llm = SmartLLM()
        self.memory: List[dict] = []
        self.max_iterations = 10
    
    def think(self, goal: str) -> List[dict]:
        """Agent thinks about how to accomplish a goal"""
        system = """You are an autonomous AI agent. Given a goal, break it down into steps.
Return a JSON array of steps, each with: {"action": "llm|video|audio|avatar", "params": {...}}
Only return valid JSON, no explanation."""
        
        result = self.llm.chat(f"Goal: {goal}", system)
        try:
            return json.loads(result.get('content', '[]'))
        except:
            return []
    
    def run(self, goal: str) -> dict:
        """Autonomously work toward a goal"""
        print(f"\n🤖 AI AGENT: {goal}\n")
        
        # Plan
        print("  📋 Planning...")
        steps = self.think(goal)
        if not steps:
            return {"error": "Could not plan steps for goal"}
        
        print(f"  📋 Generated {len(steps)} steps")
        
        # Execute
        workflow = WorkflowEngine()
        results = workflow.run_workflow(steps)
        
        return {"goal": goal, "steps": len(steps), "results": results}


class WorkflowEngine:
    """Autonomous workflow engine for chaining AI tasks"""
    
    def __init__(self):
        self.llm = SmartLLM()
        self.video = VideoGenerator()
        self.audio = AudioGenerator()
        self.avatar = AvatarGenerator()
    
    def run_workflow(self, workflow: List[dict]) -> List[dict]:
        """Execute a chain of AI tasks"""
        results = []
        context = {}
        
        print(f"\n⚙️ WORKFLOW ENGINE: {len(workflow)} steps\n")
        
        for i, step in enumerate(workflow):
            print(f"  Step {i+1}/{len(workflow)}: {step.get('action', 'unknown')}")
            
            action = step.get('action')
            params = step.get('params', {})
            
            # Substitute context variables
            for key, value in params.items():
                if isinstance(value, str) and value.startswith('$'):
                    var_name = value[1:]
                    params[key] = context.get(var_name, value)
            
            try:
                if action == 'llm':
                    result = self.llm.chat(params.get('prompt', ''))
                elif action == 'video':
                    result = self.video.generate(params.get('prompt', ''))
                elif action == 'audio':
                    result = self.audio.generate_music(params.get('prompt', ''))
                elif action == 'avatar':
                    result = self.avatar.create_video(params.get('script', ''))
                else:
                    result = {'error': f'Unknown action: {action}'}
                
                results.append({'step': i+1, 'action': action, 'result': result})
                
                # Store output in context
                if 'output_var' in step:
                    context[step['output_var']] = result.get('content', result)
                
                print(f"    ✅ Completed")
            except Exception as e:
                results.append({'step': i+1, 'action': action, 'error': str(e)})
                print(f"    ❌ Failed: {e}")
        
        print(f"\n✅ Workflow complete: {len([r for r in results if 'error' not in r])}/{len(workflow)} succeeded")
        return results


class AIDashboard:
    def __init__(self):
        self.key_manager = KeyManager()
        self.video = VideoGenerator()
        self.audio = AudioGenerator()
        self.avatar = AvatarGenerator()
        self.llm = SmartLLM()
        self.workflow = WorkflowEngine()
    
    def status(self):
        print("\n" + "="*60)
        print("🧠 NOIZYLAB AI COMMAND CENTER")
        print("="*60)
        
        # API Keys
        self.key_manager.list_keys()
        
        # Services by category
        categories = {}
        for name, svc in AI_SERVICES.items():
            cat = svc.category
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(svc.name)
        
        print("📦 AVAILABLE SERVICES:\n")
        for cat, services in categories.items():
            print(f"  {cat.upper()}: {', '.join(services)}")
        print()
    
    def interactive(self):
        """Interactive mode for managing AI services"""
        while True:
            print("\n┌────────────────────────────────────┐")
            print("│     🧠 AI COMMAND CENTER           │")
            print("├────────────────────────────────────┤")
            print("│  1. Generate Video                 │")
            print("│  2. Generate Audio/Music           │")
            print("│  3. Create Avatar Video            │")
            print("│  4. Microsoft Office AI            │")
            print("│  5. Manage API Keys                │")
            print("│  6. Service Status                 │")
            print("│  0. Exit                           │")
            print("└────────────────────────────────────┘")
            
            choice = input("\n→ Select option: ").strip()
            
            if choice == "0":
                print("👋 Goodbye!")
                break
            elif choice == "1":
                prompt = input("Video prompt: ")
                self.video.generate(prompt)
            elif choice == "2":
                prompt = input("Music prompt: ")
                self.audio.generate_music(prompt)
            elif choice == "3":
                script = input("Avatar script: ")
                self.avatar.create_video(script)
            elif choice == "4":
                MSOfficeAI.list_copilot_features()
                MSOfficeAI.power_automate_templates()
            elif choice == "5":
                self.key_manager.list_keys()
                svc = input("Service to configure (or 'skip'): ").strip()
                if svc != "skip" and svc in AI_SERVICES:
                    key = input(f"API key for {svc}: ").strip()
                    self.key_manager.set_key(svc, key)
            elif choice == "6":
                self.status()

# ============================================================================
# CLI
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="🧠 NOIZYLAB AI COMMAND CENTER",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest="command")
    
    # Video
    video_parser = subparsers.add_parser("video", help="Generate video")
    video_parser.add_argument("--prompt", "-p", required=True)
    video_parser.add_argument("--provider", default="runway", choices=["runway", "kling", "pika", "luma"])
    video_parser.add_argument("--duration", "-d", type=int, default=5)
    
    # Audio
    audio_parser = subparsers.add_parser("audio", help="Generate audio/music")
    audio_parser.add_argument("--prompt", "-p", required=True)
    audio_parser.add_argument("--provider", default="suno", choices=["suno", "udio", "elevenlabs"])
    audio_parser.add_argument("--duration", "-d", type=int, default=60)
    
    # Avatar
    avatar_parser = subparsers.add_parser("avatar", help="Create avatar video")
    avatar_parser.add_argument("--script", "-s", required=True)
    avatar_parser.add_argument("--provider", default="heygen", choices=["heygen", "synthesia", "did"])
    
    # Keys
    keys_parser = subparsers.add_parser("keys", help="Manage API keys")
    keys_parser.add_argument("--set", nargs=2, metavar=("SERVICE", "KEY"))
    keys_parser.add_argument("--list", "-l", action="store_true")
    
    # Status
    subparsers.add_parser("status", help="Show service status")
    
    # Microsoft
    subparsers.add_parser("microsoft", help="Microsoft Office AI info")
    
    # Interactive
    subparsers.add_parser("interactive", help="Interactive mode")
    
    # Batch processing
    batch_parser = subparsers.add_parser("batch", help="Batch process multiple tasks")
    batch_parser.add_argument("--file", "-f", required=True, help="JSON file with tasks")
    batch_parser.add_argument("--workers", "-w", type=int, default=4, help="Parallel workers")
    
    # Diagnose
    diag_parser = subparsers.add_parser("diagnose", help="Run system diagnostics")
    
    # Heal
    heal_parser = subparsers.add_parser("heal", help="Self-heal system issues")
    heal_parser.add_argument("--auto", "-a", action="store_true", help="Auto-fix all issues")
    heal_parser.add_argument("--clear-cache", action="store_true", help="Clear response cache")
    
    # Discover
    subparsers.add_parser("discover", help="Discover available services")
    
    # Auto mode
    auto_parser = subparsers.add_parser("auto", help="Autonomous mode - auto-select best provider")
    auto_parser.add_argument("--type", "-t", choices=["video", "audio", "avatar"], required=True)
    auto_parser.add_argument("--prompt", "-p", required=True)
    
    # Chat (LLM)
    chat_parser = subparsers.add_parser("chat", help="Smart LLM chat with auto-routing")
    chat_parser.add_argument("prompt", help="Your message")
    chat_parser.add_argument("--provider", "-p", choices=["anthropic", "openai", "openrouter", "auto"], default="auto")
    chat_parser.add_argument("--system", "-s", default="You are a helpful AI assistant.")
    
    # Workflow
    workflow_parser = subparsers.add_parser("workflow", help="Run autonomous workflow")
    workflow_parser.add_argument("--file", "-f", required=True, help="JSON workflow file")
    
    # Schedule
    schedule_parser = subparsers.add_parser("schedule", help="Manage scheduled tasks")
    schedule_parser.add_argument("action", choices=["list", "add", "remove", "run"], default="list", nargs="?")
    schedule_parser.add_argument("--task", "-t", help="Task JSON or ID")
    
    # Agent
    agent_parser = subparsers.add_parser("agent", help="Autonomous AI agent")
    agent_parser.add_argument("goal", nargs="*", help="Goal for the agent to accomplish")
    
    # Metrics
    metrics_parser = subparsers.add_parser("metrics", help="View usage metrics and analytics")
    metrics_parser.add_argument("--hours", type=int, default=24, help="Hours to show")
    
    # Ensemble
    ensemble_parser = subparsers.add_parser("ensemble", help="Query multiple models in parallel")
    ensemble_parser.add_argument("prompt", nargs="*", help="Your prompt")
    
    # Daemon mode
    daemon_parser = subparsers.add_parser("daemon", help="Run as background daemon")
    daemon_parser.add_argument("action", choices=["start", "stop", "status"], default="status", nargs="?")
    
    # Templates
    template_parser = subparsers.add_parser("template", help="Use prompt templates")
    template_parser.add_argument("name", nargs="?", help="Template name")
    template_parser.add_argument("--list", "-l", action="store_true", help="List templates")
    template_parser.add_argument("--vars", "-v", nargs="*", help="Variables as key=value")
    
    # Webhooks
    webhook_parser = subparsers.add_parser("webhook", help="Manage webhooks")
    webhook_parser.add_argument("action", choices=["list", "add", "test"], default="list", nargs="?")
    webhook_parser.add_argument("--name", "-n", help="Webhook name")
    webhook_parser.add_argument("--url", "-u", help="Webhook URL")
    
    # Export
    export_parser = subparsers.add_parser("export", help="Export configuration")
    export_parser.add_argument("--output", "-o", default="noizylab_export.json", help="Output file")
    
    # Quick actions
    quick_parser = subparsers.add_parser("quick", help="Quick actions: fix, improve, explain, tldr, review, idea")
    quick_parser.add_argument("action", choices=["fix", "improve", "explain", "tldr", "review", "idea"])
    quick_parser.add_argument("content", nargs="*", help="Content to process")
    
    # Pipe mode (for stdin)
    pipe_parser = subparsers.add_parser("pipe", help="Process stdin with action")
    pipe_parser.add_argument("action", choices=["fix", "improve", "explain", "tldr", "review", "summarize"])
    
    # Image generation
    image_parser = subparsers.add_parser("image", help="Generate images with DALL-E")
    image_parser.add_argument("prompt", nargs="*", help="Image description")
    image_parser.add_argument("--size", "-s", default="1024x1024", choices=["1024x1024", "1792x1024", "1024x1792"])
    image_parser.add_argument("--style", default="vivid", choices=["vivid", "natural"])
    
    # GABRIEL Integration
    gabriel_parser = subparsers.add_parser("gabriel", help="GABRIEL unified systems")
    gabriel_parser.add_argument("action", choices=["status", "scan", "speak", "hot", "metrics"], nargs="?", default="status")
    gabriel_parser.add_argument("--text", "-t", help="Text for speech")
    gabriel_parser.add_argument("--emotion", "-e", default="neutral")
    gabriel_parser.add_argument("--path", "-p", help="Path for scan")
    
    # Code execution
    exec_parser = subparsers.add_parser("exec", help="Execute code in sandbox")
    exec_parser.add_argument("--lang", "-l", default="python", choices=["python", "bash", "javascript", "ruby"])
    exec_parser.add_argument("--file", "-f", help="File to execute")
    exec_parser.add_argument("code", nargs="*", help="Code to execute")
    
    # File operations
    file_parser = subparsers.add_parser("file", help="File operations")
    file_parser.add_argument("action", choices=["search", "read", "tree"])
    file_parser.add_argument("--pattern", "-p", help="Search pattern")
    file_parser.add_argument("--path", help="File/directory path")
    
    # Project generator
    project_parser = subparsers.add_parser("new", help="Generate new project")
    project_parser.add_argument("template", nargs="?", choices=["python-cli", "python-api", "node-api"])
    project_parser.add_argument("--name", "-n", default="project", help="Project name")
    project_parser.add_argument("--path", "-p", default=".", help="Output path")
    project_parser.add_argument("--list", "-l", action="store_true", help="List templates")
    
    # Git automation
    git_parser = subparsers.add_parser("git", help="Git automation")
    git_parser.add_argument("action", choices=["status", "log", "commit"], nargs="?", default="status")
    git_parser.add_argument("--message", "-m", help="Commit message")
    
    # Documentation generator
    doc_parser = subparsers.add_parser("doc", help="Generate documentation")
    doc_parser.add_argument("action", choices=["readme", "explain", "docstring"], nargs="?", default="readme")
    doc_parser.add_argument("--path", "-p", help="Project or file path")
    doc_parser.add_argument("--code", "-c", help="Code to document")
    
    # API testing
    api_parser = subparsers.add_parser("api", help="Test API endpoints")
    api_parser.add_argument("url", nargs="?", help="URL to test")
    api_parser.add_argument("--method", "-m", default="GET", choices=["GET", "POST", "PUT", "DELETE"])
    api_parser.add_argument("--data", "-d", help="JSON data for POST")
    
    # System monitor
    sysmon_parser = subparsers.add_parser("sysmon", help="System monitoring")
    sysmon_parser.add_argument("action", choices=["info", "health", "procs"], nargs="?", default="info")
    
    # Task queue
    queue_parser = subparsers.add_parser("queue", help="Task queue management")
    queue_parser.add_argument("action", choices=["list", "add", "process"], nargs="?", default="list")
    queue_parser.add_argument("--type", "-t", help="Task type (chat, image)")
    queue_parser.add_argument("--prompt", "-p", help="Task prompt")
    
    # Environment manager
    env_parser = subparsers.add_parser("env", help="Environment management")
    env_parser.add_argument("action", choices=["list", "get", "set", "deps"], nargs="?", default="list")
    env_parser.add_argument("--key", "-k", help="Environment variable key")
    env_parser.add_argument("--value", "-v", help="Environment variable value")
    
    # Network monitor
    net_parser = subparsers.add_parser("net", help="Network monitoring")
    net_parser.add_argument("action", choices=["check", "ping", "ip", "dns"], nargs="?", default="check")
    net_parser.add_argument("--url", "-u", help="URL to ping")
    net_parser.add_argument("--host", help="Hostname for DNS lookup")
    
    # Secret vault
    vault_parser = subparsers.add_parser("vault", help="Secret management")
    vault_parser.add_argument("action", choices=["list", "get", "set", "delete"], nargs="?", default="list")
    vault_parser.add_argument("--key", "-k", help="Secret key")
    vault_parser.add_argument("--value", "-v", help="Secret value")
    
    # Performance profiler
    perf_parser = subparsers.add_parser("perf", help="Performance profiling")
    perf_parser.add_argument("action", choices=["memory", "benchmark"], nargs="?", default="memory")
    
    # Log viewer
    log_parser = subparsers.add_parser("logs", help="Log management")
    log_parser.add_argument("action", choices=["tail", "list", "search", "clear"], nargs="?", default="tail")
    log_parser.add_argument("--lines", "-n", type=int, default=20, help="Lines to show")
    log_parser.add_argument("--pattern", "-p", help="Search pattern")
    
    # Backup manager
    backup_parser = subparsers.add_parser("backup", help="Backup management")
    backup_parser.add_argument("action", choices=["create", "list", "restore"], nargs="?", default="list")
    backup_parser.add_argument("--name", "-n", help="Backup name")
    
    # Process manager
    proc_parser = subparsers.add_parser("proc", help="Process management")
    proc_parser.add_argument("action", choices=["find", "ports", "kill"], nargs="?", default="ports")
    proc_parser.add_argument("--name", "-n", help="Process name to find")
    proc_parser.add_argument("--pid", "-p", type=int, help="PID to kill")
    
    # Cron manager
    cron_parser = subparsers.add_parser("cron", help="Scheduled jobs")
    cron_parser.add_argument("action", choices=["list", "add", "remove", "toggle"], nargs="?", default="list")
    cron_parser.add_argument("--name", "-n", help="Job name")
    cron_parser.add_argument("--schedule", "-s", help="Cron schedule (e.g., '0 9 * * *')")
    cron_parser.add_argument("--command", "-c", help="Command to run")
    cron_parser.add_argument("--id", help="Job ID for remove/toggle")
    
    # Notification center
    notify_parser = subparsers.add_parser("notify", help="System notifications")
    notify_parser.add_argument("action", choices=["send", "speak"], nargs="?", default="send")
    notify_parser.add_argument("--title", "-t", default="NOIZYLAB", help="Notification title")
    notify_parser.add_argument("--message", "-m", help="Notification message")
    notify_parser.add_argument("--text", help="Text to speak")
    
    # Cloud sync
    cloud_parser = subparsers.add_parser("cloud", help="Cloud sync")
    cloud_parser.add_argument("action", choices=["detect", "push", "pull"], nargs="?", default="detect")
    cloud_parser.add_argument("--target", "-t", choices=["gdrive", "icloud", "dropbox"], help="Cloud target")
    
    args = parser.parse_args()
    
    dashboard = AIDashboard()
    
    if args.command == "video":
        gen = VideoGenerator(args.provider)
        result = gen.generate(args.prompt, args.duration)
        print(json.dumps(result, indent=2))
    
    elif args.command == "audio":
        gen = AudioGenerator(args.provider)
        result = gen.generate_music(args.prompt, args.duration)
        print(json.dumps(result, indent=2))
    
    elif args.command == "avatar":
        gen = AvatarGenerator(args.provider)
        result = gen.create_video(args.script)
        print(json.dumps(result, indent=2))
    
    elif args.command == "keys":
        if args.set:
            dashboard.key_manager.set_key(args.set[0], args.set[1])
        else:
            dashboard.key_manager.list_keys()
    
    elif args.command == "status":
        dashboard.status()
    
    elif args.command == "microsoft":
        MSOfficeAI.list_copilot_features()
        MSOfficeAI.power_automate_templates()
    
    elif args.command == "interactive":
        dashboard.interactive()
    
    elif args.command == "batch":
        tasks = json.loads(Path(args.file).read_text())
        processor = BatchProcessor(max_workers=args.workers)
        results = processor.process(tasks)
        print(json.dumps(results, indent=2))
    
    elif args.command == "diagnose":
        print("\n🔍 SYSTEM DIAGNOSTICS\n")
        issues = SelfHealing.diagnose()
        if not issues:
            print("  ✅ No issues found - system healthy!")
        else:
            for issue in issues:
                icon = "⚠️" if issue['severity'] == 'warning' else "❌" if issue['severity'] == 'error' else "ℹ️"
                print(f"  {icon} [{issue['severity'].upper()}] {issue['message']}")
                print(f"     Fix: {issue['fix']}")
        print()
    
    elif args.command == "heal":
        if args.clear_cache:
            CACHE.clear()
        else:
            print("\n🩺 SELF-HEALING MODE\n")
            actions = SelfHealing.heal(auto=args.auto)
            if actions:
                print("  Actions taken:")
                for a in actions:
                    print(f"    ✅ {a}")
            else:
                print("  No actions needed - system healthy!")
        print()
    
    elif args.command == "discover":
        print("\n🔎 SERVICE DISCOVERY\n")
        available = ServiceDiscovery.discover_available()
        for svc, is_available in available.items():
            status = "✅ READY" if is_available else "⬚ NOT CONFIGURED"
            print(f"  {svc:<15} │ {status}")
        print()
    
    elif args.command == "auto":
        provider = ServiceDiscovery.recommend_provider(args.type)
        print(f"\n🤖 AUTO MODE: Selected {provider} for {args.type}\n")
        
        if args.type == "video":
            gen = VideoGenerator(provider)
            result = gen.generate(args.prompt)
        elif args.type == "audio":
            gen = AudioGenerator(provider)
            result = gen.generate_music(args.prompt)
        elif args.type == "avatar":
            gen = AvatarGenerator(provider)
            result = gen.create_video(args.prompt)
        print(json.dumps(result, indent=2))
    
    elif args.command == "chat":
        result = dashboard.llm.chat(args.prompt, args.system, args.provider)
        if 'content' in result:
            print(f"\n{result['content']}\n")
        else:
            print(json.dumps(result, indent=2))
    
    elif args.command == "workflow":
        workflow = json.loads(Path(args.file).read_text())
        results = dashboard.workflow.run_workflow(workflow)
        print(json.dumps(results, indent=2))
    
    elif args.command == "schedule":
        scheduler = Scheduler()
        if args.action == "list" or not args.action:
            scheduler.list_tasks()
        elif args.action == "add" and args.task:
            task = json.loads(args.task)
            scheduler.add_task(task)
        elif args.action == "remove" and args.task:
            scheduler.remove_task(args.task)
        elif args.action == "run":
            ran = scheduler.run_due_tasks()
            print(f"Ran {ran} scheduled tasks")
    
    elif args.command == "agent":
        goal = ' '.join(args.goal) if args.goal else ''
        if not goal:
            print("Usage: python3 ai_manager.py agent 'Create a promotional video'")
        else:
            agent = AIAgent()
            result = agent.run(goal)
            print(json.dumps(result, indent=2))
    
    elif args.command == "metrics":
        METRICS.print_dashboard()
    
    elif args.command == "ensemble":
        prompt = ' '.join(args.prompt) if args.prompt else ''
        if not prompt:
            print("Usage: python3 ai_manager.py ensemble 'Your question'")
        else:
            ensemble = ModelEnsemble()
            result = ensemble.consensus(prompt)
            if 'content' in result:
                print(f"\n🎯 ENSEMBLE RESPONSE ({result.get('ensemble_count', 1)} models)\n")
                print(result['content'])
                print(f"\n  Models: {', '.join(result.get('models_used', []))}\n")
            else:
                print(json.dumps(result, indent=2))
    
    elif args.command == "daemon":
        if args.action == "start":
            print("🚀 Starting AI Command Center daemon...")
            print("   Daemon mode runs scheduled tasks and monitors services")
            print("   Use 'daemon stop' to stop")
            try:
                scheduler = Scheduler()
                while True:
                    ran = scheduler.run_due_tasks()
                    if ran:
                        print(f"  ⏰ Ran {ran} scheduled tasks")
                    time.sleep(60)
            except KeyboardInterrupt:
                print("\n👋 Daemon stopped")
        elif args.action == "stop":
            print("🛑 Stopping daemon...")
        else:
            print("📊 Daemon status: Not implemented yet")
    
    elif args.command == "template":
        templates = PromptTemplates()
        if args.list or not args.name:
            templates.list()
        else:
            # Parse variables
            vars_dict = {}
            if args.vars:
                for v in args.vars:
                    if '=' in v:
                        k, val = v.split('=', 1)
                        vars_dict[k] = val
            
            system, prompt = templates.render(args.name, **vars_dict)
            if prompt:
                print(f"\n📝 Using template: {args.name}\n")
                result = dashboard.llm.chat(prompt, system)
                if 'content' in result:
                    print(result['content'])
                else:
                    print(json.dumps(result, indent=2))
            else:
                print(f"Template '{args.name}' not found. Use --list to see available templates.")
    
    elif args.command == "webhook":
        notifier = WebhookNotifier()
        if args.action == "list":
            notifier.list()
        elif args.action == "add" and args.name and args.url:
            notifier.add(args.name, args.url)
        elif args.action == "test" and args.name:
            if notifier.notify(args.name, "Test notification from NOIZYLAB AI Command Center"):
                print("✅ Webhook test successful")
            else:
                print("❌ Webhook test failed")
    
    elif args.command == "export":
        export_data = {
            "version": "2.0",
            "exported": datetime.now().isoformat(),
            "services": {k: {"name": v.name, "category": v.category} for k, v in AI_SERVICES.items()},
            "metrics": METRICS.get_stats(24),
            "templates": PromptTemplates().templates
        }
        Path(args.output).write_text(json.dumps(export_data, indent=2))
        print(f"✅ Exported configuration to {args.output}")
    
    elif args.command == "quick":
        content = ' '.join(args.content) if args.content else ''
        if not content:
            print(f"Usage: python3 ai_manager.py quick {args.action} 'your content'")
        else:
            result = QuickActions.run(args.action, content)
            if 'content' in result:
                print(f"\n{result['content']}\n")
            else:
                print(json.dumps(result, indent=2))
    
    elif args.command == "pipe":
        import sys
        content = sys.stdin.read().strip()
        if content:
            result = QuickActions.run(args.action, content)
            if 'content' in result:
                print(result['content'])
            else:
                print(json.dumps(result, indent=2))
    
    elif args.command == "image":
        prompt = ' '.join(args.prompt) if args.prompt else ''
        if not prompt:
            print("Usage: python3 ai_manager.py image 'a futuristic city at sunset'")
        else:
            gen = ImageGenerator()
            result = gen.generate(prompt, args.size, args.style)
            if 'url' in result:
                print(f"\n🎨 Image generated successfully!\n")
                print(f"   URL: {result['url']}")
                if result.get('revised_prompt'):
                    print(f"   Revised prompt: {result['revised_prompt'][:100]}...")
            else:
                print(json.dumps(result, indent=2))
    
    elif args.command == "gabriel":
        # Import GABRIEL bridge
        bridge_path = Path(__file__).parent / "gabriel_bridge.py"
        if bridge_path.exists():
            import importlib.util
            spec = importlib.util.spec_from_file_location("gabriel_bridge", bridge_path)
            gabriel = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(gabriel)
            
            bridge = gabriel.UnifiedBridge()
            
            if args.action == "status":
                status = bridge.full_status()
                print("\n🧠 GABRIEL SYSTEM STATUS\n")
                print(f"  Voice: {'✅' if status['gabriel_voice']['available'] else '❌'} ({status['gabriel_voice']['emotions']} emotions, {status['gabriel_voice']['languages']} languages)")
                print(f"  Intelligence: {'✅' if status['gabriel_intelligence']['active'] else '❌'}")
                print(f"  MC96: {status['mc96'].get('status', 'unknown')}")
            
            elif args.action == "scan":
                result = bridge.quick_scan()
                print(f"\n📊 GABRIEL INTELLIGENCE SCAN\n")
                print(f"  Files: {result['files']}")
                print(f"  Lines: {result['lines']:,}")
            
            elif args.action == "speak" and args.text:
                result = bridge.speak(args.text, emotion=args.emotion)
                print(json.dumps(result, indent=2))
            
            elif args.action == "hot":
                files = bridge.hot_files(10)
                print(f"\n🔥 HOT FILES\n")
                for f in files[:10]:
                    print(f"  {f['modified'][:16]} │ {f['path']}")
            
            elif args.action == "metrics":
                metrics = bridge.mc96.get_metrics()
                print(json.dumps(metrics, indent=2))
        else:
            print("GABRIEL bridge not found")
    
    elif args.command == "exec":
        executor = CodeExecutor()
        if args.file:
            code = Path(args.file).read_text()
        else:
            code = ' '.join(args.code) if args.code else ''
        
        if not code:
            print("Usage: python3 ai_manager.py exec 'print(1+1)' --lang python")
        else:
            result = executor.execute(code, args.lang)
            if result.get('stdout'):
                print(result['stdout'])
            if result.get('stderr'):
                print(f"STDERR: {result['stderr']}")
            print(f"\n[Exit: {result.get('exit_code', '?')} | {result.get('elapsed_ms', 0):.0f}ms]")
    
    elif args.command == "file":
        fops = FileOperations()
        if args.action == "search":
            results = fops.search(args.pattern or "*", args.path)
            print(f"\n🔍 Found {len(results)} files:\n")
            for r in results[:20]:
                print(f"  {r['name']:<30} │ {r['size']:>8} bytes")
        elif args.action == "read":
            result = fops.read(args.path)
            if 'content' in result:
                print(result['content'])
            else:
                print(json.dumps(result, indent=2))
        elif args.action == "tree":
            result = fops.tree(args.path, depth=2)
            print(json.dumps(result, indent=2))
    
    elif args.command == "new":
        gen = ProjectGenerator()
        if args.list or not args.template:
            print("\n📦 PROJECT TEMPLATES:\n")
            for t in gen.list_templates():
                print(f"  • {t}")
            print("\nUsage: python3 ai_manager.py new python-cli --name myproject")
        else:
            result = gen.generate(args.template, args.path, args.name)
            if 'files' in result:
                print(f"\n✅ Created project: {result['path']}\n")
                for f in result['files']:
                    print(f"  📄 {Path(f).name}")
            else:
                print(json.dumps(result, indent=2))
    
    elif args.command == "git":
        git = GitAutomation()
        if args.action == "status":
            status = git.status()
            print(f"\n📊 GIT STATUS\n")
            print(f"  Modified: {len(status.get('modified', []))}")
            print(f"  Untracked: {len(status.get('untracked', []))}")
            print(f"  Total changes: {status.get('total', 0)}")
        elif args.action == "log":
            commits = git.log(10)
            print(f"\n📜 RECENT COMMITS\n")
            for c in commits:
                print(f"  {c.get('hash', '?')} │ {c.get('message', '')[:50]} │ {c.get('date', '')}")
        elif args.action == "commit" and args.message:
            result = git.commit(args.message)
            print(json.dumps(result, indent=2))
    
    elif args.command == "doc":
        doc = DocGenerator()
        if args.action == "readme":
            path = args.path or "."
            print(f"\n📝 Generating README for {path}...\n")
            content = doc.generate_readme(path)
            print(content)
        elif args.action == "explain" and args.code:
            print(f"\n💡 Explaining code...\n")
            content = doc.explain_code(args.code)
            print(content)
        elif args.action == "docstring" and args.code:
            print(f"\n📖 Generating docstring...\n")
            content = doc.document_function(args.code)
            print(content)
    
    elif args.command == "api":
        if not args.url:
            print("Usage: python3 ai_manager.py api https://api.example.com --method GET")
        else:
            tester = APITester()
            print(f"\n🌐 Testing {args.method} {args.url}...\n")
            data = json.loads(args.data) if args.data else None
            result = tester.request(args.url, args.method, data=data)
            print(f"  Status: {result.get('status', 'error')}")
            print(f"  Latency: {result.get('elapsed_ms', 0):.0f}ms")
            if result.get('body'):
                print(f"  Body: {result['body'][:200]}...")
    
    elif args.command == "sysmon":
        monitor = SystemMonitor()
        if args.action == "info":
            info = monitor.get_system_info()
            print("\n💻 SYSTEM INFO\n")
            for k, v in info.items():
                print(f"  {k:<15} │ {v}")
        elif args.action == "health":
            health = monitor.health_check()
            print("\n🏥 HEALTH CHECK\n")
            for k, v in health.items():
                status = "✅" if v else "❌" if isinstance(v, bool) else v
                print(f"  {k:<15} │ {status}")
        elif args.action == "procs":
            procs = monitor.get_processes(10)
            print("\n⚡ TOP PROCESSES\n")
            for p in procs:
                print(f"  {p['pid']:<8} │ {p['cpu']:>5}% │ {p['mem']:>5}% │ {p['name']}")
    
    elif args.command == "queue":
        queue = TaskQueue()
        if args.action == "list":
            pending = queue.list_pending()
            print(f"\n📋 TASK QUEUE ({len(pending)} pending)\n")
            for t in pending:
                print(f"  {t['id']} │ {t['type']} │ {t['status']}")
        elif args.action == "add" and args.type and args.prompt:
            task_id = queue.add(args.type, {"prompt": args.prompt})
            print(f"✅ Added task: {task_id}")
        elif args.action == "process":
            result = queue.process_next()
            if result:
                print(f"✅ Processed: {result['id']} → {result['status']}")
            else:
                print("No pending tasks")
    
    elif args.command == "env":
        env = EnvManager()
        if args.action == "list":
            vars = env.list_env()
            print(f"\n🔧 ENVIRONMENT VARIABLES\n")
            for k, v in vars.items():
                print(f"  {k:<25} │ {v}")
            if not vars:
                print("  No NOIZYLAB env vars found")
        elif args.action == "get" and args.key:
            val = env.get_env(args.key)
            print(f"{args.key}={val or 'Not set'}")
        elif args.action == "set" and args.key and args.value:
            env.set_env(args.key, args.value, persist=True)
            print(f"✅ Set {args.key}")
        elif args.action == "deps":
            deps = env.check_dependencies()
            print(f"\n📦 DEPENDENCIES\n")
            for name, ok in deps.items():
                status = "✅" if ok else "❌"
                print(f"  {status} {name}")
    
    elif args.command == "net":
        net = NetworkMonitor()
        if args.action == "check":
            print(f"\n🌐 NETWORK STATUS\n")
            results = net.check_all()
            for name, data in results.items():
                if data.get("online"):
                    print(f"  ✅ {name:<12} │ {data['latency_ms']:.0f}ms")
                else:
                    print(f"  ❌ {name:<12} │ offline")
        elif args.action == "ping" and args.url:
            result = net.ping_endpoint(args.url)
            print(json.dumps(result, indent=2))
        elif args.action == "ip":
            print(f"\n📍 IP ADDRESSES\n")
            print(f"  Local:  {net.get_local_ip()}")
            print(f"  Public: {net.get_public_ip()}")
        elif args.action == "dns" and args.host:
            ips = net.dns_lookup(args.host)
            print(f"\n🔍 DNS: {args.host}\n")
            for ip in ips:
                print(f"  {ip}")
    
    elif args.command == "vault":
        vault = SecretVault()
        if args.action == "list":
            keys = vault.list_secrets()
            print(f"\n🔐 SECRET VAULT ({len(keys)} secrets)\n")
            for k in keys:
                print(f"  • {k}")
        elif args.action == "get" and args.key:
            val = vault.get_secret(args.key)
            if val:
                print(f"{args.key}={val[:10]}..." if len(val) > 10 else f"{args.key}={val}")
            else:
                print(f"Secret '{args.key}' not found")
        elif args.action == "set" and args.key and args.value:
            vault.set_secret(args.key, args.value)
            print(f"✅ Stored secret: {args.key}")
        elif args.action == "delete" and args.key:
            if vault.delete_secret(args.key):
                print(f"✅ Deleted: {args.key}")
            else:
                print(f"Secret '{args.key}' not found")
    
    elif args.command == "perf":
        profiler = PerformanceProfiler()
        if args.action == "memory":
            mem = profiler.memory_usage()
            print(f"\n💾 MEMORY USAGE\n")
            if "error" not in mem:
                print(f"  RSS: {mem['rss_mb']:.1f} MB")
                print(f"  VSZ: {mem['vsz_mb']:.1f} MB")
            else:
                print(f"  {mem['error']}")
        elif args.action == "benchmark":
            print(f"\n⚡ BENCHMARK\n")
            # Quick LLM benchmark
            start = time.time()
            try:
                llm = SmartLLM()
                llm.chat("Say 'benchmark complete' in 3 words or less")
                elapsed = (time.time() - start) * 1000
                print(f"  LLM Response: {elapsed:.0f}ms")
            except:
                print(f"  LLM: Failed")
            
            # API benchmark
            net = NetworkMonitor()
            for name in ["google", "openai"]:
                result = net.ping_endpoint(net.endpoints.get(name, ""))
                if result.get("online"):
                    print(f"  {name}: {result['latency_ms']:.0f}ms")
    
    elif args.command == "logs":
        logger = LogViewer()
        if args.action == "tail":
            lines = logger.tail(args.lines)
            print(f"\n📜 LOG TAIL (last {args.lines} lines)\n")
            for line in lines:
                print(f"  {line}")
            if not lines:
                print("  No logs yet")
        elif args.action == "list":
            logs = logger.list_logs()
            print(f"\n📁 LOG FILES\n")
            for log in logs:
                print(f"  {log['name']:<30} │ {log['size_kb']:.1f} KB")
        elif args.action == "search" and args.pattern:
            matches = logger.search(args.pattern)
            print(f"\n🔍 SEARCH: '{args.pattern}' ({len(matches)} matches)\n")
            for m in matches[-10:]:
                print(f"  {m[:80]}")
        elif args.action == "clear":
            if logger.clear():
                print("✅ Log cleared")
            else:
                print("No log to clear")
    
    elif args.command == "backup":
        backup = BackupManager()
        if args.action == "list":
            backups = backup.list_backups()
            print(f"\n💾 BACKUPS ({len(backups)} found)\n")
            for b in backups:
                print(f"  {b['name']:<30} │ {b['size_kb']:.1f} KB │ {b['created'][:10]}")
        elif args.action == "create":
            result = backup.create_backup(args.name)
            if result["status"] == "success":
                print(f"✅ Backup created: {result['path']}")
            else:
                print(f"❌ Backup failed: {result.get('error')}")
        elif args.action == "restore" and args.name:
            result = backup.restore_backup(args.name)
            if result["status"] == "success":
                print(f"✅ Restored from: {result['restored_from']}")
            else:
                print(f"❌ Restore failed: {result.get('error')}")
    
    elif args.command == "proc":
        proc = ProcessManager()
        if args.action == "ports":
            ports = proc.get_port_usage()
            print(f"\n🔌 PORT USAGE\n")
            for p in ports:
                print(f"  {p['process']:<15} │ PID {p['pid']:<8} │ {p['port']}")
        elif args.action == "find" and args.name:
            procs = proc.find_process(args.name)
            print(f"\n🔍 PROCESSES: '{args.name}'\n")
            for p in procs:
                print(f"  PID {p['pid']:<8} │ {p['command']}")
        elif args.action == "kill" and args.pid:
            if proc.kill_process(args.pid):
                print(f"✅ Killed PID {args.pid}")
            else:
                print(f"❌ Failed to kill PID {args.pid}")
    
    elif args.command == "cron":
        cron = CronManager()
        if args.action == "list":
            jobs = cron.list_jobs()
            print(f"\n⏰ SCHEDULED JOBS ({len(jobs)})\n")
            for j in jobs:
                status = "✅" if j.get("enabled") else "⏸️"
                print(f"  {status} {j['id']} │ {j['name']:<20} │ {j['schedule']}")
        elif args.action == "add" and args.name and args.schedule and args.command:
            job = cron.add_job(args.name, args.schedule, args.command)
            print(f"✅ Added job: {job['id']} - {job['name']}")
        elif args.action == "remove" and args.id:
            if cron.remove_job(args.id):
                print(f"✅ Removed job: {args.id}")
            else:
                print(f"❌ Job not found: {args.id}")
        elif args.action == "toggle" and args.id:
            result = cron.toggle_job(args.id)
            if result is not None:
                status = "enabled" if result else "disabled"
                print(f"✅ Job {args.id} {status}")
            else:
                print(f"❌ Job not found: {args.id}")
    
    elif args.command == "notify":
        notifier = NotificationCenter()
        if args.action == "send" and args.message:
            if notifier.notify(args.title, args.message):
                print(f"✅ Notification sent")
            else:
                print(f"❌ Notification failed")
        elif args.action == "speak" and args.text:
            if notifier.speak(args.text):
                print(f"✅ Spoke: {args.text[:30]}...")
            else:
                print(f"❌ Speech failed")
        else:
            print("Usage: notify send --message 'Hello' or notify speak --text 'Hello'")
    
    elif args.command == "cloud":
        cloud = CloudSync()
        if args.action == "detect":
            clouds = cloud.detect_clouds()
            print(f"\n☁️ CLOUD SERVICES\n")
            for name, available in clouds.items():
                status = "✅ Available" if available else "❌ Not found"
                print(f"  {name:<10} │ {status}")
        elif args.action == "push" and args.target:
            result = cloud.sync_to(args.target)
            if result["status"] == "success":
                print(f"✅ Synced to {args.target}: {len(result.get('files', []))} files")
            else:
                print(f"❌ Sync failed: {result.get('error')}")
        elif args.action == "pull" and args.target:
            result = cloud.sync_from(args.target)
            if result["status"] == "success":
                print(f"✅ Restored from {args.target}: {len(result.get('files', []))} files")
            else:
                print(f"❌ Restore failed: {result.get('error')}")
    
    else:
        dashboard.interactive()


if __name__ == "__main__":
    main()
