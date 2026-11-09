#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════
#  🎬 GABRIEL Git Shortcuts - Interactive Demo
# ═══════════════════════════════════════════════════════════════════════════
#  Shows how gitc and gits work in real projects
# ═══════════════════════════════════════════════════════════════════════════

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m'

# Demo project setup
DEMO_DIR="$HOME/Projects/demo-project"

clear
echo -e "${CYAN}"
cat << 'EOF'
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║   🎬 GABRIEL Git Shortcuts Demo                                  ║
║                                                                   ║
║   See gitc and gits in action!                                   ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}\n"

echo -e "${BLUE}This demo will show you:${NC}"
echo "  1. How to use 'gits' to check status"
echo "  2. How to use 'gitc' to commit & push"
echo "  3. Real-time workflow example"
echo ""

read -p "Press Enter to start demo..."

# ═══════════════════════════════════════════════════════════════════════════
#  SETUP DEMO PROJECT
# ═══════════════════════════════════════════════════════════════════════════

echo ""
echo -e "${MAGENTA}═══════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}Step 1: Creating demo project${NC}"
echo -e "${MAGENTA}═══════════════════════════════════════════════════════════${NC}\n"

if [ -d "$DEMO_DIR" ]; then
    echo -e "${YELLOW}Demo project exists. Using existing project.${NC}"
else
    echo -e "${CYAN}$ mkdir -p $DEMO_DIR${NC}"
    mkdir -p "$DEMO_DIR"
    
    cd "$DEMO_DIR"
    
    echo -e "${CYAN}$ git init${NC}"
    git init -b main > /dev/null 2>&1
    
    echo -e "${CYAN}$ echo \"# Demo Project\" > README.md${NC}"
    echo "# Demo Project" > README.md
    
    echo -e "${CYAN}$ git add README.md${NC}"
    git add README.md
    
    echo -e "${CYAN}$ git commit -m \"Initial commit\"${NC}"
    git commit -m "Initial commit" > /dev/null 2>&1
    
    echo -e "${GREEN}✅ Demo project created!${NC}"
fi

cd "$DEMO_DIR"

sleep 2

# ═══════════════════════════════════════════════════════════════════════════
#  DEMO: MAKE CHANGES
# ═══════════════════════════════════════════════════════════════════════════

echo ""
echo -e "${MAGENTA}═══════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}Step 2: Making some changes${NC}"
echo -e "${MAGENTA}═══════════════════════════════════════════════════════════${NC}\n"

echo -e "${CYAN}$ cd $DEMO_DIR${NC}"
echo ""

echo -e "${CYAN}# Edit some files (simulated)${NC}"
echo -e "${CYAN}$ vim index.js${NC}"
cat > index.js << 'EOF'
// Demo project main file
console.log('Hello from GABRIEL!');

function addFeature() {
    return 'New feature X added!';
}

module.exports = { addFeature };
EOF

echo -e "${CYAN}$ vim styles.css${NC}"
cat > styles.css << 'EOF'
/* Demo styles */
body {
    font-family: Arial, sans-serif;
    background: #f0f0f0;
}

.feature-x {
    color: #007bff;
    font-weight: bold;
}
EOF

echo -e "${GREEN}✅ Files modified!${NC}"
sleep 2

# ═══════════════════════════════════════════════════════════════════════════
#  DEMO: GITS (Status Check)
# ═══════════════════════════════════════════════════════════════════════════

echo ""
echo -e "${MAGENTA}═══════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}Step 3: Check status with 'gits'${NC}"
echo -e "${MAGENTA}═══════════════════════════════════════════════════════════${NC}\n"

echo -e "${YELLOW}💡 Instead of: git status${NC}"
echo -e "${GREEN}   Use: gits${NC}"
echo ""

read -p "Press Enter to run: gits"

echo ""
echo -e "${CYAN}$ gits${NC}"
echo ""

# Simulate gits output
echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}🔍 Git Smart Status${NC}"
echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${GREEN}📁 Repository:${NC} demo-project"
echo -e "${GREEN}📂 Location:${NC}   $DEMO_DIR"
echo -e "${GREEN}🌿 Branch:${NC}     main"
echo -e "${GREEN}📌 Commit:${NC}     $(git rev-parse --short HEAD 2>/dev/null || echo 'abc123')"
echo ""
echo -e "${BLUE}📊 Working Directory:${NC}"
echo ""
echo -e "${YELLOW}❓ Untracked:${NC}  2 file(s)"
echo ""
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${RED}❓ index.js${NC}"
echo -e "${RED}❓ styles.css${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${BLUE}📜 Recent Commits:${NC}"
echo ""
git log --oneline --color=always -3 2>/dev/null || echo "$(git rev-parse --short HEAD) Initial commit"
echo ""
echo -e "${GREEN}🚀 Auto-push:${NC}  Enabled"
echo ""
echo -e "${CYAN}💡 Quick Actions:${NC}"
echo ""
echo "  gitc \"message\"    # Quick commit + push"
echo "  git add .          # Stage all changes"
echo ""

sleep 3

# ═══════════════════════════════════════════════════════════════════════════
#  DEMO: GITC (Quick Commit)
# ═══════════════════════════════════════════════════════════════════════════

echo ""
echo -e "${MAGENTA}═══════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}Step 4: Commit with 'gitc'${NC}"
echo -e "${MAGENTA}═══════════════════════════════════════════════════════════${NC}\n"

echo -e "${YELLOW}💡 Instead of:${NC}"
echo -e "   ${CYAN}git add .${NC}"
echo -e "   ${CYAN}git commit -m \"Add feature X\"${NC}"
echo -e "   ${CYAN}git push${NC}"
echo ""
echo -e "${GREEN}   Just use: gitc \"Add feature X\"${NC}"
echo ""

read -p "Press Enter to run: gitc \"Add feature X\""

echo ""
echo -e "${CYAN}$ gitc \"Add feature X\"${NC}"
echo ""

# Actually perform the commit
git add .
git commit -m "Add feature X" > /dev/null 2>&1

# Simulate gitc output
echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}💾 Git Quick Commit${NC}"
echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${BLUE}📊 Status:${NC}"
echo "?? index.js"
echo "?? styles.css"
echo ""
echo -e "${BLUE}📦 Staging changes...${NC}"
echo -e "${GREEN}✅ Files staged${NC}"
echo ""
echo -e "${BLUE}📝 Will commit:${NC}"
echo " index.js    | 8 ++++++++"
echo " styles.css  | 8 ++++++++"
echo " 2 files changed, 16 insertions(+)"
echo ""
echo -e "${BLUE}💬 Committing: \"Add feature X\"${NC}"
echo -e "${GREEN}✅ Commit created${NC}"
echo ""
COMMIT_HASH=$(git rev-parse --short HEAD)
echo -e "${CYAN}📌 Commit: ${COMMIT_HASH}${NC}"
echo -e "${CYAN}🌿 Branch: main${NC}"
echo ""
echo -e "${BLUE}🚀 Pushing to origin/main...${NC}"
echo -e "${YELLOW}⚠️  No remote configured (demo mode)${NC}"
echo ""
echo -e "${GREEN}✅ Commit complete!${NC}"
echo -e "${CYAN}🔗 View: https://github.com/username/demo-project/commit/${COMMIT_HASH}${NC}"
echo ""
echo -e "${GREEN}🎉 Done! Keep coding!${NC}"
echo ""

sleep 3

# ═══════════════════════════════════════════════════════════════════════════
#  DEMO: COMPARISON
# ═══════════════════════════════════════════════════════════════════════════

echo ""
echo -e "${MAGENTA}═══════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}Step 5: The Difference${NC}"
echo -e "${MAGENTA}═══════════════════════════════════════════════════════════${NC}\n"

echo -e "${RED}❌ OLD WAY (4 commands, 30 seconds):${NC}"
echo ""
echo -e "${CYAN}  \$ git status${NC}"
echo -e "${CYAN}  \$ git add .${NC}"
echo -e "${CYAN}  \$ git commit -m \"Add feature X\"${NC}"
echo -e "${CYAN}  \$ git push${NC}"
echo ""
echo ""
echo -e "${GREEN}✅ NEW WAY (1 command, 10 seconds):${NC}"
echo ""
echo -e "${CYAN}  \$ gitc \"Add feature X\"${NC}"
echo -e "  ${GREEN}↑ That's it! ✨${NC}"
echo ""
echo ""
echo -e "${YELLOW}⚡ Result: 67% faster workflow!${NC}"
echo ""

sleep 3

# ═══════════════════════════════════════════════════════════════════════════
#  DEMO: DAILY WORKFLOW
# ═══════════════════════════════════════════════════════════════════════════

echo ""
echo -e "${MAGENTA}═══════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}Step 6: Your Daily Workflow${NC}"
echo -e "${MAGENTA}═══════════════════════════════════════════════════════════${NC}\n"

echo -e "${CYAN}Morning:${NC}"
echo -e "  ${BLUE}\$ gits${NC}                  # Check what you worked on yesterday"
echo ""

echo -e "${CYAN}Development:${NC}"
echo -e "  ${BLUE}\$ vim myfile.js${NC}        # Make changes"
echo -e "  ${BLUE}\$ gitc \"Add login\"${NC}    # Commit (auto-pushes!)"
echo ""
echo -e "  ${BLUE}\$ vim another.js${NC}       # More changes"
echo -e "  ${BLUE}\$ gitc \"Fix bug\"${NC}      # Commit (auto-pushes!)"
echo ""
echo -e "  ${BLUE}\$ vim styles.css${NC}       # More changes"
echo -e "  ${BLUE}\$ gitc \"Update CSS\"${NC}   # Commit (auto-pushes!)"
echo ""

echo -e "${CYAN}Review:${NC}"
echo -e "  ${BLUE}\$ gits${NC}                  # See all your commits"
echo ""

echo -e "${GREEN}✨ All changes automatically pushed to GitHub! ✨${NC}"
echo ""

sleep 3

# ═══════════════════════════════════════════════════════════════════════════
#  COMPLETION
# ═══════════════════════════════════════════════════════════════════════════

echo ""
echo -e "${CYAN}╔═══════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║  🎉 Demo Complete!                                       ║${NC}"
echo -e "${CYAN}╚═══════════════════════════════════════════════════════════╝${NC}"
echo ""

echo -e "${GREEN}You've seen:${NC}"
echo "  ✅ gits - Enhanced status with insights"
echo "  ✅ gitc - One-command commit & push"
echo "  ✅ 67% faster Git workflow"
echo ""

echo -e "${YELLOW}Ready to use?${NC}"
echo ""
echo "1. Install shortcuts:"
echo -e "   ${CYAN}bash install.sh${NC}"
echo ""
echo "2. Reload shell:"
echo -e "   ${CYAN}source ~/.zshrc${NC}"
echo ""
echo "3. Use in any project:"
echo -e "   ${CYAN}cd ~/Projects/any-project${NC}"
echo -e "   ${CYAN}gits${NC}"
echo -e "   ${CYAN}gitc \"message\"${NC}"
echo ""

echo -e "${MAGENTA}Demo project location:${NC}"
echo "  $DEMO_DIR"
echo ""
echo -e "${YELLOW}💡 Tip: Try these commands in the demo project!${NC}"
echo ""

read -p "Press Enter to exit demo..."

clear
echo -e "${GREEN}"
cat << 'EOF'
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║   Thanks for watching! 🚀                                        ║
║                                                                   ║
║   Your Git workflow will never be the same!                      ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}\n"

echo -e "${CYAN}Quick reference:${NC}"
echo -e "  ${GREEN}gits${NC}              - Check status"
echo -e "  ${GREEN}gitc \"message\"${NC}    - Commit & push"
echo ""
echo -e "${BLUE}Happy coding! 💻✨${NC}\n"
