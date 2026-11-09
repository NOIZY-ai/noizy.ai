import os
import sys
import subprocess
import time
from pathlib import Path

try:
    import turbo_config as cfg
except ImportError:
    sys.path.append(str(Path(__file__).parent))
    import turbo_config as cfg

def run_step(step_name, script_name, args=[]):
    cfg.print_step(step_name, "START")
    start_t = time.time()
    
    cmd = ["python3", str(cfg.SCRIPTS_DIR / script_name)] + args
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        cfg.print_step(step_name, "FAIL")
        cfg.system_log(f"Error details: {e}", "ERROR")
        return False
    except KeyboardInterrupt:
        cfg.system_log(f"Interrupted: {step_name}", "WARN")
        return False
        
    duration = time.time() - start_t
    cfg.print_step(f"{step_name} ({duration:.1f}s)", "SUCCESS")
    return True

def run_omega(target_dir):
    cfg.print_header("⚡ THE OMEGA PROTOCOL", "TOTAL SYSTEM UNIFICATION")
    print(f"CORE > Target: {target_dir}")
    print(f"CORE > Mode:   FULL AUTONOMY (Zero Latency)")
    
    target_path = Path(target_dir)
    if not target_path.exists():
        cfg.system_log("❌ Target not found.", "ERROR")
        return

    # 1. VACUUM (The Black Hole Part 1)
    if not run_step("VACUUM (Deep Clean)", "turbo_vacuum.py", [str(target_path)]): return
    
    cfg.system_log("⚠️  WARNING: SINGULARITY EVENT IMMINENT.", "WARN")

    # 2. WORMHOLE SCANNER (Universal Ingestion)
    if not run_step("WORMHOLE (External Ingestion)", "turbo_wormhole.py", []): return

    # 3. VACUUM (Black Hole Part 2)
    if not run_step("VACUUM (Black Hole)", "turbo_vacuum.py", [str(target_path)]): return

    # 4. NEURAL INDEX (Genesis Scan)
    if not run_step("NEURAL INDEX (Genesis Scan)", "turbo_indexer.py", [str(target_path)]): return

    # 5. SINGULARITY (Atomic Fix)
    if not run_step("SINGULARITY (Atomic Unification)", "turbo_singularity.py", [str(target_path)]): return

    # 6. FINAL INDEX
    library_path = Path.expanduser(Path("~/Universal/Library"))
    if not run_step("NEURAL INDEX (Final Update)", "turbo_indexer.py", [str(library_path)]): return

    cfg.print_header("⛩️  OMEGA PROTOCOL COMPLETE", "The System is Perfection.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 turbo_omega.py <target_dir>")
    else:
        run_omega(sys.argv[1])
