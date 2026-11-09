#!/usr/bin/env bash
# Complete backup and restore operations

BACKUP_VERSION="2"
MAX_BACKUPS="${MAX_BACKUPS:-30}"

cmd_backup_create() {
    local timestamp=$(date +%Y%m%d_%H%M%S)
    local backup_name="backup_v${BACKUP_VERSION}_${timestamp}"
    local backup_file="${BACKUP_DIR}/${backup_name}.tar.gz"
    local manifest_file="${BACKUP_DIR}/${backup_name}.manifest.json"
    
    echo "[*] Creating backup: $backup_name"
    mkdir -p "$BACKUP_DIR"
    
    local temp_dir=$(mktemp -d)
    trap "rm -rf '$temp_dir'" EXIT
    
    echo "[*] Backing up configuration..."
    cp -r "${SCRIPT_DIR}/config" "${temp_dir}/" 2>/dev/null || true
    
    echo "[*] Capturing folder structures..."
    mkdir -p "${temp_dir}/state"
    
    if [[ "$OSTYPE" == darwin* ]]; then
        {
            echo "# Apple Mail folders - captured $(date -u +%Y-%m-%dT%H:%M:%SZ)"
            echo "app: applemail"
            echo "folders:"
            osascript -e 'tell application "Mail" to set allMailboxes to every mailbox' \
                -e 'repeat with mb in allMailboxes' \
                -e 'log (name of mb)' \
                -e 'end repeat' 2>/dev/null | while read -r line; do 
                [[ -n "$line" ]] && echo "  - \"$line\""; 
            done
        } > "${temp_dir}/state/applemail_folders.yaml" 2>/dev/null || echo "# Apple Mail not available" > "${temp_dir}/state/applemail_folders.yaml"
    fi
    
    echo "[*] Backing up data files..."
    if [[ -d "${SCRIPT_DIR}/data" ]]; then
        cp -r "${SCRIPT_DIR}/data" "${temp_dir}/" 2>/dev/null || true
    fi
    
    echo "[*] Creating manifest..."
    cat > "${temp_dir}/manifest.json" << JSON
{
    "version": "${BACKUP_VERSION}",
    "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
    "hostname": "$(hostname)",
    "user": "$(whoami)",
    "os": "$(uname -s)",
    "mail_manager_version": "${VERSION}",
    "contents": {
        "config": true,
        "state": true,
        "data": $([ -d "${temp_dir}/data" ] && echo "true" || echo "false")
    },
    "checksum": ""
}
JSON
    
    tar -czf "$backup_file" -C "$temp_dir" . 2>/dev/null || { err "Backup creation failed"; return 1; }
    
    local checksum=$(shasum -a 256 "$backup_file" 2>/dev/null | cut -d' ' -f1 || echo "")
    cp "${temp_dir}/manifest.json" "$manifest_file"
    [[ -n "$checksum" ]] && sed -i '' "s/\"checksum\": \"\"/\"checksum\": \"${checksum}\"/" "$manifest_file" 2>/dev/null || true
    
    ln -sf "$backup_file" "${BACKUP_DIR}/backup_latest.tar.gz" 2>/dev/null || true
    
    success "Backup created: $backup_file"
}

cmd_backup_restore() {
    local backup_selector="${1:-latest}"
    local backup_file=""
    
    if [[ "$backup_selector" == "latest" ]]; then
        backup_file="${BACKUP_DIR}/backup_latest.tar.gz"
    elif [[ -f "$backup_selector" ]]; then
        backup_file="$backup_selector"
    else
        backup_file=$(ls -1 "${BACKUP_DIR}"/backup_v*"${backup_selector}"*.tar.gz 2>/dev/null | head -1)
    fi
    
    [[ ! -f "$backup_file" ]] && { err "Backup not found: $backup_selector"; return 1; }
    
    echo "[*] Restoring from: $(basename "$backup_file")"
    
    local temp_dir=$(mktemp -d)
    trap "rm -rf '$temp_dir'" EXIT
    
    tar -xzf "$backup_file" -C "$temp_dir" || { err "Failed to extract backup"; return 1; }
    
    [[ -d "${temp_dir}/config" ]] && cp -r "${temp_dir}/config/"* "${SCRIPT_DIR}/config/" 2>/dev/null || true
    [[ -d "${temp_dir}/data" ]] && { mkdir -p "${SCRIPT_DIR}/data"; cp -r "${temp_dir}/data/"* "${SCRIPT_DIR}/data/" 2>/dev/null || true; }
    
    success "Restore complete!"
}

cmd_backup_list() {
    echo "[*] Available backups:"
    echo ""
    
    [[ ! -d "$BACKUP_DIR" ]] && { echo "No backups found"; return 0; }
    
    ls -1t "${BACKUP_DIR}"/backup_v*.tar.gz 2>/dev/null | while read -r backup; do
        local name=$(basename "$backup")
        local size=$(du -h "$backup" 2>/dev/null | cut -f1)
        local date=$(stat -f "%Sm" -t "%Y-%m-%d %H:%M" "$backup" 2>/dev/null || echo "unknown")
        printf "  %-40s %10s %20s\n" "$name" "$size" "$date"
    done
}

