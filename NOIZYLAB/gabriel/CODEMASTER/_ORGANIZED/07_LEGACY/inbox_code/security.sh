#!/usr/bin/env bash
#═══════════════════════════════════════════════════════════════════════════════
#  🔐 SECURITY MODULE - Mail Manager Pro v3.5.0
#  Encryption, Password Management, and Security Features
#═══════════════════════════════════════════════════════════════════════════════

set -euo pipefail

readonly SECURITY_DIR="${SCRIPT_DIR:-$(dirname "$0")/..}/data/security"
readonly KEYCHAIN_SERVICE="com.mailmgr.credentials"
readonly ENCRYPTION_CIPHER="aes-256-cbc"

# Initialize security directory
mkdir -p "$SECURITY_DIR" 2>/dev/null || true
chmod 700 "$SECURITY_DIR" 2>/dev/null || true

#───────────────────────────────────────────────────────────────────────────────
# macOS KEYCHAIN INTEGRATION
#───────────────────────────────────────────────────────────────────────────────
keychain_store() {
    local account="$1"
    local password="$2"
    local service="${3:-$KEYCHAIN_SERVICE}"
    
    # Delete existing if present
    security delete-generic-password -s "$service" -a "$account" 2>/dev/null || true
    
    # Store new password
    security add-generic-password -s "$service" -a "$account" -w "$password" -U
    
    echo "Credential stored for: $account"
}

keychain_retrieve() {
    local account="$1"
    local service="${2:-$KEYCHAIN_SERVICE}"
    
    security find-generic-password -s "$service" -a "$account" -w 2>/dev/null
}

keychain_delete() {
    local account="$1"
    local service="${2:-$KEYCHAIN_SERVICE}"
    
    security delete-generic-password -s "$service" -a "$account" 2>/dev/null
    echo "Credential deleted: $account"
}

keychain_list() {
    echo "Stored credentials (service: $KEYCHAIN_SERVICE):"
    security dump-keychain 2>/dev/null | grep -A4 "\"$KEYCHAIN_SERVICE\"" | grep "\"acct\"" | sed 's/.*="//; s/".*$//' || echo "  (none)"
}

#───────────────────────────────────────────────────────────────────────────────
# FILE ENCRYPTION
#───────────────────────────────────────────────────────────────────────────────
encrypt_file() {
    local input_file="$1"
    local output_file="${2:-${input_file}.enc}"
    local password="${3:-}"
    
    if [[ -z "$password" ]]; then
        read -rsp "Enter encryption password: " password
        echo ""
    fi
    
    openssl enc -$ENCRYPTION_CIPHER -salt -pbkdf2 -in "$input_file" -out "$output_file" -pass pass:"$password"
    
    echo "Encrypted: $input_file → $output_file"
}

decrypt_file() {
    local input_file="$1"
    local output_file="${2:-${input_file%.enc}}"
    local password="${3:-}"
    
    if [[ -z "$password" ]]; then
        read -rsp "Enter decryption password: " password
        echo ""
    fi
    
    openssl enc -$ENCRYPTION_CIPHER -d -pbkdf2 -in "$input_file" -out "$output_file" -pass pass:"$password"
    
    echo "Decrypted: $input_file → $output_file"
}

encrypt_string() {
    local plaintext="$1"
    local password="$2"
    
    echo -n "$plaintext" | openssl enc -$ENCRYPTION_CIPHER -base64 -pbkdf2 -pass pass:"$password"
}

decrypt_string() {
    local ciphertext="$1"
    local password="$2"
    
    echo "$ciphertext" | openssl enc -$ENCRYPTION_CIPHER -d -base64 -pbkdf2 -pass pass:"$password"
}

#───────────────────────────────────────────────────────────────────────────────
# SECURE BACKUP ENCRYPTION
#───────────────────────────────────────────────────────────────────────────────
encrypt_backup() {
    local backup_path="$1"
    local password="${2:-}"
    
    if [[ ! -f "$backup_path" ]]; then
        echo "Backup file not found: $backup_path" >&2
        return 1
    fi
    
    if [[ -z "$password" ]]; then
        read -rsp "Enter backup encryption password: " password
        echo ""
        read -rsp "Confirm password: " password2
        echo ""
        
        if [[ "$password" != "$password2" ]]; then
            echo "Passwords do not match" >&2
            return 1
        fi
    fi
    
    local encrypted_path="${backup_path}.encrypted"
    
    # Create encrypted archive with checksum
    local checksum=$(shasum -a 256 "$backup_path" | cut -d' ' -f1)
    
    # Prepend checksum to file before encryption
    (echo "$checksum" && cat "$backup_path") | openssl enc -$ENCRYPTION_CIPHER -salt -pbkdf2 -out "$encrypted_path" -pass pass:"$password"
    
    echo "Encrypted backup created: $encrypted_path"
    echo "Original checksum: $checksum"
}

decrypt_backup() {
    local encrypted_path="$1"
    local output_path="${2:-${encrypted_path%.encrypted}}"
    local password="${3:-}"
    
    if [[ ! -f "$encrypted_path" ]]; then
        echo "Encrypted file not found: $encrypted_path" >&2
        return 1
    fi
    
    if [[ -z "$password" ]]; then
        read -rsp "Enter backup decryption password: " password
        echo ""
    fi
    
    # Decrypt and extract checksum
    local decrypted=$(openssl enc -$ENCRYPTION_CIPHER -d -pbkdf2 -in "$encrypted_path" -pass pass:"$password")
    local stored_checksum=$(echo "$decrypted" | head -1)
    
    # Write content (excluding checksum line)
    echo "$decrypted" | tail -n +2 > "$output_path"
    
    # Verify checksum
    local actual_checksum=$(shasum -a 256 "$output_path" | cut -d' ' -f1)
    
    if [[ "$stored_checksum" == "$actual_checksum" ]]; then
        echo "Decrypted and verified: $output_path"
    else
        echo "WARNING: Checksum mismatch! File may be corrupted." >&2
        return 1
    fi
}

#───────────────────────────────────────────────────────────────────────────────
# TOKEN MANAGEMENT
#───────────────────────────────────────────────────────────────────────────────
token_store() {
    local provider="$1"  # gmail, outlook, etc.
    local token="$2"
    local token_type="${3:-access_token}"
    
    local token_file="${SECURITY_DIR}/tokens/${provider}_${token_type}"
    mkdir -p "$(dirname "$token_file")"
    
    # Encrypt and store
    echo "$token" | openssl enc -$ENCRYPTION_CIPHER -base64 -pbkdf2 -pass pass:"$(get_machine_id)" > "$token_file"
    chmod 600 "$token_file"
    
    echo "Token stored: $provider ($token_type)"
}

token_retrieve() {
    local provider="$1"
    local token_type="${2:-access_token}"
    
    local token_file="${SECURITY_DIR}/tokens/${provider}_${token_type}"
    
    if [[ ! -f "$token_file" ]]; then
        return 1
    fi
    
    cat "$token_file" | openssl enc -$ENCRYPTION_CIPHER -d -base64 -pbkdf2 -pass pass:"$(get_machine_id)"
}

token_delete() {
    local provider="$1"
    local token_type="${2:-}"
    
    if [[ -n "$token_type" ]]; then
        rm -f "${SECURITY_DIR}/tokens/${provider}_${token_type}"
    else
        rm -f "${SECURITY_DIR}/tokens/${provider}_"*
    fi
    
    echo "Token(s) deleted: $provider"
}

token_list() {
    echo "Stored tokens:"
    echo "─────────────────────────────────────────"
    
    if [[ -d "${SECURITY_DIR}/tokens" ]]; then
        for token in "${SECURITY_DIR}/tokens"/*; do
            if [[ -f "$token" ]]; then
                local name=$(basename "$token")
                local modified=$(stat -f "%Sm" -t "%Y-%m-%d" "$token" 2>/dev/null || stat -c "%y" "$token" 2>/dev/null | cut -d' ' -f1)
                echo "  🔑 $name (modified: $modified)"
            fi
        done
    else
        echo "  (no tokens stored)"
    fi
}

#───────────────────────────────────────────────────────────────────────────────
# MACHINE ID (For encryption key derivation)
#───────────────────────────────────────────────────────────────────────────────
get_machine_id() {
    # Use hardware UUID on macOS
    if [[ -x /usr/sbin/ioreg ]]; then
        ioreg -rd1 -c IOPlatformExpertDevice | grep -oE 'IOPlatformUUID.*' | cut -d'"' -f4
    # Fallback to /etc/machine-id on Linux
    elif [[ -f /etc/machine-id ]]; then
        cat /etc/machine-id
    else
        # Generate and store a random ID
        local id_file="${SECURITY_DIR}/.machine_id"
        if [[ ! -f "$id_file" ]]; then
            uuidgen > "$id_file"
            chmod 600 "$id_file"
        fi
        cat "$id_file"
    fi
}

#───────────────────────────────────────────────────────────────────────────────
# SECURITY AUDIT
#───────────────────────────────────────────────────────────────────────────────
security_audit() {
    echo ""
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║              🔐 SECURITY AUDIT REPORT                        ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo ""
    
    local issues=0
    
    # Check directory permissions
    echo "📁 Directory Permissions:"
    local script_dir="${SCRIPT_DIR:-$(dirname "$0")/..}"
    
    local data_perms=$(stat -f "%Lp" "$script_dir/data" 2>/dev/null || echo "N/A")
    if [[ "$data_perms" == "700" || "$data_perms" == "750" ]]; then
        echo "  ✓ data/ directory: $data_perms (secure)"
    else
        echo "  ⚠ data/ directory: $data_perms (should be 700 or 750)"
        ((issues++))
    fi
    
    # Check config file permissions
    echo ""
    echo "📄 Configuration Files:"
    local config_file="$script_dir/config/config.yaml"
    if [[ -f "$config_file" ]]; then
        local config_perms=$(stat -f "%Lp" "$config_file" 2>/dev/null || echo "N/A")
        if [[ "$config_perms" == "600" || "$config_perms" == "644" ]]; then
            echo "  ✓ config.yaml: $config_perms"
        else
            echo "  ⚠ config.yaml: $config_perms"
        fi
    fi
    
    # Check for stored credentials
    echo ""
    echo "🔑 Credentials:"
    local token_count=$(find "${SECURITY_DIR}/tokens" -type f 2>/dev/null | wc -l | tr -d ' ')
    echo "  Tokens stored: $token_count"
    
    local keychain_count=$(security dump-keychain 2>/dev/null | grep -c "\"$KEYCHAIN_SERVICE\"" || echo 0)
    echo "  Keychain entries: $keychain_count"
    
    # Check encryption status of backups
    echo ""
    echo "📦 Backup Encryption:"
    local total_backups=$(find "$script_dir/data/backups" -name "*.tar.gz" 2>/dev/null | wc -l | tr -d ' ')
    local encrypted_backups=$(find "$script_dir/data/backups" -name "*.encrypted" 2>/dev/null | wc -l | tr -d ' ')
    echo "  Total backups: $total_backups"
    echo "  Encrypted: $encrypted_backups"
    
    if ((total_backups > 0 && encrypted_backups == 0)); then
        echo "  ⚠ Consider encrypting backups for added security"
        ((issues++))
    fi
    
    # OpenSSL version
    echo ""
    echo "🔧 Security Tools:"
    local openssl_version=$(openssl version 2>/dev/null | head -1)
    echo "  OpenSSL: $openssl_version"
    
    # Summary
    echo ""
    if ((issues == 0)); then
        echo "✓ Security audit passed with no issues"
    else
        echo "⚠ Security audit found $issues issue(s)"
    fi
    echo ""
}

#───────────────────────────────────────────────────────────────────────────────
# SECURE DELETE
#───────────────────────────────────────────────────────────────────────────────
secure_delete() {
    local file="$1"
    local passes="${2:-3}"
    
    if [[ ! -f "$file" ]]; then
        echo "File not found: $file" >&2
        return 1
    fi
    
    local size=$(stat -f%z "$file" 2>/dev/null || stat -c%s "$file")
    
    echo "Securely deleting: $file ($passes passes)"
    
    for ((i=1; i<=passes; i++)); do
        # Overwrite with random data
        dd if=/dev/urandom of="$file" bs="$size" count=1 conv=notrunc 2>/dev/null
        echo "  Pass $i/$passes complete"
    done
    
    # Final deletion
    rm -f "$file"
    echo "File securely deleted"
}

#───────────────────────────────────────────────────────────────────────────────
# PASSWORD GENERATOR
#───────────────────────────────────────────────────────────────────────────────
generate_password() {
    local length="${1:-32}"
    local charset="${2:-alphanumeric}"
    
    local chars=""
    case "$charset" in
        alphanumeric)
            chars='A-Za-z0-9'
            ;;
        alphanumeric-special)
            chars='A-Za-z0-9!@#$%^&*()_+-='
            ;;
        hex)
            chars='0-9a-f'
            ;;
        numeric)
            chars='0-9'
            ;;
        *)
            chars='A-Za-z0-9'
            ;;
    esac
    
    LC_ALL=C tr -dc "$chars" < /dev/urandom | head -c "$length"
    echo ""
}

generate_api_key() {
    local prefix="${1:-mm}"
    local key=$(LC_ALL=C tr -dc 'A-Za-z0-9' < /dev/urandom | head -c 32)
    echo "${prefix}_${key}"
}

#───────────────────────────────────────────────────────────────────────────────
# EXPORT
#───────────────────────────────────────────────────────────────────────────────
export -f keychain_store keychain_retrieve keychain_delete keychain_list 2>/dev/null || true
export -f encrypt_file decrypt_file encrypt_string decrypt_string 2>/dev/null || true
export -f encrypt_backup decrypt_backup 2>/dev/null || true
export -f token_store token_retrieve token_delete token_list 2>/dev/null || true
export -f security_audit secure_delete 2>/dev/null || true
export -f generate_password generate_api_key 2>/dev/null || true

echo "🔐 Security module loaded" >&2
