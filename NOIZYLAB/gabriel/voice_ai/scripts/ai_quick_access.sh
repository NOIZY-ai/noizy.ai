#!/bin/zsh
# 🚀 GOOGLE & MICROSOFT AI QUICK ACCESS
# GORUNFREE Protocol - Maximum Velocity

echo "🚀 AI QUICK ACCESS MENU"
echo "======================"
echo ""
echo "GOOGLE AI:"
echo "  1) Gemini - https://gemini.google.com"
echo "  2) NotebookLM - https://notebooklm.google.com"
echo "  3) AI Studio - https://aistudio.google.com"
echo "  4) Antigravity App"
echo ""
echo "MICROSOFT AI:"
echo "  5) Copilot - https://copilot.microsoft.com"
echo "  6) Designer - https://designer.microsoft.com"
echo "  7) Azure Portal - https://portal.azure.com"
echo "  8) Edge Browser (Copilot)"
echo ""
echo "TOOLS:"
echo "  9) Test Google AI API"
echo "  10) Test Azure CLI"
echo "  11) Open All Web Tools"
echo ""
read -p "Select option (1-11): " choice

case $choice in
  1) open https://gemini.google.com ;;
  2) open https://notebooklm.google.com ;;
  3) open https://aistudio.google.com ;;
  4) open -a "Antigravity" ;;
  5) open -a "Microsoft Edge" https://copilot.microsoft.com ;;
  6) open https://designer.microsoft.com ;;
  7) open https://portal.azure.com ;;
  8) open -a "Microsoft Edge" ;;
  9) python3 << 'EOF'
import os
try:
    import google.generativeai as genai
    api_key = os.environ.get("GOOGLE_AI_API_KEY")
    if api_key:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content("Hello from Gemini!")
        print("✅ Google AI API: WORKING")
        print(f"Response: {response.text[:100]}...")
    else:
        print("⚠️  GOOGLE_AI_API_KEY not set")
        print("Get key at: https://aistudio.google.com/apikey")
except ImportError:
    print("⚠️  Install: pip3 install google-generativeai")
except Exception as e:
    print(f"❌ Error: {e}")
EOF
    ;;
  10) az --version && echo "✅ Azure CLI: WORKING" || echo "❌ Azure CLI: NOT FOUND" ;;
  11) 
    open https://gemini.google.com
    sleep 1
    open https://notebooklm.google.com
    sleep 1
    open https://aistudio.google.com
    sleep 1
    open -a "Microsoft Edge" https://copilot.microsoft.com
    sleep 1
    open https://designer.microsoft.com
    echo "✅ All web tools opened!"
    ;;
  *) echo "Invalid option" ;;
esac

