#!/bin/bash
# CLOUDFLARE_DNS_NAVIGATION.sh
# Guide to navigate to DNS page

clear

cat > "$HOME/Desktop/GO_TO_DNS.txt" << 'DNS_NAV_EOF'
╔══════════════════════════════════════════════════════════════════════╗
║     📍 GET TO DNS PAGE - SIMPLE STEPS                                ║
╚══════════════════════════════════════════════════════════════════════╝

YOU'RE ON THE RULES PAGE. YOU NEED TO GO TO DNS PAGE.

══════════════════════════════════════════════════════════════════════

STEP 1: LOOK AT THE LEFT SIDEBAR
──────────────────────────────────

On the left side of the page, you'll see a menu.

Look for these items:
• Overview
• Recents
• fishmusicinc.com
• Rules (you're here now)
• DNS ← CLICK THIS ONE!
• Email
• SSL/TLS
• Security
• etc.

══════════════════════════════════════════════════════════════════════

STEP 2: CLICK "DNS"
────────────────────

Find "DNS" in the left sidebar menu.

It's probably right below "Rules" or near it.

Click on "DNS"

══════════════════════════════════════════════════════════════════════

STEP 3: YOU'LL SEE DNS RECORDS
───────────────────────────────

After clicking DNS, you'll see:
• A table with DNS records
• An "Add record" button (top right)
• Your existing records

══════════════════════════════════════════════════════════════════════

THEN FOLLOW THE NUMBERED GUIDE:
────────────────────────────────

Once you're on the DNS page, follow:
NUMBERED_GUIDE.txt - Steps 3-6

══════════════════════════════════════════════════════════════════════

QUICK SUMMARY:
──────────────

1. Look at LEFT SIDEBAR
2. Find "DNS" (below Rules)
3. Click "DNS"
4. You'll see DNS records table
5. Click "Add record" button
6. Follow NUMBERED_GUIDE.txt from Step 4

══════════════════════════════════════════════════════════════════════
DNS_NAV_EOF

open "$HOME/Desktop/GO_TO_DNS.txt"

echo "✅ GO_TO_DNS.txt created and opened!"
echo ""
echo "📋 SIMPLE STEPS:"
echo "   1. Look at LEFT SIDEBAR"
echo "   2. Find 'DNS' (below Rules)"
echo "   3. Click 'DNS'"
echo "   4. You'll see DNS records"
echo "   5. Then follow NUMBERED_GUIDE.txt"
echo ""

say "Navigation guide created. Look at the left sidebar. Find DNS below Rules. Click DNS. Then you'll see the DNS records page where you can add MX records."

