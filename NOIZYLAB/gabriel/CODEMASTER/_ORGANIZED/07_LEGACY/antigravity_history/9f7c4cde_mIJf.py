import os
import sys
import json
import base64
from dotenv import load_dotenv
from noizy_cortex import analyze_track_advanced
from noizy_memcell import memory_core

# Load environment variables
load_dotenv()

# NOIZYLAB DIRECTOR v2.0 (UPGRADED)
# "The Auteur" Module: Advanced AI Integration
# Powered by MemCell & Multi-Persona Architecture (SHIRL/ENGR)

def check_api_key():
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        print("!!! ERROR: ANTHROPIC_API_KEY not found.")
        return False
    return True

def get_claude_direction(audio_file, persona="DIRECTOR"):
    if not check_api_key(): return

    try:
        import anthropic
    except ImportError:
        print("!!! ERROR: Anthropic SDK not found.")
        return

    # 1. MEMCELL SYNC
    server_time = memory_core.get_time_matrix()["human"]
    print(f"\n>>> [DIRECTOR v2] TIME MATRIX: {server_time}")
    memory_core.log_interaction(f"Analyzing {os.path.basename(audio_file)}", "DIRECTOR_START", persona)

    # 2. ANALYZE (The Ears)
    print(f"    -> [SENSORS] Scanning Audio: {os.path.basename(audio_file)}...")
    features = analyze_track_advanced(audio_file)
    
    # 3. PROMPT GENERATION (The Mind)
    # Dynamic Persona Injection
    directive = memory_core.get_persona_directive(persona)
    role_desc = directive["role"] if directive else "Creative Visionary"
    
    system_prompt = f"""
    You are the NOIZYLAB DIRECTOR AI ({role_desc}).
    OPERATING PARAMETERS: MAXIMUM STRENGTH, ZERO LATENCY, 100% INTUITIVE INTELLIGENCE.
    
    PERSONA CONTEXT:
    - If 'SHIRL': Focus on Temporal Logic, Historical Context, and Emotional Resonance.
    - If 'ENGR': Focus on Technical Precision, Optimization, Acoustics, and Fabrication.
    - If 'DIRECTOR': Focus on Avant-Garde Visuals, Narrative Flow, and Cinematic Excellence.
    
    YOUR MISSION: Transform the audio analysis into a supreme creative output.
    """
    
    user_prompt = f"""
    [INPUT DATA STREAM]
    Target: {os.path.basename(audio_file)}
    Time: {server_time}
    
    [AUDIO TELEMETRY]
    - BPM: {features['bpm']}
    - Key: {features['key']}
    - Energy: {features['energy_db']} dB
    - Timbre: {features['timbre']} Hz
    - Chord Probability: {features.get('chord', 'Unknown')}
    
    [DIRECTIVE]
    Generate a 'Master Plan' for this audio.
    1. CONCEPT: A high-concept visual or thematic hook.
    2. EXECUTION: Specific editing/technical techniques (sync to BPM).
    3. AI PROMPT: A perfect prompt for Sora/Veo generation.
    4. OPTIMIZATION: One 'Pro Tip' to improve the track itself (Mix/Composition).
    """
    
    print(f"\n>>> [UPLINK] CONTACTING CLAUDE 3.5 ({persona} MODE)...")
    
    client = anthropic.Anthropic()
    stream = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=1500,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}],
        stream=True
    )
    
    print("\n>>> [TRANSMISSION RECEIVED]")
    print("---------------------------------------------------")
    
    full_response = ""
    for event in stream:
        if event.type == "content_block_delta":
            text = event.delta.text
            sys.stdout.write(text)
            sys.stdout.flush()
            full_response += text
            
    print("\n---------------------------------------------------")

    # Save to Hive Mind
    out_file = audio_file + f"_{persona}_BRIEF.md"
    with open(out_file, "w") as f:
        f.write(f"# DIRECTOR'S FLIGHT PLAN ({persona})\n")
        f.write(f"Generated: {server_time}\n\n")
        f.write(full_response)
        
    print(f"    -> Brief saved to: {out_file}")
    memory_core.log_interaction("Brief Generated", "SUCCESS", persona)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 anthropic_director.py <audio_file> [PERSONA]")
        sys.exit(1)
        
    target_file = sys.argv[1]
    target_persona = sys.argv[2] if len(sys.argv) > 2 else "DIRECTOR"
    
    get_claude_direction(target_file, target_persona)
