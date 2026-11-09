#!/bin/zsh
# 🚀 GABRIEL QUICK START
# GORUNFREE Protocol

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GABRIEL_DIR="$(dirname "$SCRIPT_DIR")"

cd "$GABRIEL_DIR"

echo "🎤 GABRIEL - QUICK START"
echo "========================"
echo ""
echo "Choose an option:"
echo "  1) Core - Basic voice generation"
echo "  2) Advanced - Advanced features"
echo "  3) Ultra - Zero latency (optimized)"
echo "  4) Web - Web interface"
echo "  5) API - REST API server"
echo "  6) List all services"
echo ""
read -p "Choice [1-6]: " choice

case $choice in
    1)
        cd core
        python3 voice_ai_universal.py --list
        ;;
    2)
        cd advanced
        python3 voice_ai_pro.py --list
        ;;
    3)
        cd ultra
        python3 voice_ai_optimized.py --generate "Test" --service edge
        ;;
    4)
        cd web
        python3 voice_ai_web.py
        ;;
    5)
        cd api
        python3 voice_ai_api_server.py
        ;;
    6)
        cd advanced
        python3 voice_ai_pro.py --list
        ;;
    *)
        echo "Invalid choice"
        ;;
esac

