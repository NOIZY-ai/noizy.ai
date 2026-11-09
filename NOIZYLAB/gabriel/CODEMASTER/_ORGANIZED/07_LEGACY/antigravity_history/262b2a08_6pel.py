import sqlite3
#!/usr/bin/env python3
import json
import os
from pathlib import Path
from datetime import datetime

# Configuration
DB_PATH = Path("/Users/m2ultra/.gemini/antigravity/playground/infinite-omega/Audio_Unitor/Database/universe.db")
REPORT_PATH = Path("/Users/m2ultra/.gemini/antigravity/playground/infinite-omega/universe_status.html")

# Theme
TITLE = "AUDIO UNIVERSE STATUS"

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>AUDIO UNIVERSE STATUS</title>
    <style>
        body {{ 
            background-color: #050505; 
            color: #00ff9d; 
            font-family: 'Courier New', monospace; 
            margin: 0; 
            padding: 40px; 
            background-image: radial-gradient(circle at 50% 50%, #111 0%, #000 100%);
            min-height: 100vh;
        }}
        h1 {{ 
            font-size: 48px; 
            letter-spacing: 5px; 
            text-shadow: 0 0 10px #00ff9d; 
            margin-bottom: 10px; 
            text-align: center;
        }}
        h2 {{
            font-size: 18px;
            color: #666;
            text-align: center;
            margin-bottom: 40px;
            font-weight: normal;
            letter-spacing: 2px;
        }}
        .grid {{ 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); 
            gap: 20px; 
            max-width: 1200px;
            margin: 0 auto;
        }}
        .card {{ 
            border: 1px solid #333; 
            padding: 25px; 
            background: rgba(10, 10, 10, 0.8); 
            backdrop-filter: blur(5px);
            box-shadow: 0 0 20px rgba(0, 255, 157, 0.05); 
            border-radius: 8px;
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        .card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 0 30px rgba(0, 255, 157, 0.15);
            border-color: #00ff9d;
        }}
        .stat-value {{ 
            font-size: 42px; 
            font-weight: bold; 
            color: #fff; 
            margin-bottom: 5px;
        }}
        .stat-label {{ 
            font-size: 12px; 
            opacity: 0.7; 
            text-transform: uppercase; 
            letter-spacing: 1px;
            color: #888;
        }}
        .bar {{ 
            height: 4px; 
            background: #222; 
            margin-top: 15px; 
            width: 100%; 
            position: relative; 
            border-radius: 2px;
            overflow: hidden;
        }}
        .fill {{ 
            height: 100%; 
            background: linear-gradient(90deg, #00ff9d, #00ccff); 
            width: 0%; 
            box-shadow: 0 0 10px #00ff9d; 
            transition: width 1s ease-out;
        }}
        .log {{ 
            margin-top: 60px; 
            border-top: 1px solid #333; 
            padding-top: 20px; 
            font-size: 12px; 
            color: #444; 
            text-align: center;
        }}
        .blink {{ animation: blink 2s infinite; }}
        @keyframes blink {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0.3; }} }}
        
        .pulse {{ animation: pulse 3s infinite; color: #ff0055; text-shadow: 0 0 10px #ff0055; }}
        @keyframes pulse {{ 0% {{ opacity: 0.8; }} 50% {{ opacity: 1; text-shadow: 0 0 20px #ff0055; }} 100% {{ opacity: 0.8; }} }}

        .focus-text {{ color: #00ccff; text-shadow: 0 0 10px #00ccff; }}
    </style>
</head>

<body>
    <h1>AUDIO UNIVERSE <span class="blink">●</span></h1>
    <h2>SYSTEM STATUS DASHBOARD [v{version}]</h2>
    
    <div class="grid">
        <div class="card">
            <div class="stat-value pulse">{vibe}%</div>
            <div class="stat-label">System Vibe (Relationship)</div>
            <div class="bar"><div class="fill" style="width: {vibe}%; background: #ff0055; box-shadow: 0 0 10px #ff0055;"></div></div>
        </div>

        <div class="card">
            <div class="stat-value focus-text">{focus}</div>
            <div class="stat-label">Current Focus</div>
        </div>

        <div class="card">
            <div class="stat-value">{total_files}</div>
            <div class="stat-label">Indexed Samples</div>
            <div class="bar"><div class="fill" style="width: 100%"></div></div>
        </div>
        
        <div class="card">
            <div class="stat-value">{plugins_count}</div>
            <div class="stat-label">Active Plugins</div>
            <div class="bar"><div class="fill" style="width: {plugins_pct}%"></div></div>
        </div>
        
        <div class="card">
            <div class="stat-value">{memories}</div>
            <div class="stat-label">Total Memories</div>
        </div>

        <div class="card">
            <div class="stat-value">{last_update}</div>
            <div class="stat-label">Last Database Sync</div>
        </div>
    </div>
    
    <div class="log">
        SYSTEM ID: MC96-OMEGA-TURBO<br>
        LOC: {location}<br>
        STATUS: OPTIMAL
    </div>
</body>
</html>
"""

def generate_report():
    print(f"Generating Visual Report...")
    
    conn = sqlite3.connect(str(DB_PATH))
    c = conn.cursor()
    
    # 1. Vibe & Focus
    vibe = 50
    focus = "STANDBY"
    try:
        # Try finding the Covenant Cell first
        c.execute("SELECT id FROM memcells WHERE topic LIKE '%COVENANT%'")
        res = c.fetchone()
        cid = res[0] if res else 0
        
        if cid:
             c.execute("SELECT vibe_score, content FROM memory_events WHERE cell_id=? ORDER BY timestamp DESC LIMIT 1", (cid,))
             row = c.fetchone()
             if row:
                 vibe = row[0]
                 # Focus usually comes from Goals, but lets use last content if short
                 focus_text = row[1]
                 focus = (focus_text[:15] + '..') if len(focus_text) > 15 else focus_text
    except: pass
    
    # 2. Stats
    total_files = 0
    try:
        c.execute("SELECT COUNT(*) FROM memory_events WHERE event_type='FILE_INDEX'") # Hypothetical
        total_files = c.fetchone()[0]
    except: pass # Table might not exist yet if scanned by Singularity vs Oracle. 
                 # Actually Singularity tracks 'provenance', let's sum that.
    try:
        c.execute("SELECT COUNT(*) FROM provenance")
        total_files = c.fetchone()[0]
    except: pass
    
    plugins = 0
    try:
        # Assuming we have an 'instruments' or 'assets' table, or just counting memcells of type 'software'?
        # Let's count keys in 'provenance' that are plugins?
        # Or if we ran turbo_seed.py, we might have a table.
        # Let's check for 'soft_instruments' table from seed, or 'memcells'?
        # We will assume a 'assets' table or similar if we build it.
        # For now, let's just count 'provenance' where final_path ends in vst/component
        c.execute("SELECT COUNT(*) FROM provenance WHERE final_path LIKE '%.vst%' OR final_path LIKE '%.component%'")
        plugins = c.fetchone()[0]
        
        # Also check separate table if seeded
        try:
           c.execute("SELECT COUNT(*) FROM plugins") # Future proofing
           plugins += c.fetchone()[0]
        except: pass
    except: pass
    
    # 3. Memory Count
    memories = 0
    try:
        c.execute("SELECT COUNT(*) FROM memory_events")
        memories = c.fetchone()[0]
    except: pass
    
    conn.close()
    
    # Calculations
    plugins_pct = min(100, (plugins / 200) * 100) # Arbitrary goal
    
    html = HTML_TEMPLATE.format(
        version="2.0-TURBO",
        vibe=vibe,
        focus=focus,
        total_files=f"{total_files:,}",
        plugins_count=plugins,
        plugins_pct=plugins_pct,
        memories=f"{memories:,}",
        last_update=datetime.now().strftime("%H:%M:%S"),
        location=str(DB_PATH)
    )
    
    with open(REPORT_PATH, 'w') as f:
        f.write(html)
        
    print(f"✅ Report Generated: {REPORT_PATH}")

if __name__ == "__main__":
    generate_report()
