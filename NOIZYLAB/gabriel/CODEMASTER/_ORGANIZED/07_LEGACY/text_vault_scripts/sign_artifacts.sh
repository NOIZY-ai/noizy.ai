#!/usr/bin/env bash
# sign_artifacts.sh - Sign artifacts with checksums and optional GPG
# Usage: ./sign_artifacts.sh [artifacts_dir]
set -euo pipefail

DIR="${1:-artifacts}"
GPG_KEY="${GPG_KEY_ID:-}"

echo "═══════════════════════════════════════════════════════════"
echo "SIGN ARTIFACTS"
echo "═══════════════════════════════════════════════════════════"

# Import GPG key if provided
if [ -n "${GPG_PRIVATE_KEY:-}" ]; then
    echo "Importing GPG key..."
    echo "$GPG_PRIVATE_KEY" | gpg --batch --import 2>/dev/null || true
fi

# Find and sign artifacts
MANIFEST="$DIR/manifest.json"
echo "{\"files\":[" > "$MANIFEST"
FIRST=true

for f in "$DIR"/*.json "$DIR"/*.txt "$DIR"/*.sh; do
    [ -f "$f" ] || continue
    [[ "$f" == *.sha256 ]] && continue
    [[ "$f" == *.sha512 ]] && continue
    [[ "$f" == *.asc ]] && continue
    [[ "$f" == *manifest.json ]] && continue

    NAME=$(basename "$f")
    SHA256=$(sha256sum "$f" | cut -d' ' -f1)
    
    # Write checksum
    echo "$SHA256  $NAME" > "$f.sha256"
    echo "  ✅ $NAME"
    echo "     SHA256: ${SHA256:0:16}..."
    
    # GPG sign if key available
    GPG_SIGNED=false
    if [ -n "$GPG_KEY" ]; then
        if gpg --batch --yes --local-user "$GPG_KEY" --detach-sign --armor --output "$f.asc" "$f" 2>/dev/null; then
            GPG_SIGNED=true
            echo "     GPG: signed"
        fi
    fi
    
    # Add to manifest
    if [ "$FIRST" = true ]; then
        FIRST=false
    else
        echo "," >> "$MANIFEST"
    fi
    echo "{\"name\":\"$NAME\",\"sha256\":\"$SHA256\",\"gpg_signed\":$GPG_SIGNED}" >> "$MANIFEST"
done

echo "]}" >> "$MANIFEST"

# Sign manifest
if [ -n "$GPG_KEY" ]; then
    gpg --batch --yes --local-user "$GPG_KEY" --detach-sign --armor --output "$MANIFEST.asc" "$MANIFEST" 2>/dev/null || true
fi

echo ""
echo "✅ Manifest: $MANIFEST"
echo "═══════════════════════════════════════════════════════════"
