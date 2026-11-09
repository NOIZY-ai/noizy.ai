#!/bin/bash
# ============================================================
# GABRIEL OMEN CONNECTOR
# Connect to GABRIEL on HP-OMEN via WireGuard VPN
# ============================================================

echo "⚡ GABRIEL OMEN CONNECTOR"
echo "========================="

# Check if WireGuard tunnel is active
VPN_STATUS=$(wg show 2>/dev/null | head -1)

if [ -z "$VPN_STATUS" ]; then
    echo "🔒 VPN Status: DISCONNECTED"
    echo ""
    echo "Starting WireGuard VPN tunnel..."
    sudo wg-quick up /Users/m2ultra/NOIZYLAB/GABRIEL/VPN/wg0.conf
    sleep 3
else
    echo "🟢 VPN Status: CONNECTED"
    wg show | head -10
fi

# Test connection to HP-OMEN
echo ""
echo "Testing connection to HP-OMEN (10.100.0.2)..."
if ping -c 1 -t 2 10.100.0.2 &>/dev/null; then
    echo "✅ HP-OMEN is REACHABLE!"
    
    # Test GABRIEL service
    echo ""
    echo "Testing GABRIEL API on HP-OMEN..."
    RESPONSE=$(curl -s --connect-timeout 3 "http://10.100.0.2:5174/api/status" 2>/dev/null)
    
    if [ -n "$RESPONSE" ]; then
        echo "✅ GABRIEL is ONLINE on HP-OMEN!"
        echo "Response: $RESPONSE"
        echo ""
        echo "🌐 Access Dreamchamber: http://10.100.0.2:5174/dreamchamber"
        echo "🔌 API Endpoint: http://10.100.0.2:5174/api/"
    else
        echo "⚠️  HP-OMEN is up but GABRIEL not running on port 5174"
        echo "Start GABRIEL on HP-OMEN with:"
        echo "  cd NOIZYLAB/GABRIEL && python mc96_server.py"
    fi
else
    echo "❌ HP-OMEN is NOT REACHABLE"
    echo ""
    echo "Possible issues:"
    echo "1. HP-OMEN is offline"
    echo "2. WireGuard not running on HP-OMEN"
    echo "3. Firewall blocking connections"
    echo ""
    echo "Try these IPs on local network:"
    echo "  10.0.0.46 (SSH available)"
    echo "  10.0.0.91, 10.0.0.111, 10.0.0.130, 10.0.0.132"
fi

echo ""
echo "========================="
echo "VPN Network Topology:"
echo "  M2Ultra:     10.100.0.1 (This machine)"
echo "  HP-OMEN:     10.100.0.2"
echo "  PORTAL_PAD:  10.100.0.3"
echo "  MOBILE:      10.100.0.4"
