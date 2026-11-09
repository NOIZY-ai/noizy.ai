#!/bin/bash
# SIMPLE_EMAIL_SETUP.sh
# SUPER SIMPLE - Step by step, easy to follow

clear

echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║     📧 SIMPLE EMAIL SETUP - EASY STEPS                              ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo ""

echo "Hi! Let's set up your email addresses step by step."
echo ""
echo "You want these email addresses to work:"
echo "  • rp@fishmusicinc.com"
echo "  • rsp@noizylab.ca"
echo "  • help@noizylab.ca"
echo ""
echo "All emails will go to: rsplowman@gmail.com"
echo ""

# Create super simple guide
cat > "$HOME/Desktop/SIMPLE_EMAIL_STEPS.txt" << 'SIMPLE_EOF'
╔══════════════════════════════════════════════════════════════════════╗
║     📧 SIMPLE EMAIL SETUP - EASY STEPS                                ║
╚══════════════════════════════════════════════════════════════════════╝

WHAT YOU WANT:
──────────────

You want people to be able to email you at:
  • rp@fishmusicinc.com
  • rsp@noizylab.ca
  • help@noizylab.ca

And all those emails should go to: rsplowman@gmail.com

══════════════════════════════════════════════════════════════════════
STEP 1: CLOUDFLARE (Add 3 Records)
══════════════════════════════════════════════════════════════════════

I'll open Cloudflare for you. You need to add 3 records.

WHAT TO DO:
  1. Page will open automatically
  2. Look for a button that says "Add record" (usually at top)
  3. Click it
  4. Fill in the form 3 times (I'll tell you what to type)

RECORD 1:
  • Click "Add record"
  • Where it says "Type" - choose "MX"
  • Where it says "Name" - type: @
  • Where it says "Priority" - type: 10
  • Where it says "Mail server" - type: mx1.improvmx.com.
  • Click "Save"

RECORD 2:
  • Click "Add record" again
  • Type: MX
  • Name: @
  • Priority: 20
  • Mail server: mx2.improvmx.com.
  • Click "Save"

RECORD 3:
  • Click "Add record" again
  • Type: TXT
  • Name: @
  • Content: v=spf1 include:spf.improvmx.com ~all
  • Click "Save"

THAT'S IT! Wait 2 minutes, then go to Step 2.

══════════════════════════════════════════════════════════════════════
STEP 2: IMPROVMX (Create Alias)
══════════════════════════════════════════════════════════════════════

I'll open ImprovMX for you.

WHAT TO DO:
  1. Page will open automatically
  2. Find "fishmusicinc.com" (click on it)
  3. Look for "Aliases" tab (click it)
  4. Click "Add alias"
  5. Fill in:
     • Alias: rp
     • Forward to: rsplowman@gmail.com
  6. Click "Save"

THAT'S IT!

══════════════════════════════════════════════════════════════════════
STEP 3: GMAIL (Add "Send As")
══════════════════════════════════════════════════════════════════════

I'll open Gmail settings for you.

WHAT TO DO:
  1. Page will open automatically
  2. Look for "Send mail as" (use CMD+F to find it)
  3. Click "Add another email address"
  4. Type: rp@fishmusicinc.com
  5. Click "Next"
  6. Check your email for verification
  7. Click the link in the email

THAT'S IT!

══════════════════════════════════════════════════════════════════════
THAT'S ALL!
══════════════════════════════════════════════════════════════════════

After these 3 steps, you're done!

People can email you at:
  • rp@fishmusicinc.com
  • rsp@noizylab.ca (already done!)
  • help@noizylab.ca (already done!)

All emails go to: rsplowman@gmail.com

══════════════════════════════════════════════════════════════════════

SIMPLE_EOF

# Create simple launcher
cat > "$HOME/Desktop/START_EMAIL_SETUP.command" << 'START_EOF'
#!/bin/bash
# START_EMAIL_SETUP - Super Simple

clear

echo "📧 Let's set up your email addresses!"
echo ""
echo "I'll open 3 pages for you."
echo "Follow the simple steps in: SIMPLE_EMAIL_STEPS.txt"
echo ""
echo "Opening pages now..."
echo ""

# Open Cloudflare
echo "1. Opening Cloudflare..."
open "https://dash.cloudflare.com/1323e14ace0c8d7362612d5b5c0d41bb/fishmusicinc.com/dns/records"
sleep 2

# Open ImprovMX
echo "2. Opening ImprovMX..."
open "https://app.improvmx.com/"
sleep 2

# Open Gmail
echo "3. Opening Gmail..."
open "https://mail.google.com/mail/u/0/#settings/accounts"
sleep 1

# Open guide
echo "4. Opening simple guide..."
open "$HOME/Desktop/SIMPLE_EMAIL_STEPS.txt"

echo ""
echo "✅ All pages opened!"
echo ""
echo "📋 Follow the steps in: SIMPLE_EMAIL_STEPS.txt"
echo ""
echo "It's just 3 simple steps!"
echo ""

say "Email setup started. Three pages opened. Follow the simple steps guide."
START_EOF

chmod +x "$HOME/Desktop/START_EMAIL_SETUP.command"

# Open the simple guide
open "$HOME/Desktop/SIMPLE_EMAIL_STEPS.txt"

echo "✅ Simple guide created!"
echo ""
echo "📋 SIMPLE GUIDE: SIMPLE_EMAIL_STEPS.txt on Desktop"
echo ""
echo "🚀 TO START:"
echo "   Double-click: START_EMAIL_SETUP.command"
echo ""
echo "It will open everything and show you simple steps!"
echo ""

say "Simple email setup guide created. Double click START EMAIL SETUP to begin."

