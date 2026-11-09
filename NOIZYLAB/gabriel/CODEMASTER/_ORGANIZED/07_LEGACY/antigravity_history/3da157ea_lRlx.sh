#!/bin/bash
# Verify Jumbo Frames (MTU 9000)
# Pings the gateway with a massive 8184 byte payload (+8 byte header = 8192 bytes)
# If the switch isn't configured, this WILL fail.

GATEWAY="10.0.0.1"
PAYLOAD_SIZE=8184 

echo "🐘 Testing Jumbo Frames to Gateway ($GATEWAY)..."
echo "📦 Packet Size: $PAYLOAD_SIZE bytes (Total 8192)"

if ping -D -c 3 -s $PAYLOAD_SIZE $GATEWAY > /dev/null 2>&1; then
    echo "✅ SUCCESS: Jumbo Frames are flowing!"
    echo "🚀 Your network is ready for heavy hauling."
else
    echo "❌ FAILURE: Large packets are being dropped."
    echo "⚠️  ACTION REQUIRED: Check your D-Link DGS-1210-10 settings."
    echo "    1. Go to L2 Functions > Jumbo Frame"
    echo "    2. Enable it (Max 10000)"
    echo "    3. Save Configuration"
fi
