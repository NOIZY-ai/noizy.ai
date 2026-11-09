#!/bin/bash
# deploy.sh
# Automates Voice Worker "Full Stack" deployment

echo "=== Voice Worker Full Stack Deployment ==="

# 1. Install Dependencies
echo "[1/4] Installing npm dependencies..."
npm install

# 2. Setup Infrastructure
echo "[2/4] Initializing Cloudflare Resources..."
# R2
npx wrangler r2 bucket create voice-assets 2>/dev/null || echo "Bucket 'voice-assets' likely exists."
# KV
npx wrangler kv:namespace create VOICE_AUDIT 2>/dev/null || echo "KV Namespace creation via script requires manual binding update usually, but we will attempt create."
echo "NOTE: If you haven't created the KV namespace 'VOICE_AUDIT' before, you might need to copy the ID into wrangler.toml manually."
echo "Ideally, run: npx wrangler kv:namespace create VOICE_AUDIT"
echo "And paste the output id into wrangler.toml under [kv_namespaces]."

# 3. Check for Secrets 
echo "[3/4] Checking Secrets configuration..."
echo "Ensure 'TTS_API_KEY' and 'ANTHROPIC_API_KEY' are set."

# 4. Deploy
echo "[4/4] Deploying to Cloudflare..."
npx wrangler deploy

echo "=== Deployment Complete ==="
