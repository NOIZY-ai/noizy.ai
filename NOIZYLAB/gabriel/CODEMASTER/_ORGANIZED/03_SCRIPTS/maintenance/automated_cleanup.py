#!/usr/bin/env python3
"""
AUTOMATED CLEANUP SYSTEM - AI-Powered Volume Cleanup
Intelligent cleanup recommendations for critical volumes
"""

import subprocess
import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
import shutil

class AutomatedCleanup:
    """AI-powered automated cleanup system"""
    
    CRITICAL_THRESHOLD = 95
    WARNING_THRESHOLD = 85
    
    # Safe cleanup patterns (always safe to clean)
    SAFE_CLEANUP_PATTERNS = [
        "**/.DS_Store",
        "**/.AppleDouble",
        "**/.LSOverride",
        "**/.fseventsd",
        "**/.Spotlight-V100",
        "**/.TemporaryItems",
        "**/.Trashes",
        "**/__pycache__",
        "**/*.pyc",
        "**/*.pyo",
        "**/.pytest_cache",
        "**/node_modules/.cache",
        "**/.cache",
        "**/Library/Caches/*",
        "**/Library/Logs/*",
        "**/tmp/*",
        "**/var/tmp/*"
    ]
    
    def __init__(self):
        self.cleanup_log = []
        self.total_space_freed = 0
    
    def analyze_volume(self, volume_path: str) -> Dict:
        """Analyze volume for cleanup opportunities"""
        path = Path(volume_path)
        if not path.exists():
            return {"error": f"Volume not found: {volume_path}"}
        
        analysis = {
            "volume": volume_path,
            "total_size": 0,
            "cleanup_opportunities": [],
            "estimated_space": 0,
            "critical_files": []
        }
        
        # Check disk usage
        try:
            result = subprocess.run(
                ["df", "-h", volume_path],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                parts = result.stdout.split('\n')[-1].split()
                if len(parts) >= 5:
                    analysis["total_size"] = parts[1]
                    analysis["used"] = parts[2]
                    analysis["available"] = parts[3]
                    analysis["usage_pct"] = int(parts[4].replace('%', ''))
        except:
            pass
        
        # Find cleanup opportunities
        cleanup_items = self._find_cleanup_items(path)
        analysis["cleanup_opportunities"] = cleanup_items
        
        # Estimate space that can be freed
        estimated = sum(item.get("size_bytes", 0) for item in cleanup_items)
        analysis["estimated_space"] = self._format_bytes(estimated)
        analysis["estimated_space_bytes"] = estimated
        
        return analysis
    
    def _find_cleanup_items(self, root: Path, max_depth: int = 3) -> List[Dict]:
        """Find items safe to clean"""
        items = []
        
        # Check for common cache/temp directories
        cache_dirs = [
            root / "Library" / "Caches",
            root / "Library" / "Logs",
            root / ".cache",
            root / "tmp",
            root / "var" / "tmp"
        ]
        
        for cache_dir in cache_dirs:
            if cache_dir.exists() and cache_dir.is_dir():
                try:
                    size = sum(
                        f.stat().st_size for f in cache_dir.rglob('*')
                        if f.is_file()
                    )
                    if size > 0:
                        items.append({
                            "path": str(cache_dir),
                            "type": "cache_directory",
                            "size_bytes": size,
                            "size": self._format_bytes(size),
                            "safe": True
                        })
                except:
                    pass
        
        # Find .DS_Store files
        try:
            ds_store_files = list(root.rglob('.DS_Store'))[:100]  # Limit to first 100
            if ds_store_files:
                total_size = sum(f.stat().st_size for f in ds_store_files)
                items.append({
                    "path": f"{len(ds_store_files)} .DS_Store files",
                    "type": "ds_store",
                    "size_bytes": total_size,
                    "size": self._format_bytes(total_size),
                    "safe": True,
                    "count": len(ds_store_files)
                })
        except:
            pass
        
        # Find __pycache__ directories
        try:
            pycache_dirs = list(root.rglob('__pycache__'))[:50]
            if pycache_dirs:
                total_size = sum(
                    sum(f.stat().st_size for f in d.rglob('*') if f.is_file())
                    for d in pycache_dirs
                )
                items.append({
                    "path": f"{len(pycache_dirs)} __pycache__ directories",
                    "type": "pycache",
                    "size_bytes": total_size,
                    "size": self._format_bytes(total_size),
                    "safe": True,
                    "count": len(pycache_dirs)
                })
        except:
            pass
        
        return items
    
    def _format_bytes(self, bytes: int) -> str:
        """Format bytes to human readable"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes < 1024.0:
                return f"{bytes:.2f} {unit}"
            bytes /= 1024.0
        return f"{bytes:.2f} PB"
    
    def cleanup_volume(self, volume_path: str, dry_run: bool = True) -> Dict:
        """Clean up volume (dry run by default)"""
        analysis = self.analyze_volume(volume_path)
        
        if "error" in analysis:
            return analysis
        
        results = {
            "volume": volume_path,
            "dry_run": dry_run,
            "items_cleaned": [],
            "space_freed": 0,
            "errors": []
        }
        
        if not dry_run:
            # Perform actual cleanup
            for item in analysis["cleanup_opportunities"]:
                if item.get("safe"):
                    try:
                        item_path = Path(item["path"])
                        if item_path.exists():
                            if item["type"] in ["ds_store", "pycache"]:
                                # Handle multiple files/dirs
                                if item_path.is_file():
                                    size = item_path.stat().st_size
                                    item_path.unlink()
                                    results["space_freed"] += size
                                    results["items_cleaned"].append({
                                        "path": str(item_path),
                                        "size": size
                                    })
                            elif item_path.is_dir():
                                # Remove directory
                                size = sum(
                                    f.stat().st_size for f in item_path.rglob('*')
                                    if f.is_file()
                                )
                                shutil.rmtree(item_path)
                                results["space_freed"] += size
                                results["items_cleaned"].append({
                                    "path": str(item_path),
                                    "size": size,
                                    "type": "directory"
                                })
                    except Exception as e:
                        results["errors"].append({
                            "path": item["path"],
                            "error": str(e)
                        })
        else:
            # Dry run - just report what would be cleaned
            results["would_clean"] = analysis["cleanup_opportunities"]
            results["estimated_space"] = analysis["estimated_space_bytes"]
        
        results["space_freed_formatted"] = self._format_bytes(results["space_freed"])
        
        return results
    
    def generate_cleanup_report(self, analyses: List[Dict]) -> str:
        """Generate cleanup report"""
        report = []
        report.append("╔══════════════════════════════════════════════════════════════╗")
        report.append("║           AUTOMATED CLEANUP REPORT                           ║")
        report.append("╚══════════════════════════════════════════════════════════════╝")
        report.append(f"\n📅 Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        for analysis in analyses:
            if "error" in analysis:
                continue
            
            report.append(f"📁 Volume: {analysis['volume']}")
            report.append(f"   Usage: {analysis.get('usage_pct', 'N/A')}%")
            report.append(f"   Available: {analysis.get('available', 'N/A')}")
            report.append(f"   Cleanup Opportunities: {len(analysis['cleanup_opportunities'])}")
            report.append(f"   Estimated Space to Free: {analysis['estimated_space']}")
            
            if analysis['cleanup_opportunities']:
                report.append("   Items:")
                for item in analysis['cleanup_opportunities'][:5]:
                    report.append(f"     • {item['path']}: {item['size']}")
            report.append("")
        
        return "\n".join(report)

def main():
    """Main cleanup function"""
    cleanup = AutomatedCleanup()
    
    # Get critical volumes
    try:
        from volume_monitor_UPGRADED import VolumeMonitorUpgraded
        monitor = VolumeMonitorUpgraded()
        monitor.scan_volumes()
        critical_volumes = monitor.get_critical_volumes()
        
        print("╔══════════════════════════════════════════════════════════════╗")
        print("║           AUTOMATED CLEANUP SYSTEM                           ║")
        print("╚══════════════════════════════════════════════════════════════╝")
        print(f"\n🔍 Analyzing {len(critical_volumes)} critical volumes...\n")
        
        analyses = []
        for vol_name in critical_volumes[:3]:  # Analyze first 3 critical
            vol_info = monitor.volumes.get(vol_name)
            if vol_info:
                print(f"📁 Analyzing: {vol_info['mount']}")
                analysis = cleanup.analyze_volume(vol_info['mount'])
                analyses.append(analysis)
                print(f"   ✓ Found {len(analysis.get('cleanup_opportunities', []))} cleanup opportunities")
                print(f"   ✓ Estimated space: {analysis.get('estimated_space', 'N/A')}")
        
        # Dry run cleanup
        print("\n🧹 Running dry-run cleanup...")
        for analysis in analyses:
            if "error" not in analysis:
                result = cleanup.cleanup_volume(analysis['volume'], dry_run=True)
                print(f"   {analysis['volume']}: Would free {result.get('estimated_space', 0)} bytes")
        
        # Generate report
        report = cleanup.generate_cleanup_report(analyses)
        print("\n" + report)
        
        # Save report
        report_path = Path(__file__).parent / "cleanup_report.md"
        with open(report_path, "w") as f:
            f.write(report)
        print(f"\n📊 Report saved to: {report_path}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

