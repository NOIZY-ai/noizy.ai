#!/bin/bash
# QUICK_DOMAINS_SETUP.sh
# Quick setup for fishmusicinc.com and noizylab.ca

clear

echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║     🚀 QUICK DOMAINS SETUP                                          ║"
echo "║     fishmusicinc.com & noizylab.ca                                   ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo ""

# Open ImprovMX
echo "📧 Opening ImprovMX..."
open "https://app.improvmx.com/"

sleep 2

# Create quick reference
QUICK_REF="$HOME/Desktop/DOMAINS_QUICK_REFERENCE.txt"

cat > "$QUICK_REF" << 'EOF'
╔══════════════════════════════════════════════════════════════════════╗
║     🚀 QUICK DOMAINS SETUP REFERENCE                                 ║
╚══════════════════════════════════════════════════════════════════════╝

DOMAINS:
  • fishmusicinc.com
  • noizylab.ca

PRIMARY EMAIL: rsplowman@gmail.com

══════════════════════════════════════════════════════════════════════
IMPROVMX SETUP (Currently Open)
══════════════════════════════════════════════════════════════════════

STEP 1: ADD DOMAINS
────────────────────

Domain 1: fishmusicinc.com
  • TAB to "Add domain" button
  • SPACE to click
  • Type: fishmusicinc.com
  • TAB, RETURN to add

Domain 2: noizylab.ca
  • TAB to "Add domain" button
  • SPACE to click
  • Type: noizylab.ca
  • TAB, RETURN to add

STEP 2: CREATE ALIASES
──────────────────────

For fishmusicinc.com:
  • TAB to "Add alias" or "Create alias"
  • SPACE to click
  • Alias field: Type "rp"
  • Forward to field: Type "rsplowman@gmail.com"
  • TAB to "Save", RETURN

For noizylab.ca:
  Alias 1:
    • Alias: "rsp"
    • Forward to: "rsplowman@gmail.com"
  
  Alias 2:
    • Alias: "help"
    • Forward to: "rsplowman@gmail.com"

══════════════════════════════════════════════════════════════════════
VOICE COMMANDS
══════════════════════════════════════════════════════════════════════

Say: "Click Add domain"
Say: "Type fishmusicinc.com"
Say: "Click Add"
Say: "Type noizylab.ca"
Say: "Click Add alias"
Say: "Type rp"
Say: "Type rsplowman@gmail.com"
Say: "Click Save"

══════════════════════════════════════════════════════════════════════
KEYBOARD SHORTCUTS
══════════════════════════════════════════════════════════════════════

TAB:        Navigate to next field/button
SHIFT+TAB:  Navigate to previous field/button
SPACE:      Click button/checkbox
RETURN:     Submit form/click primary button
CMD+F:      Find/search on page
ESC:        Cancel/close dialog

══════════════════════════════════════════════════════════════════════
FINAL ALIASES SUMMARY
══════════════════════════════════════════════════════════════════════

✅ rp@fishmusicinc.com → rsplowman@gmail.com
✅ rsp@noizylab.ca → rsplowman@gmail.com
✅ help@noizylab.ca → rsplowman@gmail.com

══════════════════════════════════════════════════════════════════════

ImprovMX is open and ready!
Follow the steps above to complete setup.

EOF

echo "✅ Quick reference created: $QUICK_REF"
echo ""
echo "📋 IMPROVMX IS NOW OPEN"
echo ""
echo "Next steps:"
echo "  1. Add domain: fishmusicinc.com"
echo "  2. Add domain: noizylab.ca"
echo "  3. Create aliases (see reference above)"
echo ""
echo "📖 Reference guide: $QUICK_REF"
echo ""

# Open the reference
open "$QUICK_REF" 2>/dev/null || cat "$QUICK_REF"

say "ImprovMX opened. Domains ready to add: fishmusicinc.com and noizylab.ca"

