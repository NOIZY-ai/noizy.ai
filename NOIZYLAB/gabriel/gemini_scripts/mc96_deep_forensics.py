import os
import sys
import struct
import json
import time
import wave
from datetime import datetime

# CONFIGURATION
ROOT_TARGET = "/Volumes/6TB/Sample_Libraries"
OUTPUT_JSON = "/Users/m2ultra/.gemini/mc96_forensics_data.json"
OUTPUT_REPORT = "/Users/m2ultra/.gemini/mc96_reconstruction_plan.md"

print(f"🕵️‍♀️ CB_01 DEEP FORENSICS ACTIVATED")
print(f"🎯 Target: {ROOT_TARGET}")
print(f"⚡️ Mode: MAXIMUM DEPTH (Metadata, Timestamps, Quality Analysis)")

scan_stats = {
    "total_files": 0,
    "processed_files": 0,
    "bext_found": 0,
    "originals_identified": 0,
    "start_time": time.time(),
    "file_registry": {}  # Key: Filename, Value: List of versions (path, size, quality_score)
}

def parse_wav_header(path):
    """Deep parses WAV for BEXT and Format info"""
    info = {"type": "wav", "depth": 0, "rate": 0, "channels": 0, "bext": None}
    try:
        with open(path, 'rb') as f:
            header = f.read(12)
            if header[:4] != b'RIFF' or header[8:12] != b'WAVE':
                return None
            
            while True:
                chunk_header = f.read(8)
                if len(chunk_header) < 8: break
                chunk_id = chunk_header[:4]
                chunk_size = struct.unpack('<I', chunk_header[4:])[0]
                
                if chunk_id == b'fmt ':
                    fmt_data = f.read(min(chunk_size, 40)) # Read enough for basic fmt
                    # AudioFormat(2), NumChannels(2), SampleRate(4), ByteRate(4), BlockAlign(2), BitsPerSample(2)
                    if len(fmt_data) >= 16:
                        info['channels'] = struct.unpack('<H', fmt_data[2:4])[0]
                        info['rate'] = struct.unpack('<I', fmt_data[4:8])[0]
                        info['depth'] = struct.unpack('<H', fmt_data[14:16])[0]
                    # Handle Extended fmt for float etc if needed, but basic 16/24 int is standard
                    remaining = chunk_size - len(fmt_data)
                    if remaining > 0: f.seek(remaining, 1)
                    
                elif chunk_id == b'bext':
                    # Broadcast Wave Extension
                    # Description(256), Originator(32), OrigRef(32), Date(10), Time(8)
                    bext_data = f.read(min(chunk_size, 338))
                    try:
                        info['bext'] = {
                            "description": bext_data[:256].split(b'\0', 1)[0].decode('ascii', errors='ignore').strip(),
                            "originator": bext_data[256:288].split(b'\0', 1)[0].decode('ascii', errors='ignore').strip(),
                            "date": bext_data[320:330].decode('ascii', errors='ignore').strip(),
                            "time": bext_data[330:338].decode('ascii', errors='ignore').strip()
                        }
                    except:
                        pass
                    remaining = chunk_size - len(bext_data)
                    if remaining > 0: f.seek(remaining, 1)
                    
                else:
                    f.seek(chunk_size, 1)
                    
        return info
    except Exception:
        return None

def scan_file(path, filename):
    stats = os.stat(path)
    meta = {
        "path": path,
        "size": stats.st_size,
        "created": stats.st_ctime, # On Unix, ctime is change, birthtime is creation if available
        "modified": stats.st_mtime,
        "ext": os.path.splitext(filename)[1].lower()
    }
    
    # Try to get birthtime (Mac specific)
    try:
        meta["created_birth"] = stats.st_birthtime
    except AttributeError:
        meta["created_birth"] = stats.st_ctime

    # Audio Deep Dive
    if meta['ext'] == '.wav':
        wav_info = parse_wav_header(path)
        if wav_info:
            meta.update(wav_info)
            if wav_info.get("bext"):
                scan_stats["bext_found"] += 1
                
    # Quality Score (Simple Heuristic: BitDepth * Rate)
    # 24bit/48k = 1152 | 16bit/44.1k = 705
    meta["quality_score"] = (meta.get("depth", 0) * meta.get("rate", 0)) if meta.get("depth") else 0
    
    return meta

# EXECUTE SCAN
try:
    for root, dirs, files in os.walk(ROOT_TARGET):
        for file in files:
            path = os.path.join(root, file)
            scan_stats["total_files"] += 1
            
            # Skip likely junk
            if file.startswith("._") or file == ".DS_Store":
                continue
                
            file_data = scan_file(path, file)
            
            # Add to registry
            if file not in scan_stats["file_registry"]:
                scan_stats["file_registry"][file] = []
            scan_stats["file_registry"][file].append(file_data)
            
            scan_stats["processed_files"] += 1
            
            # Progress
            if scan_stats["processed_files"] % 500 == 0:
                 sys.stdout.write(f"\rScanning: {scan_stats['processed_files']}... (BEXT Found: {scan_stats['bext_found']})")
                 sys.stdout.flush()

except KeyboardInterrupt:
    print("\nScan interrupted.")

# ANALYSIS & REPORTING
print("\nGenerated Analysis...")

unique_names = len(scan_stats["file_registry"])
duplicates = scan_stats["processed_files"] - unique_names

report = f"""# 🧬 MC96 FORENSIC RECONSTRUCTION REPORT
**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Target:** `{ROOT_TARGET}`

## 📊 SCAN STATISTICS
- **Total Files Scanned:** {scan_stats['processed_files']}
- **Unique Filenames:** {unique_names}
- **Potential Duplicates/Versions:** {duplicates}
- **Files with BEXT Metadata:** {scan_stats['bext_found']}

## 🏆 HIGHEST QUALITY ORIGINALS IDENTIFIED
*(Files with metadata or high bit-depth indicating master source)*

| Score | Filename | Format | Date | Originator (if found) |
|-------|----------|--------|------|-----------------------|
"""

# Sort by quality score
high_quality = []
for fname, versions in scan_stats["file_registry"].items():
    # Find best version
    best = max(versions, key=lambda x: x["quality_score"])
    if best["quality_score"] > 800: # Higher than CD quality (approx)
        high_quality.append(best)

# Sort strictly by score desc
high_quality.sort(key=lambda x: x["quality_score"], reverse=True)

for item in high_quality[:50]:
    bext = item.get("bext") or {}
    orig = bext.get("originator", "-")
    date_str = bext.get("date", "-")
    # Formatted Date from timestamp if BEXT missing
    if date_str == "-":
        date_str = datetime.fromtimestamp(item["created_birth"]).strftime('%Y-%m-%d')
        
    report += f"| {item['quality_score']} | `{os.path.basename(item['path'])}` | {item.get('depth')}bit/{item.get('rate')}Hz | {date_str} | {orig} |\n"

report += "\n## 🗓️ OLDEST FILES (ARCHAEOLOGY)\n"
# Flatten all files
all_files_flat = [v for versions in scan_stats["file_registry"].values() for v in versions]
all_files_flat.sort(key=lambda x: x["created_birth"])

for item in all_files_flat[:20]:
     d_str = datetime.fromtimestamp(item["created_birth"]).strftime('%Y-%m-%d')
     report += f"- **{d_str}**: `{item['path']}`\n"


with open(OUTPUT_REPORT, "w") as f:
    f.write(report)
    
# Save JSON
# Convert sets to lists etc if needed (none here)
with open(OUTPUT_JSON, "w") as f:
    json.dump(scan_stats["file_registry"], f, default=str)

print(f"\n✅ FORENSICS COMPLETE!")
print(f"📄 Plan: {OUTPUT_REPORT}")
