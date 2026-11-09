#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════
#  💾 GIT QUICK COMMIT - Smart commit with auto-push
# ═══════════════════════════════════════════════════════════════════════════
#  Usage: gitc "commit message"
#  Alias: gc "message"
# ═══════════════════════════════════════════════════════════════════════════

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m'

# Get commit message
COMMIT_MSG="$*"

if [ -z "$COMMIT_MSG" ]; then
    echo -e "${RED}❌ Commit message required${NC}"
    echo ""
    echo "Usage: gitc \"Your commit message\""
    echo ""
    echo "Examples:"
    echo "  gitc \"Add feature X\""
    echo "  gitc \"Fix bug in login\""
    echo "  gitc \"Update README\""
    exit 1
fi

# Check if in git repo
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo -e "${RED}❌ Not a git repository${NC}"
    exit 1
fi

# Banner
echo ""
echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}💾 Git Quick Commit${NC}"
echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"
echo ""

# Show status
echo -e "${BLUE}📊 Status:${NC}"
git status --short
echo ""

# Stage all changes
echo -e "${BLUE}📦 Staging changes...${NC}"
git add .

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Files staged${NC}"
else
    echo -e "${RED}❌ Failed to stage files${NC}"
    exit 1
fi

# Check if anything to commit
if git diff --cached --quiet; then
    echo -e "${YELLOW}⚠️  No changes to commit${NC}"
    exit 0
fi

# Show what will be committed
echo ""
echo -e "${BLUE}📝 Will commit:${NC}"
git diff --cached --stat
echo ""

# Commit
echo -e "${BLUE}💬 Committing: \"${COMMIT_MSG}\"${NC}"
git commit -m "$COMMIT_MSG"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Commit created${NC}"
    
    # Show commit info
    COMMIT_HASH=$(git rev-parse --short HEAD)
    BRANCH=$(git rev-parse --abbrev-ref HEAD)
    echo ""
    echo -e "${CYAN}📌 Commit: ${COMMIT_HASH}${NC}"
    echo -e "${CYAN}🌿 Branch: ${BRANCH}${NC}"
    
    # Auto-push (if hook exists, it will push)
    # But we'll also try manual push for immediate feedback
    echo ""
    echo -e "${BLUE}🚀 Pushing to origin/${BRANCH}...${NC}"
    
    git push origin "$BRANCH" 2>&1 | while IFS= read -r line; do
        if echo "$line" | grep -q "Everything up-to-date"; then
            echo -e "${GREEN}✅ Already up to date${NC}"
        elif echo "$line" | grep -q "100%"; then
            echo -e "${GREEN}✅ Push complete${NC}"
        elif echo "$line" | grep -q "Writing objects"; then
            echo -e "${CYAN}📤 Uploading...${NC}"
        elif echo "$line" | grep -qi "error\|failed\|rejected"; then
            echo -e "${RED}❌ $line${NC}"
        else
            echo "$line"
        fi
    done
    
    if [ ${PIPESTATUS[0]} -eq 0 ]; then
        echo ""
        echo -e "${GREEN}✅ Successfully pushed to GitHub!${NC}"
        
        # Show remote URL
        REMOTE_URL=$(git config --get remote.origin.url)
        if [[ $REMOTE_URL == git@github.com:* ]]; then
            # Extract owner/repo from SSH URL
            REPO_PATH=$(echo "$REMOTE_URL" | sed 's/git@github.com://; s/.git$//')
            GITHUB_URL="https://github.com/${REPO_PATH}/commit/${COMMIT_HASH}"
            echo -e "${CYAN}🔗 View: ${GITHUB_URL}${NC}"
        fi
    else
        echo ""
        echo -e "${YELLOW}⚠️  Push failed (hook may retry)${NC}"
        echo -e "${CYAN}💡 Try: git push origin ${BRANCH}${NC}"
    fi
    
    echo ""
    echo -e "${GREEN}🎉 Done! Keep coding!${NC}"
    echo ""
else
    echo -e "${RED}❌ Commit failed${NC}"
    exit 1
fi
