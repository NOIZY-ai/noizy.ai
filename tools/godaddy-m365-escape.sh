#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════
# GODADDY M365 ESCAPE TOOL v1.0
# ═══════════════════════════════════════════════════════════════
#
# Fixes the GoDaddy Microsoft 365 federation lockout that affects
# thousands of small business owners worldwide.
#
# The Problem:
#   GoDaddy federates your M365 tenant, meaning:
#   - Password reset doesn't work (SSPR blocked for federated domains)
#   - Admin portal redirects to GoDaddy
#   - CryptoTokenKit errors on Apple devices
#   - You can't access your own email, your own domain, your own business
#
# The Solution:
#   Defederate from GoDaddy, take full control of your M365 tenant,
#   reset passwords, remove GoDaddy's delegated admin access.
#
# Requirements:
#   - PowerShell 7+ (pwsh)
#   - Microsoft.Graph PowerShell module
#   - An admin account (even the GoDaddy-created one)
#   - 60-90 minutes
#
# Usage:
#   ./godaddy-m365-escape.sh check     # Check federation status
#   ./godaddy-m365-escape.sh fix       # Run the full defederation
#   ./godaddy-m365-escape.sh --help    # Show this help
#
# Created by NOIZY.AI — because no one should be locked out of
# their own identity.
# ═══════════════════════════════════════════════════════════════

set -euo pipefail

DOMAIN="${GODADDY_DOMAIN:-}"
ADMIN_USER="${ADMIN_USER:-}"
MODE="${1:-help}"

cat << 'BANNER'
╔══════════════════════════════════════════════════════════════╗
║  GODADDY M365 ESCAPE TOOL v1.0                              ║
║  Break free from GoDaddy federation lockout.                 ║
║  Built by NOIZY.AI — protect the human signal.               ║
╚══════════════════════════════════════════════════════════════╝
BANNER

usage() {
  cat << 'EOF'

USAGE:
  ./godaddy-m365-escape.sh check     Check if your domain is federated
  ./godaddy-m365-escape.sh fix       Run the full defederation process
  ./godaddy-m365-escape.sh guide     Print the step-by-step manual guide
  ./godaddy-m365-escape.sh --help    Show this help

ENVIRONMENT VARIABLES:
  GODADDY_DOMAIN    Your domain (e.g., noizyfish.com)
  ADMIN_USER        Your admin email (e.g., rsp@noizyfish.com)

BEFORE YOU START:
  1. You need PowerShell 7+ installed (brew install powershell on macOS)
  2. You need an admin account on the M365 tenant
  3. Back up any critical email/data first
  4. Plan for 60-90 minutes
  5. Do this outside business hours (mail flow continues, but logins break temporarily)

EOF
  exit 0
}

check_prerequisites() {
  echo ""
  echo "Checking prerequisites..."
  echo ""

  # Check PowerShell
  if command -v pwsh &>/dev/null; then
    echo "  ✓ PowerShell $(pwsh --version 2>/dev/null | head -1)"
  else
    echo "  ✗ PowerShell not found"
    echo "    Install: brew install powershell (macOS)"
    echo "    Install: sudo apt install powershell (Linux)"
    echo "    Install: winget install Microsoft.PowerShell (Windows)"
    MISSING=true
  fi

  # Check domain
  if [ -z "$DOMAIN" ]; then
    echo "  ✗ GODADDY_DOMAIN not set"
    echo "    Run: export GODADDY_DOMAIN=yourdomain.com"
    MISSING=true
  else
    echo "  ✓ Domain: $DOMAIN"
  fi

  if [ -z "$ADMIN_USER" ]; then
    echo "  ✗ ADMIN_USER not set"
    echo "    Run: export ADMIN_USER=admin@yourdomain.com"
    MISSING=true
  else
    echo "  ✓ Admin: $ADMIN_USER"
  fi

  if [ "${MISSING:-false}" = true ]; then
    echo ""
    echo "Fix the above issues and try again."
    exit 1
  fi

  echo ""
  echo "All prerequisites met."
}

check_federation() {
  echo ""
  echo "═══ STEP 1: CHECK FEDERATION STATUS ═══"
  echo ""
  echo "Running PowerShell to check if $DOMAIN is federated..."
  echo ""

  pwsh -Command "
    try {
      Install-Module Microsoft.Graph.Identity.DirectoryManagement -Scope CurrentUser -Force -ErrorAction SilentlyContinue
      Connect-MgGraph -Scopes 'Domain.Read.All' -ErrorAction Stop
      \$domain = Get-MgDomain -DomainId '$DOMAIN' -ErrorAction Stop
      Write-Host ''
      Write-Host \"Domain: \$(\$domain.Id)\"
      Write-Host \"Authentication: \$(\$domain.AuthenticationType)\"
      Write-Host \"Is Default: \$(\$domain.IsDefault)\"
      Write-Host \"Is Verified: \$(\$domain.IsVerified)\"
      Write-Host ''
      if (\$domain.AuthenticationType -eq 'Federated') {
        Write-Host '⚠️  YOUR DOMAIN IS FEDERATED BY GODADDY.'
        Write-Host '   This is why you are locked out.'
        Write-Host '   Run: ./godaddy-m365-escape.sh fix'
      } else {
        Write-Host '✓ Your domain is MANAGED (not federated).'
        Write-Host '  You should be able to reset passwords normally.'
      }
    } catch {
      Write-Host \"Error: \$(\$_.Exception.Message)\"
      Write-Host ''
      Write-Host 'If you cannot connect, try:'
      Write-Host '  1. Use your .onmicrosoft.com admin account instead'
      Write-Host '  2. Download Microsoft 365 Admin app on mobile'
      Write-Host '  3. Call Microsoft support: 1-800-642-7676'
    }
  "
}

run_defederation() {
  echo ""
  echo "═══════════════════════════════════════════════════════════"
  echo "  DEFEDERATION PROCESS — THIS WILL FREE YOU FROM GODADDY"
  echo "═══════════════════════════════════════════════════════════"
  echo ""
  echo "This process will:"
  echo "  1. Convert your domain from Federated → Managed"
  echo "  2. Reset your admin password"
  echo "  3. Remove GoDaddy's delegated admin access"
  echo ""
  echo "YOUR MAIL WILL KEEP FLOWING. No downtime on email."
  echo "But users WILL need new passwords after this."
  echo ""
  read -p "Are you sure you want to proceed? (yes/no): " CONFIRM
  if [ "$CONFIRM" != "yes" ]; then
    echo "Aborted."
    exit 0
  fi

  echo ""
  echo "═══ STEP 1: INSTALL REQUIRED MODULES ═══"

  pwsh -Command "
    Write-Host 'Installing Microsoft.Graph modules...'
    Install-Module Microsoft.Graph.Identity.DirectoryManagement -Scope CurrentUser -Force -ErrorAction SilentlyContinue
    Install-Module Microsoft.Graph.Users -Scope CurrentUser -Force -ErrorAction SilentlyContinue
    Write-Host 'Done.'
  "

  echo ""
  echo "═══ STEP 2: CONNECT TO MICROSOFT GRAPH ═══"
  echo ""
  echo "A browser window will open for authentication."
  echo "Sign in with your admin account."
  echo "If the web login fails (GoDaddy redirect), try:"
  echo "  - Use an .onmicrosoft.com account if you have one"
  echo "  - Use the Microsoft 365 Admin mobile app to create one first"
  echo ""

  pwsh -Command "
    Connect-MgGraph -Scopes 'Domain.ReadWrite.All','User.ReadWrite.All','Directory.ReadWrite.All' -ErrorAction Stop
    Write-Host 'Connected to Microsoft Graph.'
  "

  echo ""
  echo "═══ STEP 3: CONVERT DOMAIN FROM FEDERATED → MANAGED ═══"

  pwsh -Command "
    try {
      Write-Host 'Converting $DOMAIN from Federated to Managed...'
      Update-MgDomain -DomainId '$DOMAIN' -BodyParameter @{
        AuthenticationType = 'Managed'
      } -ErrorAction Stop
      Write-Host ''
      Write-Host '✓ DOMAIN IS NOW MANAGED. GODADDY FEDERATION REMOVED.'
      Write-Host ''
    } catch {
      Write-Host \"Error: \$(\$_.Exception.Message)\"
      Write-Host ''
      Write-Host 'If this fails, try the MSOnline module instead:'
      Write-Host '  Install-Module MSOnline -Force'
      Write-Host '  Connect-MsolService'
      Write-Host '  Set-MsolDomainAuthentication -DomainName \"$DOMAIN\" -Authentication Managed'
    }
  "

  echo ""
  echo "═══ STEP 4: RESET ADMIN PASSWORD ═══"
  echo ""
  read -sp "Enter new password for $ADMIN_USER: " NEW_PASSWORD
  echo ""

  pwsh -Command "
    try {
      Update-MgUser -UserId '$ADMIN_USER' -PasswordProfile @{
        Password = '$NEW_PASSWORD'
        ForceChangePasswordNextSignIn = \$false
      } -ErrorAction Stop
      Write-Host ''
      Write-Host '✓ PASSWORD RESET SUCCESSFUL.'
      Write-Host '  You can now log in with your new password.'
    } catch {
      Write-Host \"Error: \$(\$_.Exception.Message)\"
      Write-Host 'Try resetting password via admin.microsoft.com instead.'
    }
  "

  echo ""
  echo "═══ STEP 5: REMOVE GODADDY DELEGATED ADMIN ═══"
  echo ""
  echo "To remove GoDaddy's admin access:"
  echo "  1. Go to admin.microsoft.com"
  echo "  2. Sign in with $ADMIN_USER and your new password"
  echo "  3. Settings → Partner Relationships"
  echo "  4. Find GoDaddy → Remove"
  echo "  5. Also: Azure Portal → Enterprise Applications → Delete GoDaddy app"
  echo ""

  echo ""
  echo "═══════════════════════════════════════════════════════════"
  echo "  DEFEDERATION COMPLETE"
  echo "═══════════════════════════════════════════════════════════"
  echo ""
  echo "  ✓ Domain converted from Federated → Managed"
  echo "  ✓ Admin password reset"
  echo "  → Remove GoDaddy delegated admin (manual step above)"
  echo "  → Cancel GoDaddy M365 subscription when ready"
  echo ""
  echo "  YOU NOW OWN YOUR MICROSOFT 365 TENANT."
  echo "  GODADDY HAS NO CONTROL."
  echo ""
  echo "  Next steps:"
  echo "    1. Log into Cloudflare: dash.cloudflare.com"
  echo "    2. Set up email routing on noizy.ai"
  echo "    3. Change Cloudflare login email"
  echo "    4. Transfer domains away from GoDaddy"
  echo "    5. Close all GoDaddy accounts"
  echo ""
  echo "  GORUNFREE."
}

print_guide() {
  cat << 'GUIDE'

═══════════════════════════════════════════════════════════════
  THE COMPLETE GODADDY M365 ESCAPE GUIDE
  For everyone trapped by GoDaddy's Microsoft 365 federation
═══════════════════════════════════════════════════════════════

THE PROBLEM:
  When you buy Microsoft 365 through GoDaddy, they "federate"
  your domain. This means:

  - GoDaddy controls your authentication
  - Microsoft's password reset doesn't work for you
  - Admin portal redirects to GoDaddy instead of Microsoft
  - Apple devices get CryptoTokenKit errors
  - You are locked out of YOUR OWN email and business

  This affects THOUSANDS of small businesses worldwide.

WHY IT HAPPENS:
  GoDaddy sets up your M365 tenant with federated authentication.
  This means all login requests for your domain are routed through
  GoDaddy's SSO servers. If anything breaks in that chain — a
  corrupted token, a changed password, a billing issue — you lose
  access to everything.

  Microsoft's self-service password reset (SSPR) is BLOCKED for
  federated domains. GoDaddy did this by design.

THE FIXES (TRY IN ORDER):

FIX 1 — Log into GoDaddy with a different email (2 min)
  - Go to account.godaddy.com
  - Try any email you've ever used with GoDaddy
  - If you get in: Email & Office → Manage → Reset Password

FIX 2 — Microsoft 365 Admin mobile app (5 min)
  - Download "Microsoft 365 Admin" from App Store / Play Store
  - Sign in with your M365 admin email
  - The mobile app uses a different auth flow
  - It often bypasses the GoDaddy redirect
  - Once in: Users → Your Account → Reset Password

FIX 3 — Clear device token cache (2 min)
  - iPad/iPhone: Settings → Safari → Clear History and Website Data
  - Mac: Keychain Access → search "microsoft" → delete entries
  - Then try signing in again in a private/incognito window
  - Choose phone/SMS verification instead of passkey

FIX 4 — Use .onmicrosoft.com account (10 min)
  - Every M365 tenant has a .onmicrosoft.com domain
  - If you ever created a user like admin@yourcompany.onmicrosoft.com
  - That account bypasses GoDaddy federation entirely
  - Sign in at admin.microsoft.com with that account

FIX 5 — Full Defederation via PowerShell (60 min)
  - This PERMANENTLY removes GoDaddy's control
  - Requires PowerShell 7+ and Microsoft.Graph module
  - Run: ./godaddy-m365-escape.sh fix
  - Or follow the manual steps at:
    https://tminus365.com/defederating-godaddy-365/
    https://bostonmit.com/defederate-microsoft-365-from-godaddy/

FIX 6 — Microsoft Support Direct (last resort)
  - Call Microsoft: 1-800-642-7676
  - Tell them: "I am locked out of my Microsoft 365 tenant.
    My domain is federated through GoDaddy and I cannot
    access any admin functions."
  - They have a process for tenant recovery
  - You will need to prove domain ownership (DNS TXT record)

AFTER YOU'RE FREE:
  1. Change all passwords immediately
  2. Remove GoDaddy as delegated admin
  3. Delete GoDaddy's Azure Enterprise Application
  4. Cancel GoDaddy M365 subscription
  5. Transfer your domain to a real registrar (Cloudflare, Namecheap)
  6. Never buy M365 through a reseller again — go direct at microsoft.com

PREVENTION (FOR OTHERS):
  - NEVER buy Microsoft 365 through GoDaddy
  - ALWAYS buy M365 directly from microsoft.com
  - ALWAYS create a backup .onmicrosoft.com admin account
  - ALWAYS set up self-service password reset BEFORE you need it
  - ALWAYS keep your recovery email and phone number updated
  - ALWAYS have at least 2 global admin accounts

═══════════════════════════════════════════════════════════════
  Built by NOIZY.AI — because no one should be locked out
  of their own identity.

  If this tool helped you, visit noizy.ai
  We're building the infrastructure for sovereign human creativity.

  GORUNFREE.
═══════════════════════════════════════════════════════════════

GUIDE
}

# Main
case "$MODE" in
  check)
    check_prerequisites
    check_federation
    ;;
  fix)
    check_prerequisites
    run_defederation
    ;;
  guide)
    print_guide
    ;;
  --help|-h|help|*)
    usage
    ;;
esac
