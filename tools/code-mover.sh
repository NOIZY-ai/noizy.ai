#!/usr/bin/env bash
# NOIZY Code Mover v1.0
# Moves code from scattered drives into the unified archive
#
# Usage: ./code-mover.sh <source_path> <archive_volume> [--dry-run]
# Example: ./code-mover.sh /Volumes/GOD_PRIMARY/projects /Volumes/ARCHIVE1/code-archive
# Example: ./code-mover.sh /Users/m2ultra/repos /Volumes/ARCHIVE1/code-archive --dry-run
#
# What it does:
#   1. Scans source for git repos and code projects
#   2. Creates organized archive structure: /archive/YYYY-MM/<project-name>/
#   3. Copies (not moves) to archive with full git history preserved
#   4. Logs every operation to D1 aquarium-archive
#   5. Generates a manifest for each archived project
#   6. Optional: creates a .archived marker in the source after successful copy

set -euo pipefail

SOURCE_PATH="${1:?Usage: ./code-mover.sh <source_path> <archive_volume> [--dry-run]}"
ARCHIVE_PATH="${2:?Provide archive destination path}"
DRY_RUN="${3:-}"

ACCOUNT_ID="${CLOUDFLARE_ACCOUNT_ID:?Set CLOUDFLARE_ACCOUNT_ID}"
API_TOKEN="${CLOUDFLARE_API_TOKEN:?Set CLOUDFLARE_API_TOKEN}"
D1_ID="${CLOUDFLARE_D1_ID:-e6f98279-656b-4f7a-979d-9197821193f5}"
API_BASE="https://api.cloudflare.com/client/v4/accounts/${ACCOUNT_ID}/d1/database/${D1_ID}/query"

ARCHIVE_DATE=$(date +%Y-%m)
ARCHIVE_DEST="${ARCHIVE_PATH}/${ARCHIVE_DATE}"
MOVE_ID="move_$(date +%Y%m%d_%H%M%S)"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

echo "╔══════════════════════════════════════════════════╗"
echo "║  NOIZY CODE MOVER v1.0                           ║"
echo "║  Source:  ${SOURCE_PATH}                         ║"
echo "║  Archive: ${ARCHIVE_DEST}                        ║"
echo "║  Mode:    ${DRY_RUN:-LIVE}                       ║"
echo "╚══════════════════════════════════════════════════╝"

d1_query() {
  local sql="$1"
  curl -s -X POST "${API_BASE}" \
    -H "Authorization: Bearer ${API_TOKEN}" \
    -H "Content-Type: application/json" \
    -d "{\"sql\": \"$(echo "$sql" | sed "s/\"/\\\\\"/g")\"}"
}

sql_escape() {
  echo "$1" | sed "s/'/''/g"
}

# Create archive destination
if [ "${DRY_RUN}" != "--dry-run" ]; then
  mkdir -p "${ARCHIVE_DEST}"
fi

MOVED_COUNT=0
SKIPPED_COUNT=0
FAILED_COUNT=0
TOTAL_BYTES_MOVED=0

# Find all git repos in source
find "${SOURCE_PATH}" -maxdepth 4 -name ".git" -type d 2>/dev/null | while read -r gitdir; do
  REPO_PATH=$(dirname "$gitdir")
  REPO_NAME=$(basename "$REPO_PATH")
  REPO_SIZE=$(du -sk "$REPO_PATH" 2>/dev/null | cut -f1)
  REPO_SIZE_BYTES=$((REPO_SIZE * 1024))

  # Check if already archived
  if [ -f "${REPO_PATH}/.archived" ]; then
    echo "  SKIP: ${REPO_NAME} (already archived)"
    SKIPPED_COUNT=$((SKIPPED_COUNT + 1))
    continue
  fi

  # Check if destination already exists
  if [ -d "${ARCHIVE_DEST}/${REPO_NAME}" ]; then
    echo "  SKIP: ${REPO_NAME} (already in archive)"
    SKIPPED_COUNT=$((SKIPPED_COUNT + 1))
    continue
  fi

  # Get git info
  REMOTE_URL=$(cd "$REPO_PATH" && git remote get-url origin 2>/dev/null || echo "none")
  LAST_COMMIT=$(cd "$REPO_PATH" && git log -1 --format="%H %s" 2>/dev/null || echo "unknown")
  BRANCH=$(cd "$REPO_PATH" && git branch --show-current 2>/dev/null || echo "unknown")

  echo "  ARCHIVE: ${REPO_NAME}"
  echo "    Size: ${REPO_SIZE}KB | Remote: ${REMOTE_URL}"
  echo "    Branch: ${BRANCH} | Last: ${LAST_COMMIT:0:60}"

  if [ "${DRY_RUN}" == "--dry-run" ]; then
    echo "    [DRY RUN] Would copy to ${ARCHIVE_DEST}/${REPO_NAME}"
  else
    # Copy with full git history
    cp -a "$REPO_PATH" "${ARCHIVE_DEST}/${REPO_NAME}" 2>/dev/null
    if [ $? -eq 0 ]; then
      # Mark source as archived
      echo "${MOVE_ID} ${TIMESTAMP} ${ARCHIVE_DEST}/${REPO_NAME}" > "${REPO_PATH}/.archived"

      # Generate manifest
      cat > "${ARCHIVE_DEST}/${REPO_NAME}/.archive-manifest.json" <<MANIFEST
{
  "archive_id": "${MOVE_ID}",
  "repo_name": "${REPO_NAME}",
  "source_path": "$(sql_escape "$REPO_PATH")",
  "archive_path": "${ARCHIVE_DEST}/${REPO_NAME}",
  "archived_at": "${TIMESTAMP}",
  "size_bytes": ${REPO_SIZE_BYTES},
  "git_remote": "$(sql_escape "$REMOTE_URL")",
  "git_branch": "${BRANCH}",
  "last_commit": "$(sql_escape "$LAST_COMMIT")",
  "archived_by": "NOIZY Code Mover v1.0"
}
MANIFEST

      # Log to D1
      d1_query "INSERT INTO archive_items (name, source_path, archive_path, file_type, size_bytes, archived_at, archive_id, status) VALUES ('$(sql_escape "$REPO_NAME")', '$(sql_escape "$REPO_PATH")', '$(sql_escape "${ARCHIVE_DEST}/${REPO_NAME}")', 'git_repo', ${REPO_SIZE_BYTES}, '${TIMESTAMP}', '${MOVE_ID}', 'archived')" 2>/dev/null || true

      MOVED_COUNT=$((MOVED_COUNT + 1))
      TOTAL_BYTES_MOVED=$((TOTAL_BYTES_MOVED + REPO_SIZE_BYTES))
      echo "    ✓ Archived successfully"
    else
      FAILED_COUNT=$((FAILED_COUNT + 1))
      echo "    ✗ FAILED to copy"
    fi
  fi
done

# Find standalone code projects (directories with package.json, Cargo.toml, etc.)
find "${SOURCE_PATH}" -maxdepth 3 \( -name "package.json" -o -name "Cargo.toml" -o -name "requirements.txt" -o -name "go.mod" \) -not -path "*/.git/*" -not -path "*/node_modules/*" 2>/dev/null | while read -r projfile; do
  PROJ_PATH=$(dirname "$projfile")

  # Skip if inside a git repo (already handled above)
  if [ -d "${PROJ_PATH}/.git" ] || [ -f "${PROJ_PATH}/.archived" ]; then
    continue
  fi

  PROJ_NAME=$(basename "$PROJ_PATH")
  echo "  CODE PROJECT (no git): ${PROJ_NAME} ($(basename "$projfile"))"

  if [ "${DRY_RUN}" != "--dry-run" ]; then
    PROJ_SIZE=$(du -sk "$PROJ_PATH" 2>/dev/null | cut -f1)
    mkdir -p "${ARCHIVE_DEST}/${PROJ_NAME}"
    cp -a "$PROJ_PATH" "${ARCHIVE_DEST}/${PROJ_NAME}" 2>/dev/null || true
    echo "${MOVE_ID} ${TIMESTAMP}" > "${PROJ_PATH}/.archived"
  fi
done

echo ""
echo "╔══════════════════════════════════════════════════╗"
echo "║  ARCHIVE COMPLETE                                ║"
echo "║  Move ID: ${MOVE_ID}                             ║"
echo "║  Moved:   ${MOVED_COUNT} repos                   ║"
echo "║  Skipped: ${SKIPPED_COUNT}                       ║"
echo "║  Failed:  ${FAILED_COUNT}                        ║"
echo "║  Bytes:   ${TOTAL_BYTES_MOVED}                   ║"
echo "╚══════════════════════════════════════════════════╝"
