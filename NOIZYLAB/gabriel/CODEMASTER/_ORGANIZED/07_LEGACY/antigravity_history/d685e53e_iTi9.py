
import streamlit as st
import asyncio
import os
import time

# Set Page Config
st.set_page_config(
    page_title="NOIZYVOX AGENCY",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for "The Stage" Aesthetic
st.markdown("""
<style>
    .stApp {
        background-color: #0e1117;
        color: #fafafa;
    }
    .stTextInput > div > div > input {
        background-color: #262730;
        color: #ffffff;
    }
    .stTextArea > div > div > textarea {
        background-color: #262730;
        color: #ffffff;
    }
    h1 {
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 700;
        background: -webkit-linear-gradient(45deg, #00C9FF, #92FE9D);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .status-box {
        padding: 10px;
        border-radius: 5px;
        background-color: #1e1e1e;
        border: 1px solid #333;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Import Agency Logic
# We need to add the current dir to path to import unified_agency
import sys
sys.path.append("/Users/m2ultra/NOIZYLAB/GABRIEL")

try:
    from unified_agency import Agency
    AGENCY_AVAILABLE = True
except ImportError as e:
    st.error(f"Failed to load Agency: {e}")
    AGENCY_AVAILABLE = False

def get_agency():
    if "agency" not in st.session_state:
        st.session_state.agency = Agency()
    return st.session_state.agency

async def run_direction(text, force_agent=None):
    agency = get_agency()
    
    with st.status("🎬 lights... Camera... ACTION!", expanded=True) as status:
        st.write("🧠 Casting Director is analyzing script...")
        actor, emotion, sfx, reason = agency.cast_actor(text, force_agent)
        
        st.write(f"🎭 **Cast**: {actor.name}")
        st.write(f"💭 **Reason**: {reason}")
        st.write(f"❤️ **Emotion**: {emotion}")
        st.write(f"🔊 **SFX**: {sfx}")
        
        status.update(label="🎙️ Recording in progress...", state="running")
        
        # Run the async speak method
        # We need to run this in the event loop
        audio_file = await actor.speak(text, emotion, sfx)
        
        status.update(label="✅ It's a wrap!", state="complete", expanded=False)
        
    return actor, emotion, sfx, reason, audio_file

# --- SIDEBAR ---
with st.sidebar:
    st.title("🎛️ CONTROL ROOM")
    st.markdown("---")
    
    st.header("Pipeline Status")
    
    # Check RVC
    rvc_path = "/Users/m2ultra/NOIZYLAB/GABRIEL/bin/rvc_runner.py"
    if os.path.exists(rvc_path):
        st.success("RVC Inference: ONLINE (MPS)")
    else:
        st.error("RVC Inference: OFFLINE")

    # Check Model
    model_path = os.environ.get("RVC_MODEL_PATH", "/Users/m2ultra/NOIZYLAB/GABRIEL/bin/models/gabriel_rvc.pth")
    if os.path.exists(model_path):
        st.success(f"Model Loaded: {os.path.basename(model_path)}")
    else:
        st.warning("⚠️ No Custom Model Found (Using Raw TTS)")
        
    st.markdown("---")
    st.write("v18.0.1 - THE STAGE")

# --- MAIN STAGE ---
st.title("NOIZYVOX AGENCY")
st.caption("Where AI Voices Come Alive. Directed by Gemini. Powered by RVC + DeepFilter.")

if AGENCY_AVAILABLE:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        script = st.text_area("✍️ The Script", height=150, placeholder="Enter dialogue here...")
        
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🎬 ACTION (Auto-Cast)", type="primary", use_container_width=True):
                if script:
                    actor, emotion, sfx, reason, audio = asyncio.run(run_direction(script))
                    st.session_state["last_run"] = {
                        "script": script,
                        "actor": actor.name,
                        "audio": audio,
                        "reason": reason,
                        "emotion": emotion,
                        "sfx": sfx
                    }
        with c2:
            override = st.selectbox("Force Actor", ["Auto", "Gabriel", "Riva", "Jamie"])
            if st.button("🎥 FORCE DIRECT", use_container_width=True):
                if script:
                    forced = None if override == "Auto" else override
                    actor, emotion, sfx, reason, audio = asyncio.run(run_direction(script, forced))
                    st.session_state["last_run"] = {
                        "script": script,
                        "actor": actor.name,
                        "audio": audio,
                        "reason": reason,
                        "emotion": emotion,
                        "sfx": sfx
                    }

    with col2:
        st.markdown("### 📽️ The Takes")
        if "last_run" in st.session_state:
            run = st.session_state["last_run"]
            
            # Display Card
            st.markdown(f"""
            <div class="status-box">
                <h3>{run['actor']}</h3>
                <p><i>"{run['reason']}"</i></p>
                <hr>
                <p><b>Emotion:</b> {run['emotion']}</p>
                <p><b>SFX:</b> {run['sfx']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.audio(run['audio'])
            
            with st.expander("📝 Script History"):
                st.info(run['script'])

else:
    st.error("System Offline. Please check unified_agency.py")
