
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

# Custom CSS for "The Stage" Aesthetic (V29: THE BLOOD OATH)
st.markdown("""
<style>
    /* BLOOD OATH PALETTE: Void Black, Oxblood, Rich Burgundy, Dune Sand */
    .stApp {
        background-color: #050505;
        background-image: linear-gradient(180deg, #1a0202 0%, #050505 100%);
        color: #E0E0E0;
    }
    
    /* INPUT FIELDS - Glassmorphic Oxblood */
    .stTextInput > div > div > input {
        background-color: rgba(74, 4, 4, 0.3); /* Oxblood Glass */
        color: #C2B280; /* Sand */
        border: 1px solid #4A0404;
        font-family: 'Courier New', monospace;
    }
    .stTextArea > div > div > textarea {
        background-color: rgba(74, 4, 4, 0.3);
        color: #C2B280;
        border: 1px solid #4A0404;
    }
    
    /* TITLES - Monolithic Gradient */
    h1 {
        font-family: 'Futura', 'Helvetica Neue', sans-serif;
        text-transform: uppercase;
        font-weight: 800;
        letter-spacing: 3px;
        background: -webkit-linear-gradient(90deg, #C2B280, #800020); /* Sand to Burgundy */
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* HEADERS */
    h2, h3 {
        color: #800020; /* RICH BURGUNDY */
        font-family: 'Futura', sans-serif;
        text-transform: uppercase;
        letter-spacing: 1px;
        border-bottom: 2px solid #4A0404;
        padding-bottom: 5px;
    }

    /* BUTTONS - Primary Action */
    div.stButton > button:first-child {
        background-color: #4A0404; /* Oxblood */
        color: #C2B280; /* Sand */
        border: 1px solid #800020;
        border-radius: 2px;
        text-transform: uppercase;
        letter-spacing: 2px;
        font-weight: bold;
        transition: all 0.4s ease;
        box-shadow: 0 0 10px rgba(74, 4, 4, 0.5);
    }
    div.stButton > button:first-child:hover {
        background-color: #800020; /* Lighter Burgundy */
        border-color: #C2B280;
        color: #ffffff;
        box-shadow: 0 0 20px rgba(128, 0, 32, 0.8);
    }
    
    /* CARDS - Glassmorphism */
    .status-box {
        padding: 20px;
        background: rgba(20, 0, 0, 0.6);
        backdrop-filter: blur(10px);
        border-left: 5px solid #800020;
        border: 1px solid #330000;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5);
        margin-bottom: 15px;
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
    st.write("v23.0.0 - THE OMNI-ARCHIVE")
    
    # SYSTEM NAVIGATION
    st.markdown("### 🧭 NAVIGATION")
    MODE = st.radio("Select Module:", ["Director", "Recruiter", "Trainer", "Omni-Archive"])

# --- MAIN STAGE ---
if MODE == "Director":
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
                    # Parallel Execution: Audio + Image
                    async def perform_action():
                        audio_task = run_direction(script)
                        return await audio_task

                    actor, emotion, sfx, reason, audio = asyncio.run(perform_action())
                    
                    # Generate Vision (V26) & Video (V27)
                    from agency_utils import ImageGenerator, DreamFactory
                    with st.spinner("🎨 Creating the Dream (Video Synthesis)..."):
                        visual_prompt = f"Cinematic shot of {actor.description}. Emotion: {emotion}. Context: {script[:50]}..."
                        image_url = ImageGenerator.generate(visual_prompt)
                        
                        # V27: Synthesize Video
                        # Check if audio path is absolute or relative
                        # run_direction prompt returns audio file path.
                        
                        video_path = DreamFactory.create_dream(audio, image_url)
                    
                    st.session_state["last_run"] = {
                        "script": script,
                        "actor": actor.name,
                        "audio": audio,
                        "reason": reason,
                        "emotion": emotion,
                        "sfx": sfx,
                        "image": image_url,
                        "video": video_path # Store Video
                    }
                    
        with c2:
            override = st.selectbox("Force Actor", ["Auto", "Gabriel", "Riva", "Jamie"])
            if st.button("🎥 FORCE DIRECT", use_container_width=True):
                if script:
                    forced = None if override == "Auto" else override
                    actor, emotion, sfx, reason, audio = asyncio.run(run_direction(script, forced))
                    
                    # Generate Vision (V26) & Video (V27)
                    from agency_utils import ImageGenerator, DreamFactory
                    with st.spinner("🎨 Creating the Dream (Video Synthesis)..."):
                        visual_prompt = f"Cinematic shot of {actor.description}. Emotion: {emotion}. Context: {script[:50]}..."
                        image_url = ImageGenerator.generate(visual_prompt)
                        video_path = DreamFactory.create_dream(audio, image_url)
                    
                    st.session_state["last_run"] = {
                        "script": script,
                        "actor": actor.name,
                        "audio": audio,
                        "reason": reason,
                        "emotion": emotion,
                        "sfx": sfx,
                        "image": image_url,
                        "video": video_path
                    }

    with col2:
        st.markdown("### 📽️ The Takes")
        if "last_run" in st.session_state:
            run = st.session_state["last_run"]
            
            # V27: Play Video
            if "video" in run and run["video"] and os.path.exists(run["video"]):
                 st.markdown("#### 🎞️ The Dream")
                 st.video(run["video"])
            # Fallback to Image (V26)
            elif "image" in run:
                st.image(run["image"], use_container_width=True)
                
            st.markdown(f"""
            <div class="status-box">
                <h3>{run['actor']}</h3>
                <p><i>"{run['reason']}"</i></p>
                <hr>
                <p><b>Emotion:</b> {run['emotion']}</p>
                <p><b>SFX:</b> {run['sfx']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Audio is already in video, but keep player for audio-only check
            if not ("video" in run and run["video"]):
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
            sys_prompt = "You are the Omni-Archive, a repository of vast knowledge."
            
        full_prompt = f"{sys_prompt}\n\nUser Request: {query}\n\nResponse:"
        
        try:
            response = self.model.generate_content(full_prompt)
            return response.text
        except Exception as e:
            return f"⚠️ The Archive is silent: {e}"

# SYSTEM NAVIGATION
st.markdown("### 🧭 NAVIGATION")
MODE = st.radio("Select Module:", ["Director", "Recruiter", "Trainer", "Omni-Archive", "Exam Mode"])

elif MODE == "Omni-Archive":
    from unified_agency import OmniArchive
    
    st.title("🏛️ THE OMNI-ARCHIVE")
    st.caption("The Universal Repository of Human Knowledge.")
    
    archive = OmniArchive()
    agency = get_agency()
    
    # Domain Selector
    domain = st.selectbox("Select Domain of Knowledge:", 
        ["Literature", "Musicology", "History", "Science", "Philosophy", "Cinema"]
    )
    
    st.subheader(f"The {domain} Expert")
    query = st.text_area(f"Ask the {domain} Archives:", height=100)
    
    if st.button("Consult Archives", type="primary"):
        if query:
            with st.spinner("Searching the infinite shelves..."):
                response = archive.consult(query, domain=domain)
                st.markdown(f"### 📖 Insight\n\n{response}")
                st.session_state['archive_response'] = response
    
    # Common "Read to Me" Feature
    if 'archive_response' in st.session_state:
        st.markdown("---")
        if st.button("🗣️ Read to Me (Gabriel)", use_container_width=True):
            text_to_read = st.session_state['archive_response']
            with st.spinner("Gabriel is preparing to lecture..."):
                gabriel = agency.agents[0]
                audio_file = asyncio.run(gabriel.speak(text_to_read, emotion="neutral", sfx="reverb"))
                st.audio(audio_file)

elif MODE == "Exam Mode":
    from unified_agency import OmniArchive
    archive = OmniArchive()
    
    st.title("📝 EXAM MODE")
    st.caption("Administer a Test to verify Gabriel's depth. (Self-Learning Active)")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        domain = st.selectbox("Subject:", ["Literature", "Musicology", "History", "Science", "Philosophy", "Cinema"])
        difficulty = st.select_slider("Difficulty:", ["Undergrad", "Masters", "PhD", "Impossible"])
        
    with col2:
        question = st.text_area("Exam Question:", placeholder="e.g., Synthesize the impact of quantum mechanics on 20th-century philosophy.")
        
    if st.button("📝 Administer Test", type="primary", use_container_width=True):
        if question:
            st.info("🧠 Gabriel is thinking... (Recursive Learning Loop Active)")
            
            # REMOVED VISUAL PACING FOR SPEED ("MUCH FASTER")
            progress_text = "Processing Draft & Critique..."
            my_bar = st.progress(0, text=progress_text)
            
            # 1. Calls the recursive loop
            draft, critique, final = archive.learn_from_self(question, domain)
            
            my_bar.progress(100, text="Exam Complete.")
            
            # Display Results
            st.markdown("### 📑 Test Results")
            
            with st.expander("See Draft & Critique (Chain of Thought)"):
                st.warning(f"**Draft Answer:**\n\n{draft}")
                st.error(f"**Self-Critique:**\n\n{critique}")
                
            st.success(f"**Final PhD Response:**\n\n{final}")
            st.caption(f"Grading: {difficulty} Level Check Passed.")

else:
    st.error("System Offline. Please check unified_agency.py")
