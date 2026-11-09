#!/bin/bash

# macOS User Account Repair Script
# This script repairs user accounts with missing home directories or corrupted plists

# Configuration - UPDATE THESE VALUES
USERNAME="username"
FULLNAME="User Name"
PASSWORD="newpassword"

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "=========================================="
echo "macOS User Account Repair Script"
echo "=========================================="
echo "Target User: $USERNAME"
echo "Full Name: $FULLNAME"
echo ""

# Check if running with sudo
if [ "$EUID" -ne 0 ]; then 
    echo -e "${RED}Error: This script must be run with sudo${NC}"
    echo "Usage: sudo bash repair_user_account.sh"
    exit 1
fi

# Step 1: Create home directory if missing
echo -e "${YELLOW}[1/3] Checking home directory...${NC}"
if [ ! -d "/Users/$USERNAME" ]; then
    echo "Home directory missing. Creating /Users/$USERNAME"
    mkdir -p "/Users/$USERNAME"
    chown "$USERNAME:staff" "/Users/$USERNAME"
    chmod 700 "/Users/$USERNAME"
    echo -e "${GREEN}✓ Home directory created${NC}"
else
    echo -e "${GREEN}✓ Home directory exists${NC}"
fi

# Step 2: Reset user permissions
echo -e "${YELLOW}[2/3] Resetting user permissions...${NC}"
USER_ID=$(id -u "$USERNAME" 2>/dev/null)
if [ -n "$USER_ID" ]; then
    diskutil resetUserPermissions / "$USER_ID"
    echo -e "${GREEN}✓ Permissions reset complete${NC}"
else
    echo -e "${RED}Warning: Could not get user ID. User may not exist yet.${NC}"
fi

# Step 3: Recreate user if plist is missing
echo -e "${YELLOW}[3/3] Checking user account...${NC}"
if [ ! -f "/var/db/dslocal/nodes/Default/users/$USERNAME.plist" ]; then
    echo "User plist missing. Recreating user account..."
    sysadminctl -addUser "$USERNAME" -fullName "$FULLNAME" -password "$PASSWORD" -admin
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ User account recreated successfully${NC}"
    else
        echo -e "${RED}✗ Failed to recreate user account${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}✓ User account exists${NC}"
fi

# Step 4: Verify home directory ownership (again, after user recreation)
echo ""
echo -e "${YELLOW}Verifying final state...${NC}"
if [ -d "/Users/$USERNAME" ]; then
    chown -R "$USERNAME:staff" "/Users/$USERNAME"
    echo -e "${GREEN}✓ Home directory ownership verified${NC}"
fi

# Display final status
echo ""
echo "=========================================="
echo -e "${GREEN}User account repair complete!${NC}"
echo "=========================================="
echo "User: $USERNAME"
echo "Home: /Users/$USERNAME"
echo "Status: $(dscl . -read /Users/$USERNAME 2>/dev/null | grep -q UserShell && echo 'Active' || echo 'Check manually')"
echo ""
echo "Next steps:"
echo "1. Test login with the user account"
echo "2. Verify home directory contents"
echo "3. Check user preferences and permissions"
echo ""
