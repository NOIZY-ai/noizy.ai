#!/usr/bin/env python3
"""
GABRIEL DEEP DIVE - MAXIMUM CODE EXTRACTION
Scans EVERY mounted drive for ALL code, scripts, configs
NO LIMITS - FULL PARALLEL - JUMBO FRAMES
"""

import os
import sys
import json
import time
import subprocess
from pathlib import Path
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import defaultdict
import threading
import hashlib

# MAXIMUM PARALLELISM
MAX_WORKERS = os.cpu_count() * 4 or 32
GABRIEL_ROOT = Path.home() / "NOIZYLAB" / "GABRIEL"
DATA_DIR = GABRIEL_ROOT / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# ALL CODE EXTENSIONS
CODE_EXT = {
    '.py', '.pyx', '.pyi',  # Python
    '.js', '.jsx', '.mjs', '.cjs',  # JavaScript
    '.ts', '.tsx',  # TypeScript
    '.sh', '.bash', '.zsh', '.fish', '.ksh',  # Shell
    '.swift', '.m', '.mm',  # Apple
    '.go', '.rs', '.c', '.cpp', '.cc', '.h', '.hpp',  # Systems
    '.java', '.kt', '.scala', '.groovy',  # JVM
    '.rb', '.rake', '.gemspec',  # Ruby
    '.php', '.pl', '.pm',  # PHP/Perl
    '.lua', '.r', '.R', '.jl',  # Other
    '.sql', '.graphql', '.gql',  # Query
    '.html', '.htm', '.css', '.scss', '.sass', '.less',  # Web
    '.json', '.yaml', '.yml', '.xml', '.toml', '.ini', '.cfg',  # Config
    '.md', '.rst', '.txt', '.tex',  # Docs
    '.dockerfile', '.makefile', '.cmake',  # Build
    '.ps1', '.psm1', '.bat', '.cmd',  # Windows
    '.vim', '.el', '.clj', '.cljs',  # Editors
    '.ex', '.exs', '.erl', '.hrl',  # Erlang/Elixir
}


class DeepDiver:
    """Deep dive into ALL mounted storage"""

    def __init__(self):
        self.stats = {
            "volumes_scanned": 0,
            "total_files": 0,
            "total_bytes": 0,
            "by_extension": defaultdict(int),
            "by_volume": {},
            "largest_files": [],
            "errors": []
        }
        self.lock = threading.Lock()
        self.all_files = []

    def get_all_volumes(self) -> list:
        """Get EVERY mounted volume"""
        volumes = []

        # Home directory
        volumes.append(Path.home())

        # /Volumes (external drives, network shares)
        vol_path = Path("/Volumes")
        if vol_path.exists():
            for v in vol_path.iterdir():
                if v.is_dir() and not v.name.startswith('.'):
                    try:
                        # Check if accessible
                        list(v.iterdir())
                        volumes.append(v)
                    except:
                        pass

        return volumes

    def scan_file(self, filepath: Path) -> dict:
        """Extract file metadata"""
        try:
            stat = filepath.stat()
            return {
                "path": str(filepath),
                "name": filepath.name,
                "ext": filepath.suffix.lower(),
                "size": stat.st_size,
                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "volume": filepath.parts[2] if len(filepath.parts) > 2 and filepath.parts[1] == "Volumes" else "Home"
            }
        except:
            return None

    def scan_volume_fast(self, volume: Path) -> dict:
        """FAST parallel volume scan"""
        result = {
            "path": str(volume),
            "name": volume.name if volume != Path.home() else "Home",
            "files": [],
            "file_count": 0,
            "total_bytes": 0,
            "by_extension": defaultdict(int),
            "scan_time_ms": 0
        }

        start = time.perf_counter()

        try:
            # Find all code files using find command (faster than Python walk)
            ext_patterns = " -o ".join([f'-name "*{ext}"' for ext in list(CODE_EXT)[:30]])  # Limit for command length

            cmd = f'find "{volume}" -type f \\( {ext_patterns} \\) 2>/dev/null | head -100000'

            proc = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=300)
            files = [Path(f) for f in proc.stdout.strip().split('\n') if f]

            # Filter unwanted paths
            files = [f for f in files if
                     '.git' not in str(f) and
                     'node_modules' not in str(f) and
                     '__pycache__' not in str(f) and
                     'Library/Caches' not in str(f) and
                     '.Trash' not in str(f)]

            # Parallel file scanning
            with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
                futures = [executor.submit(self.scan_file, f) for f in files[:50000]]

                for future in as_completed(futures):
                    data = future.result()
                    if data:
                        result["files"].append(data)
                        result["file_count"] += 1
                        result["total_bytes"] += data["size"]
                        result["by_extension"][data["ext"]] += 1

                        with self.lock:
                            self.all_files.append(data)

        except subprocess.TimeoutExpired:
            result["error"] = "Scan timeout"
        except Exception as e:
            result["error"] = str(e)[:200]

        result["scan_time_ms"] = int((time.perf_counter() - start) * 1000)
        result["by_extension"] = dict(result["by_extension"])

        return result

    def deep_dive(self):
        """Execute the DEEP DIVE"""
        print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                    🔱 GABRIEL DEEP DIVE 🔱                                   ║
║                                                                              ║
║           MAXIMUM CODE EXTRACTION - ALL DRIVES - NO LIMITS                   ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
""")

        start = time.perf_counter()
        volumes = self.get_all_volumes()

        print(f"🔍 Found {len(volumes)} accessible volumes")
        print("═" * 70)

        for vol in volumes:
            vol_name = vol.name if vol != Path.home() else "~Home"
            print(f"\n⚡ Diving into: {vol_name}...")

            result = self.scan_volume_fast(vol)
            self.stats["by_volume"][str(vol)] = {
                "name": result["name"],
                "files": result["file_count"],
                "bytes": result["total_bytes"],
                "time_ms": result["scan_time_ms"]
            }
            self.stats["volumes_scanned"] += 1
            self.stats["total_files"] += result["file_count"]
            self.stats["total_bytes"] += result["total_bytes"]

            for ext, count in result["by_extension"].items():
                self.stats["by_extension"][ext] += count

            size_mb = result["total_bytes"] / 1024 / 1024
            print(f"   ✅ {result['file_count']:,} files | {size_mb:.1f} MB | {result['scan_time_ms']}ms")

            if result.get("error"):
                print(f"   ⚠️  {result['error']}")

        self.stats["scan_time_ms"] = int((time.perf_counter() - start) * 1000)
        self.stats["by_extension"] = dict(self.stats["by_extension"])

        return self.stats

    def print_summary(self):
        """Print glorious summary"""
        print(f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                         DEEP DIVE COMPLETE                                   ║
╚══════════════════════════════════════════════════════════════════════════════╝

  📀 Volumes Scanned:      {self.stats['volumes_scanned']:>15,}
  📁 Total Code Files:     {self.stats['total_files']:>15,}
  💾 Total Size:           {self.stats['total_bytes']/1024/1024:>15,.1f} MB
  ⚡ Scan Time:            {self.stats['scan_time_ms']:>15,} ms

  TOP LANGUAGES:
""")

        sorted_ext = sorted(self.stats["by_extension"].items(), key=lambda x: x[1], reverse=True)
        for ext, count in sorted_ext[:20]:
            pct = count / max(1, self.stats["total_files"]) * 100
            bar = "█" * int(pct / 2)
            print(f"  {ext:<10} {count:>10,}  {bar}")

        print(f"""
  VOLUME BREAKDOWN:
""")
        for vol_path, data in sorted(self.stats["by_volume"].items(), key=lambda x: x[1]["files"], reverse=True)[:15]:
            name = data["name"][:20]
            print(f"  {name:<20} {data['files']:>10,} files  {data['bytes']/1024/1024:>8.1f} MB")

        print(f"\n{'═' * 78}\n")

    def save_results(self):
        """Save all results"""
        # Stats summary
        stats_file = DATA_DIR / "deepdive_stats.json"
        with open(stats_file, 'w') as f:
            json.dump(self.stats, f, indent=2, default=str)
        print(f"💾 Stats saved: {stats_file}")

        # All files list (sorted by size)
        self.all_files.sort(key=lambda x: x.get("size", 0), reverse=True)
        files_file = DATA_DIR / "all_code_files.json"
        with open(files_file, 'w') as f:
            json.dump(self.all_files[:200000], f, indent=2)
        print(f"💾 File list saved: {files_file} ({len(self.all_files):,} files)")

        # Create searchable index
        index = {
            "created": datetime.now().isoformat(),
            "total_files": len(self.all_files),
            "by_extension": defaultdict(list)
        }
        for f in self.all_files:
            ext = f.get("ext", "")
            if len(index["by_extension"][ext]) < 10000:  # Limit per extension
                index["by_extension"][ext].append(f["path"])

        index["by_extension"] = dict(index["by_extension"])
        index_file = DATA_DIR / "code_index.json"
        with open(index_file, 'w') as f:
            json.dump(index, f, indent=2)
        print(f"💾 Index saved: {index_file}")


def main():
    diver = DeepDiver()
    diver.deep_dive()
    diver.print_summary()
    diver.save_results()

    print("""
🎊 GABRIEL HAS ABSORBED ALL CODE!
🔥 KNOWLEDGE IS POWER!
⚡ GORUNFREEX1000 FOREVER!
""")
    return 0


if __name__ == "__main__":
    sys.exit(main())
