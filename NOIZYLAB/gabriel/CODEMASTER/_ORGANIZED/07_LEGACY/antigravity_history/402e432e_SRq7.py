import streamlit as st
import google.generativeai as genai
import os
import json
from datetime import datetime
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

# --- CONFIGURATION & CONSTANTS ---
AGENTS = {
    "GABRIEL": {"role": "System Bridge & Messenger", "traits": ["reliable", "fast", "connected"], "icon": "🌐"},
    "SHIRL": {"role": "Business Operations Manager", "traits": ["organized", "efficient", "warm"], "icon": "💼"},
    "POPS": {"role": "Creative Director", "traits": ["artistic", "experienced", "quality-focused"], "icon": "🎨"},
    "ENGR_KEITH": {"role": "Technical Engineering Lead", "traits": ["precise", "methodical", "thorough"], "icon": "🔧"},
    "DREAM": {"role": "Strategic Visionary", "traits": ["imaginative", "strategic", "ambitious"], "icon": "🔮"},
    "HEX": {"role": "Visual Architect (Web & Art)", "traits": ["aesthetic", "bold", "pixel-perfect"], "icon": "💅"}
}

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
        list(AGENTS.keys())
    )
    
    agent_data = AGENTS[selected_agent]
    st.sidebar.info(f"**{agent_data['icon']} {selected_agent}**\n\n{agent_data['role']}")


# --- DATABASE (MemCells) ---
DB_PATH = "noizylab_memory.json"

def init_db():
    if not os.path.exists(DB_PATH):
        with open(DB_PATH, "w") as f:
            json.dump([], f)

def load_memories():
    init_db()
    try:
        with open(DB_PATH, "r") as f:
            return json.load(f)
    except:
        return []

def save_memory(agent, input_text, output_text, type="TEXT"):
    memories = load_memories()
    new_memory = {
        "timestamp": str(datetime.now()),
        "agent": agent,
        "type": type,
        "input": input_text,
        "output": output_text
    }
    memories.append(new_memory)
    with open(DB_PATH, "w") as f:
        json.dump(memories, f, indent=4)
    return new_memory

# --- MAIN FUNCTIONS ---

def analyze_prompt(text_input, agent_name="GABRIEL"):
    """Uses Gemini 1.5 Flash for text logic with Agent Persona"""
    agent_data = AGENTS.get(agent_name, AGENTS["GABRIEL"])
    
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
    
    # Save to Memory
    save_memory(agent_name, text_input, response.text, "INTELLIGENCE")
    
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
    """
    return model.generate_content(prompt).text

def generate_design_system(concept):
    """Generates a Visual Language for a concept"""
    model = genai.GenerativeModel('gemini-1.5-pro')
    prompt = "You are HEX. Generate a comprehensive Design System for: " + concept + ". Output must be valid JSON: { \"palette\": { \"primary\": \"#...\", \"secondary\": \"#...\", \"bg\": \"#...\", \"text\": \"#...\" }, \"typography\": { \"headings\": \"font\", \"body\": \"font\" }, \"moodboard\": [\"keyword1\", \"keyword2\", \"keyword3\"], \"css_suggestion\": \"css code snippet for a button...\" }"
    return model.generate_content(prompt).text

# --- THE UI LAYOUT ---
st.title("🎛️ NOIZYLAB // MASTER CONTROL")

# TABS for distinct workflows
# TABS for distinct workflows
# TABS for distinct workflows
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🧠 INTELLIGENCE", "🔊 SENSORS (Audio)", "⚡ AUDIT", "🎨 STUDIO", "🗄️ ARCHIVES"])

# TAB 5: ARCHIVES (Database View)
with tab5:
    st.header("🗄️ NOIZYLAB ARCHIVES")
    st.write("Persistent Memory of all Consoles Operations.")
    
    memories = load_memories()
    if not memories:
        st.info("No data recorded yet. Start using the tools!")
    else:
        # Reverse to show newest first
        for mem in reversed(memories):
            with st.expander(f"[{mem['timestamp']}] {mem['agent']} // {mem['type']}"):
                st.write(f"**INPUT:** {mem['input']}")
                st.write(f"**OUTPUT:** {mem['output']}")


# TAB 1: INTELLIGENCE
with tab1:
    st.header("Human-System Interface")
    user_idea = st.text_area("Input your raw idea (e.g., 'Sad robot walking in rain')", height=100)
    
    if st.button("OPTIMIZE PROMPT"):
        if not api_key:
            st.error("⚠️ API KEY MISSING")
        else:
            with st.spinner(f"{selected_agent} is Processing..."):
                result = analyze_prompt(user_idea, selected_agent)
                st.subheader(f"{AGENTS[selected_agent]['icon']} {selected_agent}'s Output:")
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

# TAB 4: DESIGN STUDIO
with tab4:
    st.header("💅 HEX // VISUAL ARCHITECT")
    st.write("Generate professional Grade Design Systems & Art Direction.")
    
    design_concept = st.text_input("Enter Design Concept (e.g., 'Cyberpunk Coffee Shop', 'Minimalist AI Dashboard')")
    
    if st.button("GENERATE VISUAL LANGUAGE"):
        if not api_key:
            st.error("⚠️ API KEY MISSING")
        else:
            with st.spinner("HEX is crafting the aesthetic..."):
                design = generate_design_system(design_concept)
                st.subheader("🎨 Design System")
                
                # Simple parsing attempt to show colors visually if possible, or just raw text
                st.code(design, language="json")
                st.info("Copy this JSON for your frontend developer or into your CSS variables.")

# TAB 2: SENSORS
with tab2:
    st.header("Wideband Audio Sensor")
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
