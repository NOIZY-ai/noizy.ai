#!/bin/bash
# CLOUDFLARE_DNS_SETUP.sh
# Guide for setting up DNS in Cloudflare for ImprovMX

clear

echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║     🌐 CLOUDFLARE DNS SETUP FOR IMPROVMX                            ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo ""

DOMAIN="fishmusicinc.com"

echo "📋 DNS SETUP REQUIRED FOR: $DOMAIN"
echo ""
echo "⚠️  IMPORTANT: ImprovMX requires DNS changes to work"
echo "   But we'll make it as easy as possible!"
echo ""

# Create Cloudflare setup guide
cat > "$HOME/Desktop/CLOUDFLARE_DNS_SETUP_GUIDE.txt" << 'GUIDE_EOF'
╔══════════════════════════════════════════════════════════════════════╗
║     🌐 CLOUDFLARE DNS SETUP GUIDE                                    ║
║     For: fishmusicinc.com                                            ║
╚══════════════════════════════════════════════════════════════════════╝

CURRENT SITUATION:
──────────────────

✅ fishmusicinc.com domain added in ImprovMX
❌ DNS records need to be configured in Cloudflare
❌ MX records currently point to Google (need to change to ImprovMX)
❌ SPF record needs to be added

WHAT YOU NEED TO DO:
────────────────────

Add/Update DNS records in Cloudflare for fishmusicinc.com

══════════════════════════════════════════════════════════════════════
STEP 1: OPEN CLOUDFLARE
══════════════════════════════════════════════════════════════════════

1. Open: https://dash.cloudflare.com/
2. Log in to your Cloudflare account
3. Select: fishmusicinc.com domain
4. Click: "DNS" in the left sidebar

VOICE: "Open Cloudflare"
       "Click DNS"

KEYBOARD: TAB to navigate, SPACE to click

══════════════════════════════════════════════════════════════════════
STEP 2: REMOVE OLD GOOGLE MX RECORDS (If Present)
══════════════════════════════════════════════════════════════════════

Look for these MX records and DELETE them:
  • alt4.aspmx.l.google.com
  • aspmx.l.google.com
  • alt3.aspmx.l.google.com
  • alt1.aspmx.l.google.com
  • alt2.aspmx.l.google.com

HOW TO DELETE:
  1. Find the MX record
  2. Click the "..." menu (three dots)
  3. Click "Delete"
  4. Confirm deletion

VOICE: "Click [record name]"
       "Click Delete"
       "Click Confirm"

KEYBOARD: TAB to record, SPACE to open menu, TAB to Delete, RETURN

══════════════════════════════════════════════════════════════════════
STEP 3: ADD IMPROVMX MX RECORDS
══════════════════════════════════════════════════════════════════════

Add these TWO MX records:

RECORD 1:
  Type: MX
  Name: @ (or leave blank, or fishmusicinc.com)
  Priority: 10
  Mail Server: mx1.improvmx.com.
  (Note: Include the dot at the end!)

RECORD 2:
  Type: MX
  Name: @ (or leave blank, or fishmusicinc.com)
  Priority: 20
  Mail Server: mx2.improvmx.com.
  (Note: Include the dot at the end!)

HOW TO ADD:
  1. Click "Add record" button
  2. Select "MX" from Type dropdown
  3. Name field: Type "@" or leave blank
  4. Priority field: Type "10" (for first record)
  5. Mail server field: Type "mx1.improvmx.com."
  6. Click "Save"
  7. Repeat for second record (Priority: 20, mx2.improvmx.com.)

VOICE: "Click Add record"
       "Select MX"
       "Type @"
       "Type 10"
       "Type mx1.improvmx.com."
       "Click Save"

KEYBOARD: TAB to Add record, SPACE, TAB through fields, type values

══════════════════════════════════════════════════════════════════════
STEP 4: ADD SPF RECORD
══════════════════════════════════════════════════════════════════════

Add this TXT record:

  Type: TXT
  Name: @ (or leave blank, or fishmusicinc.com)
  Content: v=spf1 include:spf.improvmx.com ~all

HOW TO ADD:
  1. Click "Add record" button
  2. Select "TXT" from Type dropdown
  3. Name field: Type "@" or leave blank
  4. Content field: Type "v=spf1 include:spf.improvmx.com ~all"
  5. Click "Save"

VOICE: "Click Add record"
       "Select TXT"
       "Type @"
       "Type v=spf1 include:spf.improvmx.com ~all"
       "Click Save"

KEYBOARD: TAB to Add record, SPACE, TAB through fields, type values

══════════════════════════════════════════════════════════════════════
STEP 5: VERIFY IN IMPROVMX
══════════════════════════════════════════════════════════════════════

After adding DNS records:
  1. Wait 1-2 minutes for DNS to propagate
  2. Go back to ImprovMX: https://app.improvmx.com/
  3. Select fishmusicinc.com domain
  4. Check DNS Settings
  5. Should show green checkmarks ✅

VERIFICATION:
  • MX records should show ✅
  • SPF record should show ✅
  • Status should be "Active"

══════════════════════════════════════════════════════════════════════
QUICK REFERENCE - DNS RECORDS TO ADD
══════════════════════════════════════════════════════════════════════

MX RECORDS (2 records):
───────────────────────

Record 1:
  Type: MX
  Name: @
  Priority: 10
  Value: mx1.improvmx.com.

Record 2:
  Type: MX
  Name: @
  Priority: 20
  Value: mx2.improvmx.com.

SPF RECORD (1 record):
──────────────────────

  Type: TXT
  Name: @
  Content: v=spf1 include:spf.improvmx.com ~all

══════════════════════════════════════════════════════════════════════
TROUBLESHOOTING
══════════════════════════════════════════════════════════════════════

If records don't verify:
  • Wait 2-5 minutes (DNS propagation takes time)
  • Check for typos (especially the dot at end of MX records)
  • Verify you're editing the correct domain
  • Check Cloudflare DNS inspector: inspector.improvmx.com

If you see errors:
  • Make sure MX records have the dot (.) at the end
  • Make sure SPF record is exactly: v=spf1 include:spf.improvmx.com ~all
  • Check that old Google MX records are deleted

══════════════════════════════════════════════════════════════════════
VOICE COMMANDS SUMMARY
══════════════════════════════════════════════════════════════════════

"Open Cloudflare"
"Click DNS"
"Click Add record"
"Select MX"
"Type @"
"Type 10"
"Type mx1.improvmx.com."
"Click Save"
"Select TXT"
"Type v=spf1 include:spf.improvmx.com ~all"

══════════════════════════════════════════════════════════════════════
KEYBOARD SHORTCUTS
══════════════════════════════════════════════════════════════════════

TAB: Navigate between fields/buttons
SPACE: Click button/select option
RETURN: Submit/save
ESC: Cancel/close
CMD+F: Find/search
Arrow keys: Navigate dropdowns

══════════════════════════════════════════════════════════════════════

⏱️  ESTIMATED TIME: 5-10 minutes
🎯 FOCUS: Add 2 MX records + 1 TXT record
✅ After setup: Email forwarding will work!

GUIDE_EOF

# Create quick action script
cat > "$HOME/Desktop/OPEN_CLOUDFLARE_DNS.command" << 'CLOUDFLARE_EOF'
#!/bin/bash
# Open Cloudflare DNS settings

echo "🌐 Opening Cloudflare DNS settings..."
open "https://dash.cloudflare.com/"

sleep 2

echo ""
echo "📋 NEXT STEPS:"
echo "  1. Log in to Cloudflare"
echo "  2. Select fishmusicinc.com domain"
echo "  3. Click 'DNS' in sidebar"
echo "  4. Follow the guide: CLOUDFLARE_DNS_SETUP_GUIDE.txt"
echo ""

say "Cloudflare opened. Log in and select fishmusicinc.com domain. Then click DNS."
CLOUDFLARE_EOF

chmod +x "$HOME/Desktop/OPEN_CLOUDFLARE_DNS.command"

# Open the guide
open "$HOME/Desktop/CLOUDFLARE_DNS_SETUP_GUIDE.txt"

echo "✅ Cloudflare DNS setup guide created!"
echo ""
echo "📋 GUIDE: CLOUDFLARE_DNS_SETUP_GUIDE.txt on Desktop"
echo ""
echo "🚀 QUICK ACTION:"
echo "   OPEN_CLOUDFLARE_DNS.command - Opens Cloudflare"
echo ""
echo "📋 WHAT TO DO:"
echo "  1. Open Cloudflare DNS"
echo "  2. Add 2 MX records (mx1 and mx2.improvmx.com)"
echo "  3. Add 1 TXT record (SPF)"
echo "  4. Wait 2 minutes"
echo "  5. Verify in ImprovMX"
echo ""

say "Cloudflare DNS setup guide created. Follow the instructions to add MX and TXT records."

