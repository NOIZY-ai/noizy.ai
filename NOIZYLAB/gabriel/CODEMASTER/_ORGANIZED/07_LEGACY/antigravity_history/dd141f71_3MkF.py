
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
import subprocess # Added for Trainer/Recruiter
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
    st.write("v22.0.0 - THE EAR")

# --- MAIN STAGE ---
st.title("NOIZYVOX AGENCY")
st.caption("Where AI Voices Come Alive. Directed by Gemini. Powered by RVC + DeepFilter + Whisper.")

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

elif MODE == "Recruiter":
    from dataset_engine import Recorder, DatasetProcessor, AutoTranscriber
    
    @st.cache_resource
    def get_transcriber():
        return AutoTranscriber(model_size="base.en")
    
    st.title("🎤 THE RECRUITER")
    st.caption("Autonomous Dataset Generator. Build your Digital Twin.")
    
    # Session Config
    session_name = st.text_input("Session Name (e.g., 'your_name')", value="user_voice")
    dataset_base = "/Users/m2ultra/NOIZYLAB/GABRIEL/voice_data"
    session_dir = os.path.join(dataset_base, session_name)
    
    processor = DatasetProcessor(session_dir)
    recorder = Recorder()
    
    # Options
    auto_transcribe = st.checkbox("👂 Auto-Transcribe (Verify Identity)", value=True)
    
    if "interview_step" not in st.session_state:
        st.session_state.interview_step = 0
        
    QUESTIONS = [
        {"q": "Please count from one to ten clearly and steadily.", "emo": "neutral", "dur": 10},
        {"q": "Tell me a secret you have never told anyone.", "emo": "whisper", "dur": 8},
        {"q": "Imagine you won the lottery! Shout it out!", "emo": "joy", "dur": 6},
        {"q": "You are furious at a machine. Yell at it!", "emo": "anger", "dur": 6},
        {"q": "Describe the most beautiful place you've ever seen.", "emo": "neutral", "dur": 10}
    ]
    
    step = st.session_state.interview_step
    
    if step < len(QUESTIONS):
        q = QUESTIONS[step]
        st.subheader(f"Step {step+1}/{len(QUESTIONS)}")
        st.info(f"🗣️ Gabriel Asks: {q['q']}")
        
        # Gabriel Speaks First
        if st.button("🔊 Hear Question"):
             asyncio.run(get_agency().agents[0].speak(q['q']))
             
        st.write(f"**Target Emotion:** {q['emo']} | **Duration:** {q['dur']}s")
        
        if st.button("🔴 RECORD ANSWER", type="primary"):
            with st.spinner(f"Recording for {q['dur']}s..."):
                raw_path = os.path.join(processor.raw_dir, f"take_{step:03d}.wav")
                recorder.record(q['dur'], raw_path)
                st.success("Stopped.")
                
                final_transcript = q['q'] # Default to prompt
                
                if auto_transcribe:
                    with st.spinner("👂 Listening/Transcribing..."):
                        transcriber = get_transcriber()
                        final_transcript = transcriber.transcribe(raw_path)
                        st.info(f"📝 Heard: {final_transcript}")
                
                out_path = processor.process_raw_sample(raw_path, final_transcript, session_name)
                st.audio(out_path)
                
            st.session_state.interview_step += 1
            st.rerun()
            
    else:
        st.success("🎉 INTERVIEW COMPLETE!")
        st.write(f"Dataset generated at: `{session_dir}/processed`")
        if st.button("Reset Session"):
            st.session_state.interview_step = 0
            st.rerun()

elif MODE == "Trainer":
    st.title("🏋️ THE TRAINER")
    st.caption("Turn your dataset into an AI Voice Model (RVC).")
    
    # 1. Select Dataset
    dataset_base = "/Users/m2ultra/NOIZYLAB/GABRIEL/voice_data"
    if os.path.exists(dataset_base):
        datasets = [d for d in os.listdir(dataset_base) if os.path.isdir(os.path.join(dataset_base, d))]
    else:
        datasets = []
        
    session_name = st.selectbox("Select Dataset to Train", datasets)
    
    # 2. Config
    epochs = st.slider("Epochs (Training Cycles)", 10, 200, 100)
    
    # 3. Action
    if st.button("🚀 START TRAINING", type="primary"):
        if session_name:
            dataset_path = os.path.join(dataset_base, session_name, "processed")
            model_name = f"{session_name}_v1"
            
            st.info(f"Initialized Training for: {model_name}")
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Call Wrapper
            # In real scenario, we'd use subprocess.Popen to stream logs
            cmd = [
                "/Users/m2ultra/NOIZYLAB/GABRIEL/xtts_venv/bin/python3",
                "/Users/m2ultra/NOIZYLAB/GABRIEL/bin/train_rvc.py",
                "--name", model_name,
                "--dataset", dataset_path,
                "--epochs", str(epochs)
            ]
            
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            
            # Stream Output
            logs = st.empty()
            log_content = ""
            
            while True:
                line = process.stdout.readline()
                if not line and process.poll() is not None:
                    break
                if line:
                    log_content += line
                    logs.code(log_content[-1000:], language="bash") # Show last 1000 chars
                    if "step" in line:
                        progress_bar.progress(50) # Dummy progress update
                        
            if process.returncode == 0:
                progress_bar.progress(100)
                st.success("✅ TRAINING COMPLETE!")
                st.balloons()
                st.write(f"Model saved to `bin/models/{model_name}.pth`")
                
                # Auto-Set as Gabriel's Model?
                if st.button("Load into Gabriel"):
                    os.environ["RVC_MODEL_PATH"] = f"/Users/m2ultra/NOIZYLAB/GABRIEL/bin/models/{model_name}.pth"
                    st.success("Set as Active Model!")
            else:
                st.error("Training Failed.")
    
else:
    st.error("System Offline. Please check unified_agency.py")


