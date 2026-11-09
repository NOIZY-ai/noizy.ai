#!/usr/bin/env python3
"""
🎧 TURBO AUDIO AI - AI-Powered Audio Processing
Part of the MC96ECOUNIVERSE
PROTOCOL: GORUNFREE | LATENCY: ZERO | TRUTH: ONE

Integrates:
- Demucs (META AI) - Source Separation
- Spleeter (Deezer) - Stem Splitting
- Whisper (OpenAI) - Speech-to-Text
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

try:
    import turbo_config as cfg
    import turbo_prompts as prompts
    from turbo_memcell import MemCell
except ImportError:
    sys.path.append(str(Path(__file__).parent))
    import turbo_config as cfg
    import turbo_prompts as prompts
    from turbo_memcell import MemCell

# Configuration
OUTPUT_DIR = cfg.ASSETS_DIR / "Audio" / "AI_Processed"

# Tool Registry
AI_AUDIO_TOOLS = {
    "demucs": {
        "name": "Demucs (META AI)",
        "purpose": "Source Separation - Isolate vocals, drums, bass, other",
        "install": "pip install demucs",
        "command": "demucs",
        "free": True,
        "url": "https://github.com/facebookresearch/demucs"
    },
    "spleeter": {
        "name": "Spleeter (Deezer)",
        "purpose": "Stem Splitting - 2/4/5 stems",
        "install": "pip install spleeter",
        "command": "spleeter",
        "free": True,
        "url": "https://github.com/deezer/spleeter"
    },
    "whisper": {
        "name": "Whisper (OpenAI)",
        "purpose": "Speech-to-Text Transcription",
        "install": "pip install openai-whisper",
        "command": "whisper",
        "free": True,
        "url": "https://github.com/openai/whisper"
    },
    "izotope_rx": {
        "name": "iZotope RX",
        "purpose": "Industry-standard Audio Repair & Restoration",
        "install": "Commercial - https://www.izotope.com/rx",
        "command": None,
        "free": False,
        "url": "https://www.izotope.com/en/products/rx.html"
    },
    "adobe_podcast": {
        "name": "Adobe Podcast",
        "purpose": "Free Voice Enhancement (Web)",
        "install": "Web-based - https://podcast.adobe.com/enhance",
        "command": None,
        "free": True,
        "url": "https://podcast.adobe.com/enhance"
    },"apple_speech": {
        "name": "Apple Speech (Mac Native)",
        "purpose": "Local TTS via 'say' command",
        "install": "Built-in",
        "command": "say",
        "free": True,
        "url": None
    },
    "voicefixer": {
        "name": "VoiceFixer (SOTA)",
        "purpose": "AI Restoration (Noise, Reverb, Clipping)",
        "install": "pip install voicefixer",
        "command": "python3", # Library usage
        "free": True,
        "url": "https://github.com/haoheliu/voicefixer"
    }
}

# ==============================================================================
# 🧠 AUDIO ENHANCER CLASS (THE ENGINE)
# ==============================================================================
class AudioEnhancer:
    def __init__(self):
        self.brain = MemCell()
        
    def check_tool(self, tool_key):
        """Check if a CLI tool is installed."""
        tool = AI_AUDIO_TOOLS.get(tool_key)
        if not tool or not tool.get("command"):
            return False
        return shutil.which(tool["command"]) is not None

    def list_tools(self):
        """Display available AI audio tools."""
        cfg.print_header("🎧 AI AUDIO TOOLS", "Neural Audio Processing")
        
        for key, tool in AI_AUDIO_TOOLS.items():
            installed = self.check_tool(key)
            status = f"{cfg.GREEN}✅ INSTALLED{cfg.RESET}" if installed else f"{cfg.YELLOW}⚠️ NOT INSTALLED{cfg.RESET}"
            free_tag = f"{cfg.GREEN}FREE{cfg.RESET}" if tool["free"] else f"{cfg.YELLOW}COMMERCIAL{cfg.RESET}"
            
            print(f"\n{cfg.BOLD}[{key.upper()}]{cfg.RESET} {tool['name']} [{free_tag}]")
            print(f"   Purpose: {tool['purpose']}")
            print(f"   Status:  {status}")
            if not installed and tool.get("install"):
                print(f"   Install: {cfg.DIM}{tool['install']}{cfg.RESET}")

    def separate_stems(self, input_file, tool="demucs"):
        """Use AI to separate audio into stems."""
        input_path = Path(input_file)
        
        if not input_path.exists():
            cfg.system_log(f"File not found: {input_path}", "ERROR")
            return
        
        cfg.print_header(f"🎧 STEM SEPARATION", f"Using {tool.upper()}")
        self.brain.log_event(self.brain.covenant_id, "AI_AUDIO", f"Stem separation started: {input_path.name}", vibe=80, author="AUDIO_AI")
        
        cfg.ensure_dirs([OUTPUT_DIR])
        
        if tool == "demucs":
            if not self.check_tool("demucs"):
                cfg.system_log("Demucs not installed. Run: pip install demucs", "ERROR")
                return
            
            cmd = ["demucs", "-o", str(OUTPUT_DIR), str(input_path)]
            cfg.system_log(f"Running: {' '.join(cmd)}", "INFO")
            
            try:
                subprocess.run(cmd, check=True)
                cfg.system_log(f"✨ Stems saved to: {OUTPUT_DIR}", "SUCCESS")
                self.brain.log_event(self.brain.covenant_id, "AI_AUDIO_COMPLETE", f"Stems created for: {input_path.name}", vibe=100, author="AUDIO_AI")
            except subprocess.CalledProcessError as e:
                cfg.system_log(f"Demucs failed: {e}", "ERROR")
                
        elif tool == "spleeter":
            if not self.check_tool("spleeter"):
                cfg.system_log("Spleeter not installed. Run: pip install spleeter", "ERROR")
                return
            
            cmd = ["spleeter", "separate", "-o", str(OUTPUT_DIR), str(input_path)]
            cfg.system_log(f"Running: {' '.join(cmd)}", "INFO")
            
            try:
                subprocess.run(cmd, check=True)
                cfg.system_log(f"✨ Stems saved to: {OUTPUT_DIR}", "SUCCESS")
            except subprocess.CalledProcessError as e:
                cfg.system_log(f"Spleeter failed: {e}", "ERROR")

    def transcribe_audio(self, input_file, model="base"):
        """Use Whisper to transcribe audio to text."""
        input_path = Path(input_file)
        
        if not input_path.exists():
            cfg.system_log(f"File not found: {input_path}", "ERROR")
            return
        
        cfg.print_header("🎤 AUDIO TRANSCRIPTION", "Using Whisper AI")
        self.brain.log_event(self.brain.covenant_id, "AI_TRANSCRIBE", f"Transcription started: {input_path.name}", vibe=80, author="WHISPER_AI")
        
        if not self.check_tool("whisper"):
            cfg.system_log("Whisper not installed. Run: pip install openai-whisper", "ERROR")
            return
        
        output_path = input_path.parent / f"{input_path.stem}_transcript.txt"
        cmd = ["whisper", str(input_path), "--model", model, "--output_format", "txt", "--output_dir", str(input_path.parent)]
        
        try:
            subprocess.run(cmd, check=True)
            cfg.system_log(f"✨ Transcript saved to: {output_path}", "SUCCESS")
            self.brain.log_event(self.brain.covenant_id, "AI_TRANSCRIBE_COMPLETE", f"Transcript created: {input_path.name}", vibe=100, author="WHISPER_AI")
        except subprocess.CalledProcessError as e:
            cfg.system_log(f"Whisper failed: {e}", "ERROR")

    def install_free_tools(self):
        """Install all free AI audio tools."""
        cfg.print_header("📦 INSTALLING AI AUDIO TOOLS", "Setting up the Neural Audio Lab")
        
        tools_to_install = [
            ("demucs", "pip install demucs"),
            ("spleeter", "pip install spleeter"),
            ("whisper", "pip install openai-whisper")
        ]
        
        for tool_name, install_cmd in tools_to_install:
            if self.check_tool(tool_name):
                cfg.system_log(f"{tool_name}: Already installed ✅", "SUCCESS")
            else:
                cfg.system_log(f"Installing {tool_name}...", "INFO")
                try:
                    subprocess.run(install_cmd.split(), check=True)
                    cfg.system_log(f"{tool_name}: Installed ✅", "SUCCESS")
                except subprocess.CalledProcessError:
                    cfg.system_log(f"{tool_name}: Install failed ❌", "ERROR")

    def repair_audio(self, input_file, output_file=None):
        """Use VoiceFixer to repair audio."""
        input_path = Path(input_file)
        
        if not input_path.exists():
            cfg.system_log(f"File not found: {input_path}", "ERROR")
            return
            
        cfg.print_header("🩺 AI AUDIO REPAIR", "Using VoiceFixer (SOTA)")
        self.brain.log_event(self.brain.covenant_id, "AI_REPAIR", f"Repair started: {input_path.name}", vibe=80, author="VOICEFIXER")
        
        if output_file:
            output_path = Path(output_file)
        else:
            output_path = input_path.parent / f"{input_path.stem}_repaired.wav"
        
        try:
            from voicefixer import VoiceFixer
            vf = VoiceFixer()
            vf.restore(input=str(input_path), output=str(output_path), cuda=False, mode=0) 
            
            cfg.system_log(f"✨ Repaired Audio saved to: {output_path}", "SUCCESS")
            self.brain.log_event(self.brain.covenant_id, "AI_REPAIR_COMPLETE", f"Repair finished: {input_path.name}", vibe=100, author="VOICEFIXER")
            
        except ImportError:
            cfg.system_log("VoiceFixer lib not found. Run: python3 -m pip install voicefixer", "ERROR")
        except Exception as e:
            cfg.system_log(f"Repair failed: {e}", "ERROR")


# ==============================================================================
# 🚀 MAIN EXECUTION
# ==============================================================================
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="🎧 AI Audio Processing Tools")
    parser.add_argument("command", nargs="?", choices=["list", "install", "separate", "transcribe", "repair"], default="list")
    parser.add_argument("--file", "-f", help="Input audio file")
    parser.add_argument("--tool", "-t", choices=["demucs", "spleeter"], default="demucs", help="Separation tool")
    parser.add_argument("--model", "-m", default="base", help="Whisper model size")
    
    args = parser.parse_args()
    
    # Instantiate Engine
    engine = AudioEnhancer()
    
    if args.command == "list":
        engine.list_tools()
    elif args.command == "install":
        engine.install_free_tools()
    elif args.command == "separate":
        if not args.file:
            print("Error: --file required for separation")
        else:
            engine.separate_stems(args.file, args.tool)
            engine.transcribe_audio(args.file, args.model)
    elif args.command == "repair":
        if not args.file:
            print("Error: --file required for repair")
        else:
            engine.repair_audio(args.file)
