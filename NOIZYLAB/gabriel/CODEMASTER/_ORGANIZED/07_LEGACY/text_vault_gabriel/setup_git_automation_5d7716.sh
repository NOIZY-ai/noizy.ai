#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════
#  🔧 GIT AUTOMATION SETUP SCRIPT v1.0
# ═══════════════════════════════════════════════════════════════════════════
#  Purpose: Initialize Git repo with SSH keys and auto-push hooks
#  Platform: macOS, Linux, Windows (Git Bash)
#  Created: November 11, 2025
#  Features: SSH key generation, GitHub/GitLab integration, auto-push hooks
# ═══════════════════════════════════════════════════════════════════════════

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m' # No Color

# Configuration (will be set interactively)
USER_EMAIL=""
USER_NAME=""
REPO_URL=""
DEFAULT_BRANCH="main"
SSH_KEY_TYPE="ed25519"
SSH_KEY_PATH="$HOME/.ssh/id_ed25519"

# ═══════════════════════════════════════════════════════════════════════════
#  BANNER
# ═══════════════════════════════════════════════════════════════════════════

print_banner() {
    clear
    echo -e "${CYAN}"
    cat << 'EOF'
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║   🔧 GIT AUTOMATION SETUP v1.0                                   ║
║                                                                   ║
║   Initialize • SSH Keys • Auto-Push • GitHub/GitLab              ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
EOF
    echo -e "${NC}"
}

# ═══════════════════════════════════════════════════════════════════════════
#  HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════

success() {
    echo -e "${GREEN}✅ $1${NC}"
}

error() {
    echo -e "${RED}❌ $1${NC}"
}

warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

section() {
    echo ""
    echo -e "${MAGENTA}╔═══════════════════════════════════════════════════════════╗${NC}"
    echo -e "${MAGENTA}║  $1${NC}"
    echo -e "${MAGENTA}╚═══════════════════════════════════════════════════════════╝${NC}"
}

# Detect OS
detect_os() {
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macOS"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "Linux"
    elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
        echo "Windows"
    else
        echo "Unknown"
    fi
}

# ═══════════════════════════════════════════════════════════════════════════
#  SYSTEM CHECKS
# ═══════════════════════════════════════════════════════════════════════════

check_prerequisites() {
    section "CHECKING SYSTEM REQUIREMENTS"
    
    OS=$(detect_os)
    info "Detected OS: $OS"
    
    # Check Git
    if command -v git &> /dev/null; then
        GIT_VERSION=$(git --version)
        success "Git installed: $GIT_VERSION"
    else
        error "Git not found!"
        echo ""
        info "Install Git:"
        case $OS in
            macOS)
                echo "  brew install git"
                ;;
            Linux)
                echo "  sudo apt install git  (Debian/Ubuntu)"
                echo "  sudo yum install git  (RHEL/CentOS)"
                ;;
            Windows)
                echo "  Download from: https://git-scm.com/download/win"
                ;;
        esac
        exit 1
    fi
    
    # Check SSH
    if command -v ssh &> /dev/null; then
        success "SSH available"
    else
        warning "SSH not found (unusual)"
    fi
    
    # Check if in a directory
    if [ ! -d "$(pwd)" ]; then
        error "Current directory invalid"
        exit 1
    fi
    
    success "All prerequisites met"
}

# ═══════════════════════════════════════════════════════════════════════════
#  USER INPUT
# ═══════════════════════════════════════════════════════════════════════════

get_user_input() {
    section "CONFIGURATION"
    
    # Email
    read -p "Enter your Git email: " USER_EMAIL
    if [ -z "$USER_EMAIL" ]; then
        error "Email required"
        exit 1
    fi
    
    # Name
    read -p "Enter your Git name: " USER_NAME
    if [ -z "$USER_NAME" ]; then
        error "Name required"
        exit 1
    fi
    
    # Repository URL
    echo ""
    info "Repository URL examples:"
    echo "  GitHub:  git@github.com:username/repo.git"
    echo "  GitLab:  git@gitlab.com:username/repo.git"
    echo "  Bitbucket: git@bitbucket.org:username/repo.git"
    echo ""
    read -p "Enter repository URL (or leave blank to skip): " REPO_URL
    
    # Branch name
    read -p "Default branch name [main]: " INPUT_BRANCH
    if [ -n "$INPUT_BRANCH" ]; then
        DEFAULT_BRANCH="$INPUT_BRANCH"
    fi
    
    # SSH key type
    echo ""
    info "SSH key types:"
    echo "  1. ed25519 (recommended, newer, faster)"
    echo "  2. rsa (traditional, 4096-bit)"
    read -p "Choose [1]: " KEY_CHOICE
    
    if [ "$KEY_CHOICE" = "2" ]; then
        SSH_KEY_TYPE="rsa"
        SSH_KEY_PATH="$HOME/.ssh/id_rsa"
    fi
    
    # Summary
    echo ""
    section "CONFIGURATION SUMMARY"
    echo "  Email:      $USER_EMAIL"
    echo "  Name:       $USER_NAME"
    echo "  Repository: ${REPO_URL:-"(none - local only)"}"
    echo "  Branch:     $DEFAULT_BRANCH"
    echo "  SSH Key:    $SSH_KEY_TYPE"
    echo ""
    
    read -p "Proceed with setup? [Y/n]: " CONFIRM
    if [[ $CONFIRM =~ ^[Nn] ]]; then
        warning "Setup cancelled"
        exit 0
    fi
}

# ═══════════════════════════════════════════════════════════════════════════
#  GIT INITIALIZATION
# ═══════════════════════════════════════════════════════════════════════════

initialize_git() {
    section "INITIALIZING GIT REPOSITORY"
    
    # Check if already a git repo
    if [ -d ".git" ]; then
        warning "Git repository already exists"
        read -p "Reinitialize? [y/N]: " REINIT
        if [[ ! $REINIT =~ ^[Yy] ]]; then
            info "Skipping git init"
            return
        fi
    fi
    
    # Initialize
    info "Running: git init"
    git init
    
    if [ $? -eq 0 ]; then
        success "Git repository initialized"
    else
        error "Git init failed"
        exit 1
    fi
    
    # Set default branch
    info "Setting default branch to: $DEFAULT_BRANCH"
    git config --local init.defaultBranch "$DEFAULT_BRANCH"
    
    # Rename current branch if needed
    CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null)
    if [ -n "$CURRENT_BRANCH" ] && [ "$CURRENT_BRANCH" != "$DEFAULT_BRANCH" ]; then
        git branch -m "$DEFAULT_BRANCH"
        success "Branch renamed to: $DEFAULT_BRANCH"
    fi
}

# ═══════════════════════════════════════════════════════════════════════════
#  GIT CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════

configure_git() {
    section "CONFIGURING GIT"
    
    # Set user email
    info "Setting user.email: $USER_EMAIL"
    git config --local user.email "$USER_EMAIL"
    
    # Set user name
    info "Setting user.name: $USER_NAME"
    git config --local user.name "$USER_NAME"
    
    # Set pull strategy (avoid warnings)
    git config --local pull.rebase false
    
    # Set push default
    git config --local push.default current
    
    success "Git configuration complete"
    
    # Show config
    echo ""
    info "Local configuration:"
    git config --local --list | grep -E "(user\.|pull\.|push\.)"
}

# ═══════════════════════════════════════════════════════════════════════════
#  SSH KEY MANAGEMENT
# ═══════════════════════════════════════════════════════════════════════════

generate_ssh_key() {
    section "CONFIGURING SSH KEYS"
    
    # Check if key exists
    if [ -f "$SSH_KEY_PATH" ]; then
        warning "SSH key already exists: $SSH_KEY_PATH"
        read -p "Generate new key (will backup old)? [y/N]: " GENERATE_NEW
        
        if [[ $GENERATE_NEW =~ ^[Yy] ]]; then
            # Backup existing key
            BACKUP_PATH="${SSH_KEY_PATH}.backup.$(date +%Y%m%d_%H%M%S)"
            cp "$SSH_KEY_PATH" "$BACKUP_PATH"
            cp "${SSH_KEY_PATH}.pub" "${BACKUP_PATH}.pub"
            info "Backed up existing key to: $BACKUP_PATH"
        else
            info "Using existing SSH key"
            return
        fi
    fi
    
    # Generate key
    info "Generating $SSH_KEY_TYPE SSH key..."
    
    # Create .ssh directory if needed
    mkdir -p "$HOME/.ssh"
    chmod 700 "$HOME/.ssh"
    
    # Generate key based on type
    if [ "$SSH_KEY_TYPE" = "ed25519" ]; then
        ssh-keygen -t ed25519 -C "$USER_EMAIL" -f "$SSH_KEY_PATH" -N ""
    else
        ssh-keygen -t rsa -b 4096 -C "$USER_EMAIL" -f "$SSH_KEY_PATH" -N ""
    fi
    
    if [ $? -eq 0 ]; then
        success "SSH key generated: $SSH_KEY_PATH"
        chmod 600 "$SSH_KEY_PATH"
        chmod 644 "${SSH_KEY_PATH}.pub"
    else
        error "SSH key generation failed"
        exit 1
    fi
}

add_ssh_key_to_agent() {
    info "Adding SSH key to agent..."
    
    # Start ssh-agent if not running
    if [ -z "$SSH_AUTH_SOCK" ]; then
        eval "$(ssh-agent -s)" > /dev/null
    fi
    
    # Add key
    ssh-add "$SSH_KEY_PATH" 2>/dev/null
    
    if [ $? -eq 0 ]; then
        success "SSH key added to agent"
    else
        warning "Could not add key to agent (may need to run manually)"
    fi
    
    # Configure SSH config for auto-loading (macOS)
    if [ "$(detect_os)" = "macOS" ]; then
        SSH_CONFIG="$HOME/.ssh/config"
        if [ ! -f "$SSH_CONFIG" ] || ! grep -q "UseKeychain yes" "$SSH_CONFIG"; then
            info "Updating SSH config for keychain..."
            cat >> "$SSH_CONFIG" << SSHEOF

# Auto-load SSH keys (macOS)
Host *
    AddKeysToAgent yes
    UseKeychain yes
    IdentityFile $SSH_KEY_PATH
SSHEOF
            success "SSH config updated"
        fi
    fi
}

display_public_key() {
    section "SSH PUBLIC KEY"
    
    echo ""
    echo -e "${GREEN}Copy this public key to GitHub/GitLab/Bitbucket:${NC}"
    echo ""
    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    cat "${SSH_KEY_PATH}.pub"
    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    
    info "Instructions:"
    echo ""
    echo "  GitHub:"
    echo "    1. Go to: https://github.com/settings/keys"
    echo "    2. Click 'New SSH key'"
    echo "    3. Paste the key above"
    echo ""
    echo "  GitLab:"
    echo "    1. Go to: https://gitlab.com/-/profile/keys"
    echo "    2. Paste the key above"
    echo ""
    echo "  Bitbucket:"
    echo "    1. Go to: https://bitbucket.org/account/settings/ssh-keys/"
    echo "    2. Click 'Add key'"
    echo "    3. Paste the key above"
    echo ""
    
    # Copy to clipboard if possible
    OS=$(detect_os)
    case $OS in
        macOS)
            if command -v pbcopy &> /dev/null; then
                cat "${SSH_KEY_PATH}.pub" | pbcopy
                success "Key copied to clipboard!"
            fi
            ;;
        Linux)
            if command -v xclip &> /dev/null; then
                cat "${SSH_KEY_PATH}.pub" | xclip -selection clipboard
                success "Key copied to clipboard!"
            elif command -v xsel &> /dev/null; then
                cat "${SSH_KEY_PATH}.pub" | xsel --clipboard
                success "Key copied to clipboard!"
            fi
            ;;
        Windows)
            if command -v clip &> /dev/null; then
                cat "${SSH_KEY_PATH}.pub" | clip
                success "Key copied to clipboard!"
            fi
            ;;
    esac
    
    read -p "Press Enter after adding key to GitHub/GitLab..."
}

test_ssh_connection() {
    section "TESTING SSH CONNECTION"
    
    if [ -z "$REPO_URL" ]; then
        info "No repository URL provided, skipping test"
        return
    fi
    
    # Extract host from URL
    HOST=$(echo "$REPO_URL" | sed -E 's/.*@([^:]+).*/\1/')
    
    info "Testing connection to: $HOST"
    
    # Test based on host
    case $HOST in
        *github.com*)
            info "Running: ssh -T git@github.com"
            ssh -T git@github.com 2>&1 | head -n 1
            ;;
        *gitlab.com*)
            info "Running: ssh -T git@gitlab.com"
            ssh -T git@gitlab.com 2>&1 | head -n 1
            ;;
        *bitbucket.org*)
            info "Running: ssh -T git@bitbucket.org"
            ssh -T git@bitbucket.org 2>&1 | head -n 1
            ;;
        *)
            info "Running: ssh -T git@$HOST"
            ssh -T "git@$HOST" 2>&1 | head -n 1
            ;;
    esac
    
    success "SSH test complete (you may see 'Permission denied' - this is normal if key not added yet)"
}

# ═══════════════════════════════════════════════════════════════════════════
#  REMOTE REPOSITORY
# ═══════════════════════════════════════════════════════════════════════════

add_remote() {
    section "ADDING REMOTE REPOSITORY"
    
    if [ -z "$REPO_URL" ]; then
        info "No repository URL provided, skipping"
        return
    fi
    
    # Check if origin exists
    if git remote | grep -q "^origin$"; then
        warning "Remote 'origin' already exists"
        EXISTING_URL=$(git remote get-url origin)
        echo "  Current: $EXISTING_URL"
        echo "  New:     $REPO_URL"
        
        if [ "$EXISTING_URL" = "$REPO_URL" ]; then
            info "URLs match, no change needed"
            return
        fi
        
        read -p "Update remote URL? [y/N]: " UPDATE_REMOTE
        if [[ $UPDATE_REMOTE =~ ^[Yy] ]]; then
            git remote set-url origin "$REPO_URL"
            success "Remote URL updated"
        else
            info "Keeping existing remote"
        fi
    else
        info "Adding remote: $REPO_URL"
        git remote add origin "$REPO_URL"
        
        if [ $? -eq 0 ]; then
            success "Remote 'origin' added"
        else
            error "Failed to add remote"
        fi
    fi
    
    # Show remotes
    echo ""
    info "Configured remotes:"
    git remote -v
}

# ═══════════════════════════════════════════════════════════════════════════
#  AUTO-PUSH HOOK
# ═══════════════════════════════════════════════════════════════════════════

create_auto_push_hook() {
    section "CREATING AUTO-PUSH HOOK"
    
    if [ -z "$REPO_URL" ]; then
        warning "No remote repository configured"
        info "Auto-push requires a remote repository"
        read -p "Create hook anyway? [y/N]: " CREATE_ANYWAY
        if [[ ! $CREATE_ANYWAY =~ ^[Yy] ]]; then
            info "Skipping auto-push hook"
            return
        fi
    fi
    
    HOOK_FILE=".git/hooks/post-commit"
    
    if [ -f "$HOOK_FILE" ]; then
        warning "Post-commit hook already exists"
        read -p "Overwrite? [y/N]: " OVERWRITE
        if [[ ! $OVERWRITE =~ ^[Yy] ]]; then
            info "Keeping existing hook"
            return
        fi
    fi
    
    info "Creating post-commit hook..."
    
    # Create hook
    cat > "$HOOK_FILE" << 'HOOKEOF'
#!/bin/bash
# Auto-push hook - pushes to origin after every commit

BRANCH=$(git rev-parse --abbrev-ref HEAD)

echo "🚀 Auto-pushing to origin/$BRANCH..."

# Push to origin
git push origin "$BRANCH" 2>&1

if [ $? -eq 0 ]; then
    echo "✅ Push successful"
else
    echo "⚠️  Push failed (check remote configuration)"
fi
HOOKEOF
    
    # Make executable
    chmod +x "$HOOK_FILE"
    
    success "Auto-push hook created"
    info "Every commit will now auto-push to origin/$DEFAULT_BRANCH"
    
    # Warning
    echo ""
    warning "IMPORTANT:"
    echo "  • Commits will automatically push to remote"
    echo "  • Requires valid SSH key and remote access"
    echo "  • May fail if remote is ahead of local"
    echo "  • To disable: rm .git/hooks/post-commit"
}

# ═══════════════════════════════════════════════════════════════════════════
#  INITIAL COMMIT
# ═══════════════════════════════════════════════════════════════════════════

create_initial_commit() {
    section "CREATING INITIAL COMMIT"
    
    read -p "Create initial commit? [Y/n]: " DO_COMMIT
    if [[ $DO_COMMIT =~ ^[Nn] ]]; then
        info "Skipping initial commit"
        return
    fi
    
    # Create .gitignore if doesn't exist
    if [ ! -f ".gitignore" ]; then
        info "Creating .gitignore..."
        cat > .gitignore << 'IGNOREEOF'
# OS files
.DS_Store
Thumbs.db

# Editor files
.vscode/
.idea/
*.swp
*.swo

# Logs
*.log
logs/

# Dependencies
node_modules/
__pycache__/
*.pyc

# Environment
.env
.env.local

# Build outputs
dist/
build/
*.o
*.exe
IGNOREEOF
        success "Created .gitignore"
    fi
    
    # Create README if doesn't exist
    if [ ! -f "README.md" ]; then
        info "Creating README.md..."
        cat > README.md << READMEEOF
# Project

Created: $(date +"%Y-%m-%d")

## Setup

\`\`\`bash
git clone $REPO_URL
\`\`\`

## Description

Add your project description here.
READMEEOF
        success "Created README.md"
    fi
    
    # Add files
    info "Staging files..."
    git add .
    
    # Commit
    info "Creating commit..."
    git commit -m "Initial commit" -m "Initialized with git-setup script"
    
    if [ $? -eq 0 ]; then
        success "Initial commit created"
        
        # Push if remote exists
        if [ -n "$REPO_URL" ]; then
            read -p "Push to remote? [Y/n]: " DO_PUSH
            if [[ ! $DO_PUSH =~ ^[Nn] ]]; then
                info "Pushing to origin/$DEFAULT_BRANCH..."
                git push -u origin "$DEFAULT_BRANCH"
                
                if [ $? -eq 0 ]; then
                    success "Pushed to remote"
                else
                    warning "Push failed (may need to add SSH key first)"
                fi
            fi
        fi
    else
        warning "Commit failed (no changes?)"
    fi
}

# ═══════════════════════════════════════════════════════════════════════════
#  SUMMARY
# ═══════════════════════════════════════════════════════════════════════════

show_summary() {
    section "SETUP COMPLETE!"
    
    echo ""
    echo -e "${CYAN}╔═══════════════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║  Git Repository Configuration Summary                     ║${NC}"
    echo -e "${CYAN}╚═══════════════════════════════════════════════════════════╝${NC}"
    echo ""
    
    # Git status
    echo -e "${GREEN}📁 Repository:${NC}"
    echo "   Location: $(pwd)"
    echo "   Branch: $(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo 'none')"
    echo ""
    
    # Config
    echo -e "${GREEN}⚙️  Configuration:${NC}"
    echo "   User: $USER_NAME <$USER_EMAIL>"
    if [ -n "$REPO_URL" ]; then
        echo "   Remote: $REPO_URL"
    else
        echo "   Remote: (none - local only)"
    fi
    echo ""
    
    # SSH
    echo -e "${GREEN}🔑 SSH Key:${NC}"
    echo "   Type: $SSH_KEY_TYPE"
    echo "   Path: $SSH_KEY_PATH"
    if [ -f "${SSH_KEY_PATH}.pub" ]; then
        echo "   Fingerprint: $(ssh-keygen -lf "${SSH_KEY_PATH}.pub" | awk '{print $2}')"
    fi
    echo ""
    
    # Hooks
    echo -e "${GREEN}🪝 Git Hooks:${NC}"
    if [ -f ".git/hooks/post-commit" ]; then
        echo "   ✅ Auto-push: Enabled"
    else
        echo "   ❌ Auto-push: Disabled"
    fi
    echo ""
    
    # Quick commands
    echo -e "${GREEN}📝 Quick Commands:${NC}"
    echo "   git status              # Check status"
    echo "   git add .               # Stage all changes"
    echo "   git commit -m 'msg'     # Commit (auto-pushes)"
    echo "   git push                # Manual push"
    echo "   git pull                # Pull changes"
    echo "   git log --oneline       # View history"
    echo ""
    
    # Next steps
    echo -e "${YELLOW}📌 Next Steps:${NC}"
    if [ ! -f "${SSH_KEY_PATH}.pub" ]; then
        echo "   1. ❌ Add SSH key to GitHub/GitLab"
    else
        echo "   1. ✅ SSH key ready"
    fi
    echo "   2. Start coding!"
    echo "   3. Use 'git add' and 'git commit'"
    echo "   4. Changes auto-push to remote"
    echo ""
    
    success "Setup complete! Happy coding! 🚀"
}

# ═══════════════════════════════════════════════════════════════════════════
#  MAIN MENU
# ═══════════════════════════════════════════════════════════════════════════

show_menu() {
    print_banner
    echo -e "${CYAN}Select setup mode:${NC}"
    echo ""
    echo "  1. Full Setup (Recommended)"
    echo "     - Initialize Git"
    echo "     - Generate SSH keys"
    echo "     - Add remote repository"
    echo "     - Create auto-push hook"
    echo "     - Initial commit"
    echo ""
    echo "  2. Quick Setup (Existing repo)"
    echo "     - Configure Git"
    echo "     - SSH keys only"
    echo ""
    echo "  3. SSH Keys Only"
    echo "     - Generate/manage SSH keys"
    echo ""
    echo "  4. Auto-Push Hook Only"
    echo "     - Add post-commit hook"
    echo ""
    echo "  5. Custom Setup"
    echo "     - Pick individual steps"
    echo ""
    echo "  9. Exit"
    echo ""
}

# ═══════════════════════════════════════════════════════════════════════════
#  MAIN EXECUTION
# ═══════════════════════════════════════════════════════════════════════════

main() {
    # Check if running with arguments (non-interactive)
    if [ "$1" = "--auto" ]; then
        print_banner
        check_prerequisites
        get_user_input
        initialize_git
        configure_git
        generate_ssh_key
        add_ssh_key_to_agent
        display_public_key
        test_ssh_connection
        add_remote
        create_auto_push_hook
        create_initial_commit
        show_summary
        exit 0
    fi
    
    # Interactive menu
    while true; do
        show_menu
        read -p "Enter choice [1-5, 9]: " choice
        
        case $choice in
            1)
                print_banner
                check_prerequisites
                get_user_input
                initialize_git
                configure_git
                generate_ssh_key
                add_ssh_key_to_agent
                display_public_key
                test_ssh_connection
                add_remote
                create_auto_push_hook
                create_initial_commit
                show_summary
                exit 0
                ;;
            2)
                print_banner
                check_prerequisites
                get_user_input
                configure_git
                generate_ssh_key
                add_ssh_key_to_agent
                display_public_key
                test_ssh_connection
                show_summary
                exit 0
                ;;
            3)
                print_banner
                check_prerequisites
                read -p "Enter your email: " USER_EMAIL
                generate_ssh_key
                add_ssh_key_to_agent
                display_public_key
                test_ssh_connection
                exit 0
                ;;
            4)
                print_banner
                check_prerequisites
                create_auto_push_hook
                success "Hook created"
                exit 0
                ;;
            5)
                print_banner
                check_prerequisites
                get_user_input
                
                read -p "Initialize Git? [Y/n]: " DO_INIT
                [[ ! $DO_INIT =~ ^[Nn] ]] && initialize_git
                
                read -p "Configure Git? [Y/n]: " DO_CONFIG
                [[ ! $DO_CONFIG =~ ^[Nn] ]] && configure_git
                
                read -p "Generate SSH keys? [Y/n]: " DO_SSH
                if [[ ! $DO_SSH =~ ^[Nn] ]]; then
                    generate_ssh_key
                    add_ssh_key_to_agent
                    display_public_key
                    test_ssh_connection
                fi
                
                read -p "Add remote? [Y/n]: " DO_REMOTE
                [[ ! $DO_REMOTE =~ ^[Nn] ]] && add_remote
                
                read -p "Create auto-push hook? [Y/n]: " DO_HOOK
                [[ ! $DO_HOOK =~ ^[Nn] ]] && create_auto_push_hook
                
                read -p "Create initial commit? [Y/n]: " DO_COMMIT
                [[ ! $DO_COMMIT =~ ^[Nn] ]] && create_initial_commit
                
                show_summary
                exit 0
                ;;
            9)
                echo ""
                info "Goodbye!"
                exit 0
                ;;
            *)
                error "Invalid option: $choice"
                sleep 2
                ;;
        esac
    done
}

# Run main
main "$@"
