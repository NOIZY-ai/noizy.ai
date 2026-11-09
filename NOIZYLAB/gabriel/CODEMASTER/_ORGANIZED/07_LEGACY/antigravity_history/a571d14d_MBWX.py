
import os
import sys
import sqlite3
import subprocess
import time
from pathlib import Path
import logging

# CONFIG
DB_DIR = Path("GABRIEL_UNIFIED/NOIZYLAB_DB")
PC_IP = "10.90.90.20"
MOUNT_POINT = Path.home() / "Mounts/PC_Bridge"

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')
logger = logging.getLogger("DOCTOR")

class GabrielDoctor:
    def __init__(self):
        self.health_score = 100
        self.problems = []

    def check_network(self):
        logger.info("🩺 CHECKING NETWORK...")
        # Check PC Ping
        try:
            subprocess.check_call(['ping', '-c', '1', '-W', '500', PC_IP], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            logger.info("  ✅ DreamChamber (PC) is ONLINE.")
        except:
            self.report("DreamChamber PC (10.90.90.20) is OFFLINE.")
        
        # Check Jumbo Frames (MTU 9000) on active interface
        try:
             # Heuristic check for en0 or similar
             res = subprocess.check_output("networksetup -getMTU en0", shell=True).decode()
             if "9000" in res:
                 logger.info("  ✅ Jumbo Frames (MTU 9000) ACTIVE.")
             else:
                 self.report(f"Jumbo Frames NOT active on en0. Current: {res.strip()}")
        except:
            pass # benign if not using en0

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
                count = conn.execute("SELECT count(*) FROM sqlite_master").fetchone()[0]
                logger.info(f"  ✅ {db}: INTEGRITY OK ({Path(path).stat().st_size/1024/1024:.1f} MB)")
                conn.close()
            except Exception as e:
                self.report(f"CORRUPT: Database {db} failed integrity check: {e}")

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

    def run(self):
        print("\n" + "="*50)
        print("  GABRIEL SYSTEM DOCTOR - DIAGNOSTIC SCAN")
        print("="*50 + "\n")
        
        self.check_network()
        self.check_mounts()
        self.check_databases()
        self.check_scanner_process()
        
        print("\n" + "="*50)
        if self.health_score == 100:
            print("  ✅ SYSTEM HEALTH: 100% (PERFECT)")
            print("  No problems detected.")
        else:
            print(f"  ⚠️  SYSTEM HEALTH: {self.health_score}%")
            print("  ISSUES FOUND:")
            for p in self.problems:
                print(f"  - {p}")
        print("="*50 + "\n")

if __name__ == "__main__":
    doc = GabrielDoctor()
    doc.run()
