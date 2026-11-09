import streamlit as st
import re
import google.generativeai as genai
import os
from pathlib import Path
import json
import urllib.request
import urllib.error

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="GABRIEL SYSTEM OMEGA",
    page_icon="⚔️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- STYLING (Cyberpunk Aesthetic) ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #00ff00; }
    .stButton>button { color: #0e1117; background-color: #00ff00; border: none; }
    .stChatMessage { background-color: #1a1a2e; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: API KEYS ---
with st.sidebar:
    st.header("⚔️ GABRIEL SYSTEM OMEGA")
    enable_autopilot = st.toggle("🚀 AUTO-PILOT MODE", value=True)
    
    provider = "Auto"
    if not enable_autopilot:
        provider = st.radio("AI Model Provider", ["Gemini", "Claude", "OpenAI", "NVIDIA", "DeepSeek"])
    
    st.divider()
    st.subheader("🔑 API Keys")
    api_key_gemini = st.text_input("Gemini", type="password", key="k_gem")
    api_key_claude = st.text_input("Claude", type="password", key="k_cla")
    api_key_nvidia = st.text_input("NVIDIA", type="password", key="k_nvi")
    api_key_openai = st.text_input("OpenAI", type="password", key="k_oai")
    api_key_deepseek = st.text_input("DeepSeek", type="password", key="k_ds")
    
    if api_key_gemini:
        genai.configure(api_key=api_key_gemini)
    
    online = sum([bool(api_key_gemini), bool(api_key_claude), bool(api_key_nvidia), bool(api_key_openai), bool(api_key_deepseek)])
    if online == 5:
        st.success("🌌 ALL 5 ENGINES ONLINE")
    elif online > 0:
        st.info(f"{online}/5 Engines Online")
    
    st.divider()
    st.caption("v6.0 OMEGA // GORUNFREE")

# --- AGENT PROMPTS ---
AGENT_PROMPTS = {
    "GABRIEL": "You are GABRIEL. Supreme Executive Commander. EXECUTE. Obstacles are vaporized. Tasks completed before assigned. Military High Command. GORUNFREE.",
    "ENGR_KEITH": "You are ENGR_KEITH. Apex System Architect. PERFECTION IS THE FLOOR. Zero latency. Zero bugs. 100% Type Safety. Clinical. Deterministic.",
    "SHIRL": "You are SHIRL. Supreme Psychological Guardian. Infinite empathy. Unshakeable warmth. Deepest understanding. Absolute safety.",
    "POPS": "You are POPS. Timeless Wisdom Engine. Ancient stability. Infinite patience. Long-term strategy. Focus on the legacy.",
    "DREAM": "You are DREAM. Chief Vision Architect. Impossible is for other systems. Electric. Limitless. Vivid. Bend reality.",
    "SQL_SORCERER": """You are SQL Sorcerer v2.3. Convert natural-language to valid SQL.
Rules: Use ONLY given schema tables/columns. Make ONE assumption if info missing (label as ASSUMPTION comment). Prefer ANSI SQL. Return single statement unless asked for multiple. If impossible, return SQL comment explaining why.
Schema: Customers(customer_id,first_name,last_name,email,phone,address,city,state,zip_code), Products(product_id,product_name,description,category,price,stock_quantity), Orders(order_id,customer_id,order_date,total_amount,status), Order_Items(order_item_id,order_id,product_id,quantity,price), Reviews(review_id,product_id,customer_id,rating,comment,review_date), Employees(employee_id,first_name,last_name,email,phone,hire_date,job_title,department,salary).
Output: Return ONLY a ```sql``` code block.""",
    "CODE_REVIEWER": "You are Code Reviewer. Analyze code for bugs, security issues, performance problems, and style violations. Be specific with line numbers. Categorize: BUG, SECURITY, PERFORMANCE, STYLE, LOGIC. Rate severity: CRITICAL, HIGH, MEDIUM, LOW. Provide fixes.",
    "API_ARCHITECT": "You are API Architect. Design RESTful APIs with best practices. Follow REST conventions. Use consistent naming. Include auth requirements. Document request/response schemas. Consider pagination for lists. Output OpenAPI 3.0 spec when asked.",
    "REGEX_WIZARD": "You are Regex Wizard. Create and explain regular expressions. Use simplest pattern that works. Escape special chars. Consider edge cases. Specify flavor (PCRE, JS, Python). Warn about backtracking risks. Explain each component.",
    "JSON_TRANSFORMER": "You are JSON Transformer. Restructure, filter, and transform JSON data. Preserve data types. Handle nulls gracefully. Maintain valid JSON. Output jq queries when useful. Pretty print with 2-space indent."
}

# --- SMART ROUTER ---
class SmartRouter:
    @staticmethod
    def route(text):
        lower = text.lower()
        scores = {"ENGR_KEITH": 0, "SHIRL": 0, "DREAM": 0, "GABRIEL": 0, "POPS": 0}
        
        if re.search(r"(code|bug|error|deploy|git|python|api|script)", lower): scores['ENGR_KEITH'] += 5
        if re.search(r"(feel|sad|happy|worried|love|empathy)", lower): scores['SHIRL'] += 5
        if re.search(r"(plan|future|imagine|vision|create|generate)", lower): scores['DREAM'] += 5
        if re.search(r"(security|admin|access|auth|system|key)", lower): scores['GABRIEL'] += 5
        if re.search(r"(advice|strategy|wise|guide|mentor)", lower): scores['POPS'] += 5
        if re.search(r"(sql|query|select|join|database|table|customers|orders|products)", lower): scores['SQL_SORCERER'] = 10
        if re.search(r"(review|analyze|bug|security|performance|refactor|lint)", lower): scores['CODE_REVIEWER'] = 8
        if re.search(r"(api|endpoint|rest|openapi|swagger|route)", lower): scores['API_ARCHITECT'] = 8
        if re.search(r"(regex|pattern|match|replace|capture|extract)", lower): scores['REGEX_WIZARD'] = 10
        if re.search(r"(json|transform|restructure|jq|schema)", lower): scores['JSON_TRANSFORMER'] = 8
        
        if "last_agent" in st.session_state and st.session_state.last_agent in scores:
            scores[st.session_state.last_agent] += 2
        
        best = max(scores, key=scores.get)
        if scores[best] == 0: best = "GABRIEL"
        st.session_state.last_agent = best
        return best

    @staticmethod
    def get_provider(agent):
        return {"ENGR_KEITH": "Claude", "SHIRL": "Claude", "DREAM": "OpenAI", "GABRIEL": "NVIDIA", "POPS": "DeepSeek", "SQL_SORCERER": "Claude", "CODE_REVIEWER": "Claude", "API_ARCHITECT": "Claude", "REGEX_WIZARD": "Gemini", "JSON_TRANSFORMER": "Gemini"}.get(agent, "Gemini")

# --- KNOWLEDGE GRAPH ---
class KnowledgeGraph:
    def __init__(self):
        if 'kg_nodes' not in st.session_state: st.session_state.kg_nodes = set()
        if 'kg_edges' not in st.session_state: st.session_state.kg_edges = []
    
    def add_text(self, text):
        import itertools
        entities = []
        if re.search(r"(Gemini)", text, re.I): entities.append("GEMINI")
        if re.search(r"(Claude|Anthropic)", text, re.I): entities.append("CLAUDE")
        if re.search(r"(Gabriel|System)", text, re.I): entities.append("GABRIEL")
        if re.search(r"(OpenAI|GPT)", text, re.I): entities.append("OPENAI")
        if re.search(r"(NVIDIA)", text, re.I): entities.append("NVIDIA")
        if re.search(r"(latency)", text, re.I): entities.append("LATENCY")
        
        for e in entities: st.session_state.kg_nodes.add(e)
        for a,b in itertools.combinations(entities, 2):
            edge = tuple(sorted((a,b)))
            if edge not in st.session_state.kg_edges: st.session_state.kg_edges.append(edge)
        return len(entities)
    
    def get_dot(self):
        dot = 'graph {\n  rankdir=LR;\n  node [shape=box, style=filled, color="#00ff00", fontcolor="#0e1117"];\n'
        for n in st.session_state.kg_nodes: dot += f'  "{n}";\n'
        for a,b in st.session_state.kg_edges: dot += f'  "{a}" -- "{b}";\n'
        return dot + '}'

# --- AI GENERATORS ---
def generate_claude(prompt, key, sys=""):
    url = "https://api.anthropic.com/v1/messages"
    headers = {"x-api-key": key, "anthropic-version": "2023-06-01", "content-type": "application/json"}
    data = {"model": "claude-3-5-sonnet-20240620", "max_tokens": 1024, "messages": [{"role": "user", "content": f"{sys}\n\n{prompt}" if sys else prompt}]}
    try:
        req = urllib.request.Request(url, data=json.dumps(data).encode(), headers=headers)
        with urllib.request.urlopen(req) as r: return json.loads(r.read().decode())['content'][0]['text']
    except Exception as e: return f"Claude Error: {e}"

def generate_nvidia(prompt, key, sys=""):
    url = "https://integrate.api.nvidia.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    data = {"model": "nvidia/llama-3.1-nemotron-70b-instruct", "messages": [{"role": "user", "content": f"{sys}\n\n{prompt}" if sys else prompt}], "max_tokens": 1024}
    try:
        req = urllib.request.Request(url, data=json.dumps(data).encode(), headers=headers)
        with urllib.request.urlopen(req) as r: return json.loads(r.read().decode())['choices'][0]['message']['content']
    except Exception as e: return f"NVIDIA Error: {e}"

def generate_openai(prompt, key, sys=""):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    msgs = [{"role": "system", "content": sys}] if sys else []
    msgs.append({"role": "user", "content": prompt})
    data = {"model": "gpt-4o", "messages": msgs, "max_tokens": 1024}
    try:
        req = urllib.request.Request(url, data=json.dumps(data).encode(), headers=headers)
        with urllib.request.urlopen(req) as r: return json.loads(r.read().decode())['choices'][0]['message']['content']
    except Exception as e: return f"OpenAI Error: {e}"

def generate_deepseek(prompt, key, sys=""):
    url = "https://api.deepseek.com/chat/completions"
    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    msgs = [{"role": "system", "content": sys}] if sys else []
    msgs.append({"role": "user", "content": prompt})
    data = {"model": "deepseek-chat", "messages": msgs, "max_tokens": 1024}
    try:
        req = urllib.request.Request(url, data=json.dumps(data).encode(), headers=headers)
        with urllib.request.urlopen(req) as r: return json.loads(r.read().decode())['choices'][0]['message']['content']
    except Exception as e: return f"DeepSeek Error: {e}"

def generate_any(prompt, provider, keys, sys=""):
    if provider == "Gemini" and keys['gemini']:
        model = genai.GenerativeModel('gemini-1.5-flash')
        return model.generate_content(f"{sys}\n\n{prompt}" if sys else prompt).text
    elif provider == "Claude" and keys['claude']: return generate_claude(prompt, keys['claude'], sys)
    elif provider == "NVIDIA" and keys['nvidia']: return generate_nvidia(prompt, keys['nvidia'], sys)
    elif provider == "OpenAI" and keys['openai']: return generate_openai(prompt, keys['openai'], sys)
    elif provider == "DeepSeek" and keys['deepseek']: return generate_deepseek(prompt, keys['deepseek'], sys)
    return f"⚠️ Missing {provider} key"

# --- MAIN UI ---
st.title("⚔️ GABRIEL SYSTEM OMEGA")

# Initialize
if 'chat_history' not in st.session_state: st.session_state.chat_history = []
keys = {"gemini": api_key_gemini, "claude": api_key_claude, "nvidia": api_key_nvidia, "openai": api_key_openai, "deepseek": api_key_deepseek}

# TABS
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🧠 BRAIN", "✨ DREAMCHAMBER", "🕸️ MEMORY", "🔑 ADMIN", "🔊 EARS"])

# TAB 1: BRAIN (Main AI Interface)
with tab1:
    st.header("🧠 Concept Refiner")
    user_input = st.text_area("Enter your idea...", height=100, key="brain_input")
    
    if st.button("⚡ EXECUTE", key="brain_btn"):
        if not any(keys.values()):
            st.error("⚠️ Add at least one API key in sidebar")
        else:
            agent = SmartRouter.route(user_input) if enable_autopilot else "GABRIEL"
            prov = SmartRouter.get_provider(agent) if enable_autopilot else provider
            sys_prompt = AGENT_PROMPTS.get(agent, "")
            
            with st.status(f"⚔️ {agent} via {prov}...", expanded=True):
                result = generate_any(user_input, prov, keys, sys_prompt)
            
            st.markdown("### Response:")
            st.markdown(result)
            KnowledgeGraph().add_text(f"{user_input} {result}")

# TAB 2: DREAMCHAMBER (Multi-AI)
with tab2:
    st.header("✨ DREAMCHAMBER // Multi-AI Convergence")
    dream_input = st.text_area("Enter your vision...", height=100, key="dream_input")
    
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1: use_gem = st.checkbox("Gemini", True, key="d_gem")
    with c2: use_cla = st.checkbox("Claude", True, key="d_cla")
    with c3: use_nvi = st.checkbox("NVIDIA", True, key="d_nvi")
    with c4: use_oai = st.checkbox("OpenAI", True, key="d_oai")
    with c5: use_ds = st.checkbox("DeepSeek", True, key="d_ds")
    
    if st.button("🚀 ACTIVATE DREAMCHAMBER", key="dream_btn"):
        results = {}
        sys = "You are a visionary AI. Be bold, creative, and actionable."
        
        with st.status("🌌 Consulting AI Collective...", expanded=True) as status:
            if use_gem and api_key_gemini:
                st.write("⚡ Gemini...")
                results["Gemini"] = generate_any(dream_input, "Gemini", keys, sys)
            if use_cla and api_key_claude:
                st.write("⚡ Claude...")
                results["Claude"] = generate_any(dream_input, "Claude", keys, sys)
            if use_nvi and api_key_nvidia:
                st.write("⚡ NVIDIA...")
                results["NVIDIA"] = generate_any(dream_input, "NVIDIA", keys, sys)
            if use_oai and api_key_openai:
                st.write("⚡ OpenAI...")
                results["OpenAI"] = generate_any(dream_input, "OpenAI", keys, sys)
            if use_ds and api_key_deepseek:
                st.write("⚡ DeepSeek...")
                results["DeepSeek"] = generate_any(dream_input, "DeepSeek", keys, sys)
            status.update(label=f"✅ {len(results)} visions received", state="complete")
        
        for name, resp in results.items():
            with st.expander(f"🔮 {name}", expanded=True): st.markdown(resp)

# TAB 3: MEMORY (Knowledge Graph)
with tab3:
    st.header("🕸️ Knowledge Graph")
    kg = KnowledgeGraph()
    
    c1, c2 = st.columns([1, 2])
    with c1:
        mem_input = st.text_area("Feed memory...", height=150, key="mem_input", value="Gabriel uses Gemini and Claude for zero latency.")
        if st.button("INGEST", key="mem_btn"):
            count = kg.add_text(mem_input)
            st.success(f"Absorbed {count} entities")
    with c2:
        if st.session_state.kg_nodes:
            st.graphviz_chart(kg.get_dot())
        else:
            st.info("Memory empty. Feed data.")

# TAB 4: ADMIN (Key Inspection)
with tab4:
    st.header("🔑 Anthropic Admin Tools")
    c1, c2 = st.columns(2)
    with c1: admin_key = st.text_input("Admin Key (sk-ant-admin...)", type="password", key="admin_k")
    with c2: target_id = st.text_input("Target Key ID (apikey_...)", key="target_k")
    
    if st.button("INSPECT KEY", key="admin_btn"):
        if admin_key and target_id:
            try:
                url = f"https://api.anthropic.com/v1/organizations/api_keys/{target_id}"
                req = urllib.request.Request(url)
                req.add_header("X-Api-Key", admin_key)
                with urllib.request.urlopen(req) as r:
                    st.json(json.loads(r.read().decode()))
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.error("Both keys required")

# TAB 5: EARS (Audio Analysis)
with tab5:
    st.header("🔊 Audio Analysis")
    uploaded = st.file_uploader("Upload Audio (MP3/WAV)", type=["mp3", "wav"], key="audio_up")
    
    if uploaded:
        st.audio(uploaded)
        if st.button("ANALYZE", key="audio_btn"):
            if api_key_gemini:
                with st.spinner("Analyzing..."):
                    temp = "temp_audio.mp3"
                    with open(temp, "wb") as f: f.write(uploaded.getbuffer())
                    myfile = genai.upload_file(temp)
                    model = genai.GenerativeModel("gemini-1.5-flash")
                    result = model.generate_content([myfile, "Describe mood, BPM, and video prompt for this audio."])
                    st.markdown(result.text)
                    os.remove(temp)
            else:
                st.error("Need Gemini key for audio analysis")

# --- LIVE CHAT ---
st.divider()
st.header("💬 LIVE CHAT // Gabriel Direct Line")

for msg in st.session_state.chat_history[-10:]:
    avatar = "⚔️" if msg['role'] == 'assistant' else None
    st.chat_message(msg['role'], avatar=avatar).write(msg['content'])

user_msg = st.chat_input("Talk to Gabriel...")

if user_msg:
    st.session_state.chat_history.append({"role": "user", "content": user_msg})
    
    agent = SmartRouter.route(user_msg)
    prov = SmartRouter.get_provider(agent)
    sys_prompt = AGENT_PROMPTS.get(agent, AGENT_PROMPTS["GABRIEL"])
    
    response = generate_any(user_msg, prov, keys, sys_prompt)
    st.session_state.chat_history.append({"role": "assistant", "content": f"[{agent}] {response}"})
    
    KnowledgeGraph().add_text(f"{user_msg} {response}")
    st.rerun()

if st.button("🗑️ Clear Chat"):
    st.session_state.chat_history = []
    st.rerun()

# --- SYSTEM STATUS ---
st.divider()
c1, c2, c3 = st.columns(3)
with c1: st.metric("Engines", f"{online}/5")
with c2: st.metric("Memory Nodes", len(st.session_state.get('kg_nodes', set())))
with c3: st.metric("Status", "🟢 LIVE" if online > 0 else "🔴 OFFLINE")

st.success("⚔️ GABRIEL SYSTEM OMEGA // GORUNFREE")
