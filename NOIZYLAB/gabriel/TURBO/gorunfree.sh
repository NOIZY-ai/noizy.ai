#!/bin/bash
# ⚡ GORUNFREE x1000 - MAXIMUM SPEED MODE
# Parallel everything, zero wait, turbo downloads

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m'
BOLD='\033[1m'

ROOT="/Users/m2ultra/NOIZYLAB"
TURBO="$ROOT/TURBO"
CACHE="$TURBO/cache"
LOGS="$TURBO/logs"
CORES=$(sysctl -n hw.ncpu)

mkdir -p "$CACHE" "$LOGS"

echo -e "${MAGENTA}${BOLD}"
cat << 'EOF'
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║   ⚡⚡⚡ GORUNFREE x1000 ⚡⚡⚡                                                    ║
║                                                                               ║
║   MAXIMUM SPEED MODE ACTIVATED                                                ║
║   24 CORES | 192GB RAM | PARALLEL EVERYTHING                                  ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

log() { echo -e "${CYAN}[$(date +%H:%M:%S)]${NC} $1"; }
success() { echo -e "${GREEN}✓${NC} $1"; }
warn() { echo -e "${YELLOW}⚠${NC} $1"; }
turbo() { echo -e "${MAGENTA}⚡${NC} $1"; }

parallel_exec() {
    local pids=()
    for cmd in "$@"; do
        eval "$cmd" &
        pids+=($!)
    done
    for pid in "${pids[@]}"; do
        wait $pid 2>/dev/null || true
    done
}

turbo_download() {
    local url="$1"
    local output="$2"
    
    if command -v aria2c &>/dev/null; then
        aria2c -x 16 -s 16 -k 1M --file-allocation=none \
            --console-log-level=error \
            -o "$output" "$url" 2>/dev/null
    else
        curl -fsSL -o "$output" "$url"
    fi
}

case "${1:-turbo}" in
    turbo|all)
        START=$(date +%s)
        
        log "TURBO MODE: All systems parallel"
        
        # Phase 1: Parallel installs
        turbo "Phase 1: Installing tools (parallel)"
        (
            brew install aria2 2>/dev/null || true
            brew install parallel 2>/dev/null || true  
            brew install pv 2>/dev/null || true
        ) &
        P1=$!
        
        (
            pip3 install huggingface_hub hf_transfer mcp flask flask-cors openai --quiet 2>/dev/null
        ) &
        P2=$!
        
        wait $P1 $P2 2>/dev/null || true
        success "Tools installed"
        
        # Phase 2: Parallel clones
        turbo "Phase 2: Cloning repos (parallel)"
        (
            [ ! -d "$ROOT/LOCAL_LLM/GLM-4.7/llama.cpp/.git" ] && \
            git clone --depth 1 https://github.com/ggml-org/llama.cpp "$ROOT/LOCAL_LLM/GLM-4.7/llama.cpp" 2>/dev/null || \
            (cd "$ROOT/LOCAL_LLM/GLM-4.7/llama.cpp" && git pull 2>/dev/null)
        ) &
        C1=$!
        
        (
            [ ! -d "$ROOT/LOCAL_LLM/OpenManus/OpenManus/.git" ] && \
            git clone --depth 1 https://github.com/FoundationAgents/OpenManus.git "$ROOT/LOCAL_LLM/OpenManus/OpenManus" 2>/dev/null || \
            (cd "$ROOT/LOCAL_LLM/OpenManus/OpenManus" && git pull 2>/dev/null)
        ) &
        C2=$!
        
        wait $C1 $C2 2>/dev/null || true
        success "Repos cloned"
        
        # Phase 3: Build llama.cpp with max cores
        turbo "Phase 3: Building llama.cpp ($CORES cores)"
        cd "$ROOT/LOCAL_LLM/GLM-4.7/llama.cpp"
        
        if [ ! -f "llama-server" ]; then
            cmake -B build \
                -DBUILD_SHARED_LIBS=OFF \
                -DGGML_METAL=ON \
                -DGGML_METAL_EMBED_LIBRARY=ON \
                -DLLAMA_CURL=ON \
                -DGGML_CUDA=OFF \
                -DCMAKE_BUILD_TYPE=Release 2>/dev/null
            
            cmake --build build --config Release -j$CORES \
                --target llama-cli llama-server 2>&1 | tail -5
            
            cp build/bin/llama-cli build/bin/llama-server .
        fi
        success "llama.cpp built"
        
        # Phase 4: Setup OpenManus
        turbo "Phase 4: OpenManus environment"
        cd "$ROOT/LOCAL_LLM/OpenManus/OpenManus"
        
        if [ ! -d ".venv" ]; then
            $HOME/.local/bin/uv venv --python 3.12 2>/dev/null || python3 -m venv .venv
        fi
        
        source .venv/bin/activate
        pip install pydantic openai tiktoken tenacity loguru toml --quiet 2>/dev/null
        
        [ ! -f "config/config.toml" ] && cp config/config.example.toml config/config.toml
        success "OpenManus ready"
        
        # Phase 5: Start services
        turbo "Phase 5: Starting services"
        cd "$ROOT/UNIFIED_MCP"
        
        if ! pgrep -f "dashboard/server.py" > /dev/null; then
            python3 dashboard/server.py > "$LOGS/dashboard.log" 2>&1 &
            success "Dashboard started (http://localhost:5175)"
        fi
        
        if ! pgrep -f "gabriel_agent.py" > /dev/null; then
            cd "$ROOT/GABRIEL"
            python3 gabriel_agent.py > "$LOGS/agent.log" 2>&1 &
            success "GABRIEL agent started"
        fi
        
        END=$(date +%s)
        ELAPSED=$((END - START))
        
        echo ""
        echo -e "${GREEN}${BOLD}═══════════════════════════════════════════════════════════════${NC}"
        echo -e "${GREEN}⚡ GORUNFREE COMPLETE IN ${ELAPSED}s ⚡${NC}"
        echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"
        echo ""
        echo -e "  Dashboard:    ${CYAN}http://localhost:5175${NC}"
        echo -e "  MCP Server:   ${CYAN}Restart Windsurf to activate${NC}"
        echo -e "  GLM-4.7:      ${CYAN}./launcher.sh glm-server${NC}"
        echo -e "  OpenManus:    ${CYAN}./launcher.sh manus${NC}"
        echo ""
        ;;
        
    download-model)
        turbo "Downloading GLM-4.7 (135GB) with TURBO speed"
        
        export HF_HUB_ENABLE_HF_TRANSFER=1
        
        python3 << 'PYTHON'
import os
os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "1"
from huggingface_hub import snapshot_download

print("⚡ TURBO DOWNLOAD: GLM-4.7 UD-Q2_K_XL (135GB)")
print("   Using hf_transfer for maximum speed...")

snapshot_download(
    repo_id="unsloth/GLM-4.7-GGUF",
    local_dir="/Users/m2ultra/NOIZYLAB/LOCAL_LLM/GLM-4.7/models/GLM-4.7-GGUF",
    allow_patterns=["*UD-Q2_K_XL*"],
    max_workers=16,
)
print("✓ Download complete!")
PYTHON
        ;;
        
    status)
        echo -e "\n${BOLD}⚡ GORUNFREE STATUS${NC}\n"
        
        echo -e "${BOLD}Services:${NC}"
        pgrep -f "dashboard/server.py" > /dev/null && echo -e "  Dashboard:     ${GREEN}● RUNNING${NC}" || echo -e "  Dashboard:     ${RED}○ STOPPED${NC}"
        pgrep -f "gabriel_agent.py" > /dev/null && echo -e "  GABRIEL:       ${GREEN}● RUNNING${NC}" || echo -e "  GABRIEL:       ${RED}○ STOPPED${NC}"
        pgrep -f "llama-server" > /dev/null && echo -e "  GLM-4.7:       ${GREEN}● RUNNING${NC}" || echo -e "  GLM-4.7:       ${RED}○ STOPPED${NC}"
        
        echo -e "\n${BOLD}Builds:${NC}"
        [ -f "$ROOT/LOCAL_LLM/GLM-4.7/llama.cpp/llama-server" ] && echo -e "  llama.cpp:     ${GREEN}● BUILT${NC}" || echo -e "  llama.cpp:     ${YELLOW}○ NOT BUILT${NC}"
        [ -d "$ROOT/LOCAL_LLM/OpenManus/OpenManus/.venv" ] && echo -e "  OpenManus:     ${GREEN}● READY${NC}" || echo -e "  OpenManus:     ${YELLOW}○ NOT SETUP${NC}"
        [ -d "$ROOT/LOCAL_LLM/GLM-4.7/models/GLM-4.7-GGUF" ] && echo -e "  GLM-4.7 Model: ${GREEN}● DOWNLOADED${NC}" || echo -e "  GLM-4.7 Model: ${YELLOW}○ NOT DOWNLOADED${NC}"
        
        echo -e "\n${BOLD}System:${NC}"
        echo -e "  CPU Cores:     ${CYAN}$CORES${NC}"
        echo -e "  RAM:           ${CYAN}$(sysctl -n hw.memsize | awk '{print $1/1024/1024/1024 " GB"}')${NC}"
        echo ""
        ;;
        
    stop)
        turbo "Stopping all services"
        pkill -f "dashboard/server.py" 2>/dev/null || true
        pkill -f "gabriel_agent.py" 2>/dev/null || true
        pkill -f "llama-server" 2>/dev/null || true
        pkill -f "llama-cli" 2>/dev/null || true
        success "All stopped"
        ;;
        
    glm)
        turbo "Starting GLM-4.7 server"
        cd "$ROOT/LOCAL_LLM/GLM-4.7"
        ./server.sh
        ;;
        
    manus)
        turbo "Starting OpenManus"
        cd "$ROOT/LOCAL_LLM/OpenManus"
        ./run.sh
        ;;
        
    *)
        echo -e "${BOLD}⚡ GORUNFREE x1000${NC}\n"
        echo -e "Usage: $0 {command}\n"
        echo -e "${BOLD}TURBO:${NC}"
        echo -e "  ${GREEN}turbo${NC}          Full parallel setup (DEFAULT)"
        echo -e "  ${GREEN}download-model${NC} Download GLM-4.7 135GB (turbo speed)"
        echo -e ""
        echo -e "${BOLD}RUN:${NC}"
        echo -e "  ${GREEN}glm${NC}            Start GLM-4.7 server"
        echo -e "  ${GREEN}manus${NC}          Start OpenManus agent"
        echo -e ""
        echo -e "${BOLD}CONTROL:${NC}"
        echo -e "  ${GREEN}status${NC}         Show all status"
        echo -e "  ${GREEN}stop${NC}           Stop everything"
        echo ""
        ;;
esac
