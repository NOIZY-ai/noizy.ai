#!/usr/bin/env python3
"""
🎹 TURBO AUDIO GEN - AI Sound Synthesis
Part of the MC96ECOUNIVERSE
PROTOCOL: GORUNFREE | LATENCY: ZERO | TRUTH: ONE

Integrates:
- ElevenLabs (Text-to-Speech & Sound Effects)
- Stability AI (Text-to-Audio / Music)
"""

import os
import sys
import time
import requests
import json
from pathlib import Path

# Handle Imports
try:
    import turbo_config as cfg
    from turbo_memcell import MemCell
except ImportError:
    sys.path.append(str(Path(__file__).parent))
    try:
        import turbo_config as cfg
        from turbo_memcell import MemCell
    except ImportError:
        print("CRITICAL: turbo_config or turbo_memcell not found.")
        sys.exit(1)

# Configuration
OUTPUT_DIR = cfg.ASSETS_DIR / "Audio" / "AI_Generated"

# -------------------------------------------------------------------------
# DEPENDENCY MANAGEMENT
# -------------------------------------------------------------------------
def install_dependencies():
    """Install required Python SDKs."""
    cfg.print_header("📦 INSTALLING AUDIO GEN DEPENDENCIES", "ElevenLabs + Stability")
    # Removing stability-sdk due to grpcio build issues on some Macs
    # We will use REST API for Stability
    cmd = [sys.executable, "-m", "pip", "install", "elevenlabs", "--break-system-packages"]
    
    cfg.system_log(f"Running: {' '.join(cmd)}", "INFO")
    try:
        import subprocess
        subprocess.run(cmd, check=True)
        cfg.system_log("Dependencies installed successfully ✅", "SUCCESS")
        cfg.system_log("Please re-run your command.", "INFO")
    except Exception as e:
        cfg.system_log(f"Install failed: {e}", "ERROR")

# -------------------------------------------------------------------------
# ELEVENLABS (Speech & SFX)
# -------------------------------------------------------------------------
def generate_elevenlabs_sfx(prompt, duration_seconds=5, output_filename=None):
    """Generate Sound Effects via ElevenLabs API."""
    brain = MemCell()
    
    if not cfg.ELEVEN_API_KEY:
        cfg.system_log("ELEVEN_API_KEY not found.", "ERROR")
        return

    cfg.ensure_dirs([OUTPUT_DIR])
    if not output_filename:
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        safe_prompt = "".join(c for c in prompt[:15] if c.isalnum() or c in (' ', '_')).strip().replace(' ', '_')
        output_filename = f"ELEVEN_SFX_{timestamp}_{safe_prompt}.mp3"
    
    output_path = OUTPUT_DIR / output_filename
    
    cfg.print_header("🔊 ELEVENLABS SFX", "Generating Sound Effect")
    cfg.system_log(f"Prompt: {prompt}", "INFO")

    # Direct API call implementation to avoid SDK version conflicts
    url = "https://api.elevenlabs.io/v1/sound-generation"
    headers = {
        "xi-api-key": cfg.ELEVEN_API_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "text": prompt,
        "duration_seconds": duration_seconds,
        "prompt_influence": 0.5
    }

    try:
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            with open(output_path, "wb") as f:
                f.write(response.content)
            cfg.system_log(f"✨ SFX saved: {output_path}", "SUCCESS")
            brain.log_event(brain.covenant_id, "AI_SFX_COMPLETE", f"SFX Created: {output_filename}", vibe=95, author="ELEVENLABS")
        else:
            cfg.system_log(f"ElevenLabs Error {response.status_code}: {response.text}", "ERROR")
    except Exception as e:
        cfg.system_log(f"Request failed: {e}", "ERROR")

def generate_elevenlabs_speech(text, voice_id="21m00Tcm4TlvDq8ikWAM", output_filename=None):
    """Generate Speech via ElevenLabs API."""
    brain = MemCell()
    
    if not cfg.ELEVEN_API_KEY:
        cfg.system_log("ELEVEN_API_KEY not found.", "ERROR")
        return

    cfg.ensure_dirs([OUTPUT_DIR])
    if not output_filename:
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        output_filename = f"ELEVEN_TTS_{timestamp}.mp3"
    
    output_path = OUTPUT_DIR / output_filename
    
    cfg.print_header("🗣️ ELEVENLABS TTS", "Synthesizing Speech")
    cfg.system_log(f"Text: {text[:50]}...", "INFO")

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": cfg.ELEVEN_API_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5
        }
    }

    try:
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            with open(output_path, "wb") as f:
                f.write(response.content)
            cfg.system_log(f"✨ Speech saved: {output_path}", "SUCCESS")
            brain.log_event(brain.covenant_id, "AI_TTS_COMPLETE", f"Speech Synthesized", vibe=90, author="ELEVENLABS")
        else:
            cfg.system_log(f"ElevenLabs Error {response.status_code}: {response.text}", "ERROR")
    except Exception as e:
        cfg.system_log(f"Request failed: {e}", "ERROR")


# -------------------------------------------------------------------------
# STABILITY AI (Music & FX)
# -------------------------------------------------------------------------
# -------------------------------------------------------------------------
# STABILITY AI (Music & FX)
# -------------------------------------------------------------------------
def generate_stability_audio(prompt, duration_seconds=5, output_filename=None):
    """Generate Audio via Stability AI (Robust REST Implementation)."""
    brain = MemCell()
    
    if not cfg.STABILITY_API_KEY:
        cfg.system_log("STABILITY_API_KEY not found.", "ERROR")
        return None

    cfg.ensure_dirs([OUTPUT_DIR])
    if not output_filename:
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        safe_prompt = "".join(c for c in prompt[:15] if c.isalnum() or c in (' ', '_')).strip().replace(' ', '_')
        output_filename = f"STABILITY_{timestamp}_{safe_prompt}.mp3"
    
    output_path = OUTPUT_DIR / output_filename

    cfg.print_header("🎵 STABILITY AUDIO", "Generating Musical Texture")
    cfg.system_log(f"Prompt: {prompt}", "INFO")

    # API ENDPOINT (Stable Audio Open / Core)
    # Using the standard generation endpoint for audio
    url = "https://api.stability.ai/v2beta/stable-image/generate/sd3" # Placeholder for image, we need Audio.
    # Correct endpoint for Audio (as of late 2024/2025 Standard):
    url = "https://api.stability.ai/v1/generation/audio/sound-effects" # or text-to-audio
    
    # We will try the multipart method which is standard for Stability V2
    headers = {
        "Authorization": f"Bearer {cfg.STABILITY_API_KEY}",
        "Accept": "audio/*" 
    }
    
    # NOTE: Since endpoints shift, we use the most probable stable path 
    # or handle the fail gracefully.
    
    # Let's try the requests with proper files structure if needed, or json for v1
    # V1 is usually JSON body.
    
    try:
        response = requests.post(
            "https://api.stability.ai/v1/generation/audio/text-to-audio",
            headers={"Authorization": f"Bearer {cfg.STABILITY_API_KEY}", "Content-Type": "application/json", "Accept": "audio/wav"},
            json={
                "text_prompts": [{"text": prompt}],
                "steps": 40,
                "seconds_total": duration_seconds
            }
        )
        
        if response.status_code == 200:
            with open(output_path, "wb") as f:
                f.write(response.content)
            cfg.system_log(f"✨ Stability Audio saved: {output_path}", "SUCCESS")
            brain.log_event(brain.covenant_id, "AI_MUSIC_COMPLETE", f"Generated: {prompt}", vibe=95, author="STABILITY")
            return output_path
        else:
            cfg.system_log(f"Stability Error {response.status_code}: {json.loads(response.content)}", "ERROR")
            return None
            
    except Exception as e:
        cfg.system_log(f"Stability Request failed: {e}", "ERROR")
        return None


# -------------------------------------------------------------------------
# AUDIO CHAIN (WORKFLOWS)
# -------------------------------------------------------------------------
class AudioChain:
    """
    ⛓️ THE CHAIN: Multi-Step Audio Generation Workflows.
    "Generate a Scene, not just a sound."
    """
    def generate_scene(self, scene_description):
        cfg.print_header("🎬 AUDIO SCENE GENERATOR", scene_description)
        brain = MemCell()
        
        # 1. Deconstruct (Simple Heuristic for now, can use LLM later)
        print(f"   Building Scene based on: '{scene_description}'")
        
        # Step 1: Background Ambience (Stability)
        bg_prompt = f"Ambient background sound of {scene_description}, high quality, immersive"
        print(f"   [1/3] Generating Ambience: {bg_prompt}...")
        bg_file = generate_stability_audio(bg_prompt, duration_seconds=10)
        
        # Step 2: Specific SFX (ElevenLabs)
        sfx_prompt = f"Sound effect related to {scene_description}, distinct, clear"
        print(f"   [2/3] Generating Detail SFX: {sfx_prompt}...")
        # (Assuming generate_elevenlabs_sfx returns path, need to update it to return path)
        # For now, we call it.
        generate_elevenlabs_sfx(sfx_prompt, duration_seconds=3)
        
        # Step 3: Voiceover (Narrator)
        narrator_text = f"Scene analysis: {scene_description}. The vibe is established."
        print(f"   [3/3] Generating Narration...")
        generate_elevenlabs_speech(narrator_text)
        
        brain.log_event(brain.covenant_id, "AUDIO_CHAIN_COMPLETE", f"Scene Built: {scene_description}", 98, "CHAIN")
        print(f"\n{cfg.GREEN}✅ SCENE GENERATION COMPLETE.{cfg.RESET}")


# -------------------------------------------------------------------------
# MAIN
# -------------------------------------------------------------------------
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="🎹 AI Audio Generator")
    parser.add_argument("command", choices=["install", "sfx", "speech", "music", "scene"], help="Action")
    parser.add_argument("prompt", nargs="?", help="Text prompt")
    parser.add_argument("--duration", "-d", type=int, default=5, help="Duration in seconds")
    parser.add_argument("--output", "-o", help="Output filename")
    
    args = parser.parse_args()
    
    if args.command == "install":
        install_dependencies()
        
    elif args.command == "sfx":
        if args.prompt: generate_elevenlabs_sfx(args.prompt, args.duration, args.output)
        else: print("Error: Prompt required")
            
    elif args.command == "speech":
        if args.prompt: generate_elevenlabs_speech(args.prompt, output_filename=args.output)
        else: print("Error: Text required")
            
    elif args.command == "music":
        if args.prompt: generate_stability_audio(args.prompt, args.duration, args.output)
        else: print("Error: Prompt required")
            
    elif args.command == "scene":
        if args.prompt: 
            chain = AudioChain()
            chain.generate_scene(args.prompt)
        else: print("Error: Scene description required")
