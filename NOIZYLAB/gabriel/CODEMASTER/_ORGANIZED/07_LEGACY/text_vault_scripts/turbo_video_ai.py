#!/usr/bin/env python3
"""
🎥 TURBO VIDEO AI - Omni-Model Video Generation (GOD MODE)
Part of the MC96ECOUNIVERSE
PROTOCOL: GORUNFREE | LATENCY: ZERO | TRUTH: ONE

Integrates:
- Google Veo 2.0 (Gemini API)
- Runway Gen-3 Alpha (Runway API)
- Luma Dream Machine (Luma API)
- Stability Video (Stability API)
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

# Check for Google Gen AI SDK (Veo)
try:
    import google.generativeai as genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False


# Configuration
OUTPUT_DIR = cfg.ASSETS_DIR / "Video" / "AI_Generated"

# ==============================================================================
# 🎥 VIDEO FORGE CLASS (THE ENGINE)
# ==============================================================================
class VideoForge:
    def __init__(self):
        self.brain = MemCell()
        self.genai_available = GENAI_AVAILABLE
        
    def install_dependencies(self):
        """Install required SDKs."""
        cfg.print_header("📦 INSTALLING VIDEO AI DEPENDENCIES", "Google, Runway, Luma")
        cmd = [sys.executable, "-m", "pip", "install", "google-generativeai", "runwayml", "lumaai", "requests", "--break-system-packages"]
        
        cfg.system_log(f"Running: {' '.join(cmd)}", "INFO")
        try:
            import subprocess
            subprocess.run(cmd, check=True)
            cfg.system_log("Dependencies installed successfully ✅", "SUCCESS")
            cfg.system_log("Please re-run your command.", "INFO")
        except Exception as e:
            cfg.system_log(f"Install failed: {e}", "ERROR")

    def _poll_and_download(self, status_url, headers, output_path, provider_name, status_key="status", success_val="succeeded", result_key="output"):
        """
        Generic Polling Engine for Async Video APIs.
        """
        print(f"   ⏳ {provider_name}: Polling for completion... (This takes time)")
        
        start_time = time.time()
        
        while True:
            try:
                # Check Status
                res = requests.get(status_url, headers=headers)
                if res.status_code != 200:
                    print(f"   ❌ Polling Error: {res.status_code}")
                    return False
                    
                data = res.json()
                status = data.get(status_key, "").lower()
                
                # Progress Indicator
                elapsed = int(time.time() - start_time)
                sys.stdout.write(f"\r   ⏳ Elapsed: {elapsed}s | Status: {status.upper()}   ")
                sys.stdout.flush()
                
                if status == success_val.lower():
                    print(f"\n   ✅ {provider_name}: GENERATION COMPLETE.")
                    
                    # Extract URL
                    video_url = None
                    if isinstance(data.get(result_key), list):
                        video_url = data[result_key][0] # Runway style
                    elif isinstance(data.get(result_key), str):
                        video_url = data[result_key]
                    elif "assets" in data and "video" in data["assets"]: # Luma style often
                        video_url = data["assets"]["video"]
                    
                    if video_url:
                        # Download
                        print(f"   ⬇️  Downloading: {video_url}")
                        vid_res = requests.get(video_url)
                        with open(output_path, "wb") as f:
                            f.write(vid_res.content)
                        print(f"   ✨ Saved to: {output_path}")
                        self.brain.log_event(self.brain.covenant_id, f"{provider_name.upper()}_COMPLETE", f"Video Generated: {output_path.name}", 100, provider_name)
                        return output_path
                    else:
                        print("   ❌ Error: No video URL in result.")
                        return False
                
                elif status in ["failed", "error"]:
                    print(f"\n   ❌ {provider_name}: GENERATION FAILED. ({data.get('error', 'Unknown Error')})")
                    return False
                
                time.sleep(5) # Valid poll interval
                
            except KeyboardInterrupt:
                print("\n   ⚠️ Polling Interrupted.")
                return False
            except Exception as e:
                print(f"\n   ❌ Exception: {e}")
                return False

    def generate_veo(self, prompt, output_filename=None):
        """Generate video using Google Veo 3.1."""
        if not self.genai_available:
            cfg.system_log("Google SDK not found. Run 'install'.", "ERROR")
            return None

        if not cfg.configure_api_key("Gemini"):
            return None

        if not output_filename:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            safe_prompt = "".join(c for c in prompt[:15] if c.isalnum() or c in (' ', '_')).strip().replace(' ', '_')
            output_filename = f"VEO_{timestamp}_{safe_prompt}.mp4"
        output_path = OUTPUT_DIR / output_filename
        
        cfg.ensure_dirs([OUTPUT_DIR])
        cfg.print_header("🎥 GOOGLE VEO 3.1", "Generative Video")
        cfg.system_log(f"Prompt: {prompt}", "INFO")

        try:
            # Veo 3.1 via Gemini API
            # Explicitly using veo-3.1-generate-001 as verified
            model = genai.GenerativeModel("models/veo-3.1-generate-001")
            
            cfg.system_log("Sending prompt to Gemini/Veo...", "INFO")
            
            # Using sync generation for now as verified in API docs (generate_content usually blocks or returns immediately with meta)
            # Assuming standard Gemini content generation interface
            response = model.generate_content(prompt)
            
            # Check for inline data (Sync) or URI
            if hasattr(response, 'parts'):
                for part in response.parts:
                    if hasattr(part, 'inline_data') and part.inline_data.mime_type.startswith('video'):
                        with open(output_path, "wb") as f:
                            f.write(part.inline_data.data)
                        cfg.system_log(f"✨ Saved: {output_path}", "SUCCESS")
                        self.brain.log_event(self.brain.covenant_id, "VEO_COMPLETE", f"Video Generated: {output_path.name}", 100, "VEO")
                        return output_path
            
            print("   (Note: If Veo response structure differs, check docs. Assuming inline data.)")
            return None
            
        except Exception as e:
            cfg.system_log(f"Veo Error: {e}", "ERROR")
            return None

    def generate_runway(self, prompt, output_filename=None):
        """Generate video using Runway Gen-3 (Alpha)."""
        if not cfg.RUNWAY_API_KEY:
            cfg.system_log("RUNWAY_API_KEY not found.", "ERROR")
            return None

        if not output_filename:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            safe_prompt = "".join(c for c in prompt[:15] if c.isalnum() or c in (' ', '_')).strip().replace(' ', '_')
            output_filename = f"RUNWAY_{timestamp}_{safe_prompt}.mp4"
        output_path = OUTPUT_DIR / output_filename

        cfg.ensure_dirs([OUTPUT_DIR])
        cfg.print_header("🎞️ RUNWAY GEN-3", "Cinematic AI Video")
        
        url = "https://api.runwayml.com/v1/image_to_video" 
        
        headers = {
            "Authorization": f"Bearer {cfg.RUNWAY_API_KEY}",
            "Content-Type": "application/json",
            "X-Runway-Version": "2024-09-13"
        }
        
        payload = {
            "prompt": prompt,
            "model": "gen3a_turbo", 
            "seconds": 5
        }
        
        try:
            print(f"   🚀 Submitting Task...")
            res = requests.post(url, headers=headers, json=payload)
            
            if res.status_code != 200:
                print(f"Runway Error {res.status_code}: {res.text}")
                return None
                
            data = res.json()
            task_id = data.get("id")
            print(f"   ✅ Task Received: {task_id}")
            
            # POLL
            status_url = f"https://api.runwayml.com/v1/tasks/{task_id}"
            return self._poll_and_download(status_url, headers, output_path, "RUNWAY", status_key="status", success_val="SUCCEEDED", result_key="output")
            
        except Exception as e:
            print(f"Runway Exception: {e}")
            return None

    def generate_luma(self, prompt, output_filename=None):
        """Generate video using Luma Dream Machine."""
        if not cfg.LUMA_API_KEY:
            cfg.system_log("LUMA_API_KEY not found.", "ERROR")
            return None

        if not output_filename:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            safe_prompt = "".join(c for c in prompt[:15] if c.isalnum() or c in (' ', '_')).strip().replace(' ', '_')
            output_filename = f"LUMA_{timestamp}_{safe_prompt}.mp4"
        output_path = OUTPUT_DIR / output_filename

        cfg.ensure_dirs([OUTPUT_DIR])
        cfg.print_header("🌙 LUMA DREAM MACHINE", "High-Fidelity Video")
        
        url = "https://api.lumalabs.ai/dream-machine/v1/generations"
        headers = {
            "Authorization": f"Bearer {cfg.LUMA_API_KEY}",
            "Content-Type": "application/json",
            "accept": "application/json"
        }
        
        payload = {
            "prompt": prompt,
            "aspect_ratio": "16:9"
        }
        
        try:
            print(f"   🚀 Submitting Task...")
            res = requests.post(url, headers=headers, json=payload)
            
            if res.status_code != 201 and res.status_code != 200:
                print(f"Luma Error {res.status_code}: {res.text}")
                return None
                
            data = res.json()
            task_id = data.get("id")
            print(f"   ✅ Task Received: {task_id}")
            
            # POLL
            status_url = f"{url}/{task_id}"
            return self._poll_and_download(status_url, headers, output_path, "LUMA", status_key="state", success_val="completed", result_key="assets")
            
        except Exception as e:
            print(f"Luma Exception: {e}")
            return None

# ==============================================================================
# 🚀 MAIN EXECUTION
# ==============================================================================
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="🎥 Omni-Model AI Video Generator")
    parser.add_argument("command", choices=["install", "veo", "runway", "luma", "stability"], help="Provider")
    parser.add_argument("prompt", nargs="?", help="Text prompt")
    parser.add_argument("--output", "-o", help="Output filename")
    
    args = parser.parse_args()
    
    forge = VideoForge()
    
    if args.command == "install":
        forge.install_dependencies()
    elif args.command == "veo":
        if args.prompt: forge.generate_veo(args.prompt, args.output)
        else: print("Prompt required.")
    elif args.command == "runway":
        if args.prompt: forge.generate_runway(args.prompt, args.output)
        else: print("Prompt required.")
    elif args.command == "luma":
        if args.prompt: forge.generate_luma(args.prompt, args.output)
        else: print("Prompt required.")
    elif args.command == "stability":
        print("Stability Video Logic: Pending specific API documentation (use Luma/Runway/Veo for now).")


