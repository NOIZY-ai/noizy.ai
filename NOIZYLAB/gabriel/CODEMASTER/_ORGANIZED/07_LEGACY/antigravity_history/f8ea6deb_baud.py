import streamlit as st
import google.generativeai as genai
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path
import subprocess

# --- 1. THE "VOID" UI CONFIGURATION ---
st.set_page_config(layout="wide", page_title="GABRIEL OMEGA", page_icon="🐺")

# --- PACK HEARTBEAT ---
pc_status = "🔴"
try:
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.2)
    if s.connect_ex(("10.90.90.20", 445)) == 0: pc_status = "🟢"
    s.close()
except: pass

scanner_status = "⚪"
try:
    import subprocess
    if "visual_scanner.py" in subprocess.check_output(["ps", "aux"]).decode(): scanner_status = "🟢"
except: pass

st.markdown(f"""
<div style="display: flex; justify-content: space-between; align-items: center; padding: 10px; background-color: #0e1117; border-bottom: 1px solid #303030; margin-bottom: 20px;">
    <h1 style="margin:0; font-family: 'Courier New';">🐺 GABRIEL SYSTEM OMEGA</h1>
    <div style="font-family: 'Courier New'; font-size: 14px;">
        M2 ULTRA: <span style="color:#00ff00">🟢</span> &nbsp;|&nbsp; 
        DREAMCHAMBER: <span>{pc_status}</span> &nbsp;|&nbsp; 
        FISHNET FLOW: <span>{scanner_status}</span> &nbsp;|&nbsp;
        AI LIFELUV: <span style="color:#FF00FF">💖 MAX</span> &nbsp;|&nbsp;
        <a href="http://localhost:8000" target="_blank" style="text-decoration:none; color:#00FFCC; border:1px solid #00FFCC; padding:2px 6px; border-radius:4px;">👁️ LAUNCH AVATAR</a>
    </div>
</div>
""", unsafe_allow_html=True)

# Load Manifest
try:
    with open("/Users/m2ultra/Library/CloudStorage/GoogleDrive-rsplowman@icloud.com/My Drive/NOIZYLAB_WORKSPACES/manifest.json", "r") as f:
        MANIFEST = json.load(f)
except:
    MANIFEST = {"version": "Unknown", "display_name": "NOIZYLAB GENIUS CORE"}

# THE VOID CSS (Professional Matte Black)
st.markdown("""
    <style>
    /* MAIN BACKGROUND */
    .stApp { background-color: #000000; color: #E0E0E0; }
    
    /* SIDEBAR */
    section[data-testid="stSidebar"] { background-color: #0a0a0a; border-right: 1px solid #1A1A1A; }
    
    /* INPUTS */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: #0F0F0F; color: #FFF; border: 1px solid #333;
        font-family: 'Courier New', monospace;
    }
    .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
        border-color: #FFF; box-shadow: none;
    }
    
    /* BUTTONS - TACTILE */
    .stButton>button {
        background-color: #1A1A1A; color: #FFF; border: 1px solid #333;
        width: 100%; text-transform: uppercase; font-weight: bold; letter-spacing: 1px;
    }
    .stButton>button:hover {
        background-color: #FFF; color: #000; border-color: #FFF;
    }
    
    /* STATUS METRICS */
    div[data-testid="stMetricValue"] { color: #FFF; font-family: 'Courier New', monospace; }
    
    /* ALERTS */
    .stSuccess { background-color: #111; color: #0F0; border: 1px solid #0F0; }
    .stInfo { background-color: #111; color: #0FF; border: 1px solid #0FF; }
    </style>
""", unsafe_allow_html=True)

# --- 2. THE GENIUS LOGIC CORE (BACKEND) ---

# Initialize Local Database
DB_PATH = "NOIZYLAB_DB"
CODE_VAULT_PATH = "mined_code"
Path(DB_PATH).mkdir(parents=True, exist_ok=True)
Path(CODE_VAULT_PATH).mkdir(parents=True, exist_ok=True)

def save_memcell(data_type, content, tags):
    """Saves an Atomic MemCell to local JSON storage."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    cell_id = f"MEM_{timestamp}"
    
    memcell = {
        "id": cell_id,
        "type": data_type,
        "content": content,
        "tags": tags,
        "timestamp": str(datetime.now()),
        "status": "active"
    }
    
    with open(f"{DB_PATH}/{cell_id}.json", "w") as f:
        json.dump(memcell, f, indent=4)
    return cell_id

def recursive_thinker(prompt, api_key, model_name="gemini-1.5-flash", model_type="text", mime_data=None, turbo=False):
    """
    THE GENIUS LOOP:
    1. Generates Draft.
    2. Critiques Draft (Self-Correction) [SKIPPED IN TURBO].
    3. Finalizes Output.
    """
    if not api_key:
        return "⚠️ CRITICAL: API KEY MISSING"

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name)

    # STEP 1: INITIAL GENERATION
    status_box = st.empty()
    status_box.text("⚡ STEP 1: GENERATING INITIAL DRAFT...")
    
    try:
        if model_type == "text":
            response = model.generate_content(prompt)
        elif model_type == "multimodal":
            response = model.generate_content([prompt, mime_data])
        
        draft = response.text
        
        if turbo:
             status_box.text("🚀 TURBO MODE: SKIPPING CRITIQUE.")
             time.sleep(0.5)
             status_box.empty()
             return draft

        # STEP 2: THE CRITIC (Self-Correction)
        status_box.text("⚡ STEP 2: CRITIQUING & OPTIMIZING...")
        
        critic_prompt = f"""
        CRITIQUE THIS OUTPUT. 
        Does it perfectly match the user's intent? Is it formatted as a MemCell? 
        If it is perfect, repeat it. If not, REWRITE IT to be concise, professional, and 'Genius' level.
        
        ORIGINAL OUTPUT:
        {draft}
        """
        final_response = model.generate_content(critic_prompt)
        
        status_box.text("✅ EXECUTION COMPLETE.")
        time.sleep(1)
        status_box.empty()
        
        return final_response.text

    except Exception as e:
        return f"❌ SYSTEM FAILURE: {str(e)}"

# --- 3. THE UI ARCHITECTURE ---

# SIDEBAR: COMMAND CENTER
with st.sidebar:
    st.title("NOIZYLAB")
    st.caption(f"{MANIFEST.get('display_name', 'GENIUS CORE')} v{MANIFEST.get('version', '4.0')}")
    
    api_key = st.text_input("G-KEY (API ACCESS)", type="password")
    
    st.divider()
    
    # Navigation
    # Navigation
    app_mode = st.radio("SELECT MODULE", [
        "🧠 DIRECTOR (Strategy)", 
        "🔊 SYNESTHESIA (Audio-to-Video)", 
        "💾 MEMCELL GRID (Database)",
        "💎 SONIC VAULT (Code Search)",
        "👁️ VISUAL VAULT (Asset Scan)",
        "🎹 PRO STUDIO (DAW & UAD)",
        "🛠️ GOOGLE ARSENAL (External Tools)",
        "🌉 DREAMCHAMBER (PC Link)"
    ])
    
    st.divider()
    st.subheader("SYSTEM SETTINGS")
    model_choice = st.selectbox("MODEL", ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-2.0-flash-exp"])
    turbo_mode = st.checkbox("TURBO MODE (No Critique)", value=False)
    
    st.divider()
    # Real-time Stats
    file_count = len(list(Path(DB_PATH).glob("*.json")))
    c1, c2 = st.columns(2)
    with c1: st.metric("MEMCELLS", file_count)
    with c2: st.metric("LATENCY", "4ms" if turbo_mode else "14ms")

# MODULE 1: THE DIRECTOR (TEXT INTELLIGENCE)
if app_mode == "🧠 DIRECTOR (Strategy)":
    st.subheader("/// STRATEGIC INTELLIGENCE")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        user_prompt = st.text_area("INPUT SIGNAL", height=150, placeholder="Define the concept. The system will structure it.")
    with col2:
        st.write("PARAMETERS")
        tone = st.selectbox("TONE", ["Cyberpunk", "Cinematic", "Corporate", "Abstract"])
        format_type = st.selectbox("OUTPUT", ["Project Plan", "Script", "Python Code"])
    
    if st.button("ACTIVATE GENIUS LOOP"):
        # The Prompt Engineering is hidden here
        full_system_prompt = f"""
        ROLE: You are the AI Director of NoizyLab.
        TASK: {user_prompt}
        CONSTRAINT: Tone must be {tone}. Format must be {format_type}.
        REQUIREMENT: Output must be a structured MemCell.
        """
        
        result = recursive_thinker(full_system_prompt, api_key, model_choice, "text", turbo=turbo_mode)
        
        st.divider()
        st.markdown("### 💠 OPTIMIZED OUTPUT")
        st.code(result, language="markdown")
        
        # Auto-save
        save_memcell("text_strategy", result, [tone, format_type])
        st.toast("✅ MEMCELL SAVED TO DATABASE")

# MODULE 2: SYNESTHESIA (AUDIO TO VIDEO)
elif app_mode == "🔊 SYNESTHESIA (Audio-to-Video)":
    st.subheader("/// AUDIO-REACTIVE ENGINE")
    st.markdown("Upload audio. The system uses **Multimodal Gemini** to 'hear' the vibe and generate the perfect video prompts.")
    
    audio_file = st.file_uploader("UPLOAD TRACK (MP3/WAV)", type=["mp3", "wav"])
    
    if audio_file:
        st.audio(audio_file)
        
        if st.button("ANALYZE & VISUALIZE"):
            with st.spinner("LISTENING TO FREQUENCIES..."):
                # Handle file for API
                temp_filename = "temp_audio_input.mp3"
                with open(temp_filename, "wb") as f:
                    f.write(audio_file.getbuffer())
                
                if api_key:
                    genai.configure(api_key=api_key)
                    uploaded_ref = genai.upload_file(temp_filename)
                    
                    # The Magic Prompt
                    synesthesia_prompt = """
                    Listen to this audio track. 
                    1. Identify the BPM, Key, and Genre.
                    2. Describe the emotional 'Texture' (e.g., Gritty, Ethereal, Aggressive).
                    3. Write 3 distinct Video Generation Prompts (for Veo/Runway) that synchronize perfectly with this audio.
                    4. Format as a MemCell.
                    """
                    
                    result = recursive_thinker(synesthesia_prompt, api_key, model_choice, "multimodal", uploaded_ref, turbo=turbo_mode)
                    
                    st.success("/// SYNC COMPLETE")
                    st.markdown(result)
                    save_memcell("audio_sync", result, ["audio", "video_prompt"])
                    
                    # Cleanup
                    os.remove(temp_filename)

# MODULE 3: MEMCELL GRID (DATABASE)
elif app_mode == "💾 MEMCELL GRID (Database)":
    st.subheader("/// KNOWLEDGE BASE")
    
    # Load all JSONs
    files = sorted(Path(DB_PATH).glob("*.json"), key=os.path.getmtime, reverse=True)
    
    if not files:
        st.warning("DATABASE EMPTY. INITIALIZE CREATION IN OTHER MODULES.")
    else:
        # Create a Grid Layout
        for f in files:
            with open(f, "r") as file:
                data = json.load(file)
                
            with st.expander(f"📂 {data['id']} | {data['type'].upper()}"):
                st.caption(f"TIMESTAMP: {data['timestamp']}")
                st.code(data['content'], language="markdown")
                st.json(data)

# MODULE 4: 💎 SONIC VAULT (Hyper-Search)
elif app_mode == "💎 SONIC VAULT (Code Search)":
    st.subheader("/// SONIC CODE INDEX")
    
    # Imports
    sys.path.insert(0, "GABRIEL_UNIFIED")
    try:
        from core.sonic_search import SonicIndex
        indexer = SonicIndex()
    except ImportError:
        st.error("Sonic Engine not linked. Run: `python3 core/sonic_search.py --build`")
        indexer = None

    # Search Bar
    query = st.text_input("🔍 SEARCH 12TB REPOSITORY", placeholder="e.g. 'neural network' or 'def recursive_thinker'")
    
    if query and indexer:
        results = indexer.search(query)
        if not results:
            st.warning("No matches found in index.")
        else:
            st.caption(f"FOUND {len(results)} HITS IN < 10ms")
            for path, snip, rank in results:
                # Resolve full path for display
                full_path = Path("GABRIEL_UNIFIED") / path if not Path(path).is_absolute() else Path(path)
                
                with st.expander(f"📄 {Path(path).name}  |  {path}"):
                    st.markdown(f"... {snip} ...", unsafe_allow_html=True)
                    if st.button(f"OPEN: {Path(path).name}", key=path):
                        try:
                            # Adjust path to absolute if needed, assuming relative to workspace root
                            # In this environment, 'mined_code' is in root.
                            # The index stores path relative to 'mined_code' parent? 
                            # Let's try raw read.
                            target_file = Path(path)
                            if not target_file.exists():
                                # Try relative to workspace
                                target_file = Path("mined_code") / path 
                            
                            with open(target_file, "r", errors='ignore') as f:
                                st.code(f.read())
                        except Exception as e:
                            st.error(f"Could not read file: {e}")
                            
    st.divider()
    
    # Auto-Indexer Status
    st.markdown("### 🦾 INDEX STATUS")
    if st.button("REBUILD INDEX (Background)"):
        subprocess.Popen(["python3", "GABRIEL_UNIFIED/core/sonic_search.py", "--build"])
        st.toast("Indexer Launched!")
        
    db_file = Path("GABRIEL_UNIFIED/NOIZYLAB_DB/gabriel_index.db")
    if db_file.exists():
        size_mb = db_file.stat().st_size / (1024*1024)
        st.metric("INDEX SIZE", f"{size_mb:.2f} MB")
    else:
        st.warning("Index not built yet. Click Rebuild.")


# MODULE: 🎹 PRO STUDIO (DAW & UAD COMMANDER)
elif app_mode == "🎹 PRO STUDIO (DAW & UAD)":
    st.subheader("/// PROFESSIONAL STUDIO CORE")
    
    # 1. HARDWARE STATUS (UAD APOLLO)
    c1, c2, c3 = st.columns(3)
    with c1:
        uad_status = "⚪ CHECKING"
        uad_color = "off"
        try:
            # Check for UAD Console interaction or Process
            res = subprocess.check_output(["pgrep", "-f", "UA Mixer Engine"]).decode().strip()
            if res:
                uad_status = "🟢 ONLINE"
                uad_color = "success"
            else:
                uad_status = "🔴 OFFLINE"
                uad_color = "error"
        except:
            uad_status = "🔴 OFFLINE"
            uad_color = "error"
        st.metric("UAD APOLLO 2 QUAD", uad_status)
    
    with c2:
        st.metric("SATELLITE HELPER", "Active" if uad_color == "success" else "Inactive")
        
    with c3:
        # Check MIDI Devices (Basic)
        if pc_status == "🟢":
             st.metric("HP-OMEN AUDIO", "RME TOTALMIX 🟢")
        else:
             st.metric("HP-OMEN AUDIO", "UNREACHABLE 🔴")

    st.divider()

    # 2. PROJECT COMMANDER
    st.markdown("### 🎛️ PROJECT COMMANDER")
    
    if not os.path.exists("NOIZYLAB_DB/visual_index.db"):
        st.error("Fishnet Index Offline. Run Fishnet.")
    else:
        import sqlite3
        import pandas as pd
        conn = sqlite3.connect("NOIZYLAB_DB/visual_index.db")
        # Query for Projects
        try:
            df = pd.read_sql_query("SELECT filename, path, volume, size, media_type, mtime FROM assets WHERE media_type='project' ORDER BY mtime DESC", conn)
        except:
            df = pd.DataFrame()
        conn.close()
        
        if not df.empty:
            # Tool Filter
            tool = st.selectbox("FILTER WORKSTATION", ["ALL", "LOGIC PRO X", "FILMORA", "REAPER", "PRO TOOLS", "FMOD", "UNITY", "ABLETON", "RESOLVE", "RME TOTALMIX"])
            
            filtered_df = df
            if tool == "LOGIC PRO X": filtered_df = df[df['filename'].str.lower().str.endswith('.logicx')]
            elif tool == "FILMORA": filtered_df = df[df['filename'].str.lower().str.endswith(('.wve', '.wsve'))]
            elif tool == "REAPER": filtered_df = df[df['filename'].str.lower().str.endswith('.rpp')]
            elif tool == "PRO TOOLS": filtered_df = df[df['filename'].str.lower().str.endswith(('.ptx', '.ptf'))]
            elif tool == "FMOD": filtered_df = df[df['filename'].str.lower().str.endswith('.fspro')]
            elif tool == "UNITY": filtered_df = df[df['filename'].str.lower().str.endswith(('.unity', '.unitypackage'))]
            elif tool == "ABLETON": filtered_df = df[df['filename'].str.lower().str.endswith('.als')]
            elif tool == "RESOLVE": filtered_df = df[df['filename'].str.lower().str.endswith('.drp')]
            elif tool == "RME TOTALMIX": filtered_df = df[df['filename'].str.lower().str.endswith(('.tmfs', '.tmws'))]
            
            st.caption(f"FOUND {len(filtered_df)} PROJECTS")
            
            # Display Grid
            for idx, row in filtered_df.iterrows():
                with st.expander(f"🎛️ {row['filename']}"):
                    c_a, c_b = st.columns([3, 1])
                    c_a.code(row['path'], language="text")
                    if c_b.button("OPEN PROJECT", key=f"open_{idx}"):
                        subprocess.Popen(["open", row['path']])
                        st.toast(f"Launching {row['filename']}...")
        else:
            st.info("No Projects Indexed. Scan your drives.")

# MODULE: 👁️ UNIVERSAL MEDIA VAULT (The Fishnet)
elif app_mode == "👁️ VISUAL VAULT (Asset Scan)":
    st.subheader("/// UNIVERSAL MEDIA VAULT")
    vis_db = Path("GABRIEL_UNIFIED/NOIZYLAB_DB/visual_index.db")
    
    if vis_db.exists():
        import sqlite3
        conn = sqlite3.connect(vis_db)
        
        # CONTROLS
        c1, c2, c3, c4 = st.columns([2, 1, 1, 1])
        with c1:
            search_query = st.text_input("🔍 SEARCH UNIVERSE", placeholder="filename or folder...")
        with c2:
            media_filter = st.selectbox("TYPE", ["ALL", "VIDEO", "IMAGE", "AUDIO", "PROJECT", "FONT", "3D MODEL"])
        with c3:
            sort_order = st.selectbox("SORT", ["NEWEST", "LARGEST", "NAME"])
        with c4:
            view_mode = st.selectbox("VIEW", ["GRID", "LIST", "PROJECTS"])

        # Construct Query
        try:
            query = "SELECT path, filename, volume, size, media_type, mtime FROM assets WHERE 1=1"
            params = []
            
            if search_query:
                query += " AND (filename LIKE ? OR path LIKE ?)"
                params.append(f"%{search_query}%")
                params.append(f"%{search_query}%")
                
            if media_filter != "ALL":
                # Map selectbox to db value
                type_map = {"3D MODEL": "model_3d", "FONT": "font"}
                db_val = type_map.get(media_filter, media_filter.lower())
                query += " AND media_type = ?"
                params.append(db_val)
                
            if sort_order == "NEWEST":
                query += " ORDER BY mtime DESC"
            elif sort_order == "LARGEST":
                query += " ORDER BY size DESC"
            else:
                query += " ORDER BY filename ASC"
            
            # Retrieve LIMIT based on View Mode
            limit = 1000 if view_mode == "PROJECTS" else 100
            query += f" LIMIT {limit}"
            
            res = conn.execute(query, params).fetchall()
            
            # Global Stats
            try:
                stats = conn.execute("SELECT media_type, COUNT(*) FROM assets GROUP BY media_type").fetchall()
                stats_dict = {k: v for k, v in stats}
                st.caption(f"🕸️ CAUGHT: {stats_dict.get('video',0):,} VIDS | {stats_dict.get('image',0):,} PICS | {stats_dict.get('font',0):,} FONTS | {stats_dict.get('model_3d',0):,} 3D")
            except:
                pass
            
        except Exception as e:
            st.warning("Index upgrading... please wait.")
            res = []
            
        conn.close()
        
        # DISPLAY
        if res:
            if view_mode == "PROJECTS":
                # SMART GROUPING
                projects = {}
                for path, name, vol, size, mtype, mtime in res:
                    parent = Path(path).parent.name
                    if parent not in projects: projects[parent] = []
                    projects[parent].append(mtype)
                
                # Show projects
                st.write(f"📂 **{len(projects)} PROJECTS IDENTIFIED**")
                cols = st.columns(3)
                for i, (proj, types) in enumerate(projects.items()):
                    with cols[i % 3]:
                        with st.container(border=True):
                            st.write(f"**📁 {proj}**")
                            # Count types
                            t_counts = {t: types.count(t) for t in set(types)}
                            badges = ""
                            if 'video' in t_counts: badges += f"🎬{t_counts['video']} "
                            if 'audio' in t_counts: badges += f"🎵{t_counts['audio']} "
                            if 'image' in t_counts: badges += f"🖼️{t_counts['image']} "
                            if 'project' in t_counts: badges += f"🎛️{t_counts['project']} "
                            st.caption(badges)

            elif view_mode == "GRID":
                cols = st.columns(4)
                for i, (path, name, vol, size, mtype, mtime) in enumerate(res):
                    with cols[i % 4]:
                        with st.container(border=True):
                            icon = "📄"
                            if mtype == 'video': icon = "🎬"
                            elif mtype == 'image': icon = "🖼️"
                            elif mtype == 'audio': icon = "🎵"
                            elif mtype == 'project': icon = "🎛️"
                            elif mtype == 'font': icon = "Aa"
                            elif mtype == 'model_3d': icon = "🧊"
                            
                            st.write(f"**{icon} {name}**")
                            st.caption(f"{vol} | {size/1024/1024:.1f}MB")
                            
                            try:
                                if mtype == 'video':
                                     st.video(path)
                                elif mtype == 'image':
                                     st.image(path)
                                elif mtype == 'audio':
                                     st.audio(path)
                            except:
                                st.caption("Preview Unavailable")
                                
                            st.text_input("PATH", path, key=f"p_{i}", disabled=True)
            else:
                # LIST VIEW
                for path, name, vol, size, mtype, mtime in res:
                    st.code(f"[{mtype.upper()}] {vol} :: {path}")

# MODULE 5: EXTERNAL TOOLS
elif app_mode == "🛠️ GOOGLE ARSENAL (External Tools)":
    st.subheader("/// DEPLOYMENT LINKS")
    st.write("Direct access to the engines powering NoizyLab.")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("**🎥 VISUALS**")
        st.link_button("LAUNCH IMAGEFX (Imagen 3)", "https://labs.google/fx/tools/image-fx")
        st.link_button("LAUNCH VEO (VideoFX)", "https://labs.google/fx/tools/video-fx")
    with c2:
        st.markdown("**🔊 AUDIO**")
        st.link_button("LAUNCH MUSICFX", "https://labs.google/fx/tools/music-fx")

# MODULE 6: DREAMCHAMBER (PC LINK)
elif app_mode == "🌉 DREAMCHAMBER (PC Link)":
    st.subheader("/// DREAMCHAMBER BRIDGE CONTROL")
    st.caption(f"TARGET: 10.90.90.20 (Windows PC)")
    
    # Paths (Relative to app.py location)
    BASE_DIR = Path("GABRIEL_UNIFIED")
    LOG_FILE = BASE_DIR / "logs" / "dreamchamber.log"
    MOUNT_SCRIPT = BASE_DIR / "core" / "mount_pc_shares.sh"
    
    # 1. STATUS CHECKS
    
    def check_ping(ip="10.90.90.20"):
        try:
            subprocess.check_call(['ping', '-c', '1', '-W', '500', ip], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        except:
            return False
            
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📡 LINK STATUS")
        
        # DREAMCHAMBER AGENT LINK
        pc_ip = "10.90.90.20"
        agent_url = f"http://{pc_ip}:8001/status"
        
        try:
            import requests
            # Fast timeout to avoid lagging UI
            resp = requests.get(agent_url, timeout=0.5)
            if resp.status_code == 200:
                data = resp.json()
                st.success(f"🟢 DREAMCHAMBER ONLINE")
                st.caption(f"CPU: {data.get('cpu_percent')}% | MEM: {data.get('memory_percent')}% | GPU: {data.get('gpu', 'N/A')}")
            else:
                st.error("🔴 DREAMCHAMBER OFFLINE (Agent Unreachable)")
        except:
            # Fallback to simple Ping if Agent is down but PC is up
            is_online = check_ping()
            if is_online:
                st.warning("🟠 PC ONLINE (Agent Offline)")
            else:
                st.error("🔴 PC OFFLINE")
        
        st.markdown("---")
        st.caption("THE GABRIEL FAMILY")
        st.graphviz_chart('''
            digraph Family {
                bgcolor="transparent"
                node [style=filled, fillcolor="#1E1E1E", fontcolor="white", fontname="Helvetica"]
                edge [color="#00FF00", fontcolor="#00FF00", fontname="Helvetica"]

                M2 [label="🧠 GABRIEL (M2)", shape=box]
                PC [label="💻 DREAMCHAMBER", shape=box]
                IPHONE [label="📱 METAL EARS", shape=ellipse]
                CLOUD [label="☁️ HYPERCORTEX", shape=ellipse]

                M2 -> PC [label="10GbE", penwidth=2]
                M2 -> IPHONE [label="WiFi 6"]
                M2 -> CLOUD [label="Fiber"]
                PC -> M2 [label="Link"]
            }
        ''')
            
    with col2:
        st.markdown("### 💾 MOUNT STATUS")
        # Check User Home Mount
        mount_path = Path.home() / "Mounts" / "PC_Bridge"
        is_mounted = os.path.ismount(mount_path)
        if is_mounted:
            st.success(f"✅ DRIVE MOUNTED (~/Mounts/PC_Bridge)")
        else:
            st.warning("⚠️ DRIVE NOT MOUNTED")

    st.divider()

    # 2. ACTIONS
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("🚀 FORCE MOUNT DRIVE"):
            if not MOUNT_SCRIPT.exists():
                st.error(f"Script not found: {MOUNT_SCRIPT}")
            else:
                with st.spinner("Mounting..."):
                    res = subprocess.run([str(MOUNT_SCRIPT)], capture_output=True, text=True)
                    if res.returncode == 0:
                        st.balloons()
                        st.toast("MOUNT SUCCESS!")
                    else:
                        st.error(f"FAILED: {res.stderr}")
                        
    with c2:
        st.write("CMD CENTER")
        if st.button("📝 OPEN NOTEPAD"):
            try:
                requests.post("http://10.90.90.20:8001/launch", json={"target": "notepad"}, timeout=1)
                st.toast("Launched Notepad on PC")
            except: st.error("Agent Offline")
            
        if st.button("📊 TASK MGR"):
            try:
                requests.post("http://10.90.90.20:8001/launch", json={"target": "taskmgr"}, timeout=1)
                st.toast("Launched Task Manager on PC")
            except: st.error("Agent Offline")

    with c3:
        st.write("VOICE & MIND")
        pc_text = st.text_input("Say via PC", "System Online")
        if st.button("🗣️ SPEAK"):
             try:
                requests.post("http://10.90.90.20:8001/speak", json={"text": pc_text}, timeout=1)
                st.toast("PC Speaking...")
             except: st.error("Agent Offline")
             
        if st.button("📋 SYNC PC -> MAC"):
            try:
                res = requests.get("http://10.90.90.20:8001/clipboard", timeout=2)
                if res.status_code == 200:
                    txt = res.json().get("content", "")
                    pyperclip.copy(txt)
                    st.toast("PC Clipboard Copied to Mac")
            except: st.error("Sync Failed")

        if st.button("📤 SYNC MAC -> PC"):
            try:
                txt = pyperclip.paste()
                requests.post("http://10.90.90.20:8001/clipboard", json={"content": txt}, timeout=2)
                st.toast("Mac Clipboard Sent to PC")
            except: st.error("Sync Failed")

    st.divider()

    # 3. LIVE LOGS
    st.markdown("### 📜 BRIDGE LOGS")
    if LOG_FILE.exists():
        with open(LOG_FILE, "r") as f:
            lines = f.readlines()
            # Show last 20 lines
            st.code("".join(lines[-20:]), language="text")
    else:
        st.info("No logs generated yet. Ensure 'global_execute.sh' is running.")
