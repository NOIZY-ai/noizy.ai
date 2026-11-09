import streamlit as st
import google.generativeai as genai
import os
from pathlib import Path
import json
import urllib.request
import urllib.error

# --- PAGE CONFIGURATION (Real UI) ---
st.set_page_config(
    page_title="NOIZYLAB CONSOLE",
    page_icon="🎛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- STYLING (Cyberpunk Aesthetic) ---
st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
        color: #00ff00;
    }
    .stButton>button {
        color: #0e1117;
        background-color: #00ff00;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: SETTINGS ---
with st.sidebar:
    st.header("🔌 SYSTEM CORE")
    api_key = st.text_input("Enter Gemini API Key", type="password")
    if api_key:
        genai.configure(api_key=api_key)
        st.success("SYSTEM ONLINE")
    else:
        st.warning("ENTER KEY TO INITIALIZE")
    
    st.divider()
    st.write("NOIZYLAB v2.0")

# --- MAIN FUNCTIONS ---

def analyze_prompt(text_input):
    """Uses Gemini 1.5 Flash for text logic"""
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(
        f"You are the Director of NoizyLab. Convert this raw idea into a technical prompt for video and audio generation. \n\nRAW IDEA: {text_input}"
    )
    return response.text

# --- THE UI LAYOUT ---
st.title("🎛️ NOIZYLAB // MASTER CONTROL")

# TABS for distinct workflows
tab1, tab2, tab3 = st.tabs(["🧠 BRAIN (Text)", "🔊 EARS (Audio Analysis)", "🔑 ADMIN"])

# TAB 1: TEXT TO PROMPT
with tab1:
    st.header("Concept Refiner")
    user_idea = st.text_area("Input your raw idea (e.g., 'Sad robot walking in rain')", height=100)
    
    if st.button("OPTIMIZE PROMPT"):
        if not api_key:
            st.error("⚠️ API KEY MISSING")
        else:
            with st.spinner("Processing..."):
                result = analyze_prompt(user_idea)
                st.subheader("Optimized Output:")
                st.code(result, language="markdown")

# TAB 2: AUDIO TO VIDEO (The "Genius" Feature)
with tab2:
    st.header("Audio-Reactive Intelligence")
    st.write("Upload a sound file. Gemini will listen to it and describe the video that should match it.")
    
    uploaded_file = st.file_uploader("Upload Audio (MP3/WAV)", type=["mp3", "wav"])
    
    if uploaded_file is not None:
        # Display Audio Player
        st.audio(uploaded_file, format='audio/mp3')
        
        if st.button("ANALYZE AUDIO VIBE"):
            if not api_key:
                st.error("⚠️ API KEY MISSING")
            else:
                with st.spinner("Listening to file..."):
                    # 1. Save file temporarily so Gemini can read it
                    temp_filename = "temp_audio.mp3"
                    with open(temp_filename, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    # 2. Upload to Gemini (Real Multimodal Function)
                    myfile = genai.upload_file(temp_filename)
                    
                    # 3. Generate Analysis
                    model = genai.GenerativeModel("gemini-1.5-flash")
                    result = model.generate_content(
                        [myfile, "Listen to this audio. Describe the exact mood, BPM, and visual scene that should accompany this sound. Give me a prompt for a Video Generator."]
                    )
                    
                    st.success("Analysis Complete")
                    st.markdown(result.text)
                    
                    # Cleanup
                    os.remove(temp_filename)

# TAB 3: ADMIN TOOLS
with tab3:
    st.header("Anthropic Admin Tools")
    st.markdown("Inspect API Key Metadata using the `organizations/api_keys` endpoint.")
    
    col1, col2 = st.columns(2)
    with col1:
        admin_key = st.text_input("Admin API Key (sk-ant-admin...)", type="password")
    with col2:
        target_key_id = st.text_input("Target Key ID (apikey_...)")

    if st.button("INSPECT KEY"):
        if not admin_key or not target_key_id:
             st.error("⚠️ BOTH KEYS REQUIRED")
        else:
            with st.spinner("Querying Anthropic Admin API..."):
                try:
                    url = f"https://api.anthropic.com/v1/organizations/api_keys/{target_key_id}"
                    req = urllib.request.Request(url)
                    req.add_header("X-Api-Key", admin_key)
                    
                    with urllib.request.urlopen(req) as response:
                        data = json.loads(response.read().decode())
                        st.success("Key Metadata Retrieved")
                        st.json(data)
                        
                except urllib.error.HTTPError as e:
                    if e.code == 401:
                        st.error("401 Unauthorized: Check your Admin Key.")
                    elif e.code == 404:
                        st.error("404 Not Found: Key ID does not exist or invalid permissions.")
                    else:
                        st.error(f"API Error: {e.code} - {e.reason}")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
