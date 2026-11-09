#!/bin/bash
# DOMAINS_CONFIG.sh
# Configuration for fishmusicinc.com and noizylab.ca

DOMAIN1="fishmusicinc.com"
DOMAIN2="noizylab.ca"
PRIMARY_EMAIL="rsplowman@gmail.com"

echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║     📧 DOMAIN CONFIGURATION                                          ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo ""

echo "🌐 DOMAINS:"
echo "   1. $DOMAIN1"
echo "   2. $DOMAIN2"
echo ""
echo "📧 PRIMARY EMAIL: $PRIMARY_EMAIL"
echo ""

# Create configuration file
CONFIG_FILE="$HOME/NOIZYLAB/email/domains_config.txt"

cat > "$CONFIG_FILE" << EOF
EMAIL DOMAINS CONFIGURATION
===========================

Domains:
  1. fishmusicinc.com
  2. noizylab.ca

Primary Email: rsplowman@gmail.com

ALIASES TO CREATE:
──────────────────

For fishmusicinc.com:
  • rp@fishmusicinc.com → rsplowman@gmail.com

For noizylab.ca:
  • rsp@noizylab.ca → rsplowman@gmail.com
  • help@noizylab.ca → rsplowman@gmail.com

IMPROVMX SETUP:
───────────────

1. Add Domain: fishmusicinc.com
   → Go to: https://app.improvmx.com/
   → Click "Add domain"
   → Enter: fishmusicinc.com
   → Click "Add"

2. Add Domain: noizylab.ca
   → Click "Add domain"
   → Enter: noizylab.ca
   → Click "Add"

3. Create Aliases:
   
   Domain: fishmusicinc.com
   □ Alias: rp → Forward to: rsplowman@gmail.com
   
   Domain: noizylab.ca
   □ Alias: rsp → Forward to: rsplowman@gmail.com
   □ Alias: help → Forward to: rsplowman@gmail.com

GMAIL "SEND AS" SETUP:
───────────────────────

Add these addresses in Gmail:
  □ rp@fishmusicinc.com
  □ rsp@noizylab.ca
  □ help@noizylab.ca

MACOS MAIL SETUP:
─────────────────

Add these aliases to Mail app:
  □ rp@fishmusicinc.com
  □ rsp@noizylab.ca
  □ help@noizylab.ca

Created: $(date)
EOF

echo "✅ Configuration saved: $CONFIG_FILE"
echo ""
echo "📋 QUICK SETUP:"
echo ""
echo "1. Open ImprovMX: https://app.improvmx.com/"
echo "2. Add domains:"
echo "   • fishmusicinc.com"
echo "   • noizylab.ca"
echo "3. Create aliases:"
echo "   • rp@fishmusicinc.com"
echo "   • rsp@noizylab.ca"
echo "   • help@noizylab.ca"
echo ""
echo "📖 Full config: $CONFIG_FILE"
echo ""

# Open the config file
open "$CONFIG_FILE" 2>/dev/null || cat "$CONFIG_FILE"

