import os
import sys
import json
import base64
from noizy_cortex import analyze_track_advanced

# NOIZYLAB DIRECTOR v1.0
# "The Auteur" Module: Anthropic Creative Genius Integration
# Purpose: Uses Claude 3.5 Sonnet to generate high-level creative direction for Audio/Video projects.

def check_api_key():
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        print("!!! ERROR: ANTHROPIC_API_KEY not found.")
        print("    -> Usage: export ANTHROPIC_API_KEY='sk-ant-...'")
        return False
    return True

def get_claude_direction(audio_file):
    if not check_api_key():
        return

    try:
        import anthropic
    except ImportError:
        print("!!! ERROR: Anthropic SDK not found. Run pip install anthropic")
        return

    # 1. ANALYZE THE AUDIO (The "Ears")
    print(f"\n>>> [ANTHROPIC DIRECTOR] LISTENING TO: {os.path.basename(audio_file)}")
    features = analyze_track_advanced(audio_file)
    
    # 2. CONSTRUCT THE PROMPT (The "Brief")
    system_prompt = "You are a visionary Music Video Director and Audio Engineer. You create avant-garde visual concepts based on audio data."
    
    user_prompt = f"""
    I have a track with the following analysis:
    - Tempo: {features['bpm']} BPM
    - Key: {features['key']}
    - Energy: {features['energy_db']} dB
    - Timbre (Brightness): {features['timbre']} Hz
    
    Please generate a 'Super-Sonic' Creative Brief for a music video.
    1. Visual Theme (Colors, Lighting, Camera Movement).
    2. Editing Pace (Cut on every beat? Slow dissolve?).
    3. A specific AI Video Prompt I can utilize in OpenAI Sora or Google Veo.
    """
    
    print("\n>>> COMMISSIONING CLAUDE 3.5 SONNET...")
    
    client = anthropic.Anthropic()
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=1000,
        system=system_prompt,
        messages=[
            {"role": "user", "content": user_prompt}
        ]
    )
    
    print("\n>>> DIRECTOR'S TREATMENT RECEIVED:")
    print("---------------------------------------------------")
    print(message.content[0].text)
    print("---------------------------------------------------")

    # Save the brief
    out_file = audio_file + "_DIRECTOR_BRIEF.md"
    with open(out_file, "w") as f:
        f.write("# DIRECTOR'S TREATMENT\n\n")
        f.write(message.content[0].text)
    print(f"    -> Saved brief to: {out_file}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 anthropic_director.py <audio_file>")
        sys.exit(1)
        
    get_claude_direction(sys.argv[1])
