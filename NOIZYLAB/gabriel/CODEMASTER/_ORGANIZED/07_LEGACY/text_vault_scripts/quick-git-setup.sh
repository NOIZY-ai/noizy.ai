#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════
#  🚀 QUICK GIT PROJECT SETUP
# ═══════════════════════════════════════════════════════════════════════════
#  Purpose: One-command project initialization with Git + SSH + Auto-push
#  Usage: quick-git-setup project-name [github-username]
# ═══════════════════════════════════════════════════════════════════════════

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# ═══════════════════════════════════════════════════════════════════════════
#  CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════

# Get project name from argument or prompt
PROJECT_NAME="$1"
GITHUB_USER="$2"

if [ -z "$PROJECT_NAME" ]; then
    echo -e "${CYAN}╔═══════════════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║  🚀 Quick Git Project Setup                              ║${NC}"
    echo -e "${CYAN}╚═══════════════════════════════════════════════════════════╝${NC}"
    echo ""
    read -p "Project name: " PROJECT_NAME
    
    if [ -z "$PROJECT_NAME" ]; then
        echo -e "${RED}❌ Project name required${NC}"
        exit 1
    fi
fi

# Sanitize project name (remove spaces, convert to lowercase)
PROJECT_NAME=$(echo "$PROJECT_NAME" | tr '[:upper:]' '[:lower:]' | tr ' ' '-')

# Default directories
PROJECTS_DIR="$HOME/Projects"
PROJECT_PATH="$PROJECTS_DIR/$PROJECT_NAME"

# ═══════════════════════════════════════════════════════════════════════════
#  SMART DEFAULTS FROM GIT CONFIG
# ═══════════════════════════════════════════════════════════════════════════

# Try to get Git user info from global config
GIT_EMAIL=$(git config --global user.email 2>/dev/null)
GIT_NAME=$(git config --global user.name 2>/dev/null)

# If not set globally, prompt
if [ -z "$GIT_EMAIL" ]; then
    read -p "Git email: " GIT_EMAIL
fi

if [ -z "$GIT_NAME" ]; then
    read -p "Git name: " GIT_NAME
fi

# Get GitHub username
if [ -z "$GITHUB_USER" ]; then
    # Try to infer from email or existing SSH key
    INFERRED_USER=$(echo "$GIT_EMAIL" | cut -d'@' -f1)
    read -p "GitHub username [$INFERRED_USER]: " INPUT_USER
    GITHUB_USER="${INPUT_USER:-$INFERRED_USER}"
fi

# Build repository URL
REPO_URL="git@github.com:${GITHUB_USER}/${PROJECT_NAME}.git"

# ═══════════════════════════════════════════════════════════════════════════
#  DISPLAY PLAN
# ═══════════════════════════════════════════════════════════════════════════

echo ""
echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}📋 Setup Plan:${NC}"
echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"
echo ""
echo "  📁 Project:     $PROJECT_NAME"
echo "  📂 Location:    $PROJECT_PATH"
echo "  👤 Name:        $GIT_NAME"
echo "  📧 Email:       $GIT_EMAIL"
echo "  🐙 GitHub:      $GITHUB_USER"
echo "  🔗 Repo:        $REPO_URL"
echo ""
echo -e "${YELLOW}Will create:${NC}"
echo "  • Project directory"
echo "  • Git repository (main branch)"
echo "  • SSH key (if needed)"
echo "  • Auto-push hook"
echo "  • Initial commit"
echo ""

read -p "Continue? [Y/n]: " CONFIRM
if [[ $CONFIRM =~ ^[Nn] ]]; then
    echo -e "${YELLOW}⏹️  Cancelled${NC}"
    exit 0
fi

# ═══════════════════════════════════════════════════════════════════════════
#  CREATE PROJECT
# ═══════════════════════════════════════════════════════════════════════════

echo ""
echo -e "${BLUE}🏗️  Creating project...${NC}"

# Create directory
if [ -d "$PROJECT_PATH" ]; then
    echo -e "${YELLOW}⚠️  Directory exists: $PROJECT_PATH${NC}"
    read -p "Use existing directory? [Y/n]: " USE_EXISTING
    if [[ $USE_EXISTING =~ ^[Nn] ]]; then
        exit 1
    fi
else
    mkdir -p "$PROJECT_PATH"
    echo -e "${GREEN}✅ Created: $PROJECT_PATH${NC}"
fi

cd "$PROJECT_PATH" || exit 1

# ═══════════════════════════════════════════════════════════════════════════
#  GIT INITIALIZATION
# ═══════════════════════════════════════════════════════════════════════════

echo -e "${BLUE}📦 Initializing Git...${NC}"

if [ -d ".git" ]; then
    echo -e "${YELLOW}⚠️  Git already initialized${NC}"
else
    git init -b main
    echo -e "${GREEN}✅ Git initialized${NC}"
fi

# Configure Git
git config --local user.email "$GIT_EMAIL"
git config --local user.name "$GIT_NAME"
git config --local pull.rebase false
git config --local push.default current
echo -e "${GREEN}✅ Git configured${NC}"

# ═══════════════════════════════════════════════════════════════════════════
#  SSH KEY SETUP
# ═══════════════════════════════════════════════════════════════════════════

SSH_KEY="$HOME/.ssh/id_ed25519"

if [ ! -f "$SSH_KEY" ]; then
    echo -e "${BLUE}🔑 Generating SSH key...${NC}"
    ssh-keygen -t ed25519 -C "$GIT_EMAIL" -f "$SSH_KEY" -N ""
    echo -e "${GREEN}✅ SSH key generated${NC}"
    
    # Add to agent
    eval "$(ssh-agent -s)" > /dev/null 2>&1
    ssh-add "$SSH_KEY" 2>/dev/null
    echo -e "${GREEN}✅ Added to ssh-agent${NC}"
    
    # Display public key
    echo ""
    echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}🔑 Your SSH Public Key (add to GitHub):${NC}"
    echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"
    cat "${SSH_KEY}.pub"
    echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"
    echo ""
    
    # Copy to clipboard
    if command -v pbcopy &> /dev/null; then
        cat "${SSH_KEY}.pub" | pbcopy
        echo -e "${GREEN}✅ Copied to clipboard!${NC}"
    elif command -v xclip &> /dev/null; then
        cat "${SSH_KEY}.pub" | xclip -selection clipboard
        echo -e "${GREEN}✅ Copied to clipboard!${NC}"
    elif command -v clip &> /dev/null; then
        cat "${SSH_KEY}.pub" | clip
        echo -e "${GREEN}✅ Copied to clipboard!${NC}"
    fi
    
    echo ""
    echo -e "${YELLOW}📝 Add SSH key to GitHub:${NC}"
    echo "   1. Go to: https://github.com/settings/keys"
    echo "   2. Click 'New SSH key'"
    echo "   3. Paste the key above"
    echo "   4. Click 'Add SSH key'"
    echo ""
    
    read -p "Press Enter after adding key to GitHub..."
    
else
    echo -e "${GREEN}✅ SSH key exists: $SSH_KEY${NC}"
    
    # Make sure it's in agent
    ssh-add "$SSH_KEY" 2>/dev/null
fi

# ═══════════════════════════════════════════════════════════════════════════
#  TEST SSH CONNECTION
# ═══════════════════════════════════════════════════════════════════════════

echo -e "${BLUE}🔌 Testing GitHub connection...${NC}"
if ssh -T git@github.com 2>&1 | grep -q "successfully authenticated"; then
    echo -e "${GREEN}✅ GitHub SSH connection works!${NC}"
else
    echo -e "${YELLOW}⚠️  SSH test inconclusive (may need to add key)${NC}"
fi

# ═══════════════════════════════════════════════════════════════════════════
#  CREATE INITIAL FILES
# ═══════════════════════════════════════════════════════════════════════════

echo -e "${BLUE}📄 Creating project files...${NC}"

# .gitignore
if [ ! -f ".gitignore" ]; then
    cat > .gitignore << 'GITIGNORE'
# OS files
.DS_Store
Thumbs.db
*.swp

# Dependencies
node_modules/
__pycache__/
*.pyc
venv/
env/

# Build outputs
dist/
build/
*.o
*.exe

# Environment
.env
.env.local

# IDE
.vscode/
.idea/
*.swp

# Logs
*.log
logs/
GITIGNORE
    echo -e "${GREEN}✅ Created .gitignore${NC}"
fi

# README.md
if [ ! -f "README.md" ]; then
    cat > README.md << README
# $PROJECT_NAME

Created: $(date +"%B %d, %Y")

## Description

Add your project description here.

## Installation

\`\`\`bash
git clone $REPO_URL
cd $PROJECT_NAME
\`\`\`

## Usage

\`\`\`bash
# Add usage instructions
\`\`\`

## License

MIT
README
    echo -e "${GREEN}✅ Created README.md${NC}"
fi

# ═══════════════════════════════════════════════════════════════════════════
#  ADD REMOTE
# ═══════════════════════════════════════════════════════════════════════════

echo -e "${BLUE}🔗 Adding remote repository...${NC}"

if git remote | grep -q "^origin$"; then
    echo -e "${YELLOW}⚠️  Remote 'origin' exists${NC}"
    git remote set-url origin "$REPO_URL"
    echo -e "${GREEN}✅ Updated remote URL${NC}"
else
    git remote add origin "$REPO_URL"
    echo -e "${GREEN}✅ Added remote: origin${NC}"
fi

# ═══════════════════════════════════════════════════════════════════════════
#  CREATE AUTO-PUSH HOOK
# ═══════════════════════════════════════════════════════════════════════════

echo -e "${BLUE}🪝 Creating auto-push hook...${NC}"

mkdir -p .git/hooks

cat > .git/hooks/post-commit << 'HOOK'
#!/bin/bash
# Auto-push hook - pushes to origin after every commit

BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "main")

echo "🚀 Auto-pushing to origin/$BRANCH..."

git push origin "$BRANCH" 2>&1

if [ $? -eq 0 ]; then
    echo "✅ Push successful"
else
    echo "⚠️  Push failed (check remote configuration)"
    echo "   Run manually: git push origin $BRANCH"
fi
HOOK

chmod +x .git/hooks/post-commit
echo -e "${GREEN}✅ Auto-push hook created${NC}"

# ═══════════════════════════════════════════════════════════════════════════
#  INITIAL COMMIT
# ═══════════════════════════════════════════════════════════════════════════

echo -e "${BLUE}📝 Creating initial commit...${NC}"

git add .
git commit -m "Initial commit" -m "Created with quick-git-setup" > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Initial commit created${NC}"
    
    # Push to GitHub
    echo -e "${BLUE}⬆️  Pushing to GitHub...${NC}"
    
    # Create repo on GitHub first (remind user)
    echo ""
    echo -e "${YELLOW}📝 Create repository on GitHub:${NC}"
    echo "   1. Go to: https://github.com/new"
    echo "   2. Name: $PROJECT_NAME"
    echo "   3. DO NOT initialize with README"
    echo "   4. Click 'Create repository'"
    echo ""
    
    read -p "Press Enter after creating GitHub repo..."
    
    # Push
    if git push -u origin main 2>&1; then
        echo -e "${GREEN}✅ Pushed to GitHub!${NC}"
    else
        echo -e "${YELLOW}⚠️  Push failed (repo may not exist yet)${NC}"
        echo "   Create repo at: https://github.com/new"
        echo "   Then run: git push -u origin main"
    fi
else
    echo -e "${YELLOW}⚠️  No files to commit${NC}"
fi

# ═══════════════════════════════════════════════════════════════════════════
#  SUCCESS SUMMARY
# ═══════════════════════════════════════════════════════════════════════════

echo ""
echo -e "${CYAN}╔═══════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║  🎉 Project Setup Complete!                              ║${NC}"
echo -e "${CYAN}╚═══════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${GREEN}✅ Project:${NC}      $PROJECT_NAME"
echo -e "${GREEN}✅ Location:${NC}    $PROJECT_PATH"
echo -e "${GREEN}✅ GitHub:${NC}      https://github.com/$GITHUB_USER/$PROJECT_NAME"
echo -e "${GREEN}✅ Auto-push:${NC}   Enabled (commits auto-push)"
echo ""
echo -e "${BLUE}📝 Next steps:${NC}"
echo "   cd $PROJECT_PATH"
echo "   # Start coding!"
echo "   git add ."
echo "   git commit -m \"Your message\""
echo "   # ✅ Auto-pushes to GitHub!"
echo ""
echo -e "${YELLOW}🔗 Quick links:${NC}"
echo "   Repo: https://github.com/$GITHUB_USER/$PROJECT_NAME"
echo "   Settings: https://github.com/$GITHUB_USER/$PROJECT_NAME/settings"
echo ""

# Open in browser (optional)
read -p "Open GitHub repo in browser? [Y/n]: " OPEN_BROWSER
if [[ ! $OPEN_BROWSER =~ ^[Nn] ]]; then
    if command -v open &> /dev/null; then
        open "https://github.com/$GITHUB_USER/$PROJECT_NAME"
    elif command -v xdg-open &> /dev/null; then
        xdg-open "https://github.com/$GITHUB_USER/$PROJECT_NAME"
    elif command -v start &> /dev/null; then
        start "https://github.com/$GITHUB_USER/$PROJECT_NAME"
    fi
fi

echo ""
echo -e "${GREEN}🚀 Happy coding!${NC}"
