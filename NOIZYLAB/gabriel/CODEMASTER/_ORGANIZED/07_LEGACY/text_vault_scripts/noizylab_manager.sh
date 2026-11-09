#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════════════════════
# NOIZYLAB MANAGER - For Noizyfish + NOIZYLAB-io
# ═══════════════════════════════════════════════════════════════════════════════
# 
# What it does:
#   1. Lists all your repos and collaborators
#   2. Transfers repos to NOIZYLAB-io org
#   3. Removes unwanted collaborators
#   4. Audits org members
#
# Usage:
#   chmod +x noizylab_manager.sh
#   ./noizylab_manager.sh
#
# ═══════════════════════════════════════════════════════════════════════════════

set -euo pipefail

# ───────────────────────────────────────────────────────────────────────────────
# CONFIG
# ───────────────────────────────────────────────────────────────────────────────
GITHUB_USER="Noizyfish"
GITHUB_ORG="NOIZYLAB-io"
PROTECTED_USER="Noizyfish"

# ───────────────────────────────────────────────────────────────────────────────
# TOKEN SETUP
# ───────────────────────────────────────────────────────────────────────────────
if [ -z "${GH_TOKEN:-}" ]; then
    # Try keychain
    GH_TOKEN=$(security find-generic-password -a "noizylab" -s "gh_token" -w 2>/dev/null || echo "")
fi

if [ -z "$GH_TOKEN" ]; then
    echo "Enter your GitHub token (ghp_...):"
    read -s GH_TOKEN
    export GH_TOKEN
fi

# ───────────────────────────────────────────────────────────────────────────────
# FUNCTIONS
# ───────────────────────────────────────────────────────────────────────────────
api() {
    curl -s -H "Authorization: token $GH_TOKEN" -H "Accept: application/vnd.github+json" "$@"
}

show_menu() {
    echo ""
    echo "═══════════════════════════════════════════════════════════"
    echo "NOIZYLAB MANAGER"
    echo "═══════════════════════════════════════════════════════════"
    echo ""
    echo "  1) List my repos (Noizyfish)"
    echo "  2) List org repos (NOIZYLAB-io)"
    echo "  3) Check repo collaborators"
    echo "  4) Transfer repo to NOIZYLAB-io"
    echo "  5) Transfer ALL repos to NOIZYLAB-io"
    echo "  6) Remove collaborator from repo"
    echo "  7) List org members (NOIZYLAB-io)"
    echo "  8) Audit everything"
    echo "  9) Exit"
    echo ""
    read -p "Choose [1-9]: " choice
    echo ""
}

list_user_repos() {
    echo "═══ Repos under $GITHUB_USER ═══"
    api "https://api.github.com/users/$GITHUB_USER/repos?per_page=100" | \
        grep -E '"full_name"' | sed 's/.*: "//;s/".*//' | while read repo; do
        echo "  📁 $repo"
    done
}

list_org_repos() {
    echo "═══ Repos under $GITHUB_ORG ═══"
    result=$(api "https://api.github.com/orgs/$GITHUB_ORG/repos?per_page=100")
    if echo "$result" | grep -q '"full_name"'; then
        echo "$result" | grep -E '"full_name"' | sed 's/.*: "//;s/".*//' | while read repo; do
            echo "  📁 $repo"
        done
    else
        echo "  (no repos yet)"
    fi
}

check_collaborators() {
    read -p "Repo name (e.g., NOIZYLAB): " repo
    read -p "Owner (Noizyfish or NOIZYLAB-io): " owner
    echo ""
    echo "═══ Collaborators on $owner/$repo ═══"
    api "https://api.github.com/repos/$owner/$repo/collaborators" | \
        grep -E '"login"' | sed 's/.*: "//;s/".*//' | while read user; do
        if [ "$user" = "$PROTECTED_USER" ]; then
            echo "  ✅ $user (PROTECTED)"
        else
            echo "  ⚠️  $user"
        fi
    done
}

transfer_repo() {
    read -p "Repo to transfer (e.g., NOIZYLAB): " repo
    echo ""
    echo "Transferring $GITHUB_USER/$repo → $GITHUB_ORG/$repo"
    read -p "Confirm? (yes/no): " confirm
    if [ "$confirm" = "yes" ]; then
        result=$(curl -s -X POST -H "Authorization: token $GH_TOKEN" -H "Accept: application/vnd.github+json" \
            "https://api.github.com/repos/$GITHUB_USER/$repo/transfer" \
            -d "{\"new_owner\":\"$GITHUB_ORG\"}")
        if echo "$result" | grep -q '"full_name"'; then
            echo "✅ Transferred!"
        else
            echo "❌ Failed: $result"
        fi
    else
        echo "Cancelled."
    fi
}

transfer_all_repos() {
    echo "═══ Transfer ALL repos to $GITHUB_ORG ═══"
    echo ""
    repos=$(api "https://api.github.com/users/$GITHUB_USER/repos?per_page=100" | \
        grep -E '"name"' | head -20 | sed 's/.*: "//;s/".*//')
    
    echo "Will transfer:"
    for repo in $repos; do
        echo "  - $repo"
    done
    echo ""
    read -p "Transfer ALL? (yes/no): " confirm
    
    if [ "$confirm" = "yes" ]; then
        for repo in $repos; do
            echo "Transferring $repo..."
            curl -s -X POST -H "Authorization: token $GH_TOKEN" -H "Accept: application/vnd.github+json" \
                "https://api.github.com/repos/$GITHUB_USER/$repo/transfer" \
                -d "{\"new_owner\":\"$GITHUB_ORG\"}" > /dev/null
            echo "  ✅ $repo"
            sleep 1
        done
        echo ""
        echo "✅ All repos transferred!"
    else
        echo "Cancelled."
    fi
}

remove_collaborator() {
    read -p "Repo name: " repo
    read -p "Owner (Noizyfish or NOIZYLAB-io): " owner
    read -p "Collaborator to remove: " collab
    
    if [ "$collab" = "$PROTECTED_USER" ]; then
        echo "❌ Cannot remove $PROTECTED_USER (protected)"
        return
    fi
    
    echo ""
    read -p "Remove $collab from $owner/$repo? (yes/no): " confirm
    if [ "$confirm" = "yes" ]; then
        status=$(curl -s -o /dev/null -w "%{http_code}" -X DELETE \
            -H "Authorization: token $GH_TOKEN" \
            "https://api.github.com/repos/$owner/$repo/collaborators/$collab")
        if [ "$status" = "204" ]; then
            echo "✅ Removed $collab"
        else
            echo "❌ Failed (status: $status)"
        fi
    else
        echo "Cancelled."
    fi
}

list_org_members() {
    echo "═══ Members of $GITHUB_ORG ═══"
    result=$(api "https://api.github.com/orgs/$GITHUB_ORG/members")
    if echo "$result" | grep -q '"login"'; then
        echo "$result" | grep -E '"login"' | sed 's/.*: "//;s/".*//' | while read user; do
            if [ "$user" = "$PROTECTED_USER" ]; then
                echo "  ✅ $user (OWNER)"
            else
                echo "  👤 $user"
            fi
        done
    else
        echo "  (no members or no access)"
    fi
}

audit_everything() {
    echo "═══════════════════════════════════════════════════════════"
    echo "FULL AUDIT"
    echo "═══════════════════════════════════════════════════════════"
    echo ""
    
    echo "👤 Account: $GITHUB_USER"
    echo "🏢 Org: $GITHUB_ORG"
    echo ""
    
    echo "─── User Repos ───"
    list_user_repos
    echo ""
    
    echo "─── Org Repos ───"
    list_org_repos
    echo ""
    
    echo "─── Org Members ───"
    list_org_members
    echo ""
    
    echo "═══════════════════════════════════════════════════════════"
    echo "AUDIT COMPLETE"
    echo "═══════════════════════════════════════════════════════════"
}

# ───────────────────────────────────────────────────────────────────────────────
# MAIN
# ───────────────────────────────────────────────────────────────────────────────
echo "Verifying GitHub access..."
user=$(api "https://api.github.com/user" | grep -E '"login"' | head -1 | sed 's/.*: "//;s/".*//')
if [ -z "$user" ]; then
    echo "❌ Token invalid"
    exit 1
fi
echo "✅ Logged in as: $user"

while true; do
    show_menu
    case $choice in
        1) list_user_repos ;;
        2) list_org_repos ;;
        3) check_collaborators ;;
        4) transfer_repo ;;
        5) transfer_all_repos ;;
        6) remove_collaborator ;;
        7) list_org_members ;;
        8) audit_everything ;;
        9) echo "👋 Bye!"; exit 0 ;;
        *) echo "Invalid choice" ;;
    esac
done
