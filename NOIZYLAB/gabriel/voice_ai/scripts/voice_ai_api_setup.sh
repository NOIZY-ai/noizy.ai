#!/bin/zsh
# 🎤 VOICE AI API SETUP GUIDE
# GORUNFREE Protocol

echo "🎤 VOICE AI API SETUP GUIDE"
echo "============================"
echo ""

echo "📋 GET API KEYS FROM:"
echo ""
echo "1. AZURE SPEECH:"
echo "   → https://portal.azure.com"
echo "   → Create Speech Service"
echo "   → Get API key"
echo "   → Set: export AZURE_SPEECH_KEY='your-key'"
echo "   → Set: export AZURE_SPEECH_REGION='eastus'"
echo ""

echo "2. ELEVENLABS:"
echo "   → https://elevenlabs.io"
echo "   → Sign up / Login"
echo "   → Get API key from dashboard"
echo "   → Set: export ELEVENLABS_API_KEY='your-key'"
echo ""

echo "3. RESEMBLE AI:"
echo "   → https://www.resemble.ai"
echo "   → Sign up / Login"
echo "   → Get API key"
echo "   → Set: export RESEMBLE_API_KEY='your-key'"
echo ""

echo "4. REPLICA STUDIOS:"
echo "   → https://www.replicastudios.com"
echo "   → Sign up / Login"
echo "   → Get API key"
echo "   → Set: export REPLICA_API_KEY='your-key'"
echo ""

echo "5. GOOGLE CLOUD TTS:"
echo "   → https://cloud.google.com/text-to-speech"
echo "   → Create project"
echo "   → Enable API"
echo "   → Get credentials"
echo "   → Set: export GOOGLE_CLOUD_TTS_KEY='your-key'"
echo ""

echo "💾 SAVE TO ~/.zshrc:"
echo ""
echo "Add these lines to ~/.zshrc:"
echo "  export AZURE_SPEECH_KEY='your-key'"
echo "  export AZURE_SPEECH_REGION='eastus'"
echo "  export ELEVENLABS_API_KEY='your-key'"
echo "  export RESEMBLE_API_KEY='your-key'"
echo "  export REPLICA_API_KEY='your-key'"
echo ""
echo "Then run: source ~/.zshrc"
echo ""

read -p "Open Azure Portal to get API key? (y/n): " open_azure
if [ "$open_azure" = "y" ]; then
    open https://portal.azure.com
fi

read -p "Open ElevenLabs to get API key? (y/n): " open_eleven
if [ "$open_eleven" = "y" ]; then
    open https://elevenlabs.io
fi

read -p "Open Resemble AI to get API key? (y/n): " open_resemble
if [ "$open_resemble" = "y" ]; then
    open https://www.resemble.ai
fi

echo ""
echo "✅ Setup guide complete!"

