#!/usr/bin/env python3
"""
DEBUG VOLUMES - Comprehensive volume debugging with runtime evidence
Tests all volume operations in MC96ECOUNIVERSE
"""

import subprocess
import json
import sys
from datetime import datetime
from pathlib import Path
import os

# Debug logging configuration
LOG_PATH = "/Users/m2ultra/.cursor/debug.log"
SERVER_ENDPOINT = "http://127.0.0.1:7242/ingest/03bc199f-f10a-4616-8fa2-eaa8e908078b"

def debug_log(location, message, data=None, hypothesis_id=None, run_id="volumes_debug"):
    """Log debug information"""
    log_entry = {
        "id": f"log_{int(datetime.now().timestamp() * 1000)}",
        "timestamp": int(datetime.now().timestamp() * 1000),
        "location": location,
        "message": message,
        "data": data or {},
        "sessionId": "volumes_debug_session",
        "runId": run_id,
        "hypothesisId": hypothesis_id or "N/A"
    }
    
    try:
        with open(LOG_PATH, "a") as f:
            f.write(json.dumps(log_entry) + "\n")
    except Exception as e:
        print(f"LOG ERROR: {e}")

# Import volume monitor
try:
    sys.path.insert(0, str(Path(__file__).parent))
    from volume_monitor import VolumeMonitor
    debug_log("debug_volumes.py:import", "VolumeMonitor imported successfully", {"path": str(Path(__file__).parent)})
except Exception as e:
    debug_log("debug_volumes.py:import", "VolumeMonitor import failed", {"error": str(e)}, "H1")
    print(f"Import error: {e}")
    sys.exit(1)

# Import MC96 config
try:
    sys.path.insert(0, str(Path(__file__).parent.parent / "6tb_scripts"))
    from mc96_config import VOLUMES, MC96_ROOT
    debug_log("debug_volumes.py:import", "mc96_config imported successfully", {"volumes_count": len(VOLUMES)})
except Exception as e:
    debug_log("debug_volumes.py:import", "mc96_config import failed", {"error": str(e)}, "H2")
    VOLUMES = []
    MC96_ROOT = "/Volumes/6TB/Sample_Libraries"

def test_volume_scanning():
    """Test volume scanning functionality"""
    debug_log("test_volume_scanning:entry", "Starting volume scan test", {}, "H1")
    
    try:
        monitor = VolumeMonitor()
        debug_log("test_volume_scanning:monitor_created", "VolumeMonitor instance created", {})
        
        # Test scan_volumes
        monitor.scan_volumes()
        debug_log("test_volume_scanning:scan_complete", "scan_volumes() completed", {
            "volumes_found": len(monitor.volumes),
            "volume_names": list(monitor.volumes.keys())
        }, "H1")
        
        return monitor.volumes
    except Exception as e:
        debug_log("test_volume_scanning:error", "Volume scan failed", {"error": str(e), "type": type(e).__name__}, "H1")
        return {}

def test_df_command():
    """Test raw df command output"""
    debug_log("test_df_command:entry", "Testing df -h command", {}, "H3")
    
    try:
        result = subprocess.run(["df", "-h"], capture_output=True, text=True, timeout=10)
        debug_log("test_df_command:executed", "df command executed", {
            "returncode": result.returncode,
            "stdout_lines": len(result.stdout.split('\n')),
            "stderr": result.stderr
        }, "H3")
        
        # Parse volumes
        volumes_found = []
        for line in result.stdout.split('\n')[1:]:
            if '/Volumes/' in line or '/System/Volumes/' in line:
                parts = line.split()
                if len(parts) >= 6:
                    mount = ' '.join(parts[5:])
                    volumes_found.append({
                        "mount": mount,
                        "device": parts[0],
                        "size": parts[1],
                        "used": parts[2],
                        "available": parts[3],
                        "usage": parts[4]
                    })
        
        debug_log("test_df_command:parsed", "df output parsed", {
            "volumes_count": len(volumes_found),
            "volumes": volumes_found
        }, "H3")
        
        return volumes_found
    except subprocess.TimeoutExpired:
        debug_log("test_df_command:timeout", "df command timed out", {}, "H3")
        return []
    except Exception as e:
        debug_log("test_df_command:error", "df command failed", {"error": str(e)}, "H3")
        return []

def test_mc96_volumes():
    """Test all volumes from mc96_config"""
    debug_log("test_mc96_volumes:entry", "Testing MC96 configured volumes", {
        "volumes_count": len(VOLUMES)
    }, "H4")
    
    results = []
    for vol_path in VOLUMES:
        debug_log("test_mc96_volumes:checking", f"Checking volume: {vol_path}", {}, "H4")
        
        vol_path_obj = Path(vol_path)
        exists = vol_path_obj.exists()
        is_dir = vol_path_obj.is_dir() if exists else False
        is_mount = False
        
        if exists:
            try:
                # Check if it's actually a mount point
                df_result = subprocess.run(
                    ["df", vol_path], 
                    capture_output=True, 
                    text=True, 
                    timeout=5
                )
                is_mount = df_result.returncode == 0 and vol_path in df_result.stdout
            except:
                pass
        
        result = {
            "path": vol_path,
            "exists": exists,
            "is_dir": is_dir,
            "is_mount": is_mount
        }
        results.append(result)
        
        debug_log("test_mc96_volumes:result", f"Volume check result: {vol_path}", result, "H4")
    
    return results

def test_mc96_root():
    """Test MC96_ROOT path"""
    debug_log("test_mc96_root:entry", "Testing MC96_ROOT", {"path": MC96_ROOT}, "H5")
    
    root_path = Path(MC96_ROOT)
    exists = root_path.exists()
    is_dir = root_path.is_dir() if exists else False
    
    result = {
        "path": MC96_ROOT,
        "exists": exists,
        "is_dir": is_dir
    }
    
    if exists:
        try:
            # Get disk usage
            df_result = subprocess.run(
                ["df", "-h", MC96_ROOT],
                capture_output=True,
                text=True,
                timeout=5
            )
            if df_result.returncode == 0:
                parts = df_result.stdout.split('\n')[-1].split()
                if len(parts) >= 5:
                    result["size"] = parts[1]
                    result["used"] = parts[2]
                    result["available"] = parts[3]
                    result["usage"] = parts[4]
        except Exception as e:
            debug_log("test_mc96_root:df_error", "df command failed", {"error": str(e)}, "H5")
    
    debug_log("test_mc96_root:result", "MC96_ROOT check result", result, "H5")
    return result

def test_disk_diagnostics():
    """Test disk diagnostics volume enumeration"""
    debug_log("test_disk_diagnostics:entry", "Testing disk diagnostics", {}, "H2")
    
    try:
        # Import disk diagnostics
        sys.path.insert(0, str(Path(__file__).parent.parent.parent / "CODEMASTER" / "portal"))
        from gabriel_diagnostics import DiskDiagnostics
        
        debug_log("test_disk_diagnostics:imported", "DiskDiagnostics imported", {})
        
        # Run diagnostics (this is a static method, but we need to call it in executor if async)
        # For now, test the shell command directly
        df_output = subprocess.run(
            ["df", "-h"],
            capture_output=True,
            text=True,
            timeout=10
        ).stdout
        
        volumes_count = len([l for l in df_output.split('\n') if '/Volumes/' in l or '/System/Volumes/' in l])
        
        debug_log("test_disk_diagnostics:result", "Disk diagnostics test", {
            "volumes_in_df": volumes_count,
            "df_output_preview": df_output[:200]
        }, "H2")
        
        return {"volumes_count": volumes_count}
    except Exception as e:
        debug_log("test_disk_diagnostics:error", "Disk diagnostics test failed", {
            "error": str(e),
            "type": type(e).__name__
        }, "H2")
        return {"error": str(e)}

def main():
    """Run all volume debugging tests"""
    debug_log("main:entry", "Starting volume debugging", {
        "timestamp": datetime.now().isoformat()
    })
    
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║           MC96ECOUNIVERSE VOLUME DEBUG                       ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print()
    
    results = {}
    
    # Test 1: Volume scanning
    print("📊 Testing volume scanning...")
    results["volume_scan"] = test_volume_scanning()
    print(f"   Found {len(results['volume_scan'])} volumes")
    
    # Test 2: Raw df command
    print("🔍 Testing df command...")
    results["df_volumes"] = test_df_command()
    print(f"   Found {len(results['df_volumes'])} volumes in df output")
    
    # Test 3: MC96 configured volumes
    print("⚙️  Testing MC96 configured volumes...")
    results["mc96_volumes"] = test_mc96_volumes()
    accessible = sum(1 for v in results["mc96_volumes"] if v["exists"] and v["is_mount"])
    print(f"   {accessible}/{len(results['mc96_volumes'])} volumes accessible")
    
    # Test 4: MC96_ROOT
    print("📁 Testing MC96_ROOT...")
    results["mc96_root"] = test_mc96_root()
    print(f"   MC96_ROOT exists: {results['mc96_root']['exists']}")
    
    # Test 5: Disk diagnostics
    print("🔬 Testing disk diagnostics...")
    results["disk_diagnostics"] = test_disk_diagnostics()
    
    # Summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print(f"VolumeMonitor found: {len(results.get('volume_scan', {}))} volumes")
    print(f"df command found: {len(results.get('df_volumes', []))} volumes")
    print(f"MC96 configured: {len(results.get('mc96_volumes', []))} volumes")
    print(f"MC96_ROOT accessible: {results.get('mc96_root', {}).get('exists', False)}")
    
    debug_log("main:complete", "Volume debugging complete", {
        "results_summary": {
            "volume_scan_count": len(results.get("volume_scan", {})),
            "df_volumes_count": len(results.get("df_volumes", [])),
            "mc96_volumes_count": len(results.get("mc96_volumes", [])),
            "mc96_root_exists": results.get("mc96_root", {}).get("exists", False)
        }
    })
    
    return results

if __name__ == "__main__":
    main()

