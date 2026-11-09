#!/bin/zsh
# 🎤 ALL FREE VOICE TOOLS QUICK ACCESS
# GORUNFREE Protocol

echo "🎤 FREE VOICE MANIPULATION TOOLS"
echo "================================="
echo ""
echo "INSTALLED TOOLS:"
echo "  1) OpenAI Whisper (Speech Recognition)"
echo "  2) Azure Speech (Text-to-Speech)"
echo "  3) Apple Speech Framework (Built-in)"
echo ""
echo "WEB TOOLS:"
echo "  4) 15.ai (Character Voices)"
echo "  5) ElevenLabs (Voice Cloning)"
echo "  6) Typecast (AI Content)"
echo "  7) Perplexity AI"
echo ""
echo "CLOUD SERVICES:"
echo "  8) Cloudflare Workers AI"
echo "  9) Oracle OCI Speech"
echo ""
echo "OPEN SOURCE:"
echo "  10) RVC (Voice Conversion)"
echo "  11) OpenVoice (Voice Cloning)"
echo "  12) Bark (Text-to-Audio)"
echo ""
echo "TOOLS:"
echo "  13) Transcribe audio (Whisper)"
echo "  14) Generate speech (Azure)"
echo "  15) List all tools"
echo ""
read -p "Select option (1-15): " choice

case $choice in
  1)
    echo "✅ Whisper installed at: $(which whisper)"
    whisper --help | head -10
    ;;
  2)
    echo "✅ Azure Speech ready!"
    echo "Usage: voice-gen 'Your text here'"
    python3 /Users/m2ultra/NOIZYLAB/MC96/voice_generator.py --clone-info | head -20
    ;;
  3)
    echo "✅ Apple Speech Framework (Built-in)"
    echo "Available in: Speech, AVFoundation, Core ML"
    open -a Xcode 2>/dev/null || echo "Xcode not installed"
    ;;
  4)
    open https://15.dev
    ;;
  5)
    open https://elevenlabs.io
    ;;
  6)
    open https://typecast.ai
    ;;
  7)
    open https://www.perplexity.ai
    ;;
  8)
    open https://developers.cloudflare.com/workers-ai
    ;;
  9)
    open https://cloud.oracle.com/ai/speech
    ;;
  10)
    open https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI
    ;;
  11)
    open https://github.com/myshell-ai/OpenVoice
    ;;
  12)
    open https://github.com/suno-ai/bark
    ;;
  13)
    read -p "Enter audio file path: " audio_file
    if [ -f "$audio_file" ]; then
      echo "Transcribing with Whisper..."
      whisper "$audio_file" --language en --model base
    else
      echo "❌ File not found: $audio_file"
    fi
    ;;
  14)
    read -p "Enter text to speak: " text
    python3 /Users/m2ultra/NOIZYLAB/MC96/voice_generator.py "$text"
    ;;
  15)
    cat /Users/m2ultra/NOIZYLAB/MC96/ALL_FREE_VOICE_TECH_COMPLETE.md | head -100
    ;;
  *)
    echo "Invalid option"
    ;;
esac

