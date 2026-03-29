#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════
# NOIZY BROWSER — Open repair URLs from the terminal
# Run on GOD with: ./tools/noizy-browser.sh
# ═══════════════════════════════════════════════════════════

echo "╔══════════════════════════════════════════════════════╗"
echo "║  NOIZY BROWSER — REPAIR PORTAL LAUNCHER              ║"
echo "║  AI & Human Partnership for Repairs                   ║"
echo "╚══════════════════════════════════════════════════════╝"
echo ""
echo "Select a destination:"
echo ""
echo "  [1] Azure Portal          — portal.azure.com"
echo "  [2] Entra Admin Center    — entra.microsoft.com"
echo "  [3] Password Reset        — passwordreset.microsoftonline.com"
echo "  [4] M365 Admin            — admin.microsoft.com"
echo "  [5] GoDaddy Account       — account.godaddy.com"
echo "  [6] GoDaddy SSO           — sso.godaddy.com"
echo "  [7] Cloudflare Dashboard  — dash.cloudflare.com"
echo "  [8] Cloudflare Email      — dash.cloudflare.com (email routing)"
echo "  [9] Device Code Login     — microsoft.com/devicelogin"
echo "  [0] Run Freedom Script    — PowerShell defederation"
echo ""
read -p "Enter number: " CHOICE

case $CHOICE in
  1) open "https://portal.azure.com" 2>/dev/null || xdg-open "https://portal.azure.com" 2>/dev/null ;;
  2) open "https://entra.microsoft.com" 2>/dev/null || xdg-open "https://entra.microsoft.com" 2>/dev/null ;;
  3) open "https://passwordreset.microsoftonline.com" 2>/dev/null || xdg-open "https://passwordreset.microsoftonline.com" 2>/dev/null ;;
  4) open "https://admin.microsoft.com" 2>/dev/null || xdg-open "https://admin.microsoft.com" 2>/dev/null ;;
  5) open "https://account.godaddy.com" 2>/dev/null || xdg-open "https://account.godaddy.com" 2>/dev/null ;;
  6) open "https://sso.godaddy.com" 2>/dev/null || xdg-open "https://sso.godaddy.com" 2>/dev/null ;;
  7) open "https://dash.cloudflare.com/login" 2>/dev/null || xdg-open "https://dash.cloudflare.com/login" 2>/dev/null ;;
  8) open "https://dash.cloudflare.com/?to=/:account/:zone/email/routing" 2>/dev/null || xdg-open "https://dash.cloudflare.com/?to=/:account/:zone/email/routing" 2>/dev/null ;;
  9)
    echo ""
    echo "Running device code auth flow..."
    echo "A code will appear. Enter it at microsoft.com/devicelogin on ANY device."
    echo ""
    pwsh -Command "Connect-MgGraph -Scopes 'Domain.ReadWrite.All','User.ReadWrite.All' -UseDeviceCode"
    ;;
  0)
    echo ""
    echo "Running Freedom Script..."
    pwsh ./tools/freedom.ps1
    ;;
  *)
    echo "Invalid choice."
    ;;
esac
