#!/bin/bash
#╔══════════════════════════════════════════════════════════════════════╗
#║                    GORUNFREE - MASTER LAUNCHER                        ║
#║              One Command to Rule Them All                             ║
#╚══════════════════════════════════════════════════════════════════════╝

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║                    GORUNFREE - ACTIVATED                             ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo ""

case "$1" in
    heal)
        echo "🌍 Running World Healer..."
        python3 "$SCRIPT_DIR/world_healer.py"
        ;;
    turbo)
        echo "⚡ Running TURBO Healer (Zero Latency)..."
        python3 "$SCRIPT_DIR/world_healer_turbo.py"
        ;;
    monitor)
        echo "💾 Running Volume Monitor..."
        python3 "$SCRIPT_DIR/volume_monitor.py"
        ;;
    all)
        echo "🚀 RUNNING ALL SYSTEMS..."
        python3 "$SCRIPT_DIR/world_healer_turbo.py"
        echo ""
        python3 "$SCRIPT_DIR/volume_monitor.py"
        ;;
    *)
        echo "Usage: GORUNFREE.sh [heal|turbo|monitor|all]"
        echo ""
        echo "Commands:"
        echo "  heal    - Standard world healing"
        echo "  turbo   - Zero latency parallel healing"
        echo "  monitor - Check volume status"
        echo "  all     - Run everything"
        ;;
esac

echo ""
echo "════════════════════════════════════════════════════════════════════════"
echo "                         GORUNFREE COMPLETE"
echo "════════════════════════════════════════════════════════════════════════"
