import functions_framework
import google.generativeai as genai
import os
import json

# --- CONFIGURATION ---
# In a real deployment, use environment variables: os.environ.get("GEMINI_API_KEY")
# genai.configure(api_key="YOUR_KEY_HERE")

SYSTEM_VERSION = "3.0.0-GOOGLE"

# --- AGENT DNA ---
AGENTS = {
    "GABRIEL": {"role": "System Bridge", "traits": ["reliable", "fast"], "model": "gemini-1.5-flash"},
    "POPS": {"role": "Creative Director", "traits": ["artistic", "vibrant"], "model": "gemini-1.5-pro"},
    "SHIRL": {"role": "Ops Manager", "traits": ["efficient", "organized"], "model": "gemini-1.5-flash"},
    "ENGR_KEITH": {"role": "Chief Engineer", "traits": ["precise", "technical"], "model": "gemini-1.5-pro"}
}

@functions_framework.http
def noizylab_worker(request):
    """
    Google Cloud Function: NoizyLab Agent Worker
    Deploy with: gcloud functions deploy noizylab_worker --runtime python310 --trigger-http
    """
    
    # 1. CORS Setup (Allow your Streamlit app to talk to this)
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }
        return ('', 204, headers)

    headers = {'Access-Control-Allow-Origin': '*'}

    # 2. Parse Request
    try:
        request_json = request.get_json(silent=True)
        request_args = request.args
        
        # Determine Route (using a 'action' parameter or path if using generic routing)
        action = request_json.get('action') if request_json else request_args.get('action')
        
        if not action:
            return (json.dumps({"status": "alive", "version": SYSTEM_VERSION, "agents": list(AGENTS.keys())}), 200, headers)

        # 3. ROUTER // LOGIC
        
        # ACTION: ASK_AGENT
        if action == "agent_invoke":
            agent_name = request_json.get('agent', 'GABRIEL')
            prompt = request_json.get('prompt', '')
            
            if agent_name not in AGENTS:
                return (json.dumps({"error": "Unknown Agent"}), 400, headers)
                
            agent = AGENTS[agent_name]
            
            # Call Gemini
            model = genai.GenerativeModel(agent['model'])
            response = model.generate_content(
                f"You are {agent_name} ({agent['role']}). Traits: {agent['traits']}. User asks: {prompt}"
            )
            
            return (json.dumps({
                "agent": agent_name,
                "response": response.text,
                "model_used": agent['model']
            }), 200, headers)

        # ACTION: LIGHTHOUSE_AUDIT
        elif action == "lighthouse_audit":
            content = request_json.get('content', '')
            model = genai.GenerativeModel('gemini-1.5-pro') # Use Pro for deep analysis
            audit = model.generate_content(
                f"Perform a Google Lighthouse style audit (0-100 scores) for specific actionable categories on this content: {content}"
            )
            return (json.dumps({"audit_report": audit.text}), 200, headers)

        else:
            return (json.dumps({"error": "Unknown Action"}), 400, headers)

    except Exception as e:
        return (json.dumps({"error": str(e)}), 500, headers)
