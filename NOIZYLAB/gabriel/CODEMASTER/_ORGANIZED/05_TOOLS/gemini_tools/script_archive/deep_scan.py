import os
import time
import json
import sys
from datetime import datetime

# Configuration
ROOT_DIR = "/Volumes/6TB/Sample_Libraries"
OUTPUT_FILE = "/Users/m2ultra/.gemini/sample_libraries_index.json"
REPORT_FILE = "/Users/m2ultra/.gemini/scan_report.md"

# Metrics
stats = {
    "total_files": 0,
    "total_size": 0,
    "extensions": {},
    "start_time": time.time(),
    "scan_speed_files_per_sec": 0
}

files_index = []

print(f"🚀 CB_01 DEEP SCAN INITIALIZED FOR: {ROOT_DIR}")
print("⚡️ MODE: GORUNFREE (Maximum Efficiency)")

try:
    for root, dirs, files in os.walk(ROOT_DIR):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                size = os.path.getsize(file_path)
                ext = os.path.splitext(file)[1].lower()
                
                # Stats
                stats["total_files"] += 1
                stats["total_size"] += size
                stats["extensions"][ext] = stats["extensions"].get(ext, 0) + 1
                
                # Index (keeping it lightweight for now, just path/size)
                # files_index.append({"p": file_path, "s": size}) # Uncomment for full indexing if memory allows
                
            except OSError:
                pass
            
        # Progress indicator every 1000 files
        if stats["total_files"] % 1000 == 0:
            elapsed = time.time() - stats["start_time"]
            speed = stats["total_files"] / elapsed if elapsed > 0 else 0
            sys.stdout.write(f"\r📂 Scanned: {stats['total_files']} files | Speed: {speed:.0f} files/s | Size: {stats['total_size']/1024/1024/1024:.2f} GB")
            sys.stdout.flush()

except KeyboardInterrupt:
    print("\n🛑 Scan paused by USER.")

duration = time.time() - stats["start_time"]
stats["scan_speed_files_per_sec"] = stats["total_files"] / duration if duration > 0 else 0

# Generate Report
report = f"""# 📊 CB_01 SCAN REPORT: Sample_Libraries
**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Target:** `{ROOT_DIR}`

## 📈 Summary
- **Total Files:** {stats['total_files']:,}
- **Total Size:** {stats['total_size']/1024/1024/1024:.2f} GB
- **Scan Duration:** {duration:.2f} seconds
- **Scan Speed:** {stats['scan_speed_files_per_sec']:.0f} files/sec

## 📂 File Types (Top 10)
"""

sorted_exts = sorted(stats["extensions"].items(), key=lambda x: x[1], reverse=True)[:10]
for ext, count in sorted_exts:
    report += f"- **{ext or 'No Ext'}**: {count:,}\n"

print(f"\n\n✅ SCAN COMPLETE!")
print(f"📄 Report written to: {REPORT_FILE}")

with open(REPORT_FILE, "w") as f:
    f.write(report)

# Optional: Save full index if needed (memory intensive for millions of files, but fine for thousands)
# with open(OUTPUT_FILE, "w") as f:
#     json.dump(files_index, f)
