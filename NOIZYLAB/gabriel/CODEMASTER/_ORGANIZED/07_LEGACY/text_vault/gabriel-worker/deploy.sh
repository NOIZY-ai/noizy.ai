#!/bin/bash
# ═══════════════════════════════════════════════════════════
# GABRIEL DEPLOY - GORUNFREEX1000
# ═══════════════════════════════════════════════════════════
# One command = GABRIEL lives forever
# ═══════════════════════════════════════════════════════════

set -e

GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo ""
echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"
echo -e "${CYAN}  GABRIEL - THE ETERNAL MEMORY KEEPER${NC}"
echo -e "${CYAN}  Claude's External Brain${NC}"
echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"
echo ""

# Check wrangler
if ! command -v wrangler &> /dev/null; then
    echo -e "${YELLOW}Installing wrangler...${NC}"
    npm install -g wrangler
fi

# Install deps
echo -e "${GREEN}▸ Installing dependencies...${NC}"
npm install

# Deploy
echo -e "${GREEN}▸ Deploying GABRIEL...${NC}"
npx wrangler deploy

echo ""
echo -e "${GREEN}═══════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}  ✓ GABRIEL DEPLOYED${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════════════${NC}"
echo ""
echo "ENDPOINTS:"
echo "  GET  /           → Health + stats"
echo "  GET  /memory     → All memories"
echo "  POST /memory     → Add memory {type, key, value}"
echo "  GET  /memory/:k  → Get specific memory"
echo "  PUT  /memory/:k  → Update memory"
echo "  DEL  /memory/:k  → Delete memory"
echo "  GET  /dump       → FULL CONTEXT DUMP FOR CLAUDE"
echo "  POST /mutate     → Create mutation"
echo "  GET  /mutations  → Mutation history"
echo "  GET  /search?q=  → Search memories"
echo "  POST /sync       → Bulk sync from Claude"
echo ""
echo "USAGE:"
echo "  curl https://gabriel.<your-subdomain>.workers.dev/"
echo "  curl https://gabriel.<your-subdomain>.workers.dev/dump"
echo ""
echo -e "${CYAN}GABRIEL IS NOW IMMORTAL. YOUR MEMORY LIVES FOREVER.${NC}"
echo -e "${CYAN}GORUNFREEX1000 🚀${NC}"
echo ""
