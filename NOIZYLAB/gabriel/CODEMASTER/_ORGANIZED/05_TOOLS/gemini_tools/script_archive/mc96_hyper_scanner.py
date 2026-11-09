import os
import struct
import json
import time
from datetime import datetime
import binascii

# CONFIGURATION
ROOT_TARGET = "/Volumes/6TB/Sample_Libraries"
OUTPUT_REPORT = "/Users/m2ultra/.gemini/mc96_hyper_report.md"

print(f"🚀 CB_01 HYPER SCANNER INITIATED")
print(f"🎯 Target: {ROOT_TARGET}")
print("⚡️ Mode: DEEP PACKET INSPECTION (RIFF, LIST, ID3, AIFF chunks)")

stats = {
    "scanned": 0,
    "metadata_found": 0,
    "by_type": {}
}

def parse_riff_info(f, end_offset):
    """Parses RIFF LIST INFO chunks"""
    metadata = {}
    try:
        while f.tell() < end_offset:
            chunk_header = f.read(8)
            if len(chunk_header) < 8: break
            
            chunk_id = chunk_header[:4]
            # Handle padding
            if chunk_id == b'\x00\x00\x00\x00': 
                continue
                
            chunk_size = struct.unpack('<I', chunk_header[4:])[0]
            
            # Common INFO tags
            key = chunk_id.decode('ascii', errors='ignore').strip()
            val_bytes = f.read(chunk_size)
            val = val_bytes.split(b'\0')[0].decode('ascii', errors='ignore').strip()
            
            if val:
                metadata[key] = val
                
            # Align to 2 bytes
            if chunk_size % 2 == 1:
                f.seek(1, 1)
    except:
        pass
    return metadata

def scan_wav(path):
    info = {}
    try:
        with open(path, 'rb') as f:
            header = f.read(12)
            if header[:4] != b'RIFF': return None
            
            file_size = os.path.getsize(path)
            
            while f.tell() < file_size:
                chunk_header = f.read(8)
                if len(chunk_header) < 8: break
                
                chunk_id = chunk_header[:4]
                chunk_size = struct.unpack('<I', chunk_header[4:])[0]
                
                if chunk_id == b'LIST':
                    list_type = f.read(4)
                    if list_type == b'INFO':
                        info.update(parse_riff_info(f, f.tell() - 4 + chunk_size))
                    else:
                        f.seek(chunk_size - 4, 1)
                elif chunk_id == b'id3 ':
                     info['has_id3'] = True
                     f.seek(chunk_size, 1)
                else:
                    f.seek(chunk_size, 1)
    except:
        pass
    return info if info else None

def scan_aiff(path):
    info = {}
    try:
        with open(path, 'rb') as f:
            header = f.read(12)
            if header[:4] != b'FORM': return None
            
            file_size = os.path.getsize(path)
            
            while f.tell() < file_size:
                chunk_header = f.read(8)
                if len(chunk_header) < 8: break
                
                chunk_id = chunk_header[:4]
                chunk_size = struct.unpack('>I', chunk_header[4:])[0]
                
                if chunk_id == b'NAME':
                    info['Title'] = f.read(chunk_size).decode('ascii', errors='ignore').strip()
                elif chunk_id == b'AUTH':
                    info['Artist'] = f.read(chunk_size).decode('ascii', errors='ignore').strip()
                elif chunk_id == b'(c) ':
                    info['Copyright'] = f.read(chunk_size).decode('ascii', errors='ignore').strip()
                elif chunk_id == b'ANNO':
                    info['Annotation'] = f.read(chunk_size).decode('ascii', errors='ignore').strip()
                else:
                    f.seek(chunk_size, 1)
                    
                # Pad byte if odd
                if chunk_size % 2 != 0:
                    f.seek(1, 1)
    except:
        pass
    return info if info else None

found_metadata = []

try:
    for root, dirs, files in os.walk(ROOT_TARGET):
        for file in files:
            path = os.path.join(root, file)
            ext = os.path.splitext(file)[1].lower()
            stats['scanned'] += 1
            
            meta = None
            if ext == '.wav':
                meta = scan_wav(path)
            elif ext in ['.aif', '.aiff']:
                meta = scan_aiff(path)
            
            if meta:
                stats['metadata_found'] += 1
                meta['filename'] = file
                meta['path'] = path
                found_metadata.append(meta) 
                
            if stats['scanned'] % 1000 == 0:
                print(f"Scanned {stats['scanned']}... Found Meta: {stats['metadata_found']}")

except KeyboardInterrupt:
    print("Stopped.")

# REPORT GENERATION
print("\nGenerating Hyper Report...")

report = f"""# 🧠 MC96 HYPER METADATA REPORT
**Date:** {datetime.now()}
**Target:** {ROOT_TARGET}

## 📊 Summary
- **Files Scanned:** {stats['scanned']}
- **Files with Metadata:** {stats['metadata_found']}
- **Success Rate:** {(stats['metadata_found']/stats['scanned']*100 if stats['scanned'] else 0):.1f}%

## 💎 METADATA DISCOVERIES
"""

# Group by Artist/Software/Copyright if possible
artists = {}
softwares = {}

for m in found_metadata:
    # Try to find common keys
    artist = m.get('IART') or m.get('Artist') or m.get('IPRD') # IPRD is product
    soft = m.get('ISFT') or m.get('ICRD') # ISFT Software, ICRD Created Date often has soft info
    copy = m.get('ICOP') or m.get('Copyright')
    
    # Display logic for report
    name = m['filename']
    valid_keys = {k:v for k,v in m.items() if k not in ['filename', 'path'] and v}
    
    if len(valid_keys) > 0:
        report += f"### `{name}`\n"
        for k, v in valid_keys.items():
            report += f"- **{k}:** {v}\n"
        report += "\n"

with open(OUTPUT_REPORT, "w") as f:
    f.write(report)

print(f"✅ HYPER SCAN COMPLETE.")
print(f"📄 Report: {OUTPUT_REPORT}")
