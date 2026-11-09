#!/bin/bash

# ============================================================================
# GABRIEL LIVING AVATAR - Quick Setup Script
# ============================================================================

echo "🔥 GABRIEL Living Avatar - Quick Setup"
echo "========================================"
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check current directory
if [ ! -f "MASTER_PACKAGE.md" ]; then
    echo "❌ Error: Please run this script from the GABRIEL root directory"
    exit 1
fi

echo -e "${BLUE}What would you like to do?${NC}"
echo ""
echo "1) Start Web Version (Browser-based)"
echo "2) View Unity Setup Instructions"
echo "3) Run AI Server (for both Web and Unity)"
echo "4) Download Sample Avatar (Ready Player Me)"
echo "5) View Complete Documentation"
echo "6) Run All (Web + AI Server)"
echo ""
read -p "Enter choice [1-6]: " choice

case $choice in
    1)
        echo ""
        echo -e "${GREEN}🚀 Starting Web Version...${NC}"
        echo ""
        cd WebAvatar
        
        # Check if Python 3 is available
        if command -v python3 &> /dev/null; then
            echo "Opening web server on http://localhost:8000"
            echo ""
            echo -e "${YELLOW}📝 Quick Tips:${NC}"
            echo "  • Add your avatar to: WebAvatar/models/avatar.glb"
            echo "  • You'll be prompted for OpenAI API key on first run"
            echo "  • Press Ctrl+C to stop the server"
            echo ""
            echo "Opening browser in 3 seconds..."
            sleep 3
            
            # Try to open browser
            if command -v open &> /dev/null; then
                open http://localhost:8000
            elif command -v xdg-open &> /dev/null; then
                xdg-open http://localhost:8000
            fi
            
            python3 -m http.server 8000
        else
            echo "❌ Python 3 not found. Please install Python 3."
            exit 1
        fi
        ;;
        
    2)
        echo ""
        echo -e "${GREEN}📖 Unity Setup Instructions${NC}"
        echo ""
        echo "File: Unity3D/UNITY_SETUP_COMPLETE.md"
        echo ""
        
        if command -v less &> /dev/null; then
            less Unity3D/UNITY_SETUP_COMPLETE.md
        else
            cat Unity3D/UNITY_SETUP_COMPLETE.md
        fi
        ;;
        
    3)
        echo ""
        echo -e "${GREEN}🤖 Starting AI Server...${NC}"
        echo ""
        
        # Check if Flask is installed
        if python3 -c "import flask" &> /dev/null; then
            echo "Starting Flask server on http://localhost:5000"
            echo ""
            echo -e "${YELLOW}📝 Server Info:${NC}"
            echo "  • Endpoint: http://localhost:5000"
            echo "  • Supports both Web and Unity clients"
            echo "  • Press Ctrl+C to stop"
            echo ""
            python3 gabriel_unity_server.py
        else
            echo "❌ Flask not installed. Installing dependencies..."
            pip3 install flask flask-cors
            echo ""
            echo "✅ Dependencies installed. Starting server..."
            python3 gabriel_unity_server.py
        fi
        ;;
        
    4)
        echo ""
        echo -e "${GREEN}📥 Avatar Download Guide${NC}"
        echo ""
        echo "To get a sample avatar:"
        echo ""
        echo "1. Visit: https://readyplayer.me/"
        echo "2. Create your avatar (free)"
        echo "3. Export as GLB format"
        echo "4. Save to: WebAvatar/models/avatar.glb"
        echo ""
        echo "Alternative sources:"
        echo "  • Mixamo: https://www.mixamo.com/"
        echo "  • Blender: Use gabriel_blender_exporter.py"
        echo "  • MetaHuman: For Unreal Engine"
        echo ""
        read -p "Press Enter to open Ready Player Me in browser..."
        
        if command -v open &> /dev/null; then
            open https://readyplayer.me/
        elif command -v xdg-open &> /dev/null; then
            xdg-open https://readyplayer.me/
        fi
        ;;
        
    5)
        echo ""
        echo -e "${GREEN}📚 Documentation${NC}"
        echo ""
        echo "Available documentation:"
        echo ""
        echo "1. MASTER_PACKAGE.md - Complete overview"
        echo "2. WebAvatar/README_WEB.md - Web implementation guide"
        echo "3. Unity3D/UNITY_SETUP_COMPLETE.md - Unity setup"
        echo "4. Unity3D/UNREAL_ENGINE_5_GUIDE.md - Unreal setup"
        echo "5. GABRIEL_3D_COMPLETE.md - Architecture overview"
        echo ""
        read -p "Enter number to view [1-5]: " doc_choice
        
        case $doc_choice in
            1) file="MASTER_PACKAGE.md" ;;
            2) file="WebAvatar/README_WEB.md" ;;
            3) file="Unity3D/UNITY_SETUP_COMPLETE.md" ;;
            4) file="Unity3D/UNREAL_ENGINE_5_GUIDE.md" ;;
            5) file="GABRIEL_3D_COMPLETE.md" ;;
            *) echo "Invalid choice"; exit 1 ;;
        esac
        
        echo ""
        if command -v less &> /dev/null; then
            less "$file"
        else
            cat "$file"
        fi
        ;;
        
    6)
        echo ""
        echo -e "${GREEN}🚀 Starting Complete Stack...${NC}"
        echo ""
        
        # Start AI server in background
        echo "Starting AI Server..."
        python3 gabriel_unity_server.py &
        SERVER_PID=$!
        sleep 2
        
        # Start web server
        echo "Starting Web Server..."
        cd WebAvatar
        
        echo ""
        echo -e "${YELLOW}📝 All Systems Running:${NC}"
        echo "  • AI Server: http://localhost:5000"
        echo "  • Web App: http://localhost:8000"
        echo ""
        echo "Press Ctrl+C to stop all servers"
        echo ""
        
        # Cleanup on exit
        trap "kill $SERVER_PID 2>/dev/null" EXIT
        
        sleep 2
        if command -v open &> /dev/null; then
            open http://localhost:8000
        fi
        
        python3 -m http.server 8000
        ;;
        
    *)
        echo "Invalid choice"
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}✅ Done!${NC}"
