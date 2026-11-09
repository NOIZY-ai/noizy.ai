# 🤖 SYSTEM FILE: find_missing_god_mode.py
# Optimized by Healer Drone

import os

docs_dir = "docs"
print("🔎 SEARCHING FOR NON-COMPLIANT DOCS...")
count = 0
for filename in os.listdir(docs_dir):
    if filename.endswith(".md") and not filename.startswith("CB_01") and "LOG" not in filename:
        path = os.path.join(docs_dir, filename)
        with open(path, 'r') as f:
            content = f.read(100)
            if "GOD MODE SYSTEM" not in content and "ZERO LATENCY" not in content:
                print(f"❌ MISSING HEADER: {filename}")
                count += 1

print(f"Total Missing: {count}")
