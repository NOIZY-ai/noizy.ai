#!/bin/bash
# GABRIEL REMOTE LINK
# Connects to HP-OMEN via Microsoft Remote Desktop (Windows App)
# Target: VPN IP (10.100.0.2) - Ensure VPN is active!

GABRIEL_IP="10.100.0.2"

echo "╔════════════════════════════════════════════╗"
echo "║      CONNECTING TO GABRIEL (HP-OMEN)     ║"
echo "╚════════════════════════════════════════════╝"
echo "📡 TARGET IP: $GABRIEL_IP"
echo "🚀 LAUNCHING RDP SESSION..."

# Check if port 3389 is reachable (timeout 1s)
nc -z -G 2 $GABRIEL_IP 3389 > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ PORT 3389 OPEN. ESTABLISHING LINK."
else
    echo "⚠️  WARNING: PORT 3389 UNREACHABLE."
    echo "   Ensure GABRIEL is connected to WireGuard."
    echo "   Ensure 'Enable Remote Desktop' is ON in Windows Settings."
fi

# Launch
open "rdp://$GABRIEL_IP"

