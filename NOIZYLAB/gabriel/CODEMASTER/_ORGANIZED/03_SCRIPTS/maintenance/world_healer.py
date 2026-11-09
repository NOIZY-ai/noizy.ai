#!/usr/bin/env python3
"""
WORLD HEALER - Automated System Maintenance
Gabriel System Health & Optimization Tool
"""

import os
import subprocess
import shutil
from pathlib import Path
from datetime import datetime

class WorldHealer:
    def __init__(self):
        self.home = Path.home()
        self.results = []
        self.space_freed = 0
        
    def log(self, msg):
        print(f"  {msg}")
        self.results.append(msg)
    
    def clean_ide_caches(self):
        """Clean IDE caches and logs"""
        print("\n🧹 Cleaning IDE Caches...")
        
        ide_paths = [
            ("Cursor", self.home / "Library/Application Support/Cursor"),
            ("VSCode", self.home / "Library/Application Support/Code"),
            ("Windsurf", self.home / "Library/Application Support/Windsurf"),
            ("Code Insiders", self.home / "Library/Application Support/Code - Insiders"),
        ]
        
        for name, base_path in ide_paths:
            if base_path.exists():
                for subdir in ["Cache", "CachedData", "logs", "Crashpad"]:
                    cache_path = base_path / subdir
                    if cache_path.exists():
                        try:
                            size = sum(f.stat().st_size for f in cache_path.rglob('*') if f.is_file())
                            shutil.rmtree(cache_path)
                            cache_path.mkdir(exist_ok=True)
                            self.space_freed += size
                            self.log(f"✅ {name} {subdir} cleaned ({size // 1024 // 1024}MB)")
                        except Exception as e:
                            self.log(f"⚠️ {name} {subdir}: {e}")
    
    def clean_python_cache(self):
        """Remove __pycache__ directories"""
        print("\n🐍 Cleaning Python Cache...")
        count = 0
        for pycache in self.home.rglob("__pycache__"):
            try:
                shutil.rmtree(pycache)
                count += 1
            except:
                pass
        self.log(f"✅ Removed {count} __pycache__ directories")
    
    def clean_npm_cache(self):
        """Clean NPM cache"""
        print("\n📦 Cleaning NPM Cache...")
        try:
            result = subprocess.run(["npm", "cache", "clean", "--force"], 
                                   capture_output=True, text=True)
            self.log("✅ NPM cache cleaned")
        except:
            self.log("⚠️ NPM not available")
    
    def clean_go_cache(self):
        """Clean Go build cache"""
        print("\n🔧 Cleaning Go Cache...")
        try:
            subprocess.run(["go", "clean", "-cache"], capture_output=True)
            self.log("✅ Go cache cleaned")
        except:
            self.log("⚠️ Go not available")
    
    def check_volumes(self):
        """Check volume health"""
        print("\n💾 Volume Status...")
        result = subprocess.run(["df", "-h"], capture_output=True, text=True)
        for line in result.stdout.split('\n'):
            if '/Volumes/' in line or '/System/Volumes/Data' in line:
                parts = line.split()
                if len(parts) >= 5:
                    pct = int(parts[4].replace('%', ''))
                    name = parts[-1].replace('/Volumes/', '')
                    if pct >= 95:
                        self.log(f"🔴 CRITICAL: {name} at {pct}%")
                    elif pct >= 85:
                        self.log(f"🟡 HIGH: {name} at {pct}%")
    
    def vacuum_databases(self):
        """Optimize SQLite databases"""
        print("\n🗄️ Optimizing Databases...")
        db_path = self.home / ".gemini/antigravity/playground/iridescent-station/NOIZYLAB_WORKSPACES_LOCAL/NOIZYLAB_DB"
        if db_path.exists():
            for db in db_path.glob("*.db"):
                try:
                    subprocess.run(["sqlite3", str(db), "VACUUM;"], capture_output=True)
                    self.log(f"✅ Optimized {db.name}")
                except:
                    pass
    
    def heal(self):
        """Run full healing cycle"""
        print("╔══════════════════════════════════════════════════════════════╗")
        print("║              WORLD HEALER - AUTOMATED MAINTENANCE            ║")
        print("╚══════════════════════════════════════════════════════════════╝")
        print(f"\n🕐 Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        self.clean_ide_caches()
        self.clean_python_cache()
        self.clean_npm_cache()
        self.clean_go_cache()
        self.vacuum_databases()
        self.check_volumes()
        
        print(f"\n═══════════════════════════════════════════════════════════════")
        print(f"  💾 Total space freed: {self.space_freed // 1024 // 1024}MB")
        print(f"  🕐 Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"═══════════════════════════════════════════════════════════════")

if __name__ == "__main__":
    healer = WorldHealer()
    healer.heal()
