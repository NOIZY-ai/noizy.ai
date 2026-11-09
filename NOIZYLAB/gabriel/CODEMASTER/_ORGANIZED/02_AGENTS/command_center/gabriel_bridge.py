#!/usr/bin/env python3
"""
🧠 GABRIEL BRIDGE - Unified Intelligence Connector
Connects AI Command Center with GABRIEL's voice, intelligence, and MC96 systems
"""

import os
import sys
import json
import subprocess
import time
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
from concurrent.futures import ThreadPoolExecutor

# Path constants
GABRIEL_ROOT = Path("/Users/m2ultra/NOIZYLAB/GABRIEL")
MC96_ROOT = Path("/Users/m2ultra/NOIZYLAB/MC96")
NOIZYLAB_ROOT = Path("/Users/m2ultra/NOIZYLAB")


class GabrielVoice:
    """Interface to GABRIEL's voice synthesis system"""
    
    EMOTIONS = [
        "neutral", "joy", "anger", "surprised", "fear", 
        "sadness", "disgust", "trust", "anticipation",
        "whisper", "god", "8bit", "phone"
    ]
    
    LANGUAGES = ["en", "fr", "es", "it", "ja", "zh", "zh-hk", "zh-tw"]
    
    def __init__(self):
        self.voice_server = GABRIEL_ROOT / "gabriel_voice.py"
        self.cache_dir = Path("/tmp/almeida")
        self.cache_dir.mkdir(exist_ok=True)
    
    def speak(self, text: str, emotion: str = "neutral", 
              lang: str = "en", output_file: str = None) -> dict:
        """Generate speech with emotion and language support"""
        print(f"🎤 GABRIEL Voice: {emotion} ({lang})")
        
        # Use edge-tts for synthesis
        try:
            voice_id = self._get_voice_id(lang)
            output = output_file or f"/tmp/gabriel_speech_{int(time.time())}.mp3"
            
            cmd = [
                "edge-tts",
                "--voice", voice_id,
                "--text", text,
                "--write-media", output
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                return {
                    "status": "success",
                    "file": output,
                    "emotion": emotion,
                    "language": lang
                }
            else:
                return {"error": result.stderr}
        except Exception as e:
            return {"error": str(e)}
    
    def _get_voice_id(self, lang: str) -> str:
        voices = {
            "en": "en-GB-RyanNeural",
            "fr": "fr-FR-RemyMultilingualNeural",
            "es": "es-ES-AlvaroNeural",
            "it": "it-IT-GiuseppeMultilingualNeural",
            "ja": "ja-JP-KeitaNeural",
            "zh": "zh-CN-YunjianNeural"
        }
        return voices.get(lang, "en-GB-RyanNeural")


class GabrielIntelligence:
    """Interface to GABRIEL's intelligence engine"""
    
    def __init__(self):
        self.watch_path = NOIZYLAB_ROOT
        self.stats_file = GABRIEL_ROOT / "intelligence_report.json"
    
    def scan(self, path: str = None) -> dict:
        """Scan codebase for intelligence"""
        target = Path(path) if path else self.watch_path
        
        print(f"🔍 GABRIEL Intelligence scanning: {target}")
        
        stats = {
            "timestamp": datetime.now().isoformat(),
            "path": str(target),
            "files": 0,
            "lines": 0,
            "languages": {}
        }
        
        lang_map = {
            ".py": "Python", ".js": "JavaScript", ".sh": "Shell",
            ".go": "Go", ".rs": "Rust", ".c": "C", ".cpp": "C++",
            ".html": "HTML", ".css": "CSS", ".md": "Markdown"
        }
        
        for ext, lang in lang_map.items():
            stats["languages"][lang] = {"files": 0, "lines": 0}
        
        for root, dirs, files in os.walk(target):
            # Skip hidden and venv directories
            dirs[:] = [d for d in dirs if not d.startswith('.') and 'venv' not in d]
            
            for file in files:
                filepath = Path(root) / file
                ext = filepath.suffix.lower()
                
                if ext in lang_map:
                    lang = lang_map[ext]
                    stats["files"] += 1
                    stats["languages"][lang]["files"] += 1
                    
                    try:
                        lines = sum(1 for _ in open(filepath, 'r', errors='ignore'))
                        stats["lines"] += lines
                        stats["languages"][lang]["lines"] += lines
                    except:
                        pass
        
        return stats
    
    def get_hot_files(self, limit: int = 10) -> List[dict]:
        """Get recently modified files"""
        hot_files = []
        
        for root, dirs, files in os.walk(self.watch_path):
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            
            for file in files:
                filepath = Path(root) / file
                try:
                    mtime = filepath.stat().st_mtime
                    hot_files.append({
                        "path": str(filepath.relative_to(self.watch_path)),
                        "modified": datetime.fromtimestamp(mtime).isoformat()
                    })
                except:
                    pass
        
        hot_files.sort(key=lambda x: x["modified"], reverse=True)
        return hot_files[:limit]


class MC96Controller:
    """Interface to MC96 Mission Control"""
    
    def __init__(self):
        self.server_url = "http://localhost:5174"
        self.portal_url = "http://localhost:5173"
    
    def status(self) -> dict:
        """Get MC96 system status"""
        try:
            import urllib.request
            req = urllib.request.Request(f"{self.server_url}/api/status")
            with urllib.request.urlopen(req, timeout=5) as resp:
                return json.loads(resp.read().decode())
        except Exception as e:
            return {"status": "offline", "error": str(e)}
    
    def start_server(self) -> bool:
        """Start MC96 server"""
        server_script = GABRIEL_ROOT / "mc96_server.py"
        if server_script.exists():
            subprocess.Popen([sys.executable, str(server_script)], 
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        return False
    
    def get_metrics(self) -> dict:
        """Get system metrics"""
        try:
            # CPU usage
            cpu = subprocess.run(["top", "-l", "1"], capture_output=True, text=True)
            cpu_line = [l for l in cpu.stdout.split('\n') if 'CPU usage' in l]
            cpu_usage = cpu_line[0] if cpu_line else "Unknown"
            
            # Memory
            mem = subprocess.run(["memory_pressure"], capture_output=True, text=True)
            mem_line = [l for l in mem.stdout.split('\n') if 'System-wide' in l]
            mem_usage = mem_line[0] if mem_line else "Unknown"
            
            return {
                "cpu": cpu_usage,
                "memory": mem_usage,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {"error": str(e)}


class UnifiedBridge:
    """Unified bridge connecting all GABRIEL systems"""
    
    def __init__(self):
        self.voice = GabrielVoice()
        self.intelligence = GabrielIntelligence()
        self.mc96 = MC96Controller()
    
    def full_status(self) -> dict:
        """Get status of all systems"""
        return {
            "timestamp": datetime.now().isoformat(),
            "gabriel_voice": {
                "available": self.voice.voice_server.exists(),
                "emotions": len(self.voice.EMOTIONS),
                "languages": len(self.voice.LANGUAGES)
            },
            "gabriel_intelligence": {
                "watch_path": str(self.intelligence.watch_path),
                "active": True
            },
            "mc96": self.mc96.status()
        }
    
    def quick_scan(self) -> dict:
        """Quick intelligence scan"""
        return self.intelligence.scan()
    
    def speak(self, text: str, **kwargs) -> dict:
        """Generate speech"""
        return self.voice.speak(text, **kwargs)
    
    def hot_files(self, limit: int = 10) -> List[dict]:
        """Get recently modified files"""
        return self.intelligence.get_hot_files(limit)


# CLI interface
def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="🧠 GABRIEL Bridge")
    subparsers = parser.add_subparsers(dest="command")
    
    # Status
    subparsers.add_parser("status", help="Full system status")
    
    # Scan
    scan_parser = subparsers.add_parser("scan", help="Intelligence scan")
    scan_parser.add_argument("--path", "-p", help="Path to scan")
    
    # Speak
    speak_parser = subparsers.add_parser("speak", help="Voice synthesis")
    speak_parser.add_argument("text", nargs="*", help="Text to speak")
    speak_parser.add_argument("--emotion", "-e", default="neutral")
    speak_parser.add_argument("--lang", "-l", default="en")
    
    # Hot files
    hot_parser = subparsers.add_parser("hot", help="Recently modified files")
    hot_parser.add_argument("--limit", "-n", type=int, default=10)
    
    # Metrics
    subparsers.add_parser("metrics", help="System metrics")
    
    args = parser.parse_args()
    bridge = UnifiedBridge()
    
    if args.command == "status":
        print(json.dumps(bridge.full_status(), indent=2))
    
    elif args.command == "scan":
        result = bridge.intelligence.scan(args.path)
        print(f"\n📊 GABRIEL INTELLIGENCE SCAN\n")
        print(f"  Files: {result['files']}")
        print(f"  Lines: {result['lines']:,}")
        print(f"\n  Languages:")
        for lang, stats in result['languages'].items():
            if stats['files'] > 0:
                print(f"    {lang:<12} │ {stats['files']} files │ {stats['lines']:,} lines")
    
    elif args.command == "speak":
        text = ' '.join(args.text) if args.text else "Hello, I am Gabriel"
        result = bridge.speak(text, emotion=args.emotion, lang=args.lang)
        print(json.dumps(result, indent=2))
    
    elif args.command == "hot":
        files = bridge.hot_files(args.limit)
        print(f"\n🔥 HOT FILES (Last {args.limit})\n")
        for f in files:
            print(f"  {f['modified'][:16]} │ {f['path']}")
    
    elif args.command == "metrics":
        metrics = bridge.mc96.get_metrics()
        print(json.dumps(metrics, indent=2))
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
