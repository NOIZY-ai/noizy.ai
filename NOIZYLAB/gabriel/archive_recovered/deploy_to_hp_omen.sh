#!/bin/bash
#
# DEPLOY GABRIEL TO HP-OMEN
# Package and transfer network bridge to remote machine
#
set -e

GREEN='\033[0;32m'
CYAN='\033[0;36m'
PURPLE='\033[0;35m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "${PURPLE}╔════════════════════════════════════════════════════════════════╗${NC}"
echo "${PURPLE}║  📦 GABRIEL DEPLOYMENT PACKAGE - HP-OMEN                     ║${NC}"
echo "${PURPLE}╔════════════════════════════════════════════════════════════════╗${NC}"
echo ""

cd "$(dirname "$0")"

# Create deployment directory
DEPLOY_DIR="gabriel_hp_omen_deployment"
mkdir -p "$DEPLOY_DIR"

echo "${CYAN}📋 Creating deployment package...${NC}"

# Copy essential files
cp network_bridge.py "$DEPLOY_DIR/"
cp requirements.txt "$DEPLOY_DIR/" 2>/dev/null || echo "flask>=2.3.0
flask-cors>=4.0.0
requests>=2.31.0" > "$DEPLOY_DIR/requirements.txt"

# Create HP-OMEN launcher
cat > "$DEPLOY_DIR/start_gabriel_hp_omen.sh" <<'EOF'
#!/bin/bash
#
# START GABRIEL ON HP-OMEN
#
set -e

GREEN='\033[0;32m'
CYAN='\033[0;36m'
PURPLE='\033[0;35m'
NC='\033[0m'

echo "${PURPLE}╔════════════════════════════════════════════════════════════════╗${NC}"
echo "${PURPLE}║  🌐 GABRIEL NETWORK BRIDGE - HP-OMEN                        ║${NC}"
echo "${PURPLE}╔════════════════════════════════════════════════════════════════╗${NC}"
echo ""

cd "$(dirname "$0")"

# Install dependencies
if ! python3 -c "import flask" 2>/dev/null; then
    echo "${CYAN}📦 Installing dependencies...${NC}"
    pip3 install -r requirements.txt
fi

# Kill existing
pkill -f "network_bridge.py" 2>/dev/null || true
sleep 1

# Start network bridge
echo "${CYAN}🚀 Starting GABRIEL network bridge...${NC}"
python3 network_bridge.py > network_bridge.log 2>&1 &
BRIDGE_PID=$!

sleep 3

# Check if running
if ps -p $BRIDGE_PID > /dev/null 2>&1; then
    echo "${GREEN}✅ GABRIEL Network Bridge ONLINE (PID: $BRIDGE_PID)${NC}"
    echo ""
    echo "${CYAN}📡 Bridge will auto-discover MBP13 GABRIEL${NC}"
    echo "${CYAN}📝 Logs: tail -f network_bridge.log${NC}"
    echo ""
else
    echo "${YELLOW}⚠️  Bridge failed to start - check logs${NC}"
fi
EOF

chmod +x "$DEPLOY_DIR/start_gabriel_hp_omen.sh"

# Create README
cat > "$DEPLOY_DIR/README.md" <<'EOF'
# GABRIEL HP-OMEN Deployment

## Quick Start

1. Copy this entire folder to HP-OMEN
2. Run: `./start_gabriel_hp_omen.sh`
3. Network bridge will auto-discover MBP13

## Manual Setup

```bash
# Install dependencies
pip3 install -r requirements.txt

# Start network bridge
python3 network_bridge.py
```

## Verification

Check bridge status:
```bash
curl http://localhost:5175/api/bridge/status
```

## Network Info

- Bridge Port: 5175
- Discovery Port: 5176 (UDP broadcast)
- Auto-discovery runs every 10 seconds

## Files

- `network_bridge.py` - Network bridge service
- `start_gabriel_hp_omen.sh` - Launch script
- `requirements.txt` - Python dependencies
EOF

echo "${GREEN}✅ Deployment package created: $DEPLOY_DIR/${NC}"
echo ""
echo "${CYAN}📦 Package contents:${NC}"
ls -lh "$DEPLOY_DIR/" | tail -n +2 | awk '{print "   " $9 " (" $5 ")"}'
echo ""

# Create tarball
TARBALL="gabriel_hp_omen.tar.gz"
tar -czf "$TARBALL" "$DEPLOY_DIR"

echo "${GREEN}✅ Tarball created: $TARBALL${NC}"
echo ""

echo "${PURPLE}╔════════════════════════════════════════════════════════════════╗${NC}"
echo "${GREEN}  📡 DEPLOYMENT PACKAGE READY${NC}"
echo "${PURPLE}╔════════════════════════════════════════════════════════════════╗${NC}"
echo ""
echo "${CYAN}🚀 Next steps:${NC}"
echo ""
echo "   1. Copy to HP-OMEN:"
echo "      scp $TARBALL user@hp-omen:/path/to/destination/"
echo ""
echo "   2. On HP-OMEN, extract:"
echo "      tar -xzf $TARBALL"
echo "      cd $DEPLOY_DIR"
echo ""
echo "   3. Start GABRIEL:"
echo "      ./start_gabriel_hp_omen.sh"
echo ""
echo "${CYAN}🌐 MBP13 and HP-OMEN will auto-discover each other!${NC}"
echo ""
