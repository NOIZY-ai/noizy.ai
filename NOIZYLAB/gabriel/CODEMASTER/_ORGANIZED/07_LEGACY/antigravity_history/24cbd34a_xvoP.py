import json
import os
from datetime import datetime

INDEX_PATH = "/Users/m2ultra/.gemini/antigravity/playground/infinite-omega/Audio_Unitor/Database/oracle_index.json"
REPORT_PATH = "/Users/m2ultra/.gemini/antigravity/playground/infinite-omega/universe_status.html"

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>AUDIO UNIVERSE STATUS</title>
    <style>
        body { background-color: #050505; color: #00ff9d; font-family: 'Courier New', monospace; margin: 0; padding: 40px; }
        h1 { font-size: 48px; letter-spacing: 5px; text-shadow: 0 0 10px #00ff9d; margin-bottom: 20px; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }
        .card { border: 1px solid #333; padding: 20px; background: #0a0a0a; box-shadow: 0 0 15px rgba(0, 255, 157, 0.1); }
        .stat-value { font-size: 36px; font-weight: bold; color: #fff; }
        .stat-label { font-size: 14px; opacity: 0.7; text-transform: uppercase; }
        .bar { height: 4px; background: #333; margin-top: 10px; width: 100%; position: relative; }
        .fill { height: 100%; background: #00ff9d; width: 0%; box-shadow: 0 0 10px #00ff9d; }
        .log { margin-top: 40px; border-top: 1px solid #333; padding-top: 20px; font-size: 12px; color: #666; }
        .blink { animation: blink 1s infinite; }
        @keyframes blink { 50% { opacity: 0; } }
    </style>
</head>
<body>
    <h1>UNIVERSE STATUS <span class="blink">●</span></h1>
    
    <div class="grid">
        <div class="card">
            <div class="stat-value">{total_files}</div>
            <div class="stat-label">Indexed Samples</div>
            <div class="bar"><div class="fill" style="width: 100%"></div></div>
        </div>
        
        <div class="card">
            <div class="stat-value">{tagged_count}</div>
            <div class="stat-label">Intelligent Tags</div>
             <div class="bar"><div class="fill" style="width: {tag_pct}%"></div></div>
        </div>
        
        <div class="card">
            <div class="stat-value">{last_scan}</div>
            <div class="stat-label">Last Orbital Scan</div>
        </div>
        
        <div class="card">
            <div class="stat-value">{key_stat}</div>
            <div class="stat-label">Keys Identified</div>
        </div>
    </div>
    
    <div class="log">
        SYSTEM ID: MC96-OMEGA<br>
        LOC: /Users/m2ultra/.gemini/antigravity<br>
        STATUS: OPTIMAL
    </div>
</body>
</html>
"""

def generate_report():
    try:
        with open(INDEX_PATH, 'r') as f:
            data = json.load(f)
    except:
        print("❌ Database not found")
        return

    files = data.get('files', [])
    tags = data.get('tags', {})
    meta = data.get('meta', {})
    
    count = len(files)
    tagged = len(tags)
    tag_pct = (tagged / count * 100) if count > 0 else 0
    
    # Intelligence Stats
    keys_found = sum(1 for t in tags.values() if 'key' in t)

    html = HTML_TEMPLATE.format(
        total_files=f"{count:,}",
        tagged_count=f"{tagged:,}",
        tag_pct=f"{tag_pct:.1f}",
        last_scan=meta.get('last_scan', 'Unknown').split('.')[0],
        key_stat=f"{keys_found:,}"
    )
    
    with open(REPORT_PATH, 'w') as f:
        f.write(html)
        
    print(f"📄 Report Generated: {REPORT_PATH}")
    # os.system(f"open {REPORT_PATH}") # Auto-open? Maybe let user decide.

if __name__ == "__main__":
    generate_report()
