#!/bin/bash
# GABRIEL SYSTEM OMEGA: GITHUB FIXER
# Fixes SSH Authentication Once & For All

echo "🔐 GABRIEL SECURITY PROTOCOL: FIXING GITHUB AUTH..."

EMAIL="rsplowman@icloud.com"
KEY_PATH="$HOME/.ssh/id_ed25519_github"

# 1. Ensure .ssh dir exists
mkdir -p "$HOME/.ssh"
chmod 700 "$HOME/.ssh"

# 2. Generate Key if missing
if [ ! -f "$KEY_PATH" ]; then
    echo "🔑 Generating New SSH Key ($EMAIL)..."
    ssh-keygen -t ed25519 -C "$EMAIL" -f "$KEY_PATH" -N ""
else
    echo "✅ SSH Key exists."
fi

# 3. Add to Apple Keychain & Agent
echo "🔗 Adding to Agent..."
eval "$(ssh-agent -s)"
# Create config entry to force use of correct key
if ! grep -q "Host github.com" "$HOME/.ssh/config"; then
    echo "📝 Updating ~/.ssh/config..."
    echo -e "\nHost github.com\n  AddKeysToAgent yes\n  UseKeychain yes\n  IdentityFile $KEY_PATH" >> "$HOME/.ssh/config"
fi

ssh-add --apple-use-keychain "$KEY_PATH"

# 4. Upload to GitHub via GH CLI
echo "☁️  Uploading Key to GitHub..."
gh ssh-key add "$KEY_PATH.pub" --title "M2 Ultra Gabriel Omega ($(date +%Y-%m-%d))" --type authentication

# 5. Test Connection
echo "📡 Testing Connection..."
ssh -T git@github.com

echo "✅ GITHUB AUTH SEQUENCE COMPLETE."
