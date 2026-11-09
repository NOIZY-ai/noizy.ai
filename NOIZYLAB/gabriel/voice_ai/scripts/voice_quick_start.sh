#!/bin/zsh
# 🎤 MICROSOFT VOICE GENERATOR QUICK START
# GORUNFREE Protocol

echo "🎤 MICROSOFT VOICE GENERATOR & CLONER"
echo "===================================="
echo ""

# Check if Azure Speech SDK is installed
if ! python3 -c "import azure.cognitiveservices.speech" 2>/dev/null; then
    echo "📦 Installing Azure Speech SDK..."
    pip3 install azure-cognitiveservices-speech
    echo ""
fi

# Check for API key
if [ -z "$AZURE_SPEECH_KEY" ]; then
    echo "⚠️  AZURE_SPEECH_KEY not set!"
    echo ""
    echo "Get your key:"
    echo "1. Login: az login"
    echo "2. Create service:"
    echo "   az cognitiveservices account create \\"
    echo "     --name speech-service \\"
    echo "     --resource-group ai-resources \\"
    echo "     --kind SpeechServices \\"
    echo "     --sku S0 \\"
    echo "     --location eastus"
    echo ""
    echo "3. Get key:"
    echo "   az cognitiveservices account keys list \\"
    echo "     --name speech-service \\"
    echo "     --resource-group ai-resources"
    echo ""
    echo "4. Set: export AZURE_SPEECH_KEY='your-key'"
    echo ""
    read -p "Press Enter to open Azure Portal..."
    open https://portal.azure.com
    exit 1
fi

echo "✅ Azure Speech SDK: Ready"
echo "✅ API Key: Set"
echo ""
echo "🚀 Quick Commands:"
echo "  python3 voice_generator.py \"Your text here\""
echo "  python3 voice_generator.py \"Text\" --voice en-US-JennyNeural"
echo "  python3 voice_generator.py --list"
echo ""
echo "🌐 Web Access:"
echo "  Speech Studio: https://speech.microsoft.com/portal"
echo "  Azure Portal: https://portal.azure.com"
echo ""

# Interactive menu
echo "Choose an option:"
echo "  1) Generate speech (enter text)"
echo "  2) List available voices"
echo "  3) Open Speech Studio"
echo "  4) Open Azure Portal"
echo "  5) Voice cloning info"
echo ""
read -p "Option (1-5): " choice

case $choice in
  1)
    read -p "Enter text to convert: " text
    read -p "Voice (default: en-US-AriaNeural): " voice
    voice=${voice:-en-US-AriaNeural}
    read -p "Output file (default: output.wav): " output
    output=${output:-output.wav}
    python3 /Users/m2ultra/NOIZYLAB/MC96/voice_generator.py "$text" --voice "$voice" --output "$output"
    ;;
  2)
    python3 /Users/m2ultra/NOIZYLAB/MC96/voice_generator.py --list
    ;;
  3)
    open https://speech.microsoft.com/portal
    ;;
  4)
    open https://portal.azure.com
    ;;
  5)
    python3 /Users/m2ultra/NOIZYLAB/MC96/voice_generator.py --clone-info
    ;;
  *)
    echo "Invalid option"
    ;;
esac

