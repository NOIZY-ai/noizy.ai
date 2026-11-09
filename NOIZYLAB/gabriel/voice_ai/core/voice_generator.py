#!/usr/bin/env python3
"""
🚀 MICROSOFT VOICE GENERATOR & CLONER
Azure Speech Services - Text-to-Speech with Neural Voices
GORUNFREE Protocol
"""

import os
import sys
import azure.cognitiveservices.speech as speechsdk

def list_available_voices():
    """List all available neural voices"""
    print("🎤 Available Neural Voices:")
    print("=" * 60)
    
    # Popular neural voices
    voices = {
        "en-US": [
            ("Aria", "Female", "Neural"),
            ("Jenny", "Female", "Neural"),
            ("Guy", "Male", "Neural"),
            ("Davis", "Male", "Neural"),
            ("Amber", "Female", "Neural"),
            ("Ana", "Female", "Neural"),
            ("Ashley", "Female", "Neural"),
            ("Brandon", "Male", "Neural"),
            ("Christopher", "Male", "Neural"),
            ("Eric", "Male", "Neural"),
            ("Michelle", "Female", "Neural"),
            ("Roger", "Male", "Neural"),
            ("Steffan", "Male", "Neural"),
        ],
        "en-GB": [
            ("Libby", "Female", "Neural"),
            ("Maisie", "Female", "Neural"),
            ("Ryan", "Male", "Neural"),
            ("Sonia", "Female", "Neural"),
            ("Thomas", "Male", "Neural"),
        ],
        "en-AU": [
            ("Natasha", "Female", "Neural"),
            ("William", "Male", "Neural"),
        ],
    }
    
    for locale, voice_list in voices.items():
        print(f"\n{locale}:")
        for name, gender, style in voice_list:
            print(f"  • {name} ({gender}) - {style}")

def generate_speech(text, voice_name="en-US-AriaNeural", output_file="output.wav", 
                   speech_key=None, service_region="eastus"):
    """
    Generate speech from text using Azure Neural TTS
    
    Args:
        text: Text to convert to speech
        voice_name: Voice to use (default: Aria)
        output_file: Output audio file path
        speech_key: Azure Speech API key
        service_region: Azure region
    """
    # Get API key from environment or parameter
    if not speech_key:
        speech_key = os.environ.get("AZURE_SPEECH_KEY")
        if not speech_key:
            print("❌ Error: AZURE_SPEECH_KEY not set!")
            print("Get your key at: https://portal.azure.com")
            print("Then set: export AZURE_SPEECH_KEY='your-key'")
            return False
    
    # Configure speech synthesizer
    speech_config = speechsdk.SpeechConfig(
        subscription=speech_key,
        region=service_region
    )
    
    # Set voice
    speech_config.speech_synthesis_voice_name = voice_name
    
    # Create audio config
    audio_config = speechsdk.audio.AudioOutputConfig(filename=output_file)
    
    # Create synthesizer
    synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config,
        audio_config=audio_config
    )
    
    print(f"🎤 Generating speech with {voice_name}...")
    print(f"📝 Text: {text[:50]}...")
    
    # Synthesize
    result = synthesizer.speak_text_async(text).get()
    
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print(f"✅ Speech generated successfully!")
        print(f"📁 Saved to: {output_file}")
        return True
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speechsdk.CancellationDetails(result)
        print(f"❌ Error: {cancellation_details.reason}")
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print(f"   Details: {cancellation_details.error_details}")
        return False
    
    return False

def clone_voice_info():
    """Information about voice cloning options"""
    print("\n" + "=" * 60)
    print("🎭 VOICE CLONING OPTIONS")
    print("=" * 60)
    print("""
1. AZURE CUSTOM NEURAL VOICE (Enterprise):
   • Create custom voices from training data
   • Requires Azure subscription
   • Access: https://speech.microsoft.com/portal
   • Need: Audio recordings (minimum 1 hour)
   • Process: Upload → Train → Deploy

2. VALL-E (Research - Not Publicly Available):
   • Microsoft's 3-second voice cloning
   • Currently not released due to ethical concerns
   • Research only

3. AZURE NEURAL TTS (Available Now):
   • High-quality neural voices
   • Multiple languages and styles
   • Real-time synthesis
   • This script uses this!

SETUP INSTRUCTIONS:
1. Get Azure Speech Key:
   az login
   az cognitiveservices account create \\
     --name speech-service \\
     --resource-group ai-resources \\
     --kind SpeechServices \\
     --sku S0 \\
     --location eastus
   
   az cognitiveservices account keys list \\
     --name speech-service \\
     --resource-group ai-resources

2. Set environment variable:
   export AZURE_SPEECH_KEY="your-key"
   export AZURE_SPEECH_REGION="eastus"

3. Use this script:
   python3 voice_generator.py "Hello, this is a test!"
    """)

def main():
    if len(sys.argv) < 2:
        print("🚀 MICROSOFT VOICE GENERATOR")
        print("=" * 60)
        print("\nUsage:")
        print("  python3 voice_generator.py \"Your text here\"")
        print("  python3 voice_generator.py \"Your text\" --voice en-US-JennyNeural")
        print("  python3 voice_generator.py --list")
        print("  python3 voice_generator.py --clone-info")
        print("\nExamples:")
        print("  python3 voice_generator.py \"Hello, I am a neural voice!\"")
        print("  python3 voice_generator.py \"Test\" --voice en-GB-LibbyNeural --output test.wav")
        return
    
    if "--list" in sys.argv:
        list_available_voices()
        return
    
    if "--clone-info" in sys.argv:
        clone_voice_info()
        return
    
    # Get text
    text = sys.argv[1]
    
    # Parse options
    voice = "en-US-AriaNeural"
    output = "output.wav"
    region = os.environ.get("AZURE_SPEECH_REGION", "eastus")
    
    if "--voice" in sys.argv:
        idx = sys.argv.index("--voice")
        if idx + 1 < len(sys.argv):
            voice = sys.argv[idx + 1]
    
    if "--output" in sys.argv:
        idx = sys.argv.index("--output")
        if idx + 1 < len(sys.argv):
            output = sys.argv[idx + 1]
    
    # Generate speech
    generate_speech(text, voice, output, service_region=region)

if __name__ == "__main__":
    main()

