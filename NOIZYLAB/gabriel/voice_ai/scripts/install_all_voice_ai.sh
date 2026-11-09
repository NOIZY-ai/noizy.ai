#!/bin/zsh
# 🎤 INSTALL ALL VOICE AI TOOLS
# GORUNFREE Protocol - Maximum Velocity

echo "🎤 INSTALLING ALL VOICE AI TOOLS"
echo "================================="
echo ""

# Check Python
echo "📦 Checking Python..."
python3 --version || { echo "❌ Python 3 not found!"; exit 1; }

# Install Python packages
echo ""
echo "📦 Installing Python packages..."
pip3 install pyttsx3 gTTS edge-tts requests aiohttp python-dotenv 2>&1 | grep -E "(Successfully|Requirement|ERROR)" | tail -10

# Check Whisper
echo ""
echo "📦 Checking Whisper..."
if command -v whisper &> /dev/null; then
    echo "✅ Whisper installed"
else
    echo "⚠️  Whisper not in PATH (may be installed)"
fi

# Check Azure CLI
echo ""
echo "📦 Checking Azure CLI..."
if command -v az &> /dev/null; then
    echo "✅ Azure CLI installed"
    az --version | head -3
else
    echo "⚠️  Azure CLI not found"
fi

# Check ffmpeg
echo ""
echo "📦 Checking ffmpeg..."
if command -v ffmpeg &> /dev/null; then
    echo "✅ ffmpeg installed"
    ffmpeg -version | head -1
else
    echo "⚠️  ffmpeg not found"
fi

# Check sox
echo ""
echo "📦 Checking sox..."
if command -v sox &> /dev/null; then
    echo "✅ sox installed"
    sox --version | head -1
else
    echo "⚠️  sox not found"
fi

# Create .env template
echo ""
echo "📝 Creating .env template..."
ENV_FILE="/Users/m2ultra/NOIZYLAB/MC96/.env.voice_ai"
if [ ! -f "$ENV_FILE" ]; then
    cat > "$ENV_FILE" << 'EOF'
# Voice AI API Keys
# Get keys from:
# Azure: https://portal.azure.com
# ElevenLabs: https://elevenlabs.io
# Resemble: https://www.resemble.ai

AZURE_SPEECH_KEY=your-azure-speech-key-here
AZURE_SPEECH_REGION=eastus

ELEVENLABS_API_KEY=your-elevenlabs-key-here

RESEMBLE_API_KEY=your-resemble-key-here

# Google Cloud TTS (optional)
GOOGLE_CLOUD_TTS_KEY=your-google-key-here

# OpenAI (for Whisper)
OPENAI_API_KEY=your-openai-key-here
EOF
    echo "✅ Created $ENV_FILE"
    echo "   → Edit this file with your API keys"
else
    echo "✅ .env file already exists"
fi

# Test installations
echo ""
echo "🧪 Testing installations..."
python3 << 'PYEOF'
try:
    import azure.cognitiveservices.speech
    print("✅ Azure Speech SDK: Installed")
except:
    print("❌ Azure Speech SDK: Not installed")

try:
    import whisper
    print("✅ Whisper: Installed")
except:
    print("❌ Whisper: Not installed")

try:
    import gtts
    print("✅ gTTS: Installed")
except:
    print("❌ gTTS: Not installed")

try:
    import edge_tts
    print("✅ edge-tts: Installed")
except:
    print("❌ edge-tts: Not installed")

try:
    import pyttsx3
    print("✅ pyttsx3: Installed")
except:
    print("❌ pyttsx3: Not installed")
PYEOF

echo ""
echo "✅ INSTALLATION COMPLETE!"
echo ""
echo "🚀 Quick Start:"
echo "  python3 /Users/m2ultra/NOIZYLAB/MC96/voice_ai_universal.py --list"
echo "  python3 /Users/m2ultra/NOIZYLAB/MC96/voice_ai_universal.py --generate 'Hello!' --service azure"
echo ""
echo "📝 Next Steps:"
echo "  1. Edit $ENV_FILE with your API keys"
echo "  2. Get API keys from service providers"
echo "  3. Start generating voices!"

