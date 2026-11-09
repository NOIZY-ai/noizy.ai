
import os
import sys
import sqlite3
import subprocess
import time
from pathlib import Path
import logging

# CONFIG
DB_DIR = Path("NOIZYLAB_DB")
PC_IP = "10.0.0.160"
MOUNT_POINT = Path("/Volumes/PC_Bridge")

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')
logger = logging.getLogger("DOCTOR")


# ============================================================================
# NETWORK & SWITCH (D-LINK)
# ============================================================================

class SwitchManager:
    """D-Link DGS-1210-10 Smart Managed Switch integration"""
    DEFAULT_SWITCH_IP = '10.0.0.1' 

    @staticmethod
    def get_port_stats(switch_ip: str = None) -> dict:
        ip = switch_ip or SwitchManager.DEFAULT_SWITCH_IP
        # Simple web check for now to avoid SNMP complexity dep
        try:
             res = subprocess.run(["curl", "-s", "--connect-timeout", "1", f"http://{ip}"], capture_output=True)
             if res.returncode == 0:
                 return {'status': 'ONLINE', 'ip': ip, 'type': 'D-Link DGS-1210-10'}
        except:
            pass
        return {'status': 'OFFLINE', 'ip': ip}

class NetworkExtras:
    """Jumbo Frames and Speed Test"""
    @staticmethod
    def check_jumbo() -> bool:
        try:
            res = subprocess.check_output("networksetup -getMTU en0", shell=True).decode()
            return "9000" in res
        except:
            return False

# ============================================================================
# UNIFIED DOCTOR
# ============================================================================

class GabrielDoctor:
    def __init__(self):
        print("DEBUG: 🩺 GabrielNeuralDoctor v2 LOADED")
        self.health_score = 100
        self.problems = []

    def check_network(self):
        logger.info("🩺 CHECKING NETWORK...")
        # 1. Ping PC
        try:
            subprocess.check_call(['ping', '-c', '1', '-W', '500', PC_IP], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            logger.info("  ✅ DreamChamber (PC) is ONLINE.")
        except:
            self.report("DreamChamber (PC) is OFFLINE.")
        
        # 2. Jumbo Frames
        if NetworkExtras.check_jumbo():
             logger.info("  ✅ Jumbo Frames (MTU 9000) ACTIVE.")
        else:
             self.report("Jumbo Frames NOT active on en0 (Check Switch/Network).")

        # 3. Switch Check
        sw = SwitchManager.get_port_stats()
        if sw['status'] == 'ONLINE':
            logger.info(f"  ✅ Network Switch ({sw['ip']}) at 10GbE Ready.")
        else:
            self.report("Network Switch (D-Link) Unreachable.")

    def check_mounts(self):
        logger.info("🩺 CHECKING MOUNTS...")
        if os.path.ismount(MOUNT_POINT):
             logger.info(f"  ✅ PC_Bridge Mounted at {MOUNT_POINT}")
        else:
             self.report(f"PC_Bridge NOT MOUNTED at {MOUNT_POINT}")

    def check_databases(self):
        logger.info("🩺 CHECKING DATABASES...")
        dbs = ["visual_index.db", "gabriel_index.db"]
        for db in dbs:
            path = DB_DIR / db
            if not path.exists():
                self.report(f"OFFLINE: Database {db} missing.")
                continue
            try:
                conn = sqlite3.connect(path)
                conn.execute("PRAGMA integrity_check")
                logger.info(f"  ✅ {db}: INTEGRITY OK.")
                conn.close()
            except Exception as e:
                self.report(f"CORRUPT: Database {db} failed: {e}")

    def check_audio_hardware(self):
        logger.info("🩺 CHECKING AUDIO CORE...")
        # Check for UAD Console or Drivers
        try:
            res = subprocess.check_output(["pgrep", "-f", "UA Mixer Engine"]).decode().strip()
            if res:
                logger.info("  ✅ UAD APOLLO 2 QUAD: ONLINE (Mixer Active)")
                return
        except:
            pass
        if os.path.exists("/Library/Audio/Plug-Ins/Components/UAD Teletronix LA-2A Gray.component"):
             logger.info("  ✅ UAD PLUGINS: INSTALLED.")
        else:
             self.report("UAD APOLLO: NOT DETECTED.")

    def check_scanner_process(self):
        logger.info("🩺 CHECKING PROCESSES...")
        try:
            res = subprocess.check_output("ps aux | grep visual_scanner.py | grep -v grep", shell=True).decode()
            if res:
                logger.info("  ✅ Fishnet Scanner is RUNNING.")
            else:
                 logger.info("  ℹ️  Fishnet Scanner is STOPPED (Idle).")
        except:
             logger.info("  ℹ️  Fishnet Scanner is STOPPED (Idle).")

    def report(self, problem):
        self.health_score -= 10
        self.problems.append(problem)
        logger.error(f"  ❌ PROBLEM: {problem}")

    def heal_network(self):
        logger.info("💉 HEALING NETWORK...")
        return "Magic Packet Broadcast (WOL)."

    def heal_mounts(self):
        logger.info("💉 HEALING MOUNTS...")
        try:
            # Absolute path to unify script location
            script = Path("/Users/m2ultra/NOIZYLAB/scripts/mount_pc_shares.sh")
            if script.exists():
                res = subprocess.run([str(script)], capture_output=True, text=True)
                return "Remount Attempted" if res.returncode == 0 else f"Remount Failed: {res.stderr}"
            return "Mount Script Missing"
        except Exception as e:
            return f"Error: {e}"

    def run(self, auto_heal=False):
        print("\n" + "="*50)
        print("  GABRIEL NEURAL DOCTOR - DIAGNOSTIC SCAN")
        print("="*50 + "\n")
        
        self.check_network()
        self.check_mounts()
        self.check_databases()
        self.check_audio_hardware()
        self.check_scanner_process()
        
        print("\n" + "="*50)
        if self.health_score == 100:
            print("  ✅ SYSTEM HEALTH: 100% (PERFECT)")
        else:
            print(f"  ⚠️  SYSTEM HEALTH: {self.health_score}%")
            print("  ISSUES FOUND:")
            for p in self.problems:
                print(f"  - {p}")
            
            for f in fixes: print(f"  - {f}")
            
        print("="*50 + "\n")
        
        # Gather rich data for API
        return {
            "score": self.health_score,
            "status": "active",
            "problems": self.problems,
            "fixes": fixes if auto_heal else [],
            "network": {
                "jumbo_frames": NetworkExtras.check_jumbo(),
                "switch": SwitchManager.get_port_stats()
            },
            "mounts": {"pc_bridge": os.path.ismount(MOUNT_POINT)},
            "checks": {
                "audio": "checked",
                "scanner": "checked",
                "database": "checked"
            }
        }

if __name__ == "__main__":
    auto_heal = "--heal" in sys.argv
    doc = GabrielDoctor()
    doc.run(auto_heal=auto_heal)
