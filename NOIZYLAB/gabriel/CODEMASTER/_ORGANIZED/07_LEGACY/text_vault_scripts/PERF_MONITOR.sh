#!/bin/bash
# PERFORMANCE MONITOR - MC96
# Real-time performance monitoring

echo "╔════════════════════════════════════════════════════╗"
echo "║  PERFORMANCE MONITOR - MC96                        ║"
echo "╚════════════════════════════════════════════════════╝"
echo ""

while true; do
    clear
    echo "╔════════════════════════════════════════════════════╗"
    echo "║  PERFORMANCE MONITOR - MC96 (Press Ctrl+C to exit)║"
    echo "╚════════════════════════════════════════════════════╝"
    echo ""
    
    # CPU
    echo "⚡ CPU Usage:"
    top -l 1 | grep "CPU usage" | awk '{print "  " }'
    
    # Memory
    echo ""
    echo "💾 Memory:"
    vm_stat | head -5 | awk '{print "  " }'
    
    # Disk
    echo ""
    echo "📊 Disk Usage:"
    df -h / | tail -1 | awk '{print "  Root: "  " used ("  " free)"}'
    
    # Network
    echo ""
    echo "🌐 Network:"
    ifconfig | grep "inet " | grep -v 127.0.0.1 | awk '{print "  " }'
    
    sleep 2
done