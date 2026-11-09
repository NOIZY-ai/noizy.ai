#!/bin/bash
# CLOUDFLARE_DNS_DIRECT_SETUP.sh
# Direct setup for fishmusicinc.com DNS records

clear

echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║     🌐 CLOUDFLARE DNS DIRECT SETUP                                  ║"
echo "║     fishmusicinc.com DNS Records                                     ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo ""

CLOUDFLARE_URL="https://dash.cloudflare.com/1323e14ace0c8d7362612d5b5c0d41bb/fishmusicinc.com/dns/records"

echo "🚀 Opening Cloudflare DNS records page..."
open "$CLOUDFLARE_URL"

sleep 2

# Create direct action guide
cat > "$HOME/Desktop/CLOUDFLARE_DIRECT_SETUP.txt" << 'DIRECT_EOF'
╔══════════════════════════════════════════════════════════════════════╗
║     🌐 CLOUDFLARE DNS - DIRECT SETUP GUIDE                           ║
║     fishmusicinc.com - You're on the DNS page!                       ║
╚══════════════════════════════════════════════════════════════════════╝

✅ YOU'RE HERE: Cloudflare DNS Records Page
────────────────────────────────────────────

The page is open! You can see all your DNS records.

══════════════════════════════════════════════════════════════════════
STEP 1: DELETE OLD GOOGLE MX RECORDS (If Present)
══════════════════════════════════════════════════════════════════════

Look for MX records with these values:
  • aspmx.l.google.com
  • alt1.aspmx.l.google.com
  • alt2.aspmx.l.google.com
  • alt3.aspmx.l.google.com
  • alt4.aspmx.l.google.com

TO DELETE:
  1. Find the record in the list
  2. Click the "..." (three dots) menu on the right
  3. Click "Delete"
  4. Confirm deletion
  5. Repeat for all Google MX records

VOICE: "Click [record]"
       "Click three dots"
       "Click Delete"
       "Click Confirm"

KEYBOARD: TAB to record, SPACE to open menu, TAB to Delete, RETURN

══════════════════════════════════════════════════════════════════════
STEP 2: ADD FIRST MX RECORD
══════════════════════════════════════════════════════════════════════

1. Click "Add record" button (usually at top of page)
2. In the form that appears:
   - Type: Select "MX" from dropdown
   - Name: Type "@" (or leave blank if it auto-fills)
   - Priority: Type "10"
   - Mail server: Type "mx1.improvmx.com."
     ⚠️  IMPORTANT: Include the dot (.) at the end!
   - TTL: Leave as "Auto" or default
3. Click "Save" button

VOICE: "Click Add record"
       "Select MX"
       "Type @"
       "Type 10"
       "Type mx1.improvmx.com."
       "Click Save"

KEYBOARD: TAB to "Add record", SPACE, TAB through fields, type values

══════════════════════════════════════════════════════════════════════
STEP 3: ADD SECOND MX RECORD
══════════════════════════════════════════════════════════════════════

1. Click "Add record" button again
2. In the form:
   - Type: Select "MX" from dropdown
   - Name: Type "@" (or leave blank)
   - Priority: Type "20"
   - Mail server: Type "mx2.improvmx.com."
     ⚠️  IMPORTANT: Include the dot (.) at the end!
   - TTL: Leave as "Auto" or default
3. Click "Save" button

VOICE: "Click Add record"
       "Select MX"
       "Type @"
       "Type 20"
       "Type mx2.improvmx.com."
       "Click Save"

KEYBOARD: TAB to "Add record", SPACE, TAB through fields, type values

══════════════════════════════════════════════════════════════════════
STEP 4: ADD SPF TXT RECORD
══════════════════════════════════════════════════════════════════════

1. Click "Add record" button
2. In the form:
   - Type: Select "TXT" from dropdown
   - Name: Type "@" (or leave blank)
   - Content: Type "v=spf1 include:spf.improvmx.com ~all"
     (Copy this exactly as shown)
   - TTL: Leave as "Auto" or default
3. Click "Save" button

VOICE: "Click Add record"
       "Select TXT"
       "Type @"
       "Type v=spf1 include:spf.improvmx.com ~all"
       "Click Save"

KEYBOARD: TAB to "Add record", SPACE, TAB through fields, type values

══════════════════════════════════════════════════════════════════════
STEP 5: VERIFY RECORDS ADDED
══════════════════════════════════════════════════════════════════════

After adding all 3 records, you should see in the list:

✅ MX record: @ | Priority 10 | mx1.improvmx.com.
✅ MX record: @ | Priority 20 | mx2.improvmx.com.
✅ TXT record: @ | v=spf1 include:spf.improvmx.com ~all

══════════════════════════════════════════════════════════════════════
STEP 6: WAIT & VERIFY IN IMPROVMX
══════════════════════════════════════════════════════════════════════

1. Wait 2-5 minutes for DNS to propagate
2. Go to: https://app.improvmx.com/
3. Select: fishmusicinc.com domain
4. Click: "DNS Settings" tab
5. Should show green checkmarks ✅ for:
   - MX entries
   - SPF records

If still showing errors:
  • Wait a few more minutes
  • Check for typos (especially the dot at end of MX records)
  • Verify records are saved in Cloudflare

══════════════════════════════════════════════════════════════════════
QUICK REFERENCE - EXACT VALUES
══════════════════════════════════════════════════════════════════════

RECORD 1 (MX):
  Type: MX
  Name: @
  Priority: 10
  Mail Server: mx1.improvmx.com.
  (Note the dot at the end!)

RECORD 2 (MX):
  Type: MX
  Name: @
  Priority: 20
  Mail Server: mx2.improvmx.com.
  (Note the dot at the end!)

RECORD 3 (TXT):
  Type: TXT
  Name: @
  Content: v=spf1 include:spf.improvmx.com ~all

══════════════════════════════════════════════════════════════════════
TROUBLESHOOTING
══════════════════════════════════════════════════════════════════════

If "Add record" button not visible:
  • Scroll up on the page
  • Use CMD+F to search for "Add record"
  • Voice: "Show numbers" then "Click [number]"

If form doesn't appear:
  • Check if popup/modal opened
  • Press ESC to close and try again
  • Refresh page (CMD+R) and try again

If save fails:
  • Check all fields are filled
  • Verify MX records have dot (.) at end
  • Check for error messages (usually in red)

If verification fails in ImprovMX:
  • Wait 5-10 minutes (DNS can take time)
  • Double-check values match exactly
  • Use DNS inspector: inspector.improvmx.com

══════════════════════════════════════════════════════════════════════
VOICE COMMANDS (Complete List)
══════════════════════════════════════════════════════════════════════

"Click Add record"
"Select MX"
"Type @"
"Type 10"
"Type mx1.improvmx.com."
"Click Save"
"Select TXT"
"Type v=spf1 include:spf.improvmx.com ~all"
"Scroll down"
"Show numbers"

══════════════════════════════════════════════════════════════════════
KEYBOARD SHORTCUTS
══════════════════════════════════════════════════════════════════════

TAB: Navigate between fields/buttons
SHIFT+TAB: Navigate backwards
SPACE: Click button/select option
RETURN: Submit/save
ESC: Cancel/close
CMD+F: Find/search on page
Arrow keys: Navigate dropdowns
CMD+R: Refresh page

══════════════════════════════════════════════════════════════════════

⏱️  ESTIMATED TIME: 5-10 minutes
🎯 FOCUS: Add 3 records (2 MX + 1 TXT)
✅ After setup: Email forwarding will work!

The Cloudflare DNS page is open - you're ready to add the records!

DIRECT_EOF

open "$HOME/Desktop/CLOUDFLARE_DIRECT_SETUP.txt"

# Create quick action to reopen Cloudflare
cat > "$HOME/Desktop/OPEN_CLOUDFLARE_DNS_DIRECT.command" << 'REOPEN_EOF'
#!/bin/bash
# Reopen Cloudflare DNS page directly

open "https://dash.cloudflare.com/1323e14ace0c8d7362612d5b5c0d41bb/fishmusicinc.com/dns/records"
say "Cloudflare DNS page opened. Ready to add MX and TXT records."
REOPEN_EOF

chmod +x "$HOME/Desktop/OPEN_CLOUDFLARE_DNS_DIRECT.command"

echo "✅ Cloudflare DNS page opened!"
echo ""
echo "📋 DIRECT SETUP GUIDE:"
echo "   CLOUDFLARE_DIRECT_SETUP.txt on Desktop"
echo ""
echo "📋 QUICK REFERENCE:"
echo "   DNS_RECORDS_QUICK_REFERENCE.txt on Desktop"
echo ""
echo "🚀 TO REOPEN:"
echo "   OPEN_CLOUDFLARE_DNS_DIRECT.command"
echo ""
echo "📋 WHAT TO DO NOW:"
echo "   1. Page is open - you're on the DNS records page"
echo "   2. Delete old Google MX records (if present)"
echo "   3. Add 2 MX records (mx1 and mx2.improvmx.com)"
echo "   4. Add 1 TXT record (SPF)"
echo "   5. Wait 2-5 minutes"
echo "   6. Verify in ImprovMX"
echo ""

say "Cloudflare DNS page opened. Follow the direct setup guide. Add two MX records and one TXT record."

