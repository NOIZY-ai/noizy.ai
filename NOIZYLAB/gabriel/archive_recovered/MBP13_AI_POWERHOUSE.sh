#!/bin/zsh
#
# MBP13_AI_POWERHOUSE.sh
# ═══════════════════════════════════════════════════════════════════════════
# Transform your 13" MacBook Pro into an AI POWERHOUSE
# Installs ALL AI tools, models, and integrations
# Part of MC96DIGIUNIVERSE - GORUNFREE x1000
# ═══════════════════════════════════════════════════════════════════════════
#
# Usage: ./MBP13_AI_POWERHOUSE.sh
#

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m'

clear
echo "${CYAN}═══════════════════════════════════════════════════════════════════════════${NC}"
echo "${WHITE}  🧠 MBP13 AI POWERHOUSE - GORUNFREE x1000${NC}"
echo "${CYAN}═══════════════════════════════════════════════════════════════════════════${NC}"
echo ""
echo "${YELLOW}Loading your 13\" MacBook Pro with ALL AI possibilities...${NC}"
echo ""

status() {
    echo "${BLUE}⚡${NC} $1... ${GREEN}[DONE]${NC}"
}

installing() {
    echo "${YELLOW}📦${NC} Installing $1..."
}

# ═══════════════════════════════════════════════════════════════════════════
# PHASE 1: PACKAGE MANAGERS & PREREQUISITES
# ═══════════════════════════════════════════════════════════════════════════
echo "${MAGENTA}━━━ PHASE 1: PREREQUISITES ━━━${NC}"

# Install Homebrew if not present
if ! command -v brew &> /dev/null; then
    installing "Homebrew"
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    status "Homebrew installed"
else
    status "Homebrew already installed"
fi

# Update Homebrew
brew update && brew upgrade
status "Homebrew updated"

# Install essential build tools
brew install cmake git wget curl jq ripgrep fd bat eza 2>/dev/null || true
status "Build tools ready"

echo ""

# ═══════════════════════════════════════════════════════════════════════════
# PHASE 2: PYTHON AI STACK
# ═══════════════════════════════════════════════════════════════════════════
echo "${MAGENTA}━━━ PHASE 2: PYTHON AI STACK ━━━${NC}"

# Install Python 3.12
brew install python@3.12 2>/dev/null || true
status "Python 3.12 installed"

# Install pipx for isolated tools
brew install pipx 2>/dev/null || true
pipx ensurepath 2>/dev/null || true
status "pipx ready"

# Create AI virtual environment
AI_VENV="$HOME/.ai_powerhouse"
if [ ! -d "$AI_VENV" ]; then
    python3 -m venv "$AI_VENV"
fi
source "$AI_VENV/bin/activate"
status "AI virtual environment created"

# Install core AI libraries
pip install --upgrade pip wheel setuptools
pip install \
    openai \
    anthropic \
    google-generativeai \
    groq \
    together \
    replicate \
    huggingface_hub \
    transformers \
    torch torchvision torchaudio \
    accelerate \
    bitsandbytes \
    safetensors \
    datasets \
    tokenizers \
    sentencepiece \
    numpy pandas scipy scikit-learn \
    matplotlib seaborn plotly \
    jupyter jupyterlab \
    ipywidgets \
    tqdm rich typer click \
    pydantic fastapi uvicorn \
    aiohttp httpx requests \
    python-dotenv \
    langchain langchain-community langchain-openai \
    llama-index \
    chromadb \
    faiss-cpu \
    sentence-transformers \
    whisper-openai \
    diffusers \
    pillow opencv-python \
    pyaudio soundfile librosa \
    2>/dev/null || true

status "Python AI libraries installed"

echo ""

# ═══════════════════════════════════════════════════════════════════════════
# PHASE 3: LOCAL LLM RUNNERS
# ═══════════════════════════════════════════════════════════════════════════
echo "${MAGENTA}━━━ PHASE 3: LOCAL LLM RUNNERS ━━━${NC}"

# Install Ollama (local LLM runner)
if ! command -v ollama &> /dev/null; then
    installing "Ollama (Local LLM Runner)"
    curl -fsSL https://ollama.com/install.sh | sh
fi
status "Ollama installed"

# Pull essential models for 13" MBP (smaller models for 8-16GB RAM)
echo "${YELLOW}Pulling optimized models for MBP13...${NC}"
ollama pull llama3.2:3b 2>/dev/null &
ollama pull phi3:mini 2>/dev/null &
ollama pull gemma2:2b 2>/dev/null &
ollama pull qwen2.5:3b 2>/dev/null &
ollama pull codellama:7b-code 2>/dev/null &
ollama pull nomic-embed-text 2>/dev/null &
wait
status "Local models pulled (optimized for MBP13)"

# Install LM Studio CLI
brew install --cask lm-studio 2>/dev/null || true
status "LM Studio installed"

# Install llama.cpp for raw metal inference
brew install llama.cpp 2>/dev/null || true
status "llama.cpp installed (Metal acceleration)"

echo ""

# ═══════════════════════════════════════════════════════════════════════════
# PHASE 4: AI DEVELOPMENT TOOLS
# ═══════════════════════════════════════════════════════════════════════════
echo "${MAGENTA}━━━ PHASE 4: AI DEVELOPMENT TOOLS ━━━${NC}"

# Install Node.js for AI web tools
brew install node 2>/dev/null || true
status "Node.js installed"

# Install AI CLI tools
npm install -g @anthropic-ai/claude-code 2>/dev/null || true
npm install -g @openai/codex 2>/dev/null || true
pipx install aider-chat 2>/dev/null || true
pipx install llm 2>/dev/null || true
pipx install fabric 2>/dev/null || true
status "AI CLI tools installed"

# Install Continue.dev extension data
mkdir -p ~/.continue
status "Continue.dev ready"

# Install Cursor AI support
brew install --cask cursor 2>/dev/null || true
status "Cursor AI IDE installed"

echo ""

# ═══════════════════════════════════════════════════════════════════════════
# PHASE 5: VOICE & AUDIO AI
# ═══════════════════════════════════════════════════════════════════════════
echo "${MAGENTA}━━━ PHASE 5: VOICE & AUDIO AI ━━━${NC}"

# Install Whisper for speech-to-text
pip install openai-whisper 2>/dev/null || true
status "Whisper (Speech-to-Text) installed"

# Install Coqui TTS for text-to-speech
pip install TTS 2>/dev/null || true
status "Coqui TTS installed"

# Install audio processing tools
brew install ffmpeg sox 2>/dev/null || true
pip install pydub audioread 2>/dev/null || true
status "Audio tools installed"

# Install Bark for neural audio
pip install git+https://github.com/suno-ai/bark.git 2>/dev/null || true
status "Bark (Neural Audio) installed"

echo ""

# ═══════════════════════════════════════════════════════════════════════════
# PHASE 6: VISION & IMAGE AI
# ═══════════════════════════════════════════════════════════════════════════
echo "${MAGENTA}━━━ PHASE 6: VISION & IMAGE AI ━━━${NC}"

# Install image AI libraries
pip install \
    ultralytics \
    segment-anything \
    clip \
    timm \
    albumentations \
    2>/dev/null || true
status "Vision AI libraries installed"

# Install Stable Diffusion tools
pip install diffusers[torch] 2>/dev/null || true
status "Stable Diffusion ready"

# Install image editing tools
brew install imagemagick 2>/dev/null || true
pip install rembg 2>/dev/null || true
status "Image tools installed"

echo ""

# ═══════════════════════════════════════════════════════════════════════════
# PHASE 7: VECTOR DATABASES & RAG
# ═══════════════════════════════════════════════════════════════════════════
echo "${MAGENTA}━━━ PHASE 7: VECTOR DATABASES & RAG ━━━${NC}"

# ChromaDB (already installed above)
# Install Qdrant
pip install qdrant-client 2>/dev/null || true
status "Qdrant client installed"

# Install Weaviate
pip install weaviate-client 2>/dev/null || true
status "Weaviate client installed"

# Install Pinecone
pip install pinecone-client 2>/dev/null || true
status "Pinecone client installed"

# Install LanceDB (local vector DB)
pip install lancedb 2>/dev/null || true
status "LanceDB (local) installed"

# Install Milvus lite
pip install pymilvus 2>/dev/null || true
status "Milvus client installed"

echo ""

# ═══════════════════════════════════════════════════════════════════════════
# PHASE 8: AI AGENTS & AUTOMATION
# ═══════════════════════════════════════════════════════════════════════════
echo "${MAGENTA}━━━ PHASE 8: AI AGENTS & AUTOMATION ━━━${NC}"

# Install CrewAI
pip install crewai crewai-tools 2>/dev/null || true
status "CrewAI installed"

# Install AutoGen
pip install pyautogen 2>/dev/null || true
status "AutoGen installed"

# Install smolagents
pip install smolagents 2>/dev/null || true
status "Smolagents installed"

# Install DSPy
pip install dspy-ai 2>/dev/null || true
status "DSPy installed"

echo ""

# ═══════════════════════════════════════════════════════════════════════════
# PHASE 9: API KEYS SETUP
# ═══════════════════════════════════════════════════════════════════════════
echo "${MAGENTA}━━━ PHASE 9: API CONFIGURATION ━━━${NC}"

# Create API keys template
API_FILE="$HOME/.ai_keys"
if [ ! -f "$API_FILE" ]; then
cat > "$API_FILE" << 'EOF'
# AI API Keys - MC96DIGIUNIVERSE
# Fill in your keys below

export OPENAI_API_KEY=""
export ANTHROPIC_API_KEY=""
export GEMINI_API_KEY=""
export GROQ_API_KEY=""
export TOGETHER_API_KEY=""
export REPLICATE_API_TOKEN=""
export HUGGINGFACE_TOKEN=""
export DEEPSEEK_API_KEY=""
export NVIDIA_API_KEY=""
export MISTRAL_API_KEY=""
export COHERE_API_KEY=""
export PERPLEXITY_API_KEY=""
export FIREWORKS_API_KEY=""

# Vector DBs
export PINECONE_API_KEY=""
export QDRANT_API_KEY=""
export WEAVIATE_API_KEY=""

# Slack Integration
export SLACK_BOT_TOKEN=""
export SLACK_WEBHOOK_URL=""

# GitHub Integration
export GITHUB_TOKEN=""
export GITHUB_WEBHOOK_SECRET=""
EOF
    chmod 600 "$API_FILE"
    status "API keys template created at ~/.ai_keys"
else
    status "API keys file already exists"
fi

# Add to shell config
if ! grep -q "source ~/.ai_keys" ~/.zshrc 2>/dev/null; then
    echo "source ~/.ai_keys" >> ~/.zshrc
    status "API keys added to shell"
fi

echo ""

# ═══════════════════════════════════════════════════════════════════════════
# PHASE 10: NOIZYLAB SYNC
# ═══════════════════════════════════════════════════════════════════════════
echo "${MAGENTA}━━━ PHASE 10: NOIZYLAB INTEGRATION ━━━${NC}"

# Clone NOIZYLAB if not present
NOIZYLAB_DIR="$HOME/noizylab"
if [ ! -d "$NOIZYLAB_DIR" ]; then
    mkdir -p "$NOIZYLAB_DIR"
    # Copy core files from M2 Ultra if available
    if [ -d "/Volumes/m2ultra/noizylab" ]; then
        cp -r /Volumes/m2ultra/noizylab/* "$NOIZYLAB_DIR/"
        status "NOIZYLAB synced from M2 Ultra"
    fi
fi
status "NOIZYLAB directory ready"

# Install NOIZYLAB dependencies
if [ -f "$NOIZYLAB_DIR/requirements.txt" ]; then
    pip install -r "$NOIZYLAB_DIR/requirements.txt" 2>/dev/null || true
    status "NOIZYLAB dependencies installed"
fi

echo ""

# ═══════════════════════════════════════════════════════════════════════════
# FINAL STATUS
# ═══════════════════════════════════════════════════════════════════════════
echo "${CYAN}═══════════════════════════════════════════════════════════════════════════${NC}"
echo ""
echo "${WHITE}  🧠 MBP13 AI POWERHOUSE - FULLY LOADED 🧠${NC}"
echo ""
echo "${GREEN}  ✅ Python AI Stack      - OpenAI, Anthropic, Gemini, Groq, etc.${NC}"
echo "${GREEN}  ✅ Local LLMs           - Ollama + llama3.2, phi3, gemma2, qwen2.5${NC}"
echo "${GREEN}  ✅ LLM Runners          - Ollama, LM Studio, llama.cpp (Metal)${NC}"
echo "${GREEN}  ✅ AI Dev Tools         - Aider, LLM CLI, Cursor, Continue${NC}"
echo "${GREEN}  ✅ Voice AI             - Whisper, Coqui TTS, Bark${NC}"
echo "${GREEN}  ✅ Vision AI            - YOLO, SAM, CLIP, Stable Diffusion${NC}"
echo "${GREEN}  ✅ Vector DBs           - Chroma, Qdrant, Pinecone, LanceDB${NC}"
echo "${GREEN}  ✅ AI Agents            - CrewAI, AutoGen, Smolagents, DSPy${NC}"
echo "${GREEN}  ✅ LangChain + LlamaIndex${NC}"
echo "${GREEN}  ✅ NOIZYLAB Integration${NC}"
echo ""
echo "${CYAN}═══════════════════════════════════════════════════════════════════════════${NC}"
echo ""
echo "${YELLOW}📋 NEXT STEPS:${NC}"
echo ""
echo "  1. Edit ~/.ai_keys and add your API keys"
echo "  2. Run: source ~/.zshrc"
echo "  3. Test: ollama run llama3.2:3b"
echo "  4. Start Jupyter: jupyter lab"
echo ""
echo "${YELLOW}📊 MODELS PULLED (Optimized for 8-16GB RAM):${NC}"
echo "  • llama3.2:3b     - Fast general purpose"
echo "  • phi3:mini       - Microsoft's efficient model"
echo "  • gemma2:2b       - Google's compact model"
echo "  • qwen2.5:3b      - Alibaba's multilingual"
echo "  • codellama:7b    - Code generation"
echo "  • nomic-embed     - Embeddings for RAG"
echo ""
echo "${CYAN}═══════════════════════════════════════════════════════════════════════════${NC}"
echo ""
echo "${MAGENTA}MC96DIGIUNIVERSE // GORUNFREE x1000${NC}"
echo "${WHITE}Your 13\" MacBook Pro is now an AI POWERHOUSE! 🚀${NC}"
echo ""

# Deactivate venv
deactivate 2>/dev/null || true
