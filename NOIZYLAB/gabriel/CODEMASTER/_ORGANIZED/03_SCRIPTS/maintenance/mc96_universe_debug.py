#!/usr/bin/env python3
"""
MC96ECOUNIVERSE COMPLETE DEBUG & OPTIMIZATION
Debug all volumes, data, tech across m2ultra & HP-OMEN Gabriel
"""

import subprocess
import json
import sys
import os
from datetime import datetime
from pathlib import Path

LOG_PATH = "/Users/m2ultra/.cursor/debug.log"

def debug_log(location, message, data=None, hypothesis_id=None, run_id="mc96_universe"):
    """Log debug information"""
    log_entry = {
        "id": f"log_{int(datetime.now().timestamp() * 1000)}",
        "timestamp": int(datetime.now().timestamp() * 1000),
        "location": location,
        "message": message,
        "data": data or {},
        "sessionId": "mc96_universe_debug",
        "runId": run_id,
        "hypothesisId": hypothesis_id or "N/A"
    }
    try:
        with open(LOG_PATH, "a") as f:
            f.write(json.dumps(log_entry) + "\n")
    except Exception as e:
        print(f"LOG ERROR: {e}")

# Hypotheses for debugging
HYPOTHESES = {
    "H1": "Volume scanning fails to detect all mounted volumes",
    "H2": "MC96 config volumes list contains unmounted/inaccessible paths",
    "H3": "Disk diagnostics miss SMB/network volumes",
    "H4": "Volume path resolution fails for paths with spaces",
    "H5": "MC96_ROOT path incorrect or inaccessible",
    "H6": "Critical files missing from MC96ECOUNIVERSE",
    "H7": "Network volumes (HP-OMEN) not properly detected",
    "H8": "Volume health checks incomplete"
}

def test_all_volumes():
    """Test all volume detection methods"""
    debug_log("test_all_volumes:entry", "Starting comprehensive volume test", {}, "H1")
    
    # Method 1: df command
    try:
        df_result = subprocess.run(["df", "-h"], capture_output=True, text=True, timeout=15)
        debug_log("test_all_volumes:df", "df command executed", {
            "returncode": df_result.returncode,
            "output_lines": len(df_result.stdout.split('\n'))
        }, "H1")
        
        volumes = []
        for line in df_result.stdout.split('\n')[1:]:
            if line.strip():
                parts = line.split()
                if len(parts) >= 6:
                    mount = ' '.join(parts[5:])
                    if '/Volumes/' in mount or '/System/Volumes/' in mount:
                        volumes.append({
                            "device": parts[0],
                            "size": parts[1],
                            "used": parts[2],
                            "available": parts[3],
                            "usage": parts[4],
                            "mount": mount
                        })
        
        debug_log("test_all_volumes:df_parsed", "df volumes parsed", {
            "count": len(volumes),
            "volumes": volumes
        }, "H1")
    except Exception as e:
        debug_log("test_all_volumes:df_error", "df command failed", {"error": str(e)}, "H1")
        volumes = []
    
    return volumes

def test_mc96_config_volumes():
    """Test all volumes from MC96 config"""
    debug_log("test_mc96_config_volumes:entry", "Testing MC96 config volumes", {}, "H2")
    
    # Load MC96 config volumes
    try:
        sys.path.insert(0, str(Path(__file__).parent.parent / "6tb_scripts"))
        from mc96_config import VOLUMES, MC96_ROOT
        debug_log("test_mc96_config_volumes:imported", "MC96 config imported", {
            "volumes_count": len(VOLUMES),
            "mc96_root": MC96_ROOT
        }, "H2")
    except Exception as e:
        debug_log("test_mc96_config_volumes:import_error", "MC96 config import failed", {
            "error": str(e)
        }, "H2")
        return []
    
    results = []
    for vol_path in VOLUMES:
        vol_path_obj = Path(vol_path)
        exists = vol_path_obj.exists()
        is_dir = vol_path_obj.is_dir() if exists else False
        is_mount = False
        
        # Check if mounted
        if exists:
            try:
                df_check = subprocess.run(
                    ["df", vol_path],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                is_mount = df_check.returncode == 0
            except:
                pass
        
        result = {
            "path": vol_path,
            "exists": exists,
            "is_dir": is_dir,
            "is_mount": is_mount,
            "accessible": exists and is_mount
        }
        results.append(result)
        
        debug_log("test_mc96_config_volumes:check", f"Volume checked: {vol_path}", result, "H2")
    
    return results

def test_network_volumes():
    """Test network/SMB volumes (HP-OMEN)"""
    debug_log("test_network_volumes:entry", "Testing network volumes", {}, "H7")
    
    try:
        df_result = subprocess.run(["df", "-h"], capture_output=True, text=True, timeout=15)
        network_vols = []
        
        for line in df_result.stdout.split('\n'):
            if '//' in line or 'smb://' in line.lower():
                parts = line.split()
                if len(parts) >= 6:
                    mount = ' '.join(parts[5:])
                    network_vols.append({
                        "device": parts[0],
                        "mount": mount,
                        "size": parts[1],
                        "used": parts[2],
                        "available": parts[3],
                        "usage": parts[4]
                    })
        
        debug_log("test_network_volumes:found", "Network volumes found", {
            "count": len(network_vols),
            "volumes": network_vols
        }, "H7")
        
        return network_vols
    except Exception as e:
        debug_log("test_network_volumes:error", "Network volume test failed", {"error": str(e)}, "H7")
        return []

def test_mc96_root():
    """Test MC96_ROOT accessibility"""
    debug_log("test_mc96_root:entry", "Testing MC96_ROOT", {}, "H5")
    
    try:
        sys.path.insert(0, str(Path(__file__).parent.parent / "6tb_scripts"))
        from mc96_config import MC96_ROOT
    except:
        MC96_ROOT = "/Volumes/6TB/Sample_Libraries"
    
    root_path = Path(MC96_ROOT)
    exists = root_path.exists()
    is_dir = root_path.is_dir() if exists else False
    
    result = {"path": MC96_ROOT, "exists": exists, "is_dir": is_dir}
    
    if exists:
        try:
            # Test read access
            try:
                list(root_path.iterdir())
                result["readable"] = True
            except:
                result["readable"] = False
            
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
                    result.update({
                        "size": parts[1],
                        "used": parts[2],
                        "available": parts[3],
                        "usage": parts[4]
                    })
        except Exception as e:
            debug_log("test_mc96_root:df_error", "MC96_ROOT df failed", {"error": str(e)}, "H5")
    
    debug_log("test_mc96_root:result", "MC96_ROOT test result", result, "H5")
    return result

def test_critical_files():
    """Test critical MC96ECOUNIVERSE files"""
    debug_log("test_critical_files:entry", "Testing critical files", {}, "H6")
    
    try:
        sys.path.insert(0, str(Path(__file__).parent.parent / "6tb_scripts"))
        from mc96_config import CRITICAL_FILES, MC96_ROOT
    except:
        CRITICAL_FILES = []
        MC96_ROOT = "/Volumes/6TB/Sample_Libraries"
    
    results = []
    for file_path in CRITICAL_FILES:
        file_obj = Path(file_path)
        exists = file_obj.exists()
        is_file = file_obj.is_file() if exists else False
        size = file_obj.stat().st_size if exists and is_file else 0
        
        result = {
            "path": file_path,
            "exists": exists,
            "is_file": is_file,
            "size": size
        }
        results.append(result)
        
        debug_log("test_critical_files:check", f"Critical file: {file_path}", result, "H6")
    
    return results

def test_volume_health():
    """Test volume health checks"""
    debug_log("test_volume_health:entry", "Testing volume health", {}, "H8")
    
    try:
        # Test diskutil for macOS
        result = subprocess.run(
            ["diskutil", "list"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        health_result = {
            "diskutil_available": result.returncode == 0,
            "output_lines": len(result.stdout.split('\n')) if result.returncode == 0 else 0
        }
        
        debug_log("test_volume_health:diskutil", "diskutil test", health_result, "H8")
        
        return health_result
    except Exception as e:
        debug_log("test_volume_health:error", "Health check failed", {"error": str(e)}, "H8")
        return {"error": str(e)}

def generate_report(all_volumes, config_volumes, network_volumes, mc96_root, critical_files, health):
    """Generate comprehensive report"""
    debug_log("generate_report:entry", "Generating report", {}, "REPORT")
    
    report = {
        "timestamp": datetime.now().isoformat(),
        "summary": {
            "all_volumes_detected": len(all_volumes),
            "config_volumes_total": len(config_volumes),
            "config_volumes_accessible": sum(1 for v in config_volumes if v.get("accessible")),
            "network_volumes": len(network_volumes),
            "mc96_root_accessible": mc96_root.get("exists", False),
            "critical_files_total": len(critical_files),
            "critical_files_present": sum(1 for f in critical_files if f.get("exists"))
        },
        "all_volumes": all_volumes,
        "config_volumes": config_volumes,
        "network_volumes": network_volumes,
        "mc96_root": mc96_root,
        "critical_files": critical_files,
        "health": health
    }
    
    debug_log("generate_report:complete", "Report generated", {
        "summary": report["summary"]
    }, "REPORT")
    
    return report

def main():
    """Main debugging function"""
    debug_log("main:entry", "Starting MC96ECOUNIVERSE debug", {
        "timestamp": datetime.now().isoformat()
    })
    
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║      MC96ECOUNIVERSE COMPLETE DEBUG & OPTIMIZATION          ║")
    print("║      m2ultra & HP-OMEN Gabriel - All Volumes & Tech         ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print()
    
    print("🔍 Testing all volume detection...")
    all_volumes = test_all_volumes()
    print(f"   ✓ Found {len(all_volumes)} total volumes")
    
    print("⚙️  Testing MC96 config volumes...")
    config_volumes = test_mc96_config_volumes()
    accessible = sum(1 for v in config_volumes if v.get("accessible"))
    print(f"   ✓ {accessible}/{len(config_volumes)} config volumes accessible")
    
    print("🌐 Testing network volumes (HP-OMEN)...")
    network_volumes = test_network_volumes()
    print(f"   ✓ Found {len(network_volumes)} network volumes")
    
    print("📁 Testing MC96_ROOT...")
    mc96_root = test_mc96_root()
    print(f"   ✓ MC96_ROOT accessible: {mc96_root.get('exists', False)}")
    
    print("📄 Testing critical files...")
    critical_files = test_critical_files()
    present = sum(1 for f in critical_files if f.get("exists"))
    print(f"   ✓ {present}/{len(critical_files)} critical files present")
    
    print("💚 Testing volume health...")
    health = test_volume_health()
    print(f"   ✓ Health checks: {'OK' if not health.get('error') else 'FAILED'}")
    
    # Generate report
    report = generate_report(
        all_volumes, config_volumes, network_volumes,
        mc96_root, critical_files, health
    )
    
    # Print summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    for key, value in report["summary"].items():
        print(f"  {key}: {value}")
    
    # Save report
    report_path = Path(__file__).parent / "mc96_universe_report.json"
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)
    print(f"\n📊 Full report saved to: {report_path}")
    
    debug_log("main:complete", "MC96ECOUNIVERSE debug complete", report["summary"])
    
    return report

if __name__ == "__main__":
    main()

