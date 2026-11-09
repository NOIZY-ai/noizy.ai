#!/bin/zsh
# 🎤 GABRIEL SETUP
# Complete Voice AI System Setup
# GORUNFREE Protocol

echo "🎤 GABRIEL - VOICE AI SYSTEM SETUP"
echo "==================================="
echo ""

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GABRIEL_DIR="$(dirname "$SCRIPT_DIR")"

cd "$GABRIEL_DIR"

echo "📁 GABRIEL Structure:"
echo "  Core: core/"
echo "  Advanced: advanced/"
echo "  Ultra: ultra/"
echo "  Integrations: integrations/"
echo "  Web: web/"
echo "  API: api/"
echo "  Utils: utils/"
echo "  Docs: docs/"
echo "  Scripts: scripts/"
echo ""

# Create aliases
echo "🔧 Creating aliases..."
cat >> ~/.zshrc << EOF

# 🎤 GABRIEL Voice AI Aliases
alias gabriel-core='cd $GABRIEL_DIR/core'
alias gabriel-advanced='cd $GABRIEL_DIR/advanced'
alias gabriel-ultra='cd $GABRIEL_DIR/ultra'
alias gabriel-web='cd $GABRIEL_DIR/web'
alias gabriel-api='cd $GABRIEL_DIR/api'
alias gabriel='cd $GABRIEL_DIR'
EOF

echo "✅ Aliases created!"
echo ""
echo "🚀 Quick Access:"
echo "  gabriel - Go to GABRIEL"
echo "  gabriel-core - Core scripts"
echo "  gabriel-ultra - Ultra performance"
echo "  gabriel-api - API server"
echo ""
echo "✅ GABRIEL setup complete!"
echo ""
echo "💡 Run: source ~/.zshrc"

