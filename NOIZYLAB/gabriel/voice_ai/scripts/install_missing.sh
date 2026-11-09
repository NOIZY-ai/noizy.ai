#!/bin/zsh
# 🔧 INSTALL ALL MISSING COMPONENTS
# GORUNFREE Protocol - Complete Installation

echo "🔧 INSTALLING ALL MISSING COMPONENTS"
echo "===================================="
echo ""

# Activate virtual environment if it exists
if [ -d ".ai-env" ]; then
    echo "📦 Activating virtual environment..."
    source .ai-env/bin/activate
fi

# Install all missing Python packages
echo ""
echo "📦 Installing Python packages..."
pip3 install --upgrade pip 2>&1 | tail -3

echo ""
echo "📦 Installing voice AI packages..."
pip3 install gtts pyttsx3 openai-whisper azure-cognitiveservices-speech 2>&1 | tail -5

echo ""
echo "📦 Installing web framework packages..."
pip3 install fastapi uvicorn flask 2>&1 | tail -5

echo ""
echo "📦 Installing audio processing packages..."
pip3 install pydub librosa soundfile 2>&1 | tail -5

echo ""
echo "📦 Installing utility packages..."
pip3 install requests aiohttp python-dotenv websockets 2>&1 | tail -5

# Install system tools
echo ""
echo "🔧 Checking system tools..."

if ! command -v ffmpeg &> /dev/null; then
    echo "📦 Installing ffmpeg..."
    brew install ffmpeg 2>&1 | tail -5
else
    echo "✅ ffmpeg already installed"
fi

if ! command -v whisper &> /dev/null; then
    echo "💡 Whisper CLI: Install with 'pip3 install openai-whisper' then 'whisper --help'"
fi

# Verify installations
echo ""
echo "✅ Verifying installations..."
python3 << 'PYEOF'
import sys
modules = [
    ('gtts', 'gTTS'),
    ('pyttsx3', 'pyttsx3'),
    ('whisper', 'Whisper'),
    ('azure.cognitiveservices.speech', 'Azure Speech'),
    ('fastapi', 'FastAPI'),
    ('uvicorn', 'Uvicorn'),
    ('flask', 'Flask'),
    ('pydub', 'pydub'),
    ('librosa', 'librosa'),
    ('soundfile', 'soundfile'),
]

print("\n📊 Installation Status:")
print("-" * 40)
all_ok = True
for module, name in modules:
    try:
        __import__(module)
        print(f"✅ {name}")
    except ImportError:
        print(f"❌ {name}")
        all_ok = False

if all_ok:
    print("\n✅ ALL MODULES INSTALLED!")
else:
    print("\n⚠️  Some modules still missing")
PYEOF

echo ""
echo "✅ Installation complete!"
echo ""
echo "🚀 Test with:"
echo "  python3 voice_ai_pro.py --list"
echo "  python3 voice_ai_ultra.py --generate 'Test' --service gtts"

