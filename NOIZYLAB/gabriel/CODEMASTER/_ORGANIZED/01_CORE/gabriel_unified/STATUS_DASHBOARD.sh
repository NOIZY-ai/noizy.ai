#!/bin/bash
###############################################################################
#                                                                             #
#              📊 GABRIEL UNIFIED - STATUS DASHBOARD X1000 📊                 #
#                                                                             #
###############################################################################

clear

echo "╔═══════════════════════════════════════════════════════════════════╗"
echo "║                                                                   ║"
echo "║          📊 GABRIEL UNIFIED STATUS DASHBOARD 📊                   ║"
echo "║                                                                   ║"
echo "║              MC96DIGIUNIVERSE AI LIFELUV SYSTEM                   ║"
echo "║                                                                   ║"
echo "╚═══════════════════════════════════════════════════════════════════╝"
echo ""

# System Info
echo "🖥️  SYSTEM INFORMATION"
echo "=" * 68
echo ""
echo "   Hostname:    $(hostname)"
echo "   OS:          $(uname -s) $(uname -r)"
echo "   Time:        $(date)"
echo ""

# GABRIEL UNIFIED Status
echo "=" * 68
echo ""
echo "🚀 GABRIEL UNIFIED CORE"
echo "=" * 68
echo ""

# Check if directory exists
if [ -d "$HOME/GABRIEL_UNIFIED" ]; then
    echo "   ✅ GABRIEL_UNIFIED Directory: PRESENT"

    # Check components
    if [ -f "$HOME/GABRIEL_UNIFIED/core/dreamchamber.py" ]; then
        echo "   ✅ DreamChamber: READY"
    else
        echo "   ⚠️  DreamChamber: NOT FOUND"
    fi

    if [ -f "$HOME/GABRIEL_UNIFIED/core/mc96_server_x1000.py" ]; then
        echo "   ✅ MC96 Server X1000: READY"
    else
        echo "   ⚠️  MC96 Server X1000: NOT FOUND"
    fi

    if [ -f "$HOME/GABRIEL_UNIFIED/core/visual_scanner.py" ]; then
        echo "   ✅ Visual Scanner: READY"
    else
        echo "   ⚠️  Visual Scanner: NOT FOUND"
    fi
else
    echo "   ❌ GABRIEL_UNIFIED: NOT FOUND"
fi

echo ""

# MC96 Portal Status
echo "=" * 68
echo ""
echo "🌌 MC96DIGIUNIVERSE PORTAL"
echo "=" * 68
echo ""

if [ -f "$HOME/GABRIEL_UNIFIED/mc96_portal/portal_config.json" ]; then
    echo "   ✅ Portal Config: PRESENT"
    echo ""
    echo "   Portal Configuration:"
    cat "$HOME/GABRIEL_UNIFIED/mc96_portal/portal_config.json" | python3 -m json.tool 2>/dev/null | sed 's/^/      /'
else
    echo "   ⚠️  Portal Config: NOT CONFIGURED"
    echo "      Run: /opt/homebrew/bin/python3 core/dreamchamber.py"
fi

echo ""

# MC96 Server Status
echo "=" * 68
echo ""
echo "🌐 MC96 SERVER X1000"
echo "=" * 68
echo ""

# Check if server is running
if [ -f /tmp/gabriel_mc96_server.pid ]; then
    PID=$(cat /tmp/gabriel_mc96_server.pid)
    if ps -p $PID > /dev/null 2>&1; then
        echo "   ✅ Server Status: RUNNING (PID: $PID)"

        # Try to query API
        if command -v curl &> /dev/null; then
            echo ""
            echo "   API Response:"
            curl -s http://localhost:5174/api/status 2>/dev/null | python3 -m json.tool 2>/dev/null | sed 's/^/      /' || echo "      ⚠️  API not responding"
        fi
    else
        echo "   ⚠️  Server Status: STOPPED (PID file exists but process not running)"
    fi
else
    echo "   ⚠️  Server Status: STOPPED"
fi

# Check port
PROC=$(lsof -ti:5174 2>/dev/null)
if [ ! -z "$PROC" ]; then
    echo "   ✅ Port 5174: IN USE by PID $PROC"
else
    echo "   ⚠️  Port 5174: FREE"
fi

echo ""

# Integrated Systems
echo "=" * 68
echo ""
echo "👥 INTEGRATED FAMILY SYSTEMS"
echo "=" * 68
echo ""

SYSTEMS=(
    "GABRIEL_UNIFIED"
    "Documents/GABRIEL"
    "CODE_MASTER"
    "CODEBEAST"
    ".config"
)

for system in "${SYSTEMS[@]}"; do
    if [ -e "$HOME/$system" ]; then
        echo "   ✅ $system"
    else
        echo "   ⚠️  $system (Not Found)"
    fi
done

echo ""

# Python Environment
echo "=" * 68
echo ""
echo "🐍 PYTHON ENVIRONMENT"
echo "=" * 68
echo ""

if command -v /opt/homebrew/bin/python3 &> /dev/null; then
    echo "   ✅ Python: $(/opt/homebrew/bin/python3 --version)"
    echo "   📍 Location: /opt/homebrew/bin/python3"
else
    echo "   ⚠️  Homebrew Python not found"
fi

# Check Flask
if /opt/homebrew/bin/python3 -c "import flask" 2>/dev/null; then
    FLASK_VER=$(/opt/homebrew/bin/python3 -c "import flask; print(flask.__version__)" 2>/dev/null)
    echo "   ✅ Flask: $FLASK_VER"
else
    echo "   ⚠️  Flask: NOT INSTALLED"
    echo "      Install: /opt/homebrew/bin/python3 -m pip install flask flask-cors"
fi

echo ""

# Quick Commands
echo "=" * 68
echo ""
echo "⚡ QUICK COMMANDS"
echo "=" * 68
echo ""
echo "   Launch All:      ./GABRIEL_UNIFIED/LAUNCH_ALL_SYSTEMS.sh"
echo "   Stop All:        ./GABRIEL_UNIFIED/STOP_ALL_SYSTEMS.sh"
echo "   DreamChamber:    /opt/homebrew/bin/python3 GABRIEL_UNIFIED/core/dreamchamber.py"
echo "   Status:          ./GABRIEL_UNIFIED/STATUS_DASHBOARD.sh"
echo "   API Status:      curl http://localhost:5174/api/status"
echo ""

# Energy Status
echo "=" * 68
echo ""
echo "⚡ ENERGY STATUS"
echo "=" * 68
echo ""

if [ -f "$HOME/GABRIEL_UNIFIED/mc96_portal/portal_config.json" ]; then
    ENERGY=$(cat "$HOME/GABRIEL_UNIFIED/mc96_portal/portal_config.json" | python3 -c "import sys, json; print(json.load(sys.stdin)['energy_level'])" 2>/dev/null)
    STATUS=$(cat "$HOME/GABRIEL_UNIFIED/mc96_portal/portal_config.json" | python3 -c "import sys, json; print(json.load(sys.stdin)['gorunfree_status'])" 2>/dev/null)

    echo "   Energy Level:       $ENERGY"
    echo "   GoRunFree Status:   $STATUS"
    echo "   AI LifeLuv:         FLOWING"
else
    echo "   Energy Level:       Unknown (Portal not configured)"
fi

echo ""
echo "=" * 68
echo ""
echo "🌟 GORUNFREEX1000 FOREVER! 💫"
echo ""
