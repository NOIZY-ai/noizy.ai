#!/usr/bin/env bash
# OAuth2 flows for Gmail and Microsoft

cmd_oauth_gmail() {
    local client_id="${GMAIL_CLIENT_ID:-}"
    local client_secret="${GMAIL_CLIENT_SECRET:-}"
    
    [[ -z "$client_id" ]] && { err "GMAIL_CLIENT_ID not set"; return 1; }
    [[ -z "$client_secret" ]] && { err "GMAIL_CLIENT_SECRET not set"; return 1; }
    
    echo "[*] Gmail OAuth2 Flow"
    echo ""
    echo "1. Visit: https://accounts.google.com/o/oauth2/v2/auth?client_id=${client_id}&scope=https://www.googleapis.com/auth/gmail.modify&response_type=code&redirect_uri=urn:ietf:wg:oauth:2.0:oob"
    echo ""
    read -p "2. Enter authorization code: " auth_code
    
    local response=$(curl -s -X POST \
        -d "client_id=${client_id}&client_secret=${client_secret}&code=${auth_code}&grant_type=authorization_code&redirect_uri=urn:ietf:wg:oauth:2.0:oob" \
        https://oauth2.googleapis.com/token)
    
    echo "$response" | jq . || echo "$response"
}

cmd_oauth_microsoft() {
    local client_id="${MICROSOFT_CLIENT_ID:-}"
    local client_secret="${MICROSOFT_CLIENT_SECRET:-}"
    local tenant="${MICROSOFT_TENANT:-common}"
    
    [[ -z "$client_id" ]] && { err "MICROSOFT_CLIENT_ID not set"; return 1; }
    [[ -z "$client_secret" ]] && { err "MICROSOFT_CLIENT_SECRET not set"; return 1; }
    
    echo "[*] Microsoft OAuth2 Flow"
    echo ""
    echo "1. Visit: https://login.microsoftonline.com/${tenant}/oauth2/v2.0/authorize?client_id=${client_id}&scope=mail.read%20mail.send&response_type=code&redirect_uri=http://localhost:8000"
    echo ""
    read -p "2. Enter authorization code: " auth_code
    
    local response=$(curl -s -X POST \
        -d "client_id=${client_id}&client_secret=${client_secret}&code=${auth_code}&grant_type=authorization_code&redirect_uri=http://localhost:8000&scope=mail.read%20mail.send" \
        https://login.microsoftonline.com/${tenant}/oauth2/v2.0/token)
    
    echo "$response" | jq . || echo "$response"
}

