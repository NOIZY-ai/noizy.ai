import streamlit as st
import google.generativeai as genai
import os
from pathlib import Path

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
    st.write("NOIZYLAB v3.0 // POWERED BY GOOGLE DEEPMIND")
    
    # SYSTEM AGENTS
    st.sidebar.markdown("### 🧬 NOIZY TEAM")
    selected_agent = st.sidebar.selectbox(
        "Select Active Agent",
        ["GABRIEL", "SHIRL", "POPS", "ENGR_KEITH", "DREAM"]
    )
    
    # Store Agent personas
    agents = {
        "GABRIEL": {"role": "System Bridge & Messenger", "traits": ["reliable", "fast", "connected"], "icon": "🌐"},
        "SHIRL": {"role": "Business Operations Manager", "traits": ["organized", "efficient", "warm"], "icon": "💼"},
        "POPS": {"role": "Creative Director", "traits": ["artistic", "experienced", "quality-focused"], "icon": "🎨"},
        "ENGR_KEITH": {"role": "Technical Engineering Lead", "traits": ["precise", "methodical", "thorough"], "icon": "🔧"},
        "DREAM": {"role": "Strategic Visionary", "traits": ["imaginative", "strategic", "ambitious"], "icon": "🔮"}
    }
    
    st.sidebar.info(f"**{agents[selected_agent]['icon']} {selected_agent}**\n\n{agents[selected_agent]['role']}")


# --- MAIN FUNCTIONS ---

def analyze_prompt(text_input, agent_name="GABRIEL"):
    """Uses Gemini 1.5 Flash for text logic with Agent Persona"""
    agent_data = agents.get(agent_name, agents["GABRIEL"])
    
    system_prompt = f"""You are {agent_name}, {agent_data['role']}. 
    Your traits are: {', '.join(agent_data['traits'])}. 
    You are part of the MC96ECOUNIVERSE.
    Be helpful, concise, technical when needed, and always action-oriented.
    Philosophy: GORUNFREE - One command = everything done.
    
    Convert this raw idea into a technical prompt for video and audio generation, or answer the user's query directly if it's a question.
    """
    
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(
        f"{system_prompt}\n\nRAW INPUT: {text_input}"
    )
    return response.text

def perform_lighthouse_audit(content):
    """Simulates a Lighthouse Audit for Code/Prompts"""
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"""
    Act as Google Lighthouse but for Generative Content and Code.
    Audit the following input for:
    1. Performance (Efficiency of the prompt/code)
    2. Accessibility (Clarity and inclusivity)
    3. Best Practices (Formatting, safety, modern standards)
    4. SEO (Keyword relevance or searchability if applicable)
    
    Rate each category 0-100 and provide specific actionable improvements.
    
    INPUT TO AUDIT:
    {content}
    """
    return model.generate_content(prompt).text

# --- THE UI LAYOUT ---
st.title("🎛️ NOIZYLAB // MASTER CONTROL")

# TABS for distinct workflows
# TABS for distinct workflows
tab1, tab2, tab3 = st.tabs(["🧠 TEAM BRAIN", "🔊 EARS (Audio Analysis)", "⚡ LIGHTHOUSE AUDIT"])

# TAB 1: TEXT TO PROMPT
with tab1:
    st.header("Concept Refiner")
    user_idea = st.text_area("Input your raw idea (e.g., 'Sad robot walking in rain')", height=100)
    
    if st.button("OPTIMIZE PROMPT"):
        if not api_key:
            st.error("⚠️ API KEY MISSING")
        else:
            with st.spinner(f"{selected_agent} is Processing..."):
                result = analyze_prompt(user_idea, selected_agent)
                st.subheader(f"{agents[selected_agent]['icon']} {selected_agent}'s Output:")
                st.write(result)

# TAB 3: LIGHTHOUSE AUDIT
with tab3:
    st.header("⚡ Content Lighthouse")
    st.write("Audit your Prompts, Code, or Ideas against Google's High Standards.")
    
    audit_input = st.text_area("Content to Audit")
    
    if st.button("RUN LIGHTHOUSE"):
        if not api_key:
            st.error("⚠️ API KEY MISSING")
        else:
            with st.spinner("Running Lighthouse Analysis..."):
                audit_result = perform_lighthouse_audit(audit_input)
                st.subheader("📊 Audit Report")
                st.markdown(audit_result)

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
