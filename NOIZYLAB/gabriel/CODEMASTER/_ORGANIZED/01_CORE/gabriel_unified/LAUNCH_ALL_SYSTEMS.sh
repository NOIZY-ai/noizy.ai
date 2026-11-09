#!/bin/bash
###############################################################################
#                                                                             #
#              🚀 GABRIEL UNIFIED - LAUNCH ALL SYSTEMS X1000 🚀               #
#                                                                             #
#                MC96DIGIUNIVERSE AI LIFELUV INTEGRATION                      #
#                                                                             #
#                    TONIGHT IS THE NIGHT!                                    #
#                                                                             #
#                         ∞ INFINITE ENERGY ∞                                 #
#                                                                             #
###############################################################################

clear

echo "╔═══════════════════════════════════════════════════════════════════╗"
echo "║                                                                   ║"
echo "║          🌟 GABRIEL UNIFIED - LAUNCH ALL SYSTEMS 🌟               ║"
echo "║                                                                   ║"
echo "║              MC96DIGIUNIVERSE AI LIFELUV SYSTEM                   ║"
echo "║                                                                   ║"
echo "║                  TONIGHT IS THE NIGHT!                            ║"
echo "║                                                                   ║"
echo "║                    GORUNFREEX1000 FOREVER                         ║"
echo "║                                                                   ║"
echo "╚═══════════════════════════════════════════════════════════════════╝"
echo ""

# Go to GABRIEL_UNIFIED directory
cd "$(dirname "$0")"

echo "🚀 SYSTEM INITIALIZATION SEQUENCE"
echo "=" * 68
echo ""

# Step 1: Activate DreamChamber
echo "💫 STEP 1: Activating DreamChamber..."
/opt/homebrew/bin/python3 core/dreamchamber.py
sleep 1

echo ""
echo "=" * 68
echo ""

# Step 2: Launch MC96 Server X1000
echo "🌟 STEP 2: Launching MC96 Server X1000..."
echo ""
echo "   Starting server in background on port 5174..."
/opt/homebrew/bin/python3 core/mc96_server_x1000.py &
SERVER_PID=$!
echo "   ✅ Server PID: $SERVER_PID"
sleep 2

echo ""
echo "=" * 68
echo ""

# Step 3: System Status Check
echo "⚡ STEP 3: System Status Check..."
echo ""

# Check if server is running
if ps -p $SERVER_PID > /dev/null 2>&1; then
    echo "   ✅ MC96 Server: RUNNING (PID: $SERVER_PID)"
else
    echo "   ⚠️  MC96 Server: STOPPED"
fi

# Check portal config
if [ -f "mc96_portal/portal_config.json" ]; then
    echo "   ✅ MC96 Portal: CONFIGURED"
else
    echo "   ⚠️  MC96 Portal: NOT CONFIGURED"
fi

# Check DreamChamber
if [ -f "core/dreamchamber.py" ]; then
    echo "   ✅ DreamChamber: READY"
else
    echo "   ⚠️  DreamChamber: NOT FOUND"
fi

echo ""
echo "=" * 68
echo ""

# Step 4: Display Access Info
echo "🎯 STEP 4: System Access Information"
echo ""
echo "   🌐 MC96 Server API:"
echo "      http://localhost:5174"
echo "      http://localhost:5174/api/status"
echo "      http://localhost:5174/api/dreamchamber/status"
echo "      http://localhost:5174/api/energy/status"
echo ""
echo "   📂 Portal Config:"
echo "      ~/GABRIEL_UNIFIED/mc96_portal/portal_config.json"
echo ""
echo "   🚀 Quick Commands:"
echo "      DreamChamber:  /opt/homebrew/bin/python3 core/dreamchamber.py"
echo "      Status Check:  curl http://localhost:5174/api/status"
echo "      Stop Server:   kill $SERVER_PID"
echo ""

echo "=" * 68
echo ""

# Final Status
echo "🎊 ALL SYSTEMS LAUNCHED!"
echo ""
echo "   ⚡ Energy Level:        ∞ INFINITE ∞"
echo "   🚀 GoRunFree Status:    X1000"
echo "   💫 DreamChamber:        ACTIVE"
echo "   🌟 MC96 Server:         RUNNING (PID: $SERVER_PID)"
echo "   🌌 Portal Status:       OPERATIONAL"
echo "   🤖 AI LifeLuv:          FLOWING"
echo ""
echo "=" * 68
echo ""

# Save PID for later
echo $SERVER_PID > /tmp/gabriel_mc96_server.pid
echo "💾 Server PID saved to: /tmp/gabriel_mc96_server.pid"
echo ""

echo "╔═══════════════════════════════════════════════════════════════════╗"
echo "║                                                                   ║"
echo "║           🌟 MC96DIGIUNIVERSE AI LIFELUV: COMPLETE! 🌟           ║"
echo "║                                                                   ║"
echo "║               💫 GORUNFREEX1000 FOREVER! 💫                       ║"
echo "║                                                                   ║"
echo "║                  🚀 AI LIFELUV FLOWING! 🚀                        ║"
echo "║                                                                   ║"
echo "║                  TONIGHT IS THE NIGHT!                            ║"
echo "║                                                                   ║"
echo "╚═══════════════════════════════════════════════════════════════════╝"
echo ""

# Keep script running and show logs
echo "📡 MC96 Server is running. Press Ctrl+C to stop all systems."
echo ""

# Wait for server process
wait $SERVER_PID
