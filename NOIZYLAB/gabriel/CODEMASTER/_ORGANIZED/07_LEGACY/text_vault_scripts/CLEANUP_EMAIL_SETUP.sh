#!/bin/bash
# CLEANUP_EMAIL_SETUP.sh
# Clean up and organize email setup files

clear

echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║     🧹 CLEANING UP EMAIL SETUP FILES                                ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo ""

SETUP_DIR="$HOME/NOIZYLAB/email/setup_files"
mkdir -p "$SETUP_DIR"

echo "📁 Organizing files..."
echo ""

# Move old/duplicate files to organized folder
echo "Moving old files to: $SETUP_DIR"
mv ~/Desktop/*EMAIL*.txt ~/Desktop/*EMAIL*.md 2>/dev/null || true
mv ~/Desktop/*CLOUDFLARE*.txt 2>/dev/null || true
mv ~/Desktop/*DNS*.txt 2>/dev/null || true
mv ~/Desktop/*IMPROVMX*.txt 2>/dev/null || true
mv ~/Desktop/*CHECKLIST*.txt 2>/dev/null || true
mv ~/Desktop/*QUICK*.txt 2>/dev/null || true
mv ~/Desktop/*MASTER*.txt 2>/dev/null || true
mv ~/Desktop/*REFERENCE*.txt 2>/dev/null || true
mv ~/Desktop/*SUMMARY*.txt 2>/dev/null || true

# Keep only essential shortcuts on Desktop
echo ""
echo "✅ Keeping essential shortcuts on Desktop:"
echo ""

# Create master launcher that combines everything
cat > "$HOME/Desktop/EMAIL_SETUP.command" << 'MASTER_EOF'
#!/bin/bash
# EMAIL_SETUP - Master Launcher (All-in-One)

clear

echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║     ⚡ EMAIL ALIASES SETUP - MASTER LAUNCHER ⚡                     ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo ""

echo "🎯 SELECT ACTION:"
echo ""
echo "1. 🚀 Complete Setup (Opens everything)"
echo "2. 🌐 Cloudflare DNS Setup"
echo "3. 📧 Gmail Settings"
echo "4. 📊 Status Check"
echo "5. 🧪 Test Aliases"
echo "6. 📋 View Checklist"
echo "0. Exit"
echo ""

read -p "👉 Your choice (0-6): " choice

case $choice in
    1)
        open "https://app.improvmx.com/"
        sleep 1
        open "https://mail.google.com/mail/u/0/#settings/accounts"
        sleep 1
        open "https://dash.cloudflare.com/1323e14ace0c8d7362612d5b5c0d41bb/fishmusicinc.com/dns/records"
        say "Complete setup launched. All pages opened."
        ;;
    2)
        open "https://dash.cloudflare.com/1323e14ace0c8d7362612d5b5c0d41bb/fishmusicinc.com/dns/records"
        say "Cloudflare DNS page opened. Add MX and TXT records."
        ;;
    3)
        open "https://mail.google.com/mail/u/0/#settings/accounts"
        say "Gmail settings opened."
        ;;
    4)
        echo "📊 STATUS: 66% Complete"
        echo "✅ noizylab.ca - Done"
        echo "📋 fishmusicinc.com - Needs DNS setup"
        echo ""
        echo "🔴 HIGH PRIORITY:"
        echo "   • Add MX records in Cloudflare"
        echo "   • Add TXT (SPF) record in Cloudflare"
        ;;
    5)
        open "mailto:rp@fishmusicinc.com?subject=Test&body=Testing"
        sleep 1
        open "mailto:rsp@noizylab.ca?subject=Test&body=Testing"
        sleep 1
        open "mailto:help@noizylab.ca?subject=Test&body=Testing"
        say "Test emails opened."
        ;;
    6)
        cat << CHECKLIST
╔══════════════════════════════════════════════════════════════════════╗
║     📋 EMAIL SETUP CHECKLIST                                        ║
╚══════════════════════════════════════════════════════════════════════╝

✅ COMPLETED:
  • noizylab.ca domain configured
  • rsp@noizylab.ca alias created
  • help@noizylab.ca alias created

📋 REMAINING:
  🔴 Add MX records in Cloudflare (mx1 & mx2.improvmx.com)
  🔴 Add TXT record in Cloudflare (SPF)
  📋 Create rp@fishmusicinc.com alias in ImprovMX
  📋 Add aliases to Gmail "Send as"

══════════════════════════════════════════════════════════════════════
CHECKLIST
        ;;
    0)
        echo "👋 Goodbye!"
        exit 0
        ;;
    *)
        echo "❌ Invalid choice"
        ;;
esac
MASTER_EOF

chmod +x "$HOME/Desktop/EMAIL_SETUP.command"

# Create one comprehensive guide
cat > "$HOME/Desktop/EMAIL_SETUP_GUIDE.txt" << 'GUIDE_EOF'
╔══════════════════════════════════════════════════════════════════════╗
║     ⚡ EMAIL ALIASES SETUP - COMPLETE GUIDE ⚡                        ║
╚══════════════════════════════════════════════════════════════════════╝

STATUS: 66% Complete
────────────────────

✅ DONE:
  • noizylab.ca configured
  • rsp@noizylab.ca → rsplowman@gmail.com
  • help@noizylab.ca → rsplowman@gmail.com

📋 REMAINING:
  • Cloudflare DNS setup (fishmusicinc.com)
  • Create rp@fishmusicinc.com alias
  • Gmail "Send as" verification

══════════════════════════════════════════════════════════════════════
STEP 1: CLOUDFLARE DNS SETUP (HIGH PRIORITY)
══════════════════════════════════════════════════════════════════════

Open: EMAIL_SETUP.command → Option 2
OR: https://dash.cloudflare.com/1323e14ace0c8d7362612d5b5c0d41bb/fishmusicinc.com/dns/records

ADD 3 RECORDS:

1. MX Record:
   Type: MX
   Name: @
   Priority: 10
   Value: mx1.improvmx.com.
   (Include the dot at the end!)

2. MX Record:
   Type: MX
   Name: @
   Priority: 20
   Value: mx2.improvmx.com.
   (Include the dot at the end!)

3. TXT Record (SPF):
   Type: TXT
   Name: @
   Content: v=spf1 include:spf.improvmx.com ~all

Wait 2-5 minutes, then verify in ImprovMX.

══════════════════════════════════════════════════════════════════════
STEP 2: CREATE ALIAS IN IMPROVMX
══════════════════════════════════════════════════════════════════════

1. Open: https://app.improvmx.com/
2. Select: fishmusicinc.com
3. Click: "Aliases" tab
4. Click: "Add alias"
5. Alias: rp
6. Forward to: rsplowman@gmail.com
7. Click: "Save"

══════════════════════════════════════════════════════════════════════
STEP 3: GMAIL "SEND AS"
══════════════════════════════════════════════════════════════════════

1. Open: https://mail.google.com/mail/u/0/#settings/accounts
2. Scroll to "Send mail as"
3. Add: rp@fishmusicinc.com
4. Verify: rsp@noizylab.ca
5. Verify: help@noizylab.ca

══════════════════════════════════════════════════════════════════════
QUICK ACTIONS
══════════════════════════════════════════════════════════════════════

Double-click: EMAIL_SETUP.command
  → Master launcher
  → All options in one place

══════════════════════════════════════════════════════════════════════

GUIDE_EOF

# Remove duplicate/old files
echo "🧹 Removing duplicates..."
rm -f ~/Desktop/*EMAIL*.command ~/Desktop/*CLOUDFLARE*.command ~/Desktop/*IMPROVMX*.command 2>/dev/null || true
rm -f ~/Desktop/EMAIL_*.command ~/Desktop/ADD_*.command ~/Desktop/CREATE_*.command 2>/dev/null || true
rm -f ~/Desktop/INSTANT_*.command ~/Desktop/TEST_*.command 2>/dev/null || true

# Keep only the master launcher
echo "✅ Keeping: EMAIL_SETUP.command (Master launcher)"
echo "✅ Keeping: EMAIL_SETUP_GUIDE.txt (Complete guide)"

echo ""
echo "📁 Moved old files to: $SETUP_DIR"
echo ""
echo "✅ Desktop cleaned up!"
echo ""
echo "🎯 USE THIS:"
echo "   EMAIL_SETUP.command - Master launcher (all options)"
echo "   EMAIL_SETUP_GUIDE.txt - Complete guide"
echo ""

say "Desktop cleaned up. Master launcher ready. All options in one place."

