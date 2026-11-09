#!/bin/bash
# NOIZYLAB_COMPLETE_INSTALLER.sh
# ONE FILE - EVERYTHING EMBEDDED
# Install NOIZYLAB + Move Downloads + Delete Empty Folders + 4 Full Agents
# GORUNFREEX10000

set -e
clear

echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║        ⚡⚡⚡ NOIZYLAB COMPLETE INSTALLER ⚡⚡⚡                        ║"
echo "║        ONE FILE = EVERYTHING                                         ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo ""

NOIZYLAB="$HOME/NOIZYLAB"
DOWNLOADS="$HOME/Downloads"
CODE_DIR="$NOIZYLAB/Code"
AGENT_DIR="$NOIZYLAB/Agents"
LOG_DIR="$NOIZYLAB/Logs"
NOIZYMEMORIES="$NOIZYLAB/NOIZYMEMORIES"
SCRIPTS_DIR="$NOIZYLAB/Scripts"
LAUNCH_AGENTS="$HOME/Library/LaunchAgents"

# ═══════════════════════════════════════════════════════════════════════
# PART 1: CREATE STRUCTURE
# ═══════════════════════════════════════════════════════════════════════

echo "⚡ [1/6] Creating NOIZYLAB structure..."
mkdir -p "$AGENT_DIR" "$LOG_DIR" "$NOIZYMEMORIES" "$SCRIPTS_DIR" "$CODE_DIR" "$LAUNCH_AGENTS"
echo "✓ Created $NOIZYLAB"
echo ""

# ═══════════════════════════════════════════════════════════════════════
# PART 2: INSTALL AGENT_LUCY (COMPLETE)
# ═══════════════════════════════════════════════════════════════════════

echo "⚡ [2/6] Installing AGENT_LUCY (Creative Monitoring)..."

cat > "$AGENT_DIR/AGENT_LUCY.sh" << 'LUCY_COMPLETE'
#!/bin/bash
# AGENT_LUCY - Creative Music & Sound Design Agent
LOG_DIR="$HOME/NOIZYLAB/Logs"
LOG_FILE="$LOG_DIR/LUCY_$(date +%Y%m%d).log"
mkdir -p "$LOG_DIR"

log() {
    echo "[$(date '+%H:%M:%S')] [LUCY] $1" | tee -a "$LOG_FILE"
}

log "💜 LUCY starting - Creative/Music monitoring"

CREATIVE_DIRS=(
    "$HOME/Music"
    "$HOME/NOIZYLAB"
    "$HOME/Documents/Music"
    "$HOME/Documents/Audio"
)

while true; do
    log "Checking creative directories..."
    
    for DIR in "${CREATIVE_DIRS[@]}"; do
        if [ -d "$DIR" ]; then
            FILE_COUNT=$(find "$DIR" -type f \( -name "*.mp3" -o -name "*.wav" -o -name "*.aiff" -o -name "*.m4a" \) 2>/dev/null | wc -l | tr -d ' ')
            log "  $DIR: $FILE_COUNT audio files"
        fi
    done
    
    DISK_USAGE=$(df -h "$HOME" | tail -1 | awk '{print $5}')
    log "Disk usage: $DISK_USAGE"
    
    log "💜 Next check in 5 min"
    sleep 300
done
LUCY_COMPLETE

chmod +x "$AGENT_DIR/AGENT_LUCY.sh"
echo "✓ AGENT_LUCY installed"

# ═══════════════════════════════════════════════════════════════════════
# PART 3: INSTALL AGENT_POPS (COMPLETE)
# ═══════════════════════════════════════════════════════════════════════

echo "⚡ [3/6] Installing AGENT_POPS (System Health)..."

cat > "$AGENT_DIR/AGENT_POPS.sh" << 'POPS_COMPLETE'
#!/bin/bash
# AGENT_POPS - System Health & Network Agent
LOG_DIR="$HOME/NOIZYLAB/Logs"
LOG_FILE="$LOG_DIR/POPS_$(date +%Y%m%d).log"
mkdir -p "$LOG_DIR"

log() {
    echo "[$(date '+%H:%M:%S')] [POPS] $1" | tee -a "$LOG_FILE"
}

log "🔧 POPS starting - System Health monitoring"

DEVICES=("10.90.90.90" "10.90.90.10" "10.90.90.20" "10.90.90.30" "10.90.90.15")
DEVICE_NAMES=("MC96 Switch" "GOD" "GABRIEL" "MIKE" "DaFixer")

while true; do
    log "🔧 MC96ECOUNIVERSE network check..."
    
    ONLINE=0
    for i in "${!DEVICES[@]}"; do
        IP="${DEVICES[$i]}"
        NAME="${DEVICE_NAMES[$i]}"
        
        if ping -c 1 -W 1 "$IP" >/dev/null 2>&1; then
            log "  ✓ $NAME ($IP) online"
            ((ONLINE++))
        else
            log "  ✗ $NAME ($IP) OFFLINE!"
        fi
    done
    
    log "Network status: $ONLINE/5 devices online"
    
    CPU=$(top -l 1 | grep "CPU usage" | awk '{print $3}' | sed 's/%//')
    MEMORY=$(vm_stat | perl -ne '/page size of (\d+)/ and $size=$1; /Pages active:\s+(\d+)/ and printf("%.1f", $1 * $size / 1073741824);')
    log "System: CPU ${CPU}% | RAM ${MEMORY}GB active"
    
    DISK_FREE=$(df -h / | tail -1 | awk '{print $4}')
    log "Disk free: $DISK_FREE"
    
    log "🔧 Next check in 3 min"
    sleep 180
done
POPS_COMPLETE

chmod +x "$AGENT_DIR/AGENT_POPS.sh"
echo "✓ AGENT_POPS installed"

# ═══════════════════════════════════════════════════════════════════════
# PART 4: INSTALL AGENT_ENGR_KEITH (COMPLETE)
# ═══════════════════════════════════════════════════════════════════════

echo "⚡ [4/6] Installing AGENT_ENGR_KEITH (Engineering)..."

cat > "$AGENT_DIR/AGENT_ENGR_KEITH.sh" << 'KEITH_COMPLETE'
#!/bin/bash
# AGENT_ENGR_KEITH - Engineering & Performance
LOG_DIR="$HOME/NOIZYLAB/Logs"
LOG_FILE="$LOG_DIR/ENGR_KEITH_$(date +%Y%m%d).log"
mkdir -p "$LOG_DIR"

log() {
    echo "[$(date '+%H:%M:%S')] [KEITH] $1" | tee -a "$LOG_FILE"
}

log "⚙️ ENGR_KEITH starting - Engineering & Performance"

while true; do
    log "⚙️ Performance analysis..."
    
    CPU_USER=$(top -l 1 | grep "CPU usage" | awk '{print $3}' | sed 's/%//')
    CPU_SYS=$(top -l 1 | grep "CPU usage" | awk '{print $5}' | sed 's/%//')
    CPU_IDLE=$(top -l 1 | grep "CPU usage" | awk '{print $7}' | sed 's/%//')
    
    log "CPU: ${CPU_USER}% user | ${CPU_SYS}% sys | ${CPU_IDLE}% idle"
    
    MEMORY_USED=$(vm_stat | perl -ne '/page size of (\d+)/ and $size=$1; /Pages active:\s+(\d+)/ and printf("%.1f", $1 * $size / 1073741824);')
    MEMORY_FREE=$(vm_stat | perl -ne '/page size of (\d+)/ and $size=$1; /Pages free:\s+(\d+)/ and printf("%.1f", $1 * $size / 1073741824);')
    
    log "Memory: ${MEMORY_USED}GB used | ${MEMORY_FREE}GB free"
    
    PROCESSOR=$(sysctl -n machdep.cpu.brand_string 2>/dev/null | grep -o "M[0-9]" || echo "M2")
    log "Processor: Apple ${PROCESSOR} Ultra optimized"
    
    log "⚙️ Next analysis in 4 min"
    sleep 240
done
KEITH_COMPLETE

chmod +x "$AGENT_DIR/AGENT_ENGR_KEITH.sh"
echo "✓ AGENT_ENGR_KEITH installed"

# ═══════════════════════════════════════════════════════════════════════
# PART 5: INSTALL AGENT_DREAM (COMPLETE)
# ═══════════════════════════════════════════════════════════════════════

echo "⚡ [5/6] Installing AGENT_DREAM (Vision & Goals)..."

cat > "$AGENT_DIR/AGENT_DREAM.sh" << 'DREAM_COMPLETE'
#!/bin/bash
# AGENT_DREAM - Vision & Goals
LOG_DIR="$HOME/NOIZYLAB/Logs"
LOG_FILE="$LOG_DIR/DREAM_$(date +%Y%m%d).log"
mkdir -p "$LOG_DIR"

log() {
    echo "[$(date '+%H:%M:%S')] [DREAM] $1" | tee -a "$LOG_FILE"
}

log "💭 DREAM starting - Vision & Aspirational Planning"

CYCLE=0

while true; do
    ((CYCLE++))
    log "💭 Vision cycle #$CYCLE"
    
    log "Mission: NOIZYLAB - 12 repairs/day, \$256K+ revenue"
    log "Philosophy: GORUNFREE - One command = everything"
    log "Voice-first: Independence through accessibility"
    
    if [ $((CYCLE % 10)) -eq 0 ]; then
        log "💭 Milestone: $CYCLE vision cycles completed"
    fi
    
    log "💭 Next cycle in 6 min"
    sleep 360
done
DREAM_COMPLETE

chmod +x "$AGENT_DIR/AGENT_DREAM.sh"
echo "✓ AGENT_DREAM installed"

# ═══════════════════════════════════════════════════════════════════════
# PART 6: CREATE STARTUP LOADER & CONTROL SCRIPTS
# ═══════════════════════════════════════════════════════════════════════

echo "⚡ [6/6] Creating control system..."

cat > "$AGENT_DIR/LOAD_ALL_AGENTS.sh" << 'LOADER'
#!/bin/bash
AGENT_DIR="$HOME/NOIZYLAB/Agents"
LOG_DIR="$HOME/NOIZYLAB/Logs"
mkdir -p "$LOG_DIR"

STARTUP_LOG="$LOG_DIR/STARTUP_$(date +%Y%m%d).log"
log() { echo "[$(date '+%H:%M:%S')] $1" | tee -a "$STARTUP_LOG"; }

log "🚀 Starting all agents..."

for AGENT in LUCY POPS ENGR_KEITH DREAM; do
    SCRIPT="$AGENT_DIR/AGENT_${AGENT}.sh"
    if [ -f "$SCRIPT" ]; then
        nohup "$SCRIPT" > /dev/null 2>&1 &
        log "✓ Started AGENT_${AGENT} (PID: $!)"
        sleep 1
    fi
done

log "🚀 All agents running"
osascript -e 'display notification "All 4 agents running" with title "NOIZYLAB" subtitle "GORUNFREEX10000"' 2>/dev/null
LOADER
chmod +x "$AGENT_DIR/LOAD_ALL_AGENTS.sh"

# Control scripts
cat > "$SCRIPTS_DIR/start.sh" << EOF
#!/bin/bash
"$AGENT_DIR/LOAD_ALL_AGENTS.sh"
EOF
chmod +x "$SCRIPTS_DIR/start.sh"

cat > "$SCRIPTS_DIR/stop.sh" << 'EOF'
#!/bin/bash
pkill -f "AGENT_"
echo "All agents stopped"
EOF
chmod +x "$SCRIPTS_DIR/stop.sh"

cat > "$SCRIPTS_DIR/status.sh" << 'EOF'
#!/bin/bash
ps aux | grep "AGENT_" | grep -v grep
EOF
chmod +x "$SCRIPTS_DIR/status.sh"

cat > "$SCRIPTS_DIR/logs.sh" << EOF
#!/bin/bash
open "$LOG_DIR"
EOF
chmod +x "$SCRIPTS_DIR/logs.sh"

cat > "$SCRIPTS_DIR/code.sh" << EOF
#!/bin/bash
open "$CODE_DIR"
EOF
chmod +x "$SCRIPTS_DIR/code.sh"

echo "✓ Control scripts created"
echo ""

# ═══════════════════════════════════════════════════════════════════════
# MOVE CODE FROM DOWNLOADS
# ═══════════════════════════════════════════════════════════════════════

echo "⚡ Moving code from Downloads..."
if [ -d "$DOWNLOADS" ]; then
    MOVED=0
    for EXT in sh js py jsx html css json md txt xml yml yaml toml cfg conf; do
        for FILE in "$DOWNLOADS"/*.$EXT; do
            if [ -f "$FILE" ]; then
                mv "$FILE" "$CODE_DIR/" 2>/dev/null
                ((MOVED++))
            fi
        done
    done
    echo "✓ Moved $MOVED files to Code/"
fi
echo ""

# ═══════════════════════════════════════════════════════════════════════
# DELETE EMPTY FOLDERS
# ═══════════════════════════════════════════════════════════════════════

echo "⚡ Deleting empty folders from Downloads..."
if [ -d "$DOWNLOADS" ]; then
    DELETED=0
    while IFS= read -r -d '' DIR; do
        if [ -d "$DIR" ] && [ -z "$(ls -A "$DIR")" ]; then
            rmdir "$DIR" 2>/dev/null && ((DELETED++))
        fi
    done < <(find "$DOWNLOADS" -type d -depth -print0)
    echo "✓ Deleted $DELETED empty folders"
fi
echo ""

# ═══════════════════════════════════════════════════════════════════════
# CONFIGURE AUTO-START
# ═══════════════════════════════════════════════════════════════════════

cat > "$LAUNCH_AGENTS/com.noizylab.agents.plist" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.noizylab.agents</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>$AGENT_DIR/LOAD_ALL_AGENTS.sh</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>
EOF

launchctl unload "$LAUNCH_AGENTS/com.noizylab.agents.plist" 2>/dev/null || true
launchctl load "$LAUNCH_AGENTS/com.noizylab.agents.plist" 2>/dev/null
echo "✓ Auto-start configured"
echo ""

# ═══════════════════════════════════════════════════════════════════════
# START AGENTS NOW
# ═══════════════════════════════════════════════════════════════════════

echo "⚡ Starting agents NOW..."
"$AGENT_DIR/LOAD_ALL_AGENTS.sh" &
sleep 2
RUNNING=$(ps aux | grep "AGENT_" | grep -v grep | wc -l | tr -d ' ')
echo "✓ $RUNNING agents running"
echo ""

# ═══════════════════════════════════════════════════════════════════════
# SAVE MEMORY
# ═══════════════════════════════════════════════════════════════════════

cat > "$NOIZYMEMORIES/INSTALL_$(date +%Y%m%d_%H%M%S).md" << 'MEMORY'
# NOIZYLAB Installation Complete

All agents installed to NOIZYLAB
Auto-start configured
Code moved from Downloads
Empty folders deleted

GORUNFREEX10000 - Complete
MEMORY
echo "✓ NOIZYMEMORIES saved"
echo ""

# ═══════════════════════════════════════════════════════════════════════
# COMPLETE
# ═══════════════════════════════════════════════════════════════════════

afplay /System/Library/Sounds/Glass.aiff 2>/dev/null

echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║                  ✅✅✅ COMPLETE ✅✅✅                                 ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo ""
echo "📁 $NOIZYLAB/"
echo "   ├── Agents/   (4 full agents)"
echo "   ├── Code/     (Downloads code)"
echo "   ├── Logs/     (agent logs)"
echo "   ├── Scripts/  (start/stop/status/logs/code)"
echo "   └── NOIZYMEMORIES/"
echo ""
echo "🚀 $RUNNING agents running NOW"
echo "✅ Auto-start at boot configured"
echo "✅ Code consolidated"
echo "✅ Empty folders deleted"
echo ""
echo "⚡ COMMANDS:"
echo "   bash $SCRIPTS_DIR/start.sh"
echo "   bash $SCRIPTS_DIR/stop.sh"
echo "   bash $SCRIPTS_DIR/status.sh"
echo "   bash $SCRIPTS_DIR/logs.sh"
echo "   bash $SCRIPTS_DIR/code.sh"
echo ""
echo "⚡⚡⚡ GORUNFREEX10000 ⚡⚡⚡"
echo ""
