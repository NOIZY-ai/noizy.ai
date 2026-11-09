#!/usr/bin/env python3
"""
GABRIEL CODE INHALER - ABSORB ALL CODE
Finds and catalogs ALL code across ALL mounted drives
Deep scan - No limits - Maximum coverage
"""

import os
import sys
import json
import time
import hashlib
from pathlib import Path
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import defaultdict
import threading

# CONFIG
MAX_WORKERS = os.cpu_count() * 2 or 8
GABRIEL_ROOT = Path.home() / "NOIZYLAB" / "GABRIEL"
DATA_DIR = GABRIEL_ROOT / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Code extensions to find
CODE_EXTENSIONS = {
    'python': ['.py', '.pyx', '.pyi', '.pyw'],
    'javascript': ['.js', '.jsx', '.mjs', '.cjs'],
    'typescript': ['.ts', '.tsx'],
    'shell': ['.sh', '.bash', '.zsh', '.fish'],
    'swift': ['.swift'],
    'go': ['.go'],
    'rust': ['.rs'],
    'c_cpp': ['.c', '.cpp', '.cc', '.cxx', '.h', '.hpp', '.hxx'],
    'java': ['.java', '.kt', '.scala'],
    'ruby': ['.rb', '.rake', '.gemspec'],
    'php': ['.php'],
    'web': ['.html', '.htm', '.css', '.scss', '.sass', '.less'],
    'data': ['.json', '.yaml', '.yml', '.xml', '.toml'],
    'docs': ['.md', '.rst', '.txt'],
    'config': ['.ini', '.cfg', '.conf', '.env'],
}

ALL_CODE_EXT = set()
for exts in CODE_EXTENSIONS.values():
    ALL_CODE_EXT.update(exts)


class CodeInhaler:
    """Inhale ALL code from everywhere"""

    def __init__(self):
        self.catalog = {
            "scanned_at": datetime.now().isoformat(),
            "volumes": {},
            "summary": defaultdict(int),
            "by_language": defaultdict(list),
            "largest_files": [],
            "total_lines": 0,
            "total_bytes": 0,
            "unique_hashes": set(),
        }
        self.lock = threading.Lock()

    def get_all_volumes(self) -> list:
        """Get all mounted volumes"""
        volumes = [Path.home()]

        # /Volumes
        vol_path = Path("/Volumes")
        if vol_path.exists():
            for v in vol_path.iterdir():
                if v.is_dir() and not v.name.startswith('.'):
                    volumes.append(v)

        return volumes

    def analyze_file(self, filepath: Path) -> dict:
        """Analyze a code file"""
        try:
            stat = filepath.stat()
            size = stat.st_size

            # Skip huge files
            if size > 10 * 1024 * 1024:  # 10MB
                return None

            # Read content
            try:
                content = filepath.read_text(errors='ignore')
                lines = len(content.split('\n'))

                # Hash for dedup
                file_hash = hashlib.md5(content.encode()).hexdigest()[:16]

            except:
                content = ""
                lines = 0
                file_hash = "error"

            # Determine language
            ext = filepath.suffix.lower()
            language = "unknown"
            for lang, exts in CODE_EXTENSIONS.items():
                if ext in exts:
                    language = lang
                    break

            return {
                "path": str(filepath),
                "name": filepath.name,
                "ext": ext,
                "language": language,
                "size": size,
                "lines": lines,
                "hash": file_hash,
                "modified": stat.st_mtime,
            }

        except Exception as e:
            return None

    def scan_volume(self, volume: Path) -> dict:
        """Scan a volume for code files"""
        result = {
            "path": str(volume),
            "name": volume.name,
            "files": [],
            "total_files": 0,
            "total_bytes": 0,
            "total_lines": 0,
            "by_language": defaultdict(int),
            "scan_time_ms": 0,
        }

        scan_start = time.perf_counter()

        try:
            # Find all code files
            code_files = []
            for ext in ALL_CODE_EXT:
                try:
                    found = list(volume.rglob(f"*{ext}"))
                    code_files.extend(found)
                except:
                    pass

            # Filter out unwanted
            code_files = [f for f in code_files
                         if '.git' not in str(f)
                         and 'node_modules' not in str(f)
                         and '__pycache__' not in str(f)
                         and 'Library/Caches' not in str(f)
                         and '.Trash' not in str(f)]

            # Limit per volume
            code_files = code_files[:100000]

            # Analyze in parallel
            with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
                futures = [executor.submit(self.analyze_file, f) for f in code_files]

                for future in as_completed(futures):
                    data = future.result()
                    if data:
                        result["files"].append(data)
                        result["total_files"] += 1
                        result["total_bytes"] += data["size"]
                        result["total_lines"] += data["lines"]
                        result["by_language"][data["language"]] += 1

        except Exception as e:
            result["error"] = str(e)

        result["scan_time_ms"] = int((time.perf_counter() - scan_start) * 1000)
        result["by_language"] = dict(result["by_language"])

        return result

    def inhale_all(self) -> dict:
        """INHALE ALL CODE FROM EVERYWHERE"""
        print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                    🌪️  GABRIEL CODE INHALER 🌪️                               ║
║                                                                              ║
║               Absorbing ALL code from ALL drives                             ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
""")

        start = time.perf_counter()
        volumes = self.get_all_volumes()

        print(f"📀 Found {len(volumes)} volumes to scan")
        print("═" * 70)

        for vol in volumes:
            print(f"\n🔍 Scanning: {vol.name}...")
            result = self.scan_volume(vol)

            self.catalog["volumes"][str(vol)] = result
            self.catalog["summary"]["total_files"] += result["total_files"]
            self.catalog["summary"]["total_bytes"] += result["total_bytes"]
            self.catalog["summary"]["total_lines"] += result["total_lines"]

            for lang, count in result.get("by_language", {}).items():
                self.catalog["summary"][f"lang_{lang}"] += count

            # Print volume summary
            print(f"   ✅ {result['total_files']:,} files | {result['total_lines']:,} lines | {result['total_bytes']/1024/1024:.1f} MB | {result['scan_time_ms']}ms")

            # Top languages for this volume
            if result.get("by_language"):
                top_langs = sorted(result["by_language"].items(), key=lambda x: x[1], reverse=True)[:5]
                langs_str = ", ".join([f"{l}: {c}" for l, c in top_langs])
                print(f"   📊 {langs_str}")

        self.catalog["scan_time_ms"] = int((time.perf_counter() - start) * 1000)

        return self.catalog

    def print_summary(self):
        """Print final summary"""
        summary = self.catalog.get("summary", {})

        print(f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                         CODE INHALE COMPLETE                                 ║
╚══════════════════════════════════════════════════════════════════════════════╝

  📁 Total Code Files:     {summary.get('total_files', 0):>15,}
  📝 Total Lines of Code:  {summary.get('total_lines', 0):>15,}
  💾 Total Size:           {summary.get('total_bytes', 0)/1024/1024:>15,.1f} MB

  LANGUAGES FOUND:
""")

        # Language breakdown
        lang_stats = {k: v for k, v in summary.items() if k.startswith('lang_')}
        sorted_langs = sorted(lang_stats.items(), key=lambda x: x[1], reverse=True)

        for lang_key, count in sorted_langs[:15]:
            lang = lang_key.replace('lang_', '')
            bar_len = min(50, int(count / max(1, summary.get('total_files', 1)) * 100))
            bar = "█" * bar_len
            print(f"  {lang:<15} {count:>8,}  {bar}")

        print(f"""
  ⚡ Total Scan Time: {self.catalog.get('scan_time_ms', 0):,} ms
  📀 Volumes Scanned: {len(self.catalog.get('volumes', {}))}

══════════════════════════════════════════════════════════════════════════════
""")

    def save_catalog(self):
        """Save catalog to file"""
        # Convert sets to lists for JSON
        catalog_json = {
            "scanned_at": self.catalog["scanned_at"],
            "scan_time_ms": self.catalog.get("scan_time_ms", 0),
            "summary": dict(self.catalog["summary"]),
            "volumes": {}
        }

        for vol_path, vol_data in self.catalog["volumes"].items():
            # Only save file paths, not full data (too big)
            catalog_json["volumes"][vol_path] = {
                "name": vol_data.get("name"),
                "total_files": vol_data.get("total_files", 0),
                "total_bytes": vol_data.get("total_bytes", 0),
                "total_lines": vol_data.get("total_lines", 0),
                "by_language": vol_data.get("by_language", {}),
                "scan_time_ms": vol_data.get("scan_time_ms", 0),
            }

        output_file = DATA_DIR / "code_catalog.json"
        with open(output_file, 'w') as f:
            json.dump(catalog_json, f, indent=2)

        print(f"💾 Catalog saved: {output_file}")

        # Save detailed file list separately
        files_file = DATA_DIR / "all_code_files.json"
        all_files = []
        for vol_data in self.catalog["volumes"].values():
            all_files.extend(vol_data.get("files", []))

        # Sort by size
        all_files.sort(key=lambda x: x.get("size", 0), reverse=True)

        with open(files_file, 'w') as f:
            json.dump(all_files[:100000], f, indent=2)  # Top 100k files

        print(f"💾 File list saved: {files_file} ({len(all_files):,} files)")


def main():
    inhaler = CodeInhaler()
    inhaler.inhale_all()
    inhaler.print_summary()
    inhaler.save_catalog()
    return 0


if __name__ == "__main__":
    sys.exit(main())
