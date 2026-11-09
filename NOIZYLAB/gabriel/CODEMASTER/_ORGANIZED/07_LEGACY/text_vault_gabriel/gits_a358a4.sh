#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════
#  🔍 GIT SMART STATUS - Enhanced git status with insights
# ═══════════════════════════════════════════════════════════════════════════
#  Usage: gits
# ═══════════════════════════════════════════════════════════════════════════

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m'

# Check if in git repo
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo -e "${RED}❌ Not a git repository${NC}"
    exit 1
fi

# Banner
echo ""
echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}🔍 Git Smart Status${NC}"
echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"
echo ""

# Repository info
REPO_ROOT=$(git rev-parse --show-toplevel)
REPO_NAME=$(basename "$REPO_ROOT")
BRANCH=$(git rev-parse --abbrev-ref HEAD)
COMMIT_HASH=$(git rev-parse --short HEAD 2>/dev/null || echo "none")

echo -e "${GREEN}📁 Repository:${NC} $REPO_NAME"
echo -e "${GREEN}📂 Location:${NC}   $REPO_ROOT"
echo -e "${GREEN}🌿 Branch:${NC}     $BRANCH"
echo -e "${GREEN}📌 Commit:${NC}     $COMMIT_HASH"
echo ""

# Remote info
if git remote -v | grep -q "origin"; then
    REMOTE_URL=$(git config --get remote.origin.url)
    echo -e "${GREEN}🔗 Remote:${NC}     $REMOTE_URL"
    
    # Check if ahead/behind
    git fetch origin "$BRANCH" 2>/dev/null
    AHEAD=$(git rev-list --count origin/"$BRANCH"..HEAD 2>/dev/null || echo "0")
    BEHIND=$(git rev-list --count HEAD..origin/"$BRANCH" 2>/dev/null || echo "0")
    
    if [ "$AHEAD" -gt 0 ] || [ "$BEHIND" -gt 0 ]; then
        echo -e "${YELLOW}📊 Sync:${NC}       "
        [ "$AHEAD" -gt 0 ] && echo -e "   ${GREEN}↑${NC} Ahead by $AHEAD commit(s)"
        [ "$BEHIND" -gt 0 ] && echo -e "   ${RED}↓${NC} Behind by $BEHIND commit(s)"
    else
        echo -e "${GREEN}✅ Sync:${NC}       Up to date with origin"
    fi
    echo ""
fi

# File status
echo -e "${BLUE}📊 Working Directory:${NC}"
echo ""

STATUS_OUTPUT=$(git status --porcelain)

if [ -z "$STATUS_OUTPUT" ]; then
    echo -e "${GREEN}✨ Working directory clean${NC}"
else
    # Count file types
    STAGED=$(echo "$STATUS_OUTPUT" | grep -c "^[MARC]")
    MODIFIED=$(echo "$STATUS_OUTPUT" | grep -c "^ M")
    UNTRACKED=$(echo "$STATUS_OUTPUT" | grep -c "^??")
    DELETED=$(echo "$STATUS_OUTPUT" | grep -c "^ D")
    
    [ "$STAGED" -gt 0 ] && echo -e "${GREEN}✅ Staged:${NC}     $STAGED file(s)"
    [ "$MODIFIED" -gt 0 ] && echo -e "${YELLOW}📝 Modified:${NC}   $MODIFIED file(s)"
    [ "$UNTRACKED" -gt 0 ] && echo -e "${RED}❓ Untracked:${NC}  $UNTRACKED file(s)"
    [ "$DELETED" -gt 0 ] && echo -e "${RED}🗑️  Deleted:${NC}    $DELETED file(s)"
    
    echo ""
    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    
    # Show detailed status with colors
    git status --short | while IFS= read -r line; do
        STATUS="${line:0:2}"
        FILE="${line:3}"
        
        case "$STATUS" in
            "M "*)
                echo -e "${GREEN}✅ $FILE${NC}"
                ;;
            " M"*)
                echo -e "${YELLOW}📝 $FILE${NC}"
                ;;
            "??")
                echo -e "${RED}❓ $FILE${NC}"
                ;;
            " D"*)
                echo -e "${RED}🗑️  $FILE${NC}"
                ;;
            "A "*)
                echo -e "${GREEN}➕ $FILE${NC}"
                ;;
            *)
                echo "$line"
                ;;
        esac
    done
    
    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
fi

echo ""

# Recent commits
echo -e "${BLUE}📜 Recent Commits:${NC}"
echo ""
git log --oneline --decorate --color=always -5

echo ""

# Auto-push status
if [ -f ".git/hooks/post-commit" ]; then
    echo -e "${GREEN}🚀 Auto-push:${NC}  Enabled"
else
    echo -e "${YELLOW}⚠️  Auto-push:${NC}  Disabled"
fi

echo ""

# Quick actions
if [ -n "$STATUS_OUTPUT" ]; then
    echo -e "${CYAN}💡 Quick Actions:${NC}"
    echo ""
    echo "  gitc \"message\"    # Quick commit + push"
    echo "  git add .          # Stage all changes"
    echo "  git diff           # View changes"
    echo "  git restore <file> # Discard changes"
    echo ""
fi
