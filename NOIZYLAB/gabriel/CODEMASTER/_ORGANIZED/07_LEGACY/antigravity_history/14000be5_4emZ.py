#!/usr/bin/env python3
"""
🎥 TURBO VEO - AI Video Generation
Part of the MC96ECOUNIVERSE
PROTOCOL: GORUNFREE | LATENCY: ZERO | TRUTH: ONE

Integrates:
- Google Veo 2.0 (models/veo-2.0-generate-001) via Gemini API
"""

import os
import sys
import time

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

# Check for Google Gen AI SDK
try:
    import google.generativeai as genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False


# Configuration
OUTPUT_DIR = cfg.ASSETS_DIR / "Video" / "AI_Generated"
MODEL_NAME = "models/veo-2.0-generate-001"

def install_dependencies():
    """Install required Google AI SDK."""
    cfg.print_header("📦 INSTALLING VEO DEPENDENCIES", "Setting up Google AI SDK")
    cmd = [sys.executable, "-m", "pip", "install", "google-generativeai"]
    
    cfg.system_log(f"Running: {' '.join(cmd)}", "INFO")
    try:
        import subprocess
        subprocess.run(cmd, check=True)
        cfg.system_log("google-generativeai installed successfully ✅", "SUCCESS")
        cfg.system_log("Please re-run your command.", "INFO")
    except Exception as e:
        cfg.system_log(f"Install failed: {e}", "ERROR")

def configure_api():
    """Configure the Gemini API key."""
    if not GENAI_AVAILABLE:
        cfg.system_log("Google Generative AI SDK not found.", "ERROR")
        cfg.system_log("Run: python3 turbo_veo.py install", "WARN")
        return False

    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        cfg.system_log("No API Key found. Set GEMINI_API_KEY or GOOGLE_API_KEY environment variable.", "ERROR")
        return False
    
    genai.configure(api_key=api_key)
    return True

def generate_video(prompt, output_filename=None, duration_seconds=5):
    """
    Generate a video using Google Veo 2.0.
    
    Args:
        prompt (str): The text description of the video.
        output_filename (str): Optional filename. If None, generated from timestamp.
        duration_seconds (int): Desired duration (default 5 for Veo).
    """
    brain = MemCell()
    
    if not configure_api():
        return

    cfg.ensure_dirs([OUTPUT_DIR])
    
    # Generate filename if not provided
    if not output_filename:
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        safe_prompt = "".join(c for c in prompt[:20] if c.isalnum() or c in (' ', '_', '-')).strip().replace(' ', '_')
        output_filename = f"VEO_{timestamp}_{safe_prompt}.mp4"
    
    output_path = OUTPUT_DIR / output_filename
    
    cfg.print_header("🎥 VEO 2.0 GENERATION", "Connecting to Google AI")
    cfg.system_log(f"Prompt: {prompt}", "INFO")
    cfg.system_log(f"Model: {MODEL_NAME}", "INFO")
    
    brain.log_event(brain.covenant_id, "AI_VIDEO_START", f"Generating video: {prompt[:50]}...", vibe=90, author="VEO_AI")

    try:
        # Instantiate model
        model = genai.GenerativeModel(MODEL_NAME)
        
        cfg.system_log("Sending request to Neural Net...", "INFO")
        start_time = time.time()
        
        # Call generation
        response = model.generate_content(prompt)
        
        # Process response
        video_data = None
        
        # Inspect response for video data
        if hasattr(response, 'parts'):
            for part in response.parts:
                if hasattr(part, 'inline_data') and part.inline_data.mime_type.startswith('video'):
                    video_data = part.inline_data.data
                    break
        
        if video_data:
             with open(output_path, "wb") as f:
                f.write(video_data)
             cfg.system_log(f"✨ Video saved to: {output_path}", "SUCCESS")
             elapsed = time.time() - start_time
             cfg.system_log(f"Generation Time: {elapsed:.2f}s", "INFO")
             brain.log_event(brain.covenant_id, "AI_VIDEO_COMPLETE", f"Video created: {output_filename}", vibe=100, author="VEO_AI")
        else:
            cfg.system_log("Response received but no standard video data found.", "WARN")
            cfg.system_log(str(response), "DEBUG")

    except Exception as e:
        cfg.system_log(f"Generation Warning: {e}", "WARN")
        brain.log_event(brain.covenant_id, "AI_VIDEO_ERROR", f"Failed: {prompt[:30]}", vibe=20, author="VEO_AI")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="🎥 Google Veo 2.0 Video Generator")
    parser.add_argument("command", nargs="?", default="generate", choices=["generate", "install"], help="Action to perform")
    parser.add_argument("--prompt", "-p", help="Text prompt for video generation (required for generate)")
    parser.add_argument("--output", "-o", help="Output filename")
    
    args = parser.parse_args()
    
    if args.command == "install":
        install_dependencies()
    elif args.command == "generate":
        if args.prompt:
            generate_video(args.prompt, args.output)
        else:
            # Fallback for positional prompt argument if command is omitted or implied
            # This handles: python turbo_veo.py "Prompt"
            if len(sys.argv) > 1 and sys.argv[1] not in ["generate", "install"]:
                 generate_video(sys.argv[1], args.output)
            else:
                cfg.print_header("🎥 TURBO VEO", "Google Veo 2.0 Integration")
                print("Usage: python3 turbo_veo.py \"A futuristic cyber-city\"")
                print("       python3 turbo_veo.py install")

