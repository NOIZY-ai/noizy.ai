#!/usr/bin/env bash
# REST API server management

API_PID_FILE="${INSTALL_DIR}/data/api.pid"
API_PORT="${API_PORT:-8420}"
API_HOST="${API_HOST:-127.0.0.1}"

cmd_api_status() {
    echo "[*] API Server Status"
    
    if [[ -f "$API_PID_FILE" ]]; then
        local pid=$(cat "$API_PID_FILE")
        if kill -0 "$pid" 2>/dev/null; then
            echo "  ✓ Status: Running (PID: $pid)"
            echo "  📍 URL: http://${API_HOST}:${API_PORT}"
            echo "  📚 Docs: http://${API_HOST}:${API_PORT}/docs"
        else
            echo "  ○ Status: Stale PID"
            rm -f "$API_PID_FILE"
        fi
    else
        echo "  ✗ Status: Not running"
    fi
}

cmd_api_start() {
    echo "[*] Starting API server..."
    
    [[ -f "$API_PID_FILE" ]] && { local pid=$(cat "$API_PID_FILE"); kill -0 "$pid" 2>/dev/null && { warn "Already running"; return 0; }; rm -f "$API_PID_FILE"; }
    
    command -v python3 &>/dev/null || { err "Python 3 required"; return 1; }
    
    local api_script="${INSTALL_DIR}/api/server.py"
    [[ ! -f "$api_script" ]] && { err "API server not found"; return 1; }
    
    mkdir -p "${INSTALL_DIR}/logs"
    cd "${INSTALL_DIR}"
    nohup python3 "$api_script" --host "$API_HOST" --port "$API_PORT" > "${INSTALL_DIR}/logs/api.log" 2>&1 &
    echo $! > "$API_PID_FILE"
    
    sleep 2
    if kill -0 "$(cat "$API_PID_FILE")" 2>/dev/null; then
        success "API started on http://${API_HOST}:${API_PORT}"
    else
        err "API failed to start"
        return 1
    fi
}

cmd_api_stop() {
    echo "[*] Stopping API server..."
    
    [[ ! -f "$API_PID_FILE" ]] && { echo "Not running"; return 0; }
    
    local pid=$(cat "$API_PID_FILE")
    kill "$pid" 2>/dev/null || true
    sleep 1
    kill -9 "$pid" 2>/dev/null || true
    rm -f "$API_PID_FILE"
    
    success "API stopped"
}

