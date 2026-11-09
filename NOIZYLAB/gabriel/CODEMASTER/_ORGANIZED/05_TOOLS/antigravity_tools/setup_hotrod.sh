#!/bin/bash
# HOT ROD - AI-Powered VSCode Insiders Setup Script
# Run: chmod +x setup_hotrod.sh && ./setup_hotrod.sh

echo "🔥 HOT ROD VSCode Insiders Setup"
echo "================================"

# Check for VSCode Insiders
if ! command -v code-insiders &> /dev/null; then
    echo "❌ VSCode Insiders not found. Please install it first."
    exit 1
fi

echo "📦 Installing AI Assistants..."
code-insiders --install-extension anthropic.claude-code
code-insiders --install-extension google.geminicodeassist
code-insiders --install-extension google.gemini-cli-vscode-ide-companion
code-insiders --install-extension openai.chatgpt

echo "📦 Installing Development Tools..."
code-insiders --install-extension ms-python.python
code-insiders --install-extension ms-python.debugpy
code-insiders --install-extension redhat.java
code-insiders --install-extension vscjava.vscode-java-pack
code-insiders --install-extension golang.go
code-insiders --install-extension ms-vscode.powershell

echo "📦 Installing Git Tools..."
code-insiders --install-extension eamodio.gitlens
code-insiders --install-extension donjayamanne.githistory
code-insiders --install-extension solomonkinard.git-blame
code-insiders --install-extension github.vscode-pull-request-github
code-insiders --install-extension vivaxy.vscode-conventional-commits

echo "📦 Installing Container Tools..."
code-insiders --install-extension ms-azuretools.vscode-docker
code-insiders --install-extension ms-azuretools.vscode-containers

echo "📦 Installing Debuggers..."
code-insiders --install-extension vadimcn.vscode-lldb
code-insiders --install-extension firefox-devtools.vscode-firefox-debug
code-insiders --install-extension ms-edgedevtools.vscode-edge-devtools

echo "📦 Installing Code Quality..."
code-insiders --install-extension dbaeumer.vscode-eslint
code-insiders --install-extension davidanson.vscode-markdownlint

echo "📦 Installing Productivity..."
code-insiders --install-extension vscodevim.vim

echo ""
echo "✅ HOT ROD setup complete!"
echo "🚀 Launch with: code-insiders"
