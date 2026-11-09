
import sqlite3
from pathlib import Path
import time

DB_PATH = Path("NOIZYLAB_DB/visual_index.db")

def optimize():
    print(f"🚀 OPTIMIZING DATABASE: {DB_PATH}")
    if not DB_PATH.exists():
        print("❌ DB not found.")
        return

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # 1. Add Indices for Common Lookups
    indices = [
        ("idx_filename", "filename"),
        ("idx_media_type", "media_type"),
        ("idx_volume", "volume"),
        ("idx_mtime", "mtime")
    ]
    
    print("  Adding Indices...")
    for idx_name, col in indices:
        try:
            print(f"    - {idx_name} on {col}...")
            c.execute(f"CREATE INDEX IF NOT EXISTS {idx_name} ON assets({col})")
        except Exception as e:
            print(f"      Create failed: {e}")

    # 2. Add Composite Index for Filtering
    try:
        print("    - idx_search (media_type + filename)...")
        c.execute("CREATE INDEX IF NOT EXISTS idx_search ON assets(media_type, filename)")
    except: pass

    # 3. VACUUM (Defrag)
    print("  🧹 Vacuuming (Defrag)...")
    c.execute("VACUUM")
    
    conn.commit()
    conn.close()
    print("✅ OPTIMIZATION COMPLETE. GORUNFREE!!")

if __name__ == "__main__":
    optimize()
