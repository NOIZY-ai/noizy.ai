#!/bin/zsh
# 🚀 INSTALL ULTRA DEPENDENCIES
# GORUNFREE Protocol

echo "🚀 Installing Ultra Dependencies..."
echo "===================================="
echo ""

# Install FastAPI and Uvicorn
echo "📦 Installing FastAPI & Uvicorn..."
pip3 install fastapi uvicorn 2>&1 | tail -5

# Install gTTS if needed
echo ""
echo "📦 Checking gTTS..."
python3 -c "import gtts" 2>/dev/null && echo "✅ gTTS already installed" || pip3 install gTTS

# Install websockets for real-time
echo ""
echo "📦 Installing websockets..."
pip3 install websockets 2>&1 | tail -3

echo ""
echo "✅ Ultra dependencies installed!"
echo ""
echo "🚀 Now you can run:"
echo "  python3 voice_ai_api_server.py"
echo "  python3 voice_ai_ultra.py --generate 'Test' --service gtts"

