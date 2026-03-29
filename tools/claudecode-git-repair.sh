#!/usr/bin/env bash
set -euo pipefail

# claudecode-git-repair.sh
# NOIZY Archive Tool — Git Repository Discovery, Diagnosis & Repair
#
# Usage:
#   ./claudecode-git-repair.sh            # dry-run diagnostics only
#   ./claudecode-git-repair.sh --apply    # perform repairs (with backups)
#   ./claudecode-git-repair.sh --help     # show help
#
# Adapted for NOIZY infrastructure. Logs to D1 aquarium-archive.

ROOT_PATHS=( "/Users/m2ultra" "/Volumes/GOD_PRIMARY" "/Volumes/GOD_BACKUP" "/Volumes/ARCHIVE1" "/Volumes/ARCHIVE2" )
ARCHIVE_ROOT="${HOME}/claudecode_git_reports/$(date +%Y%m%d_%H%M%S)"
DRY_RUN=true
APPLY=false
LOG_DIR="${ARCHIVE_ROOT}/logs"
MANIFEST="${ARCHIVE_ROOT}/manifest.ndjson"

# Cloudflare D1 integration (optional)
CLOUDFLARE_ACCOUNT_ID="${CLOUDFLARE_ACCOUNT_ID:-}"
CLOUDFLARE_API_TOKEN="${CLOUDFLARE_API_TOKEN:-}"
D1_ID="${CLOUDFLARE_D1_ID:-e6f98279-656b-4f7a-979d-9197821193f5}"

usage() {
  cat <<EOF
claudecode-git-repair.sh — NOIZY Git Repair Tool
  --apply      Perform repairs and backups (default is dry-run)
  --roots PATHS Comma-separated list of root paths to scan
  --help       Show this help

Safety:
  - Dry-run by default — shows planned actions only
  - --apply creates compressed backup BEFORE any repair
  - Never deletes original data
  - Idempotent — safe to run multiple times
  - Logs everything to manifest.ndjson
EOF
  exit 0
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --apply) DRY_RUN=false; APPLY=true; shift ;;
    --roots) IFS=',' read -r -a ROOT_PATHS <<< "$2"; shift 2 ;;
    --help) usage ;;
    *) echo "Unknown arg: $1"; usage ;;
  esac
done

mkdir -p "$LOG_DIR"
echo "{\"run_started\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"dry_run\":$DRY_RUN,\"roots\":$(printf '%s\n' "${ROOT_PATHS[@]}" | jq -R . | jq -s .)}" > "$MANIFEST"

log_repo() {
  local repo="$1"; local status="$2"; local details="$3"
  local entry
  if command -v jq &>/dev/null; then
    entry=$(jq -n --arg r "$repo" --arg s "$status" --arg d "$details" --arg t "$(date -u +%Y-%m-%dT%H:%M:%SZ)" '{repo:$r,status:$s,details:$d,timestamp:$t}')
  else
    entry="{\"repo\":\"$repo\",\"status\":\"$status\",\"details\":\"$details\",\"timestamp\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"}"
  fi
  echo "$entry" >> "$MANIFEST"
}

d1_log() {
  if [[ -n "$CLOUDFLARE_ACCOUNT_ID" && -n "$CLOUDFLARE_API_TOKEN" ]]; then
    local sql="$1"
    curl -s -X POST "https://api.cloudflare.com/client/v4/accounts/${CLOUDFLARE_ACCOUNT_ID}/d1/database/${D1_ID}/query" \
      -H "Authorization: Bearer ${CLOUDFLARE_API_TOKEN}" \
      -H "Content-Type: application/json" \
      -d "{\"sql\": \"${sql}\"}" > /dev/null 2>&1 || true
  fi
}

# Discovery
DISCOVERY_FILE="${ARCHIVE_ROOT}/discovered_repos.txt"
> "$DISCOVERY_FILE"

echo "╔══════════════════════════════════════════════════╗"
echo "║  NOIZY GIT REPAIR TOOL                           ║"
echo "║  Mode: $([ "$DRY_RUN" = true ] && echo "DRY RUN" || echo "APPLY (with backups)")  ║"
echo "╚══════════════════════════════════════════════════╝"
echo ""
echo "Scanning roots: ${ROOT_PATHS[*]}"

for d in "${ROOT_PATHS[@]}"; do
  if [[ -d "$d" ]]; then
    echo "  Scanning $d ..."
    find "$d" -maxdepth 6 -xdev -type d -name ".git" -print 2>/dev/null | sed 's/\/.git$//' >> "$DISCOVERY_FILE" || true
  fi
done

sort -u "$DISCOVERY_FILE" -o "$DISCOVERY_FILE"
REPO_COUNT=$(wc -l < "$DISCOVERY_FILE" | tr -d ' ')
echo "  Found $REPO_COUNT repositories."
echo ""

process_repo() {
  local repo="$1"
  local repo_log="${LOG_DIR}/$(echo "$repo" | sed 's#[/ ]#_#g').log"
  echo "=== Processing $repo ===" | tee -a "$repo_log"

  if [[ ! -d "$repo/.git" ]]; then
    echo "  No .git found, skipping" | tee -a "$repo_log"
    log_repo "$repo" "skipped_no_git" "No .git directory"
    return
  fi

  pushd "$repo" > /dev/null

  # Basic info
  local branch
  branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "DETACHED")
  local remote
  remote=$(git remote get-url origin 2>/dev/null || echo "none")
  local last_commit
  last_commit=$(git log -1 --format="%H %s" 2>/dev/null || echo "no commits")
  local repo_size
  repo_size=$(du -sk . 2>/dev/null | cut -f1)

  echo "  Branch: $branch" | tee -a "$repo_log"
  echo "  Remote: $remote" | tee -a "$repo_log"
  echo "  Last:   ${last_commit:0:72}" | tee -a "$repo_log"
  echo "  Size:   ${repo_size}KB" | tee -a "$repo_log"

  # Diagnostics
  local fsck_status="ok"
  if git fsck --full --no-reflogs > /tmp/gitfsck_$$.out 2>&1; then
    echo "  fsck: OK" | tee -a "$repo_log"
  else
    fsck_status="issues"
    echo "  fsck: ISSUES FOUND" | tee -a "$repo_log"
    head -20 /tmp/gitfsck_$$.out | tee -a "$repo_log"
  fi

  local dangling_count
  dangling_count=$(git fsck --no-reflogs 2>/dev/null | grep -c 'dangling' || echo "0")
  echo "  Dangling objects: $dangling_count" | tee -a "$repo_log"

  # Object stats
  git count-objects -vH >> "$repo_log" 2>/dev/null || true

  # Plan
  local plan="fsck:${fsck_status};dangling:${dangling_count};branch:${branch};size:${repo_size}KB"

  if [[ "$DRY_RUN" == true ]]; then
    echo "  DRY-RUN: Would backup, repair, gc, repack" | tee -a "$repo_log"
    log_repo "$repo" "dry_run" "$plan"
    popd > /dev/null
    return
  fi

  # APPLY: Backup first
  local backup_dir="${ARCHIVE_ROOT}/backups"
  mkdir -p "$backup_dir"
  local safe_name
  safe_name=$(echo "$repo" | sed 's#[/ ]#_#g')
  local backup_tar="${backup_dir}/${safe_name}-backup.tar.gz"

  echo "  Creating backup: $backup_tar" | tee -a "$repo_log"
  tar -czf "$backup_tar" -C "$(dirname "$repo")" "$(basename "$repo")" 2>/dev/null || {
    echo "  WARNING: Backup failed, skipping repair" | tee -a "$repo_log"
    log_repo "$repo" "backup_failed" "$plan"
    popd > /dev/null
    return
  }
  echo "  Backup created" | tee -a "$repo_log"

  # Repairs
  echo "  Running repairs..." | tee -a "$repo_log"

  # Fetch and prune remotes
  if git remote | grep -q .; then
    git fetch --all --prune --tags --force >> "$repo_log" 2>&1 || true
    git remote prune origin >> "$repo_log" 2>&1 || true
  fi

  # Expire reflogs and GC
  git reflog expire --expire=now --all >> "$repo_log" 2>&1 || true
  git gc --prune=now --aggressive >> "$repo_log" 2>&1 || true
  git repack -a -d --depth=250 --window=250 >> "$repo_log" 2>&1 || true

  # Lost+found recovery
  git fsck --lost-found >> "$repo_log" 2>&1 || true

  # Post-repair check
  if git fsck --full --no-reflogs > /dev/null 2>&1; then
    echo "  Post-repair: OK ✓" | tee -a "$repo_log"
    log_repo "$repo" "repaired" "backup:$backup_tar;$plan"
  else
    echo "  Post-repair: STILL HAS ISSUES" | tee -a "$repo_log"
    log_repo "$repo" "repair_incomplete" "backup:$backup_tar;$plan"
  fi

  # Log to D1 if configured
  local escaped_repo
  escaped_repo=$(echo "$repo" | sed "s/'/''/g")
  local escaped_remote
  escaped_remote=$(echo "$remote" | sed "s/'/''/g")
  d1_log "INSERT OR REPLACE INTO audit_files (scan_id, device, volume, file_path, file_name, file_type, file_size_bytes, is_code, is_git_repo, git_remote, last_modified, created_at) VALUES ('repair_$(date +%Y%m%d)', 'GOD', 'SCAN', '${escaped_repo}', '$(basename "$repo")', 'git_repo', $((repo_size * 1024)), 1, 1, '${escaped_remote}', '$(date -u +%Y-%m-%dT%H:%M:%SZ)', '$(date -u +%Y-%m-%dT%H:%M:%SZ)')"

  popd > /dev/null
}

# Process all repos
while IFS= read -r repo; do
  process_repo "$repo"
done < "$DISCOVERY_FILE"

echo "" >> "$MANIFEST"
echo "{\"run_finished\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"repos_processed\":$REPO_COUNT}" >> "$MANIFEST"

echo ""
echo "╔══════════════════════════════════════════════════╗"
echo "║  SCAN COMPLETE                                   ║"
echo "║  Repos: $REPO_COUNT                              ║"
echo "║  Logs:  $ARCHIVE_ROOT                            ║"
echo "╚══════════════════════════════════════════════════╝"
