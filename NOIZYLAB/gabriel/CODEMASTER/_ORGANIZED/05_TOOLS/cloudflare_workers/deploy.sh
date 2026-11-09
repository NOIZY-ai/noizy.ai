#!/bin/bash
#
# NOIZYLAB Slack Repairs - Deploy Script
# ═══════════════════════════════════════════════════════════════════════════
# GORUNFREE x1000 - One command deploy
# ═══════════════════════════════════════════════════════════════════════════

set -e

echo "🚀 NOIZYLAB SLACK REPAIRS - DEPLOY"
echo "═══════════════════════════════════════════════════════════════════════════"
echo ""

# Check for wrangler
if ! command -v wrangler &> /dev/null; then
    echo "❌ Wrangler not found. Installing..."
    npm install -g wrangler
fi

# Check if logged in
echo "📋 Checking Cloudflare login..."
wrangler whoami || wrangler login

# Get D1 database ID
echo ""
echo "📊 Fetching D1 database info..."
D1_ID=$(wrangler d1 list --json 2>/dev/null | jq -r '.[] | select(.name=="noizylab-repairs") | .uuid' 2>/dev/null || echo "")

if [ -z "$D1_ID" ]; then
    echo "⚠️  Database 'noizylab-repairs' not found. Creating..."
    wrangler d1 create noizylab-repairs
    D1_ID=$(wrangler d1 list --json | jq -r '.[] | select(.name=="noizylab-repairs") | .uuid')
fi

echo "✅ Database ID: $D1_ID"

# Update wrangler.toml with actual database ID
sed -i '' "s/YOUR_D1_DATABASE_ID/$D1_ID/" wrangler.toml 2>/dev/null || \
sed -i "s/YOUR_D1_DATABASE_ID/$D1_ID/" wrangler.toml

# Initialize database schema
echo ""
echo "📊 Setting up database schema..."
wrangler d1 execute noizylab-repairs --file=schema.sql

# Check for secrets
echo ""
echo "🔐 Checking secrets..."

if ! wrangler secret list | grep -q "SLACK_BOT_TOKEN"; then
    echo ""
    echo "⚠️  SLACK_BOT_TOKEN not set!"
    echo "   Run: wrangler secret put SLACK_BOT_TOKEN"
    echo "   (paste your xoxb-... token)"
fi

if ! wrangler secret list | grep -q "SLACK_SIGNING_SECRET"; then
    echo ""
    echo "⚠️  SLACK_SIGNING_SECRET not set!"
    echo "   Run: wrangler secret put SLACK_SIGNING_SECRET"
fi

# Deploy
echo ""
echo "🚀 Deploying to Cloudflare Workers..."
wrangler deploy

echo ""
echo "═══════════════════════════════════════════════════════════════════════════"
echo "✅ DEPLOYED!"
echo ""
echo "📋 NEXT STEPS:"
echo ""
echo "1. Go to https://api.slack.com/apps and create a new app"
echo ""
echo "2. Add these Request URLs in Slack app settings:"
echo "   Slash Commands:  https://noizylab-repairs.<your-account>.workers.dev/slack/commands"
echo "   Interactivity:   https://noizylab-repairs.<your-account>.workers.dev/slack/interactive"
echo ""
echo "3. Create slash command: /repair"
echo ""
echo "4. Add bot scopes: chat:write, commands, users:read"
echo ""
echo "5. Install app to workspace"
echo ""
echo "6. Type /repair list in Slack!"
echo ""
echo "═══════════════════════════════════════════════════════════════════════════"
echo "⚡ GORUNFREE x1000"
echo ""
