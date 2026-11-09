#!/bin/bash
###############################################################################
#                                                                             #
#                 🛑 GABRIEL UNIFIED - STOP ALL SYSTEMS 🛑                    #
#                                                                             #
###############################################################################

echo ""
echo "🛑 Stopping GABRIEL UNIFIED Systems..."
echo ""

# Stop MC96 Server if PID file exists
if [ -f /tmp/gabriel_mc96_server.pid ]; then
    PID=$(cat /tmp/gabriel_mc96_server.pid)
    if ps -p $PID > /dev/null 2>&1; then
        echo "   🛑 Stopping MC96 Server (PID: $PID)..."
        kill $PID
        sleep 1
        if ps -p $PID > /dev/null 2>&1; then
            echo "      Force killing..."
            kill -9 $PID
        fi
        echo "   ✅ MC96 Server stopped"
    else
        echo "   ℹ️  MC96 Server not running"
    fi
    rm /tmp/gabriel_mc96_server.pid
else
    echo "   ℹ️  No PID file found"
fi

# Kill any remaining Python processes on port 5174
echo ""
echo "   🔍 Checking for processes on port 5174..."
PROC=$(lsof -ti:5174)
if [ ! -z "$PROC" ]; then
    echo "   🛑 Killing process on port 5174..."
    kill $PROC 2>/dev/null || kill -9 $PROC 2>/dev/null
    echo "   ✅ Port 5174 cleared"
else
    echo "   ✅ Port 5174 is free"
fi

echo ""
echo "🎯 All systems stopped."
echo ""
echo "   To restart: ./GABRIEL_UNIFIED/LAUNCH_ALL_SYSTEMS.sh"
echo ""
