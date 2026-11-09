import re
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
    
    # Auto-Pilot Mode
    enable_autopilot = st.toggle("🚀 AUTO-PILOT MODE", value=True)
    
    provider = "Auto"
    if not enable_autopilot:
        # Provider Selection
        provider = st.radio("AI Model Provider", ["Gemini", "Claude"])
    
    api_key_gemini = st.text_input("Gemini API Key", type="password")
    api_key_claude = st.text_input("Claude API Key", type="password")
    
    # Initialize Clients
    if api_key_gemini:
        genai.configure(api_key=api_key_gemini)
    
    if api_key_gemini and api_key_claude:
        st.success("ALL SYSTEMS ONLINE")
    elif api_key_gemini:
        st.info("GEMINI ONLINE")
    elif api_key_claude:
         st.info("CLAUDE ONLINE")
    
    st.divider()
    st.write("NOIZYLAB v3.0 // AUTO-PILOT")

# --- MAIN FUNCTIONS ---

# --- MAIN FUNCTIONS ---

# --- MAIN FUNCTIONS ---

class SmartRouter:
    """Decides which Agent and Model to use based on prompt content"""
    
    @staticmethod
    def route(text):
        lower = text.lower()
        scores = {
            "ENGR_KEITH": 0, "SHIRL": 0, "DREAM": 0, "GABRIEL": 0, "POPS": 0
        }
        
        # Scoring Logic (Ported from AI_ORCHESTRATION.ts)
        if re.search(r"(code|bug|error|exception|stack|deploy|git|typescript|python|api|script)", lower):
            scores['ENGR_KEITH'] += 5
        if re.search(r"(feel|sad|happy|worried|tired|love|hate|user|empathy)", lower):
            scores['SHIRL'] += 5
        if re.search(r"(plan|future|imagine|what if|roadmap|vision|create|generate|movie|video)", lower):
            scores['DREAM'] += 5
        if re.search(r"(security|admin|access|token|auth|permission|lock|system|key)", lower):
            scores['GABRIEL'] += 5
        if re.search(r"(advice|strategy|wise|help|guide|mentor)", lower):
            scores['POPS'] += 5
            
        # Context Modifiers (Sticky Routing)
        if "last_agent" in st.session_state:
            last = st.session_state.last_agent
            if last in scores:
                scores[last] += 2
            
        # Find Winner
        best_agent = max(scores, key=scores.get)
        if scores[best_agent] == 0:
            best_agent = "GENERAL"
        
        # Update Memory
        st.session_state.last_agent = best_agent
            
        return best_agent

    @staticmethod
    def get_provider_for_agent(agent):
        """Maps Agent Persona to Model Provider"""
        mapping = {
            "ENGR_KEITH": "Claude", # Claude is better at code
            "SHIRL": "Claude",      # Claude has more nuance
            "DREAM": "Gemini",      # Gemini is fast/creative
            "GABRIEL": "Gemini",    # System tasks
            "POPS": "Gemini",       # Fast wisdom
            "GENERAL": "Gemini"     # Default fast
        }
        return mapping.get(agent, "Gemini")

def generate_claude(prompt, key, system_prompt=""):
    """Uses Claude 3.5 Sonnet"""
    url = "https://api.anthropic.com/v1/messages"
    headers = {
        "x-api-key": key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }
    
    # Prepend system prompt to user message if needed (or use system param if supported, but simpler to prepend for now)
    full_content = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
    
    data = {
        "model": "claude-3-5-sonnet-20240620",
        "max_tokens": 1024,
        "messages": [{"role": "user", "content": full_content}]
    }
    
    req = urllib.request.Request(url, data=json.dumps(data).encode(), headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode())
            return result['content'][0]['text']
    except Exception as e:
        return f"Error calling Claude: {str(e)}"

def analyze_prompt_smart(text_input, manual_provider, autopilot, keys):
    """Orchestrates the generation based on settings"""
    
    agent = "USER_SELECTED"
    provider = manual_provider
    
    # 1. AUTO-PILOT ROUTING
    if autopilot:
        agent = SmartRouter.route(text_input)
        provider = SmartRouter.get_provider_for_agent(agent)
        
        # Visual Feedback
        with st.status(f"🤖 Brain Active...", expanded=True) as status:
            st.write(f"Analyzing Intent... Complete.")
            st.write(f"Selected Persona: **{agent}**")
            st.write(f"Routing to Model: **{provider}**")
            status.update(label=f"Agent: {agent} | Model: {provider}", state="complete")
            
    # 2. EXECUTION
    system_instruction = f"You are {agent}. Act accordingly."
    
    if provider == "Gemini":
        if not keys['gemini']: return "⚠️ MISSING GEMINI KEY"
        model = genai.GenerativeModel('gemini-1.5-flash')
        # Gemini 1.5 Flash is fast
        response = model.generate_content(f"{system_instruction}\n\n{text_input}")
        return response.text
        
    elif provider == "Claude":
        if not keys['claude']: return "⚠️ MISSING CLAUDE KEY"
        return generate_claude(text_input, keys['claude'], system_instruction)
        
    return "Unknown Provider"

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
    if st.button("OPTIMIZE PROMPT"):
        keys = {"gemini": api_key_gemini, "claude": api_key_claude}
        
        # Check if we have at least one key for what we need
        # (Simplified check: if autopilot, we might need either; if manual, we need specific)
        
        proceed = True
        if not enable_autopilot:
            if provider == "Gemini" and not api_key_gemini: proceed = False
            if provider == "Claude" and not api_key_claude: proceed = False
        else:
            if not api_key_gemini and not api_key_claude: proceed = False
            
        if not proceed:
            st.error("⚠️ REQUIRED API KEYS METHOD")
        else:
             result = analyze_prompt_smart(user_idea, provider, enable_autopilot, keys)
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
