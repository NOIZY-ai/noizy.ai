#!/usr/bin/env bash
# NOIZY Archive Scanner v1.0
# Run this on GOD (M2 Ultra) to scan drives and catalog files into D1
#
# Usage: ./archive-scanner.sh <volume_path> <device_name> <volume_name>
# Example: ./archive-scanner.sh /Volumes/ARCHIVE1 GOD ARCHIVE1
#
# Prerequisites:
#   - Cloudflare API token with D1 write access
#   - jq installed (brew install jq)
#   - curl installed
#
# Environment variables:
#   CLOUDFLARE_ACCOUNT_ID=2446d788cc4280f5ea22a9948410c355
#   CLOUDFLARE_API_TOKEN=<your_token>
#   CLOUDFLARE_D1_ID=e6f98279-656b-4f7a-979d-9197821193f5

set -euo pipefail

VOLUME_PATH="${1:?Usage: ./archive-scanner.sh <volume_path> <device_name> <volume_name>}"
DEVICE_NAME="${2:?Provide device name (GOD, GABRIEL, DAFIXER, MIKE, CLOUD)}"
VOLUME_NAME="${3:?Provide volume name (GOD_PRIMARY, ARCHIVE1, etc.)}"

ACCOUNT_ID="${CLOUDFLARE_ACCOUNT_ID:?Set CLOUDFLARE_ACCOUNT_ID}"
API_TOKEN="${CLOUDFLARE_API_TOKEN:?Set CLOUDFLARE_API_TOKEN}"
D1_ID="${CLOUDFLARE_D1_ID:-e6f98279-656b-4f7a-979d-9197821193f5}"

API_BASE="https://api.cloudflare.com/client/v4/accounts/${ACCOUNT_ID}/d1/database/${D1_ID}/query"

SCAN_ID="scan_$(date +%Y%m%d_%H%M%S)_${DEVICE_NAME}_${VOLUME_NAME}"
SCAN_START=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
BATCH_SIZE=50
BATCH_COUNT=0
TOTAL_FILES=0
TOTAL_DIRS=0
TOTAL_BYTES=0
CODE_FILES=0

# File extensions we consider "code"
CODE_EXTENSIONS="ts|js|tsx|jsx|py|rs|go|java|c|cpp|h|hpp|swift|kt|rb|php|sh|bash|zsh|sql|json|yaml|yml|toml|xml|html|css|scss|less|md|mdx|vue|svelte|astro|prisma|graphql|proto|tf|hcl|Dockerfile|Makefile|Gemfile|Rakefile|Cargo.toml|package.json|tsconfig.json|wrangler.toml"

echo "╔══════════════════════════════════════════════════╗"
echo "║  NOIZY ARCHIVE SCANNER v1.0                      ║"
echo "║  Device: ${DEVICE_NAME}                          ║"
echo "║  Volume: ${VOLUME_NAME}                          ║"
echo "║  Path:   ${VOLUME_PATH}                          ║"
echo "║  Scan:   ${SCAN_ID}                              ║"
echo "╚══════════════════════════════════════════════════╝"

# Function to execute D1 query
d1_query() {
  local sql="$1"
  curl -s -X POST "${API_BASE}" \
    -H "Authorization: Bearer ${API_TOKEN}" \
    -H "Content-Type: application/json" \
    -d "{\"sql\": \"${sql}\"}"
}

# Function to escape single quotes for SQL
sql_escape() {
  echo "$1" | sed "s/'/''/g"
}

# Update drive status
echo "[1/5] Updating drive status..."
d1_query "UPDATE audit_drives SET status = 'scanning', last_audit = '${SCAN_START}' WHERE device = '${DEVICE_NAME}' AND volume_name = '${VOLUME_NAME}'"

# Insert scan job
echo "[2/5] Creating scan job..."
d1_query "INSERT OR IGNORE INTO scan_jobs (id, status, started_at) VALUES ('${SCAN_ID}', 'running', '${SCAN_START}')" 2>/dev/null || true

# Scan for code directories (git repos)
echo "[3/5] Scanning for git repositories..."
REPO_COUNT=0
find "${VOLUME_PATH}" -maxdepth 5 -name ".git" -type d 2>/dev/null | while read -r gitdir; do
  REPO_PATH=$(dirname "$gitdir")
  REPO_NAME=$(basename "$REPO_PATH")
  REPO_PATH_ESC=$(sql_escape "$REPO_PATH")
  REPO_NAME_ESC=$(sql_escape "$REPO_NAME")

  # Get repo size
  REPO_SIZE=$(du -sk "$REPO_PATH" 2>/dev/null | cut -f1)
  REPO_SIZE_BYTES=$((REPO_SIZE * 1024))

  # Count files in repo
  REPO_FILE_COUNT=$(find "$REPO_PATH" -type f -not -path '*/.git/*' 2>/dev/null | wc -l | tr -d ' ')

  # Get last commit date if possible
  LAST_COMMIT=$(cd "$REPO_PATH" && git log -1 --format="%aI" 2>/dev/null || echo "unknown")
  LAST_COMMIT_ESC=$(sql_escape "$LAST_COMMIT")

  # Get remote URL
  REMOTE_URL=$(cd "$REPO_PATH" && git remote get-url origin 2>/dev/null || echo "none")
  REMOTE_URL_ESC=$(sql_escape "$REMOTE_URL")

  echo "  REPO: ${REPO_NAME} (${REPO_FILE_COUNT} files, ${REPO_SIZE}KB)"

  d1_query "INSERT INTO audit_files (scan_id, device, volume, file_path, file_name, file_type, file_size_bytes, is_code, is_git_repo, git_remote, last_modified, created_at) VALUES ('${SCAN_ID}', '${DEVICE_NAME}', '${VOLUME_NAME}', '${REPO_PATH_ESC}', '${REPO_NAME_ESC}', 'git_repo', ${REPO_SIZE_BYTES}, 1, 1, '${REMOTE_URL_ESC}', '${LAST_COMMIT_ESC}', '${SCAN_START}')" 2>/dev/null || true

  REPO_COUNT=$((REPO_COUNT + 1))
done
echo "  Found ${REPO_COUNT} git repositories"

# Scan for code files outside git repos
echo "[4/5] Scanning for standalone code files..."
find "${VOLUME_PATH}" -maxdepth 4 -type f \( \
  -name "*.ts" -o -name "*.js" -o -name "*.tsx" -o -name "*.jsx" \
  -o -name "*.py" -o -name "*.rs" -o -name "*.go" -o -name "*.java" \
  -o -name "*.swift" -o -name "*.c" -o -name "*.cpp" -o -name "*.h" \
  -o -name "*.rb" -o -name "*.php" -o -name "*.sh" \
  -o -name "package.json" -o -name "Cargo.toml" -o -name "Makefile" \
  -o -name "Dockerfile" -o -name "wrangler.toml" -o -name "*.sql" \
  \) -not -path "*/.git/*" -not -path "*/node_modules/*" -not -path "*/.next/*" \
  2>/dev/null | head -5000 | while read -r filepath; do

  FILENAME=$(basename "$filepath")
  FILESIZE=$(stat -f%z "$filepath" 2>/dev/null || stat --format=%s "$filepath" 2>/dev/null || echo 0)
  FILEPATH_ESC=$(sql_escape "$filepath")
  FILENAME_ESC=$(sql_escape "$FILENAME")
  EXT="${FILENAME##*.}"

  TOTAL_FILES=$((TOTAL_FILES + 1))
  CODE_FILES=$((CODE_FILES + 1))

  # Batch insert (log every 100)
  if [ $((TOTAL_FILES % 100)) -eq 0 ]; then
    echo "  Scanned ${TOTAL_FILES} code files..."
  fi
done

# Generate summary
echo "[5/5] Generating summary..."
SCAN_END=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Get volume stats
if [ -d "${VOLUME_PATH}" ]; then
  VOLUME_TOTAL=$(df -k "${VOLUME_PATH}" 2>/dev/null | tail -1 | awk '{print $2 * 1024}')
  VOLUME_USED=$(df -k "${VOLUME_PATH}" 2>/dev/null | tail -1 | awk '{print $3 * 1024}')
  VOLUME_FREE=$(df -k "${VOLUME_PATH}" 2>/dev/null | tail -1 | awk '{print $4 * 1024}')

  d1_query "UPDATE audit_drives SET total_bytes = ${VOLUME_TOTAL:-0}, used_bytes = ${VOLUME_USED:-0}, free_bytes = ${VOLUME_FREE:-0}, status = 'scanned', last_audit = '${SCAN_END}' WHERE device = '${DEVICE_NAME}' AND volume_name = '${VOLUME_NAME}'"
fi

d1_query "INSERT INTO audit_summary (scan_id, device, volume, total_files, total_dirs, total_bytes, code_files, git_repos, started_at, completed_at) VALUES ('${SCAN_ID}', '${DEVICE_NAME}', '${VOLUME_NAME}', ${TOTAL_FILES}, ${TOTAL_DIRS}, ${TOTAL_BYTES}, ${CODE_FILES}, 0, '${SCAN_START}', '${SCAN_END}')" 2>/dev/null || true

echo ""
echo "╔══════════════════════════════════════════════════╗"
echo "║  SCAN COMPLETE                                   ║"
echo "║  Scan ID: ${SCAN_ID}                             ║"
echo "║  Started: ${SCAN_START}                          ║"
echo "║  Ended:   ${SCAN_END}                            ║"
echo "╚══════════════════════════════════════════════════╝"
echo ""
echo "Results stored in D1: aquarium-archive"
echo "View in The Aquarium dashboard or query D1 directly."
