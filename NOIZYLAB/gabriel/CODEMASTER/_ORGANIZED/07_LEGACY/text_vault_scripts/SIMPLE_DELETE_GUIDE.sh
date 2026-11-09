#!/bin/bash
# SIMPLE_DELETE_GUIDE.sh
# Super simple delete guide

clear

cat > "$HOME/Desktop/DELETE_THESE.txt" << 'DELETE_EOF'
╔══════════════════════════════════════════════════════════════════════╗
║     🗑️  DELETE THESE - SUPER SIMPLE STEPS                           ║
╚══════════════════════════════════════════════════════════════════════╝

IN CLOUDFLARE DNS PAGE:

══════════════════════════════════════════════════════════════════════

DELETE THESE 3 THINGS:
───────────────────────

1. FIND: _autodiscover._tcp (SRV record)
   → Click the checkbox on the left
   → Click "Delete" button at bottom
   → Click "Confirm" or "Yes"

2. FIND: mandrill._domainkey (TXT record)
   → Click the checkbox on the left
   → Click "Delete" button at bottom
   → Click "Confirm" or "Yes"

3. FIND: * (wildcard) - the one with the star
   → There are 4 of them (2 A records, 2 AAAA records)
   → Click checkbox on each one
   → Click "Delete" button at bottom
   → Click "Confirm" or "Yes"

══════════════════════════════════════════════════════════════════════

THAT'S IT! Just delete those 3 things.

══════════════════════════════════════════════════════════════════════

DON'T DELETE:
─────────────
• fishmusicinc.com (any of them)
• www (any of them)
• _dmarc
• Any TXT records with "spf" in them

══════════════════════════════════════════════════════════════════════
DELETE_EOF

open "$HOME/Desktop/DELETE_THESE.txt"

# Create visual guide
cat > "$HOME/Desktop/EXACT_STEPS.txt" << 'STEPS_EOF'
EXACT STEPS TO DELETE:

1. Look at your DNS records table
2. Find the row that says: _autodiscover._tcp
3. Click the checkbox on the LEFT of that row
4. Look for a "Delete" button (usually at bottom of table)
5. Click "Delete"
6. Click "Yes" or "Confirm"

REPEAT FOR:
- mandrill._domainkey
- * (the star/wildcard records - there are 4 of them)

THAT'S IT!
STEPS_EOF

open "$HOME/Desktop/EXACT_STEPS.txt"

echo "✅ DELETE_THESE.txt created!"
echo "✅ EXACT_STEPS.txt created!"
echo ""
echo "📋 SUPER SIMPLE:"
echo ""
echo "Just delete these 3 things in Cloudflare:"
echo "   1. _autodiscover._tcp"
echo "   2. mandrill._domainkey"
echo "   3. * (wildcard - the star records)"
echo ""
echo "Click checkbox → Click Delete → Done!"
echo ""

say "Simple delete guide created. Just delete autodiscover, Mandrill, and wildcard records. Click the checkbox, then click delete."

