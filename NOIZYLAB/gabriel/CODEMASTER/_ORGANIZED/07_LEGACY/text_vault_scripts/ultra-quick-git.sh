#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════
#  ⚡ ULTRA QUICK GIT SETUP (One-Liner Mode)
# ═══════════════════════════════════════════════════════════════════════════
#  Usage: ultra-quick-git project-name github-username
#  No prompts, uses smart defaults
# ═══════════════════════════════════════════════════════════════════════════

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Get arguments
PROJECT_NAME="$1"
GITHUB_USER="$2"

# Validate
if [ -z "$PROJECT_NAME" ] || [ -z "$GITHUB_USER" ]; then
    echo -e "${RED}Usage: $0 project-name github-username${NC}"
    echo ""
    echo "Example:"
    echo "  $0 my-awesome-project username"
    exit 1
fi

# Sanitize
PROJECT_NAME=$(echo "$PROJECT_NAME" | tr '[:upper:]' '[:lower:]' | tr ' ' '-')

# Paths
PROJECT_PATH="$HOME/Projects/$PROJECT_NAME"
REPO_URL="git@github.com:${GITHUB_USER}/${PROJECT_NAME}.git"

# Git config (use global or defaults)
GIT_EMAIL=$(git config --global user.email 2>/dev/null || echo "${GITHUB_USER}@users.noreply.github.com")
GIT_NAME=$(git config --global user.name 2>/dev/null || echo "$GITHUB_USER")

# Banner
echo -e "${BLUE}⚡ Ultra Quick Setup: $PROJECT_NAME${NC}"
echo ""

# Create project
mkdir -p "$PROJECT_PATH"
cd "$PROJECT_PATH" || exit 1

# Init Git
git init -b main > /dev/null 2>&1
git config --local user.email "$GIT_EMAIL"
git config --local user.name "$GIT_NAME"
git config --local pull.rebase false
git config --local push.default current
echo -e "${GREEN}✓${NC} Git initialized"

# SSH key (generate if needed)
SSH_KEY="$HOME/.ssh/id_ed25519"
if [ ! -f "$SSH_KEY" ]; then
    ssh-keygen -t ed25519 -C "$GIT_EMAIL" -f "$SSH_KEY" -N "" > /dev/null 2>&1
    eval "$(ssh-agent -s)" > /dev/null 2>&1
    ssh-add "$SSH_KEY" > /dev/null 2>&1
    echo -e "${GREEN}✓${NC} SSH key generated"
    echo -e "${YELLOW}⚠${NC}  Add to GitHub: https://github.com/settings/keys"
    cat "${SSH_KEY}.pub"
    echo ""
else
    ssh-add "$SSH_KEY" > /dev/null 2>&1
    echo -e "${GREEN}✓${NC} SSH key ready"
fi

# Create files
cat > .gitignore << 'EOF'
.DS_Store
node_modules/
__pycache__/
*.pyc
venv/
.env
dist/
build/
*.log
EOF

cat > README.md << EOF
# $PROJECT_NAME

## Quick Start

\`\`\`bash
git clone $REPO_URL
\`\`\`
EOF

echo -e "${GREEN}✓${NC} Files created"

# Remote
git remote add origin "$REPO_URL" > /dev/null 2>&1
echo -e "${GREEN}✓${NC} Remote added"

# Auto-push hook
mkdir -p .git/hooks
cat > .git/hooks/post-commit << 'HOOK'
#!/bin/bash
git push origin $(git rev-parse --abbrev-ref HEAD) 2>&1 | grep -E "✓|✗|error" || echo "⚠ Push pending"
HOOK
chmod +x .git/hooks/post-commit
echo -e "${GREEN}✓${NC} Auto-push enabled"

# Commit
git add . > /dev/null 2>&1
git commit -m "Initial commit" > /dev/null 2>&1
echo -e "${GREEN}✓${NC} Initial commit"

# Done
echo ""
echo -e "${GREEN}✅ Complete!${NC}"
echo ""
echo "📂 Location: $PROJECT_PATH"
echo "🔗 GitHub:   https://github.com/$GITHUB_USER/$PROJECT_NAME"
echo ""
echo -e "${YELLOW}Next:${NC}"
echo "1. Create repo: https://github.com/new (name: $PROJECT_NAME)"
echo "2. cd $PROJECT_PATH"
echo "3. git push -u origin main"
echo ""
