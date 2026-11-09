#!/usr/bin/env bash
#═══════════════════════════════════════════════════════════════════════════════
#  MAIL MANAGER PRO — EXAMPLE: API USAGE
#  REST API integration examples
#═══════════════════════════════════════════════════════════════════════════════

echo "MAIL MANAGER PRO API EXAMPLES"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
CYAN='\033[0;36m'
RESET='\033[0m'

# Start API server first
echo "Starting API server (port 8420)..."
mailmgr api start &
sleep 3

API_URL="http://127.0.0.1:8420"

# Example 1: Check health
echo -e "${GREEN}1. Health Check${RESET}"
echo "GET $API_URL/health"
curl -s "$API_URL/health" | jq .
echo ""

# Example 2: Get system status
echo -e "${GREEN}2. System Status${RESET}"
echo "GET $API_URL/status"
curl -s "$API_URL/status" | jq .
echo ""

# Example 3: List backups
echo -e "${GREEN}3. List Backups${RESET}"
echo "GET $API_URL/backups"
curl -s "$API_URL/backups" | jq .
echo ""

# Example 4: Create backup
echo -e "${GREEN}4. Create Backup${RESET}"
echo "POST $API_URL/backups"
curl -s -X POST "$API_URL/backups" | jq .
echo ""

# Example 5: List folders
echo -e "${GREEN}5. List Folders${RESET}"
echo "GET $API_URL/folders"
curl -s "$API_URL/folders" | jq .
echo ""

# Example 6: Get scheduler status
echo -e "${GREEN}6. Scheduler Status${RESET}"
echo "GET $API_URL/scheduler/status"
curl -s "$API_URL/scheduler/status" | jq .
echo ""

# Example 7: View API documentation
echo -e "${GREEN}7. API Documentation${RESET}"
echo "Open in browser: $API_URL/docs"
echo "ReDoc view:     $API_URL/redoc"
echo ""

# Stop API
echo "Stopping API server..."
mailmgr api stop

echo -e "${CYAN}✓ Example complete!${RESET}"
