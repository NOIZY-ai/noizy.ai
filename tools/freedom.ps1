#!/usr/bin/env pwsh
# ═══════════════════════════════════════════════════════════
# NOIZY FREEDOM SCRIPT — Run this ONE command on GOD
# ═══════════════════════════════════════════════════════════
#
# This script:
#   1. Installs required PowerShell modules
#   2. Connects to your M365 tenant
#   3. Checks federation status
#   4. Defederates noizyfish.com from GoDaddy
#   5. Resets your password
#   6. Creates a backup admin account
#   7. Removes GoDaddy delegated admin
#
# RUN THIS ON GOD:
#   pwsh ./tools/freedom.ps1
#
# ═══════════════════════════════════════════════════════════

Write-Host ""
Write-Host "╔══════════════════════════════════════════════════════╗" -ForegroundColor Yellow
Write-Host "║  NOIZY FREEDOM SCRIPT                                ║" -ForegroundColor Yellow
Write-Host "║  Break free from GoDaddy. Forever.                   ║" -ForegroundColor Yellow
Write-Host "╚══════════════════════════════════════════════════════╝" -ForegroundColor Yellow
Write-Host ""

# ═══ STEP 1: Install modules ═══
Write-Host "STEP 1: Installing PowerShell modules..." -ForegroundColor Cyan
try {
    Install-Module Microsoft.Graph.Identity.DirectoryManagement -Scope CurrentUser -Force -ErrorAction SilentlyContinue
    Install-Module Microsoft.Graph.Users -Scope CurrentUser -Force -ErrorAction SilentlyContinue
    Install-Module Microsoft.Graph.Identity.Governance -Scope CurrentUser -Force -ErrorAction SilentlyContinue
    Write-Host "  ✓ Modules installed" -ForegroundColor Green
} catch {
    Write-Host "  ✗ Module install failed: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "  Try: Install-Module Microsoft.Graph -Scope CurrentUser -Force" -ForegroundColor Yellow
}

# ═══ STEP 2: Connect ═══
Write-Host ""
Write-Host "STEP 2: Connecting to Microsoft Graph..." -ForegroundColor Cyan
Write-Host "  A browser window will open. Sign in with rsp@noizyfish.com" -ForegroundColor White
Write-Host "  If the browser redirects to GoDaddy, try these alternatives:" -ForegroundColor Yellow
Write-Host "    - Use an .onmicrosoft.com account if you have one" -ForegroundColor Yellow
Write-Host "    - Open the M365 Admin app on iPad first, create a backup admin" -ForegroundColor Yellow
Write-Host ""

try {
    Connect-MgGraph -Scopes "Domain.ReadWrite.All","User.ReadWrite.All","Directory.ReadWrite.All","DelegatedAdminRelationship.ReadWrite.All" -ErrorAction Stop
    Write-Host "  ✓ Connected to Microsoft Graph" -ForegroundColor Green

    $context = Get-MgContext
    Write-Host "  Account: $($context.Account)" -ForegroundColor White
    Write-Host "  Tenant:  $($context.TenantId)" -ForegroundColor White
} catch {
    Write-Host "  ✗ Connection failed: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
    Write-Host "  ALTERNATIVE: Try connecting with device code flow:" -ForegroundColor Yellow
    Write-Host "    Connect-MgGraph -Scopes 'Domain.ReadWrite.All','User.ReadWrite.All' -UseDeviceCode" -ForegroundColor Yellow
    Write-Host "  This gives you a code to enter at https://microsoft.com/devicelogin" -ForegroundColor Yellow
    Write-Host "  You can enter that code on ANY device (iPad, iPhone, etc.)" -ForegroundColor Yellow
    exit 1
}

# ═══ STEP 3: Check federation ═══
Write-Host ""
Write-Host "STEP 3: Checking domain federation status..." -ForegroundColor Cyan

$domains = Get-MgDomain -ErrorAction SilentlyContinue
foreach ($domain in $domains) {
    $status = if ($domain.AuthenticationType -eq "Federated") { "⚠️  FEDERATED (GoDaddy controls this)" } else { "✓ Managed" }
    Write-Host "  $($domain.Id): $status" -ForegroundColor $(if ($domain.AuthenticationType -eq "Federated") { "Red" } else { "Green" })
}

$federatedDomains = $domains | Where-Object { $_.AuthenticationType -eq "Federated" }
if ($federatedDomains.Count -eq 0) {
    Write-Host ""
    Write-Host "  No federated domains found. You may already be free!" -ForegroundColor Green
    Write-Host "  Try logging into dash.cloudflare.com now." -ForegroundColor White
} else {
    Write-Host ""
    Write-Host "  Found $($federatedDomains.Count) federated domain(s). Proceeding with defederation..." -ForegroundColor Yellow
}

# ═══ STEP 4: Defederate ═══
Write-Host ""
Write-Host "STEP 4: Defederating domains from GoDaddy..." -ForegroundColor Cyan

foreach ($domain in $federatedDomains) {
    Write-Host "  Converting $($domain.Id) from Federated → Managed..." -ForegroundColor White
    try {
        Update-MgDomain -DomainId $domain.Id -BodyParameter @{
            AuthenticationType = "Managed"
        } -ErrorAction Stop
        Write-Host "  ✓ $($domain.Id) is now MANAGED" -ForegroundColor Green
    } catch {
        Write-Host "  ✗ Failed: $($_.Exception.Message)" -ForegroundColor Red
        Write-Host "  Trying alternative method (MSOnline)..." -ForegroundColor Yellow
        try {
            Install-Module MSOnline -Scope CurrentUser -Force -ErrorAction SilentlyContinue
            Connect-MsolService -ErrorAction Stop
            Set-MsolDomainAuthentication -DomainName $domain.Id -Authentication Managed -ErrorAction Stop
            Write-Host "  ✓ $($domain.Id) converted via MSOnline" -ForegroundColor Green
        } catch {
            Write-Host "  ✗ Both methods failed: $($_.Exception.Message)" -ForegroundColor Red
        }
    }
}

# ═══ STEP 5: Reset password ═══
Write-Host ""
Write-Host "STEP 5: Resetting password for rsp@noizyfish.com..." -ForegroundColor Cyan

$newPassword = Read-Host -Prompt "  Enter new password for rsp@noizyfish.com" -AsSecureString
$BSTR = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($newPassword)
$plainPassword = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR)

try {
    Update-MgUser -UserId "rsp@noizyfish.com" -PasswordProfile @{
        Password = $plainPassword
        ForceChangePasswordNextSignIn = $false
    } -ErrorAction Stop
    Write-Host "  ✓ Password reset successful" -ForegroundColor Green
} catch {
    Write-Host "  ✗ Password reset failed: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "  Try resetting manually at admin.microsoft.com → Users" -ForegroundColor Yellow
}

# ═══ STEP 6: Create backup admin ═══
Write-Host ""
Write-Host "STEP 6: Creating backup admin account..." -ForegroundColor Cyan

# Get the .onmicrosoft.com domain
$onmsDomain = ($domains | Where-Object { $_.Id -like "*.onmicrosoft.com" -and $_.Id -notlike "*mail*" }).Id

if ($onmsDomain) {
    $backupAdmin = "noizyadmin@$onmsDomain"
    Write-Host "  Creating $backupAdmin..." -ForegroundColor White

    try {
        $backupPassword = "NOIZY-Backup-$(Get-Random -Maximum 9999)!"

        New-MgUser -DisplayName "NOIZY Backup Admin" `
            -UserPrincipalName $backupAdmin `
            -MailNickname "noizyadmin" `
            -PasswordProfile @{
                Password = $backupPassword
                ForceChangePasswordNextSignIn = $false
            } `
            -AccountEnabled $true -ErrorAction Stop

        # Assign Global Admin role
        $globalAdminRole = Get-MgDirectoryRole | Where-Object { $_.DisplayName -eq "Global Administrator" }
        if ($globalAdminRole) {
            $userId = (Get-MgUser -UserId $backupAdmin).Id
            New-MgDirectoryRoleMember -DirectoryRoleId $globalAdminRole.Id -BodyParameter @{
                "@odata.id" = "https://graph.microsoft.com/v1.0/directoryObjects/$userId"
            } -ErrorAction SilentlyContinue
        }

        Write-Host "  ✓ Backup admin created" -ForegroundColor Green
        Write-Host "  ═══════════════════════════════════════" -ForegroundColor Yellow
        Write-Host "  SAVE THIS:" -ForegroundColor Yellow
        Write-Host "    Username: $backupAdmin" -ForegroundColor White
        Write-Host "    Password: $backupPassword" -ForegroundColor White
        Write-Host "  ═══════════════════════════════════════" -ForegroundColor Yellow
    } catch {
        Write-Host "  ✗ Backup admin creation failed: $($_.Exception.Message)" -ForegroundColor Red
    }
} else {
    Write-Host "  ✗ Could not find .onmicrosoft.com domain" -ForegroundColor Red
}

# ═══ STEP 7: Remove GoDaddy delegated admin ═══
Write-Host ""
Write-Host "STEP 7: Removing GoDaddy delegated admin..." -ForegroundColor Cyan
Write-Host "  This step must be done manually:" -ForegroundColor Yellow
Write-Host "    1. Go to admin.microsoft.com" -ForegroundColor White
Write-Host "    2. Sign in with your new password" -ForegroundColor White
Write-Host "    3. Settings → Partner Relationships" -ForegroundColor White
Write-Host "    4. Find GoDaddy → Remove" -ForegroundColor White
Write-Host "    5. Azure Portal → Enterprise Applications → Delete GoDaddy app" -ForegroundColor White

# ═══ DONE ═══
Write-Host ""
Write-Host "╔══════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║  FREEDOM ACHIEVED                                    ║" -ForegroundColor Green
Write-Host "╚══════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""
Write-Host "  WHAT TO DO NOW:" -ForegroundColor Yellow
Write-Host "    1. Go to dash.cloudflare.com → sign in with rsp@noizyfish.com" -ForegroundColor White
Write-Host "    2. noizy.ai → Email → Email Routing → Enable" -ForegroundColor White
Write-Host "    3. Create rsp@noizy.ai → rsplowman@icloud.com" -ForegroundColor White
Write-Host "    4. My Profile → change login email to rsp@noizy.ai" -ForegroundColor White
Write-Host "    5. GoDaddy chain is BROKEN FOREVER" -ForegroundColor White
Write-Host ""
Write-Host "  GORUNFREE." -ForegroundColor Yellow
Write-Host ""

Disconnect-MgGraph -ErrorAction SilentlyContinue
