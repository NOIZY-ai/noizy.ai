#!/usr/bin/env python3
"""
✅ VERIFY ALL INSTALLATIONS
Complete system verification
GORUNFREE Protocol
"""

import sys
import os

def check_module(module_name, import_name=None):
    """Check if module is installed"""
    if import_name is None:
        import_name = module_name
    
    try:
        __import__(import_name)
        return True, "✅"
    except ImportError:
        return False, "❌"

def main():
    print("🔍 VERIFYING ALL INSTALLATIONS")
    print("=" * 60)
    print()
    
    # Core voice AI modules
    modules = [
        ("gTTS", "gtts"),
        ("Edge TTS", "edge_tts"),
        ("pyttsx3", "pyttsx3"),
        ("Whisper", "whisper"),
        ("Azure Speech", "azure.cognitiveservices.speech"),
        ("Flask", "flask"),
        ("FastAPI", "fastapi"),
        ("Uvicorn", "uvicorn"),
        ("Websockets", "websockets"),
        ("pydub", "pydub"),
        ("librosa", "librosa"),
        ("soundfile", "soundfile"),
        ("requests", "requests"),
        ("aiohttp", "aiohttp"),
        ("python-dotenv", "dotenv"),
    ]
    
    print("📦 PYTHON MODULES:")
    print("-" * 60)
    all_ok = True
    for name, module in modules:
        installed, status = check_module(name, module)
        print(f"{status} {name:20s} ({module})")
        if not installed:
            all_ok = False
    
    print()
    print("🔧 SYSTEM TOOLS:")
    print("-" * 60)
    
    # Check CLI tools
    import subprocess
    
    tools = [
        ("Whisper CLI", "whisper"),
        ("Azure CLI", "az"),
        ("ffmpeg", "ffmpeg"),
        ("sox", "sox"),
    ]
    
    for name, cmd in tools:
        try:
            result = subprocess.run([cmd, "--version"], 
                                  capture_output=True, 
                                  timeout=2)
            if result.returncode == 0:
                print(f"✅ {name:20s} ({cmd})")
            else:
                print(f"❌ {name:20s} ({cmd}) - Not found")
                all_ok = False
        except:
            print(f"❌ {name:20s} ({cmd}) - Not found")
            all_ok = False
    
    print()
    print("📁 VOICE AI SCRIPTS:")
    print("-" * 60)
    
    scripts = [
        "voice_ai_universal.py",
        "voice_ai_pro.py",
        "voice_ai_ultra.py",
        "voice_ai_web.py",
        "voice_ai_api_server.py",
        "voice_cloner.py",
        "voice_generator.py",
    ]
    
    for script in scripts:
        if os.path.exists(script):
            print(f"✅ {script}")
        else:
            print(f"❌ {script} - Missing")
            all_ok = False
    
    print()
    print("🎮 INTEGRATION FILES:")
    print("-" * 60)
    
    integrations = [
        "unity_voice_integration.cs",
        "unreal_voice_integration.cpp",
    ]
    
    for integration in integrations:
        if os.path.exists(integration):
            print(f"✅ {integration}")
        else:
            print(f"❌ {integration} - Missing")
    
    print()
    print("=" * 60)
    if all_ok:
        print("✅ ALL INSTALLATIONS VERIFIED!")
        print("🚀 System ready for maximum performance!")
    else:
        print("⚠️  Some installations missing")
        print("💡 Run: ./install_ultra_dependencies.sh")
    print()

if __name__ == "__main__":
    main()

