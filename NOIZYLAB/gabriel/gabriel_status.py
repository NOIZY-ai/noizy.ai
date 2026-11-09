#!/usr/bin/env python3
"""
GABRIEL STATUS DASHBOARD
Complete system status at a glance
"""

import os
import sys
import json
import time
import socket
import subprocess
from pathlib import Path
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

GABRIEL_ROOT = Path.home() / "NOIZYLAB" / "GABRIEL"


def get_system_info() -> dict:
    """Get system information"""
    return {
        "hostname": socket.gethostname(),
        "user": os.environ.get("USER", "unknown"),
        "cpu_cores": os.cpu_count(),
        "platform": sys.platform,
        "python": sys.version.split()[0],
        "gabriel_root": str(GABRIEL_ROOT),
    }


def get_network_info() -> dict:
    """Get network status"""
    info = {"internet": False, "local_ip": None, "tailscale": False}

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        info["local_ip"] = s.getsockname()[0]
        s.close()
        info["internet"] = True
    except:
        pass

    # Check Tailscale
    try:
        result = subprocess.run(["tailscale", "status"], capture_output=True, timeout=5)
        info["tailscale"] = result.returncode == 0
    except:
        pass

    return info


def get_volume_info() -> dict:
    """Get mounted volumes"""
    volumes = []
    total_space = 0
    used_space = 0

    try:
        result = subprocess.run(["df", "-h"], capture_output=True, text=True, timeout=10)
        for line in result.stdout.strip().split('\n')[1:]:
            parts = line.split()
            if len(parts) >= 6 and parts[0].startswith('/dev'):
                mount = parts[-1]
                size = parts[1]
                used = parts[2]
                avail = parts[3]
                pct = parts[4]
                volumes.append({
                    "mount": mount,
                    "size": size,
                    "used": used,
                    "available": avail,
                    "percent": pct
                })
    except:
        pass

    return {"volumes": volumes, "count": len(volumes)}


def get_ai_status() -> dict:
    """Check AI provider status"""
    providers = {
        "claude": "ANTHROPIC_API_KEY",
        "openai": "OPENAI_API_KEY",
        "gemini": "GEMINI_API_KEY",
        "groq": "GROQ_API_KEY",
        "deepseek": "DEEPSEEK_API_KEY",
        "mistral": "MISTRAL_API_KEY",
        "cohere": "COHERE_API_KEY",
        "perplexity": "PERPLEXITY_API_KEY",
        "xai": "XAI_API_KEY",
        "together": "TOGETHER_API_KEY",
    }

    status = {}
    for name, env_key in providers.items():
        key = os.environ.get(env_key)
        status[name] = {
            "configured": bool(key),
            "key_preview": f"{key[:8]}...{key[-4:]}" if key and len(key) > 12 else "NOT SET"
        }

    return status


def get_gabriel_files() -> dict:
    """Get GABRIEL codebase stats"""
    stats = {"total_files": 0, "by_type": {}, "key_files": []}

    try:
        # Count files by extension
        for ext in ['.py', '.js', '.ts', '.sh', '.json', '.md']:
            count = len(list(GABRIEL_ROOT.rglob(f"*{ext}")))
            stats["by_type"][ext] = count
            stats["total_files"] += count

        # List key Python files
        key_files = list(GABRIEL_ROOT.glob("*.py"))
        stats["key_files"] = [f.name for f in key_files[:15]]
    except:
        pass

    return stats


def get_github_status() -> dict:
    """Check GitHub status"""
    status = {"logged_in": False, "user": None, "copilot": False}

    try:
        result = subprocess.run(["gh", "auth", "status"], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            status["logged_in"] = True
            for line in result.stdout.split('\n'):
                if 'account' in line.lower():
                    parts = line.split()
                    for i, p in enumerate(parts):
                        if 'account' in p.lower() and i + 1 < len(parts):
                            status["user"] = parts[i + 1].strip('()')
    except:
        pass

    try:
        result = subprocess.run(["gh", "copilot", "--version"], capture_output=True, timeout=5)
        status["copilot"] = result.returncode == 0
    except:
        pass

    return status


def print_status():
    """Print full status dashboard"""
    start = time.perf_counter()

    # Gather all info in parallel
    with ThreadPoolExecutor(max_workers=6) as executor:
        futures = {
            executor.submit(get_system_info): "system",
            executor.submit(get_network_info): "network",
            executor.submit(get_volume_info): "volumes",
            executor.submit(get_ai_status): "ai",
            executor.submit(get_gabriel_files): "files",
            executor.submit(get_github_status): "github",
        }

        data = {}
        for future in as_completed(futures):
            name = futures[future]
            try:
                data[name] = future.result()
            except Exception as e:
                data[name] = {"error": str(e)}

    elapsed = int((time.perf_counter() - start) * 1000)

    # Print dashboard
    print(f"""
================================================================================
                         GABRIEL SYSTEM STATUS
                         {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
================================================================================

SYSTEM
------
  Hostname:     {data['system'].get('hostname', 'unknown')}
  User:         {data['system'].get('user', 'unknown')}
  CPU Cores:    {data['system'].get('cpu_cores', '?')}
  Python:       {data['system'].get('python', '?')}

NETWORK
-------
  Internet:     {'ONLINE' if data['network'].get('internet') else 'OFFLINE'}
  Local IP:     {data['network'].get('local_ip', 'unknown')}
  Tailscale:    {'ACTIVE' if data['network'].get('tailscale') else 'NOT RUNNING'}

STORAGE ({data['volumes'].get('count', 0)} volumes)
-------""")

    for v in data['volumes'].get('volumes', [])[:10]:
        print(f"  {v['mount'][:35]:<35} {v['size']:>8} ({v['percent']})")

    print(f"""
AI PROVIDERS
------------""")

    for name, info in data['ai'].items():
        status = "READY" if info['configured'] else "NOT SET"
        print(f"  {name:<12} {status}")

    print(f"""
GITHUB
------
  Logged in:    {'YES (' + data['github'].get('user', '?') + ')' if data['github'].get('logged_in') else 'NO'}
  Copilot:      {'ACTIVE' if data['github'].get('copilot') else 'NOT INSTALLED'}

GABRIEL CODEBASE
----------------
  Total Files:  {data['files'].get('total_files', 0):,}
  Python:       {data['files'].get('by_type', {}).get('.py', 0):,}
  JavaScript:   {data['files'].get('by_type', {}).get('.js', 0):,}
  TypeScript:   {data['files'].get('by_type', {}).get('.ts', 0):,}
  Shell:        {data['files'].get('by_type', {}).get('.sh', 0):,}

================================================================================
  Status gathered in {elapsed}ms
================================================================================
""")

    return data


def main():
    """Main entry point"""
    if len(sys.argv) > 1 and sys.argv[1] == "--json":
        # Output as JSON
        data = {}
        data["system"] = get_system_info()
        data["network"] = get_network_info()
        data["volumes"] = get_volume_info()
        data["ai"] = get_ai_status()
        data["files"] = get_gabriel_files()
        data["github"] = get_github_status()
        data["timestamp"] = datetime.now().isoformat()
        print(json.dumps(data, indent=2))
    else:
        print_status()

    return 0


if __name__ == "__main__":
    sys.exit(main())
