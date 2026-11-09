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
echo "${PURPLE}╚════════════════════════════════════════════════════════════════╝${NC}"
echo ""

cd "$(dirname "$0")"

# Create deployment directory
DEPLOY_DIR="gabriel_hp_omen_deployment"
mkdir -p "$DEPLOY_DIR"

echo "${CYAN}📋 Creating deployment package...${NC}"

# Copy essential files
cp network_bridge.py "$DEPLOY_DIR/" 2>/dev/null || true
cp requirements.txt "$DEPLOY_DIR/"
cp start_gabriel_hp_omen.sh "$DEPLOY_DIR/"

chmod +x "$DEPLOY_DIR/start_gabriel_hp_omen.sh"

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
echo "${PURPLE}╚════════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo "${CYAN}🚀 Next steps:${NC}"
echo ""
echo "   1. Copy to HP-OMEN:"
echo "      scp $TARBALL m2ultra@10.100.0.2:/home/m2ultra/"
echo ""
echo "   2. On HP-OMEN, extract:"
echo "      tar -xzf $TARBALL"
echo "      cd $DEPLOY_DIR"
echo ""
echo "   3. Start GABRIEL:"
echo "      ./start_gabriel_hp_omen.sh"
echo ""
echo "${CYAN}🌐 M2Ultra and HP-OMEN will auto-discover each other!${NC}"
echo ""
