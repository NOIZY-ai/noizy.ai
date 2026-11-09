#!/bin/bash
# deploy.sh
# Automates Voice Worker deployment

echo "=== Voice Worker Deployment ==="

# 1. Install Dependencies
echo "[1/4] Installing npm dependencies..."
npm install

# 2. Create R2 Bucket (if not exists)
echo "[2/4] Ensuring R2 bucket 'voice-assets' exists..."
npx wrangler r2 bucket create voice-assets 2>/dev/null || echo "Bucket likely exists or error ignored."

# 3. Check for Secrets (Manual Step Reminder)
echo "[3/4] Checking Secrets configuration..."
echo "IMPORTANT: Ensure you have run 'wrangler secret put TTS_API_KEY' and 'ANTHROPIC_API_KEY' manually."
echo "Skipping interactive secret entry in this script to avoid blocking."

# 4. Deploy
echo "[4/4] Deploying to Cloudflare..."
npx wrangler deploy

echo "=== Deployment Complete ==="
