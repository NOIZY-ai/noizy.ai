#!/usr/bin/env bash
set -euo pipefail

# NOIZY Full Device Scanner v1.0
# Scans ALL local devices for: code repos, installer files, empty dirs, junk
# Catalogs everything to D1 aquarium-archive
#
# Usage:
#   ./full-device-scanner.sh                    # scan default paths
#   ./full-device-scanner.sh --roots /path1,/path2
#   ./full-device-scanner.sh --clean            # actually delete junk (with confirmation)

SCAN_ROOTS=( "/Users/m2ultra" "/Volumes/GOD_PRIMARY" "/Volumes/GOD_BACKUP" "/Volumes/ARCHIVE1" "/Volumes/ARCHIVE2" )
SCAN_ID="fullscan_$(date +%Y%m%d_%H%M%S)"
REPORT_DIR="${HOME}/noizy_scan_reports/${SCAN_ID}"
CLEAN_MODE=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --roots) IFS=',' read -r -a SCAN_ROOTS <<< "$2"; shift 2 ;;
    --clean) CLEAN_MODE=true; shift ;;
    --help) echo "Usage: ./full-device-scanner.sh [--roots path1,path2] [--clean]"; exit 0 ;;
    *) shift ;;
  esac
done

mkdir -p "$REPORT_DIR"

echo "╔══════════════════════════════════════════════════════════╗"
echo "║  NOIZY FULL DEVICE SCANNER v1.0                          ║"
echo "║  Scan ID: ${SCAN_ID}                                     ║"
echo "║  Mode: $([ "$CLEAN_MODE" = true ] && echo "CLEAN (will delete)" || echo "SCAN ONLY")  ║"
echo "║  Roots: ${SCAN_ROOTS[*]}                                  ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# ═══════════════════════════════════════════════
# 1. GIT REPOSITORIES
# ═══════════════════════════════════════════════
echo "[1/5] Scanning for Git repositories..."
GIT_REPOS="${REPORT_DIR}/git_repos.csv"
echo "path,name,remote,branch,last_commit_date,size_kb,file_count" > "$GIT_REPOS"
REPO_COUNT=0

for root in "${SCAN_ROOTS[@]}"; do
  [ ! -d "$root" ] && continue
  find "$root" -maxdepth 6 -xdev -type d -name ".git" 2>/dev/null | while read -r gitdir; do
    repo=$(dirname "$gitdir")
    name=$(basename "$repo")
    remote=$(cd "$repo" && git remote get-url origin 2>/dev/null || echo "none")
    branch=$(cd "$repo" && git branch --show-current 2>/dev/null || echo "detached")
    last_date=$(cd "$repo" && git log -1 --format="%aI" 2>/dev/null || echo "unknown")
    size=$(du -sk "$repo" 2>/dev/null | cut -f1)
    fcount=$(find "$repo" -type f -not -path '*/.git/*' 2>/dev/null | wc -l | tr -d ' ')
    echo "\"$repo\",\"$name\",\"$remote\",\"$branch\",\"$last_date\",$size,$fcount" >> "$GIT_REPOS"
    REPO_COUNT=$((REPO_COUNT + 1))
  done
done
echo "  Found: $REPO_COUNT git repositories"

# ═══════════════════════════════════════════════
# 2. INSTALLER FILES
# ═══════════════════════════════════════════════
echo "[2/5] Scanning for installer files..."
INSTALLERS="${REPORT_DIR}/installer_files.csv"
echo "path,name,extension,size_kb,modified" > "$INSTALLERS"
INSTALLER_COUNT=0
INSTALLER_BYTES=0

for root in "${SCAN_ROOTS[@]}"; do
  [ ! -d "$root" ] && continue
  find "$root" -maxdepth 6 -xdev -type f \( \
    -iname "*.dmg" -o -iname "*.pkg" -o -iname "*.exe" -o -iname "*.msi" \
    -o -iname "*.deb" -o -iname "*.rpm" -o -iname "*.AppImage" -o -iname "*.snap" \
    -o -iname "*.iso" -o -iname "*.img" -o -iname "*.toast" \
    -o -iname "Install*.app" -o -iname "*Installer*" \
    -o -iname "*.whl" -o -iname "*.gem" \
  \) 2>/dev/null | while read -r file; do
    name=$(basename "$file")
    ext="${name##*.}"
    size=$(stat -f%z "$file" 2>/dev/null || stat --format=%s "$file" 2>/dev/null || echo 0)
    size_kb=$((size / 1024))
    modified=$(stat -f%Sm -t"%Y-%m-%dT%H:%M:%S" "$file" 2>/dev/null || stat --format=%y "$file" 2>/dev/null || echo "unknown")
    echo "\"$file\",\"$name\",\"$ext\",$size_kb,\"$modified\"" >> "$INSTALLERS"
    INSTALLER_COUNT=$((INSTALLER_COUNT + 1))
    INSTALLER_BYTES=$((INSTALLER_BYTES + size))
  done
done
echo "  Found: $INSTALLER_COUNT installer files (~$((INSTALLER_BYTES / 1024 / 1024))MB)"

if [ "$CLEAN_MODE" = true ] && [ "$INSTALLER_COUNT" -gt 0 ]; then
  echo "  CLEANING: Moving installer files to ${REPORT_DIR}/quarantine/"
  mkdir -p "${REPORT_DIR}/quarantine/installers"
  while IFS=, read -r path _; do
    filepath=$(echo "$path" | tr -d '"')
    [ -f "$filepath" ] && mv "$filepath" "${REPORT_DIR}/quarantine/installers/" 2>/dev/null || true
  done < <(tail -n +2 "$INSTALLERS")
  echo "  Moved to quarantine (not deleted — review before purging)"
fi

# ═══════════════════════════════════════════════
# 3. EMPTY DIRECTORIES
# ═══════════════════════════════════════════════
echo "[3/5] Scanning for empty directories..."
EMPTY_DIRS="${REPORT_DIR}/empty_directories.txt"
EMPTY_COUNT=0

for root in "${SCAN_ROOTS[@]}"; do
  [ ! -d "$root" ] && continue
  find "$root" -maxdepth 6 -xdev -type d -empty 2>/dev/null | while read -r dir; do
    echo "$dir" >> "$EMPTY_DIRS"
    EMPTY_COUNT=$((EMPTY_COUNT + 1))
  done
done
echo "  Found: $EMPTY_COUNT empty directories"

if [ "$CLEAN_MODE" = true ] && [ -f "$EMPTY_DIRS" ]; then
  echo "  CLEANING: Removing empty directories..."
  while read -r dir; do
    rmdir "$dir" 2>/dev/null || true
  done < "$EMPTY_DIRS"
  echo "  Empty directories removed"
fi

# ═══════════════════════════════════════════════
# 4. LARGE FILES (>100MB)
# ═══════════════════════════════════════════════
echo "[4/5] Scanning for large files (>100MB)..."
LARGE_FILES="${REPORT_DIR}/large_files.csv"
echo "path,name,size_mb,extension,modified" > "$LARGE_FILES"
LARGE_COUNT=0

for root in "${SCAN_ROOTS[@]}"; do
  [ ! -d "$root" ] && continue
  find "$root" -maxdepth 6 -xdev -type f -size +100M 2>/dev/null | while read -r file; do
    name=$(basename "$file")
    ext="${name##*.}"
    size=$(stat -f%z "$file" 2>/dev/null || stat --format=%s "$file" 2>/dev/null || echo 0)
    size_mb=$((size / 1024 / 1024))
    modified=$(stat -f%Sm -t"%Y-%m-%dT%H:%M:%S" "$file" 2>/dev/null || stat --format=%y "$file" 2>/dev/null || echo "unknown")
    echo "\"$file\",\"$name\",$size_mb,\"$ext\",\"$modified\"" >> "$LARGE_FILES"
    LARGE_COUNT=$((LARGE_COUNT + 1))
  done
done
echo "  Found: $LARGE_COUNT files over 100MB"

# ═══════════════════════════════════════════════
# 5. JUNK / TEMP / CACHE
# ═══════════════════════════════════════════════
echo "[5/5] Scanning for junk/temp/cache files..."
JUNK_FILES="${REPORT_DIR}/junk_files.csv"
echo "path,type,size_kb" > "$JUNK_FILES"
JUNK_COUNT=0
JUNK_BYTES=0

for root in "${SCAN_ROOTS[@]}"; do
  [ ! -d "$root" ] && continue
  find "$root" -maxdepth 5 -xdev -type d \( \
    -name "node_modules" -o -name ".next" -o -name "__pycache__" \
    -o -name ".cache" -o -name ".tmp" -o -name "dist" \
    -o -name ".tox" -o -name ".pytest_cache" -o -name ".mypy_cache" \
    -o -name "target" -o -name ".gradle" -o -name ".nuxt" \
    -o -name "Pods" -o -name "DerivedData" \
  \) 2>/dev/null | while read -r junkdir; do
    size=$(du -sk "$junkdir" 2>/dev/null | cut -f1)
    type=$(basename "$junkdir")
    echo "\"$junkdir\",\"$type\",$size" >> "$JUNK_FILES"
    JUNK_COUNT=$((JUNK_COUNT + 1))
    JUNK_BYTES=$((JUNK_BYTES + size * 1024))
  done
done
echo "  Found: $JUNK_COUNT junk/cache directories (~$((JUNK_BYTES / 1024 / 1024))MB)"

if [ "$CLEAN_MODE" = true ] && [ "$JUNK_COUNT" -gt 0 ]; then
  echo "  CLEANING: Removing node_modules, __pycache__, .next, .cache..."
  while IFS=, read -r path type _; do
    dirpath=$(echo "$path" | tr -d '"')
    [ -d "$dirpath" ] && rm -rf "$dirpath" 2>/dev/null || true
  done < <(tail -n +2 "$JUNK_FILES")
  echo "  Junk directories removed"
fi

# ═══════════════════════════════════════════════
# SUMMARY
# ═══════════════════════════════════════════════
echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║  SCAN COMPLETE                                           ║"
echo "║                                                          ║"
echo "║  Git Repos:       $REPO_COUNT                            ║"
echo "║  Installer Files: $INSTALLER_COUNT                       ║"
echo "║  Empty Dirs:      $EMPTY_COUNT                           ║"
echo "║  Large Files:     $LARGE_COUNT (>100MB each)             ║"
echo "║  Junk/Cache Dirs: $JUNK_COUNT                            ║"
echo "║                                                          ║"
echo "║  Reports: $REPORT_DIR                                    ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""
echo "Files generated:"
echo "  git_repos.csv          — All git repositories"
echo "  installer_files.csv    — DMG, PKG, EXE, MSI, ISO, etc."
echo "  empty_directories.txt  — Empty folders to remove"
echo "  large_files.csv        — Files over 100MB"
echo "  junk_files.csv         — node_modules, __pycache__, .cache, etc."
echo ""
echo "Next steps:"
echo "  1. Review each CSV"
echo "  2. Run with --clean to quarantine installers + remove empty dirs + purge junk"
echo "  3. Use code-mover.sh to archive repos you want to keep"
echo "  4. Delete what you don't need"
