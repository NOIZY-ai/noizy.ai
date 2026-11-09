#!/usr/bin/env bash
#═══════════════════════════════════════════════════════════════════════════════
#  🔌 PLUGINS SYSTEM - Mail Manager Pro v3.5.0
#  Extensible Plugin Architecture for Custom Features
#═══════════════════════════════════════════════════════════════════════════════

set -euo pipefail

readonly PLUGINS_DIR="${SCRIPT_DIR:-$(dirname "$0")/..}/plugins"
readonly PLUGINS_ENABLED_DIR="${PLUGINS_DIR}/enabled"
readonly PLUGINS_AVAILABLE_DIR="${PLUGINS_DIR}/available"
readonly PLUGINS_CONFIG="${PLUGINS_DIR}/plugins.json"

# Initialize plugin directories
mkdir -p "$PLUGINS_ENABLED_DIR" "$PLUGINS_AVAILABLE_DIR" 2>/dev/null || true

#───────────────────────────────────────────────────────────────────────────────
# PLUGIN REGISTRY
#───────────────────────────────────────────────────────────────────────────────
declare -A PLUGINS_LOADED
declare -A PLUGIN_HOOKS

plugin_init_registry() {
    if [[ ! -f "$PLUGINS_CONFIG" ]]; then
        echo '{"plugins":[],"hooks":{}}' > "$PLUGINS_CONFIG"
    fi
}

#───────────────────────────────────────────────────────────────────────────────
# PLUGIN LIFECYCLE
#───────────────────────────────────────────────────────────────────────────────
plugin_load() {
    local plugin_name="$1"
    local plugin_path="${PLUGINS_ENABLED_DIR}/${plugin_name}.sh"
    
    if [[ ! -f "$plugin_path" ]]; then
        echo "Plugin not found: $plugin_name" >&2
        return 1
    fi
    
    # Source the plugin
    # shellcheck source=/dev/null
    source "$plugin_path"
    
    # Mark as loaded
    PLUGINS_LOADED["$plugin_name"]=1
    
    # Call plugin init if exists
    if declare -f "${plugin_name}_init" &>/dev/null; then
        "${plugin_name}_init"
    fi
    
    echo "Plugin loaded: $plugin_name"
}

plugin_unload() {
    local plugin_name="$1"
    
    # Call plugin cleanup if exists
    if declare -f "${plugin_name}_cleanup" &>/dev/null; then
        "${plugin_name}_cleanup"
    fi
    
    unset "PLUGINS_LOADED[$plugin_name]"
    echo "Plugin unloaded: $plugin_name"
}

plugin_load_all() {
    for plugin in "$PLUGINS_ENABLED_DIR"/*.sh; do
        if [[ -f "$plugin" ]]; then
            local name=$(basename "$plugin" .sh)
            plugin_load "$name" 2>/dev/null || true
        fi
    done
}

#───────────────────────────────────────────────────────────────────────────────
# PLUGIN MANAGEMENT
#───────────────────────────────────────────────────────────────────────────────
plugin_enable() {
    local plugin_name="$1"
    local source="${PLUGINS_AVAILABLE_DIR}/${plugin_name}.sh"
    local target="${PLUGINS_ENABLED_DIR}/${plugin_name}.sh"
    
    if [[ -f "$source" ]]; then
        ln -sf "$source" "$target"
        echo "Plugin enabled: $plugin_name"
    else
        echo "Plugin not available: $plugin_name" >&2
        return 1
    fi
}

plugin_disable() {
    local plugin_name="$1"
    rm -f "${PLUGINS_ENABLED_DIR}/${plugin_name}.sh"
    echo "Plugin disabled: $plugin_name"
}

plugin_list() {
    echo "Available Plugins:"
    echo "─────────────────────────────────────────"
    
    for plugin in "$PLUGINS_AVAILABLE_DIR"/*.sh; do
        if [[ -f "$plugin" ]]; then
            local name=$(basename "$plugin" .sh)
            local enabled="[ ]"
            [[ -f "${PLUGINS_ENABLED_DIR}/${name}.sh" ]] && enabled="[✓]"
            echo "  $enabled $name"
        fi
    done
    
    echo ""
    echo "Loaded Plugins: ${#PLUGINS_LOADED[@]}"
}

plugin_info() {
    local plugin_name="$1"
    local plugin_path="${PLUGINS_AVAILABLE_DIR}/${plugin_name}.sh"
    
    if [[ -f "$plugin_path" ]]; then
        # Extract metadata from plugin header
        echo "Plugin: $plugin_name"
        grep -E "^#[[:space:]]*(Version|Author|Description):" "$plugin_path" | sed 's/^#[[:space:]]*/  /'
    else
        echo "Plugin not found: $plugin_name"
    fi
}

#───────────────────────────────────────────────────────────────────────────────
# HOOK SYSTEM
#───────────────────────────────────────────────────────────────────────────────
plugin_register_hook() {
    local hook_name="$1"
    local callback="$2"
    
    if [[ -z "${PLUGIN_HOOKS[$hook_name]:-}" ]]; then
        PLUGIN_HOOKS["$hook_name"]="$callback"
    else
        PLUGIN_HOOKS["$hook_name"]="${PLUGIN_HOOKS[$hook_name]}:$callback"
    fi
}

plugin_call_hook() {
    local hook_name="$1"
    shift
    
    if [[ -n "${PLUGIN_HOOKS[$hook_name]:-}" ]]; then
        IFS=':' read -ra callbacks <<< "${PLUGIN_HOOKS[$hook_name]}"
        for callback in "${callbacks[@]}"; do
            if declare -f "$callback" &>/dev/null; then
                "$callback" "$@"
            fi
        done
    fi
}

# Available hooks:
# - on_email_received
# - on_email_sent
# - on_backup_created
# - on_rule_applied
# - on_folder_created
# - on_startup
# - on_shutdown

#───────────────────────────────────────────────────────────────────────────────
# PLUGIN TEMPLATE GENERATOR
#───────────────────────────────────────────────────────────────────────────────
plugin_create() {
    local plugin_name="$1"
    local plugin_path="${PLUGINS_AVAILABLE_DIR}/${plugin_name}.sh"
    
    if [[ -f "$plugin_path" ]]; then
        echo "Plugin already exists: $plugin_name"
        return 1
    fi
    
    cat > "$plugin_path" << 'PLUGIN_TEMPLATE'
#!/usr/bin/env bash
#═══════════════════════════════════════════════════════════════════════════════
# PLUGIN_NAME - Mail Manager Pro Plugin
# Version: 1.0.0
# Author: Your Name
# Description: A custom plugin for Mail Manager Pro
#═══════════════════════════════════════════════════════════════════════════════

# Called when plugin is loaded
PLUGIN_NAME_init() {
    echo "PLUGIN_NAME initialized"
    
    # Register hooks
    plugin_register_hook "on_email_received" "PLUGIN_NAME_on_email"
}

# Called when plugin is unloaded
PLUGIN_NAME_cleanup() {
    echo "PLUGIN_NAME cleanup"
}

# Hook: on_email_received
PLUGIN_NAME_on_email() {
    local email_data="$1"
    # Process email here
}

# Custom command for this plugin
PLUGIN_NAME_command() {
    echo "Custom command for PLUGIN_NAME"
}
PLUGIN_TEMPLATE

    # Replace placeholder with actual plugin name
    sed -i.bak "s/PLUGIN_NAME/$plugin_name/g" "$plugin_path"
    rm -f "${plugin_path}.bak"
    chmod +x "$plugin_path"
    
    echo "Plugin created: $plugin_path"
}

#───────────────────────────────────────────────────────────────────────────────
# BUILT-IN PLUGINS
#───────────────────────────────────────────────────────────────────────────────

# Create example plugins
_create_example_plugins() {
    # Auto-Archive Plugin
    cat > "${PLUGINS_AVAILABLE_DIR}/auto_archive.sh" << 'EOF'
#!/usr/bin/env bash
# Version: 1.0.0
# Author: Mail Manager Pro
# Description: Automatically archive old emails based on rules

auto_archive_init() {
    echo "Auto-Archive plugin initialized"
    plugin_register_hook "on_startup" "auto_archive_check"
}

auto_archive_check() {
    local days="${AUTO_ARCHIVE_DAYS:-30}"
    echo "Checking for emails older than $days days to archive..."
}

auto_archive_run() {
    local days="${1:-30}"
    echo "Archiving emails older than $days days..."
    # Implementation would go here
}

auto_archive_cleanup() {
    echo "Auto-Archive plugin cleanup"
}
EOF

    # VIP Sender Plugin
    cat > "${PLUGINS_AVAILABLE_DIR}/vip_senders.sh" << 'EOF'
#!/usr/bin/env bash
# Version: 1.0.0
# Author: Mail Manager Pro
# Description: Track and prioritize emails from VIP senders

readonly VIP_FILE="${SCRIPT_DIR}/data/vip_senders.txt"

vip_senders_init() {
    touch "$VIP_FILE" 2>/dev/null || true
    plugin_register_hook "on_email_received" "vip_senders_check"
}

vip_senders_add() {
    local email="$1"
    echo "$email" >> "$VIP_FILE"
    sort -u "$VIP_FILE" -o "$VIP_FILE"
    echo "Added VIP: $email"
}

vip_senders_remove() {
    local email="$1"
    grep -v "^${email}$" "$VIP_FILE" > "${VIP_FILE}.tmp" || true
    mv "${VIP_FILE}.tmp" "$VIP_FILE"
    echo "Removed VIP: $email"
}

vip_senders_list() {
    echo "VIP Senders:"
    cat "$VIP_FILE" 2>/dev/null || echo "  (none)"
}

vip_senders_check() {
    local sender="$1"
    if grep -qiF "$sender" "$VIP_FILE" 2>/dev/null; then
        echo "VIP email detected from: $sender"
        return 0
    fi
    return 1
}

vip_senders_cleanup() {
    echo "VIP Senders plugin cleanup"
}
EOF

    # Email Stats Plugin
    cat > "${PLUGINS_AVAILABLE_DIR}/email_stats.sh" << 'EOF'
#!/usr/bin/env bash
# Version: 1.0.0
# Author: Mail Manager Pro
# Description: Track email statistics and generate reports

readonly STATS_FILE="${SCRIPT_DIR}/data/email_stats.json"

email_stats_init() {
    if [[ ! -f "$STATS_FILE" ]]; then
        echo '{"received":0,"sent":0,"archived":0,"deleted":0,"by_day":{}}' > "$STATS_FILE"
    fi
    plugin_register_hook "on_email_received" "email_stats_increment_received"
    plugin_register_hook "on_email_sent" "email_stats_increment_sent"
}

email_stats_increment_received() {
    local current=$(jq '.received' "$STATS_FILE" 2>/dev/null || echo 0)
    jq ".received = $((current + 1))" "$STATS_FILE" > "${STATS_FILE}.tmp"
    mv "${STATS_FILE}.tmp" "$STATS_FILE"
}

email_stats_increment_sent() {
    local current=$(jq '.sent' "$STATS_FILE" 2>/dev/null || echo 0)
    jq ".sent = $((current + 1))" "$STATS_FILE" > "${STATS_FILE}.tmp"
    mv "${STATS_FILE}.tmp" "$STATS_FILE"
}

email_stats_show() {
    echo "Email Statistics:"
    echo "─────────────────────────────────────────"
    cat "$STATS_FILE" | jq .
}

email_stats_reset() {
    echo '{"received":0,"sent":0,"archived":0,"deleted":0,"by_day":{}}' > "$STATS_FILE"
    echo "Statistics reset"
}

email_stats_cleanup() {
    echo "Email Stats plugin cleanup"
}
EOF

    chmod +x "${PLUGINS_AVAILABLE_DIR}"/*.sh 2>/dev/null || true
}

# Initialize plugins
plugin_init_registry
_create_example_plugins

echo "🔌 Plugins system loaded" >&2
