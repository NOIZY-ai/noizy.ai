#!/bin/bash

# GOD_MASTER_TUNNEL.sh
# MC96 Tunnel System v2.0 - Mac Studio Deployment
# Installs Cloudflared, sets up LaunchAgent, runs Health Monitor & Watchdog.

LOG_FILE="$HOME/.mc96/tunnel.log"
PLIST_PATH="$HOME/Library/LaunchAgents/com.mc96.tunnel.plist"
mkdir -p "$HOME/.mc96"

echo "=== MC96 TUNNEL SYSTEM v2.0 (GOD) ===" | tee -a "$LOG_FILE"
date | tee -a "$LOG_FILE"

# 1. Check Dependencies
if ! command -v cloudflared &> /dev/null; then
    echo "[INSTALL] Installing cloudflared via brew..." | tee -a "$LOG_FILE"
    brew install cloudflare/cloudflare/cloudflared
else
    echo "[OK] cloudflared found." | tee -a "$LOG_FILE"
fi

if ! command -v code &> /dev/null; then
    echo "[WARN] 'code' command not found. Ensure VS Code is installed and in PATH." | tee -a "$LOG_FILE"
fi

# 2. Health Monitor (Python Background Service)
cat <<EOF > "$HOME/.mc96/health_monitor.py"
import http.server
import json
import socketserver
import subprocess

PORT = 9999

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            # Check Tunnel Process
            tunnel_status = "down"
            try:
                subprocess.check_output(["pgrep", "-f", "cloudflared tunnel run"])
                tunnel_status = "up"
            except:
                pass
                
            response = {
                "system": "GOD",
                "status": "ok",
                "tunnel": tunnel_status,
                "version": "2.0"
            }
            self.wfile.write(json.dumps(response).encode())

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Health Monitor serving on {PORT}")
    httpd.serve_forever()
EOF

# 3. Create LaunchAgent for Auto-Start (The Watchdog)
cat <<EOF > "$PLIST_PATH"
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.mc96.tunnel</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>$HOME/.mc96/run_watchdog.sh</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>$LOG_FILE</string>
    <key>StandardErrorPath</key>
    <string>$LOG_FILE</string>
</dict>
</plist>
EOF

# 4. Create Watchdog Script
cat <<EOF > "$HOME/.mc96/run_watchdog.sh"
#!/bin/bash
# Checks if tunnel is running, if not starts it.
# Also starts health monitor.

# Start Health Monitor if not running
if ! pgrep -f "health_monitor.py" > /dev/null; then
    python3 "$HOME/.mc96/health_monitor.py" &
fi

# Start Tunnel (Assuming 'GOD' tunnel is configured in default config or arguments)
# Replace 'GOD' with actual tunnel name or ID if known, defaulting to 'run' command assuming config.yml exists
# User instruction: Ensure cloudflared tunnel is created and config.yml is in ~/.cloudflared/
if ! pgrep -f "cloudflared tunnel run" > /dev/null; then
    echo "[WATCHDOG] Starting Cloudflare Tunnel..."
    /opt/homebrew/bin/cloudflared tunnel run GOD
fi
EOF
chmod +x "$HOME/.mc96/run_watchdog.sh"

# 5. Load Service
echo "[DEPLOY] Reloading LaunchAgent..." | tee -a "$LOG_FILE"
launchctl unload "$PLIST_PATH" 2>/dev/null
launchctl load "$PLIST_PATH"

echo "[SUCCESS] MC96 Tunnel v2.0 Deployed on GOD." | tee -a "$LOG_FILE"
echo "Health Monitor: http://localhost:9999" | tee -a "$LOG_FILE"
echo "Use 'tail -f $LOG_FILE' to monitor."
