#!/usr/bin/env python3
import json
import sys
import random
from pathlib import Path
import turbo_config as cfg

# ------------------------------------------------------------------------------
# 🎻 THE CONDUCTOR (CREATIVE SINGULARITY ENGINE)
# ------------------------------------------------------------------------------
# Responsibilities:
# 1. Ingest a "Vibe" or "Intent" from MemCell/User.
# 2. Translated it into vectors for Audio, Video, and Text.
# 3. Dispatch commands to sub-systems.

class Conductor:
    def __init__(self):
        self.active_vibe = None
    
    def orchestrate(self, intent):
        cfg.print_header("🎻 THE CONDUCTOR", f"Orchestrating Vibe: {intent}")
        
        # 1. DECODE INTENT (Simulated Logic for now)
        # In future, this uses the Llama-3-8B Local Model to infer params
        vibe_matrix = self.decode_vibe(intent)
        
        # 2. DISPATCH COMMANDS
        self.signal_audio_engine(vibe_matrix['audio'])
        self.signal_visual_cortex(vibe_matrix['visual'])
        self.signal_language_center(vibe_matrix['text'])
        
        print(f"\n{cfg.GREEN}CORE > ✨ SINGULARITY ACHIEVED. ALL SYSTEMS SYNCED.{cfg.RESET}")
        return vibe_matrix

    def decode_vibe(self, intent):
        """
        GENIUS UPGRADE: USES GEMINI 1.5 FLASH (Google Scooby Snacks)
        Decodes complex intent into Vibe Vectors via API.
        """
        api_key = cfg.API_KEYS.get("Gemini")
        if not api_key:
            cfg.system_log("⚠️  GEMINI API KEY MISSING. FALLING BACK TO LEGACY LOGIC.", "WARN")
            return self.decode_vibe_legacy(intent)

        cfg.print_step(f"Consulting Gemini 1.5 Flash for: '{intent}'")
        
        # PROMPT ENGINEERING for VIBE VECTORS
        prompt = f"""
        ACT AS "THE CONDUCTOR", A SYNESTHETIC AI.
        Decode the user's INTENT: "{intent}"
        
        Return a JSON object (NO MARKDOWN) with:
        - audio: {{ "bpm": int, "key": str, "style": str }}
        - visual: {{ "palette": str (Hex code + name), "style": str }}
        - text: {{ "tone": str }}
        
        RULES:
        - Be creative. "Cyberpunk" -> Industrial Techno, Neon Purple.
        - "Forest" -> Ambient, Green/Brown.
        - "Chaos" -> Breakcore, Red/Black.
        """
        
        try:
            # REST API CALL to Gemini 1.5 (Google AI Studio)
            # URL format: https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=API_KEY
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-001:generateContent?key={api_key}"
            
            payload = {
                "contents": [{"parts": [{"text": prompt}]}]
            }
            
            # Use curl/subprocess if requests is not guaranteed, but standard python usually has json/urllib
            # We will use urllib to be dependency-free (Standard Lib)
            import urllib.request
            import urllib.error
            
            data = json.dumps(payload).encode('utf-8')
            req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
            
            try:
                with urllib.request.urlopen(req) as response:
                    result = json.loads(response.read().decode('utf-8'))
            except urllib.error.HTTPError as e:
                error_body = e.read().decode()
                cfg.system_log(f"Gemini API Error {e.code}: {error_body}", "ERROR")
                raise e
                
            # Parse Response
            raw_text = result['candidates'][0]['content']['parts'][0]['text']
            # Clean Markdown wrappers if present
            clean_json = raw_text.replace("```json", "").replace("```", "").strip()
            vibe_matrix = json.loads(clean_json)
            
            print(f"   🧠 {cfg.GREEN}GEMINI FLASH: VIBE DECODED.{cfg.RESET}")
            return vibe_matrix
            
        except Exception as e:
            cfg.system_log(f"Gemini Inference Failed: {e}", "ERROR")
            return self.decode_vibe_legacy(intent)

    def decode_vibe_legacy(self, intent):
        # HARDCODED LEGACY LOGIC (Fallback)
        if "cyberpunk" in intent.lower() or "dark" in intent.lower():
            return {
                "audio": {"bpm": 140, "key": "F# Minor", "style": "Industrial Techno"},
                "visual": {"palette": "#8A2BE2 (Neon Purple)", "style": "Glitch Art, High Contrast"},
                "text": {"tone": "Staccato, Cynical, Tech-Noir"}
            }
        elif "nature" in intent.lower() or "calm" in intent.lower():
            return {
                "audio": {"bpm": 80, "key": "C Major", "style": "Ambient Drone"},
                "visual": {"palette": "#228B22 (Forest Green)", "style": "Organic, Soft Focus"},
                "text": {"tone": "Flowing, poetic, serene"}
            }
        else:
            return {
                "audio": {"bpm": 120, "key": "A Minor", "style": "House"},
                "visual": {"palette": "#000000 (Monochrome)", "style": "Minimalist"},
                "text": {"tone": "Neutral, informative"}
            }

    def signal_audio_engine(self, params):
        print(f"   🔊 {cfg.CYAN}AUDIO:{cfg.RESET} BPM={params['bpm']} | KEY={params['key']} | STYLE={params['style']}")
        # Integration Point: Send to Ableton / MaxMSP / MusicGen

    def signal_visual_cortex(self, params):
        print(f"   🎨 {cfg.MAGENTA}VIDEO:{cfg.RESET} PALETTE={params['palette']} | STYLE={params['style']}")
        # Integration Point: Send to ComfyUI / TouchDesigner

    def signal_language_center(self, params):
        print(f"   📝 {cfg.WHITE}TEXT :{cfg.RESET} TONE={params['tone']}")
        # Integration Point: Set System Prompt for Chat

if __name__ == "__main__":
    if len(sys.argv) > 1:
        Conductor().orchestrate(sys.argv[1])
    else:
        Conductor().orchestrate("Cyberpunk Anxiety")
