#!/bin/bash
# EXTENSION CLEANUP SCRIPT - NUKE REDUNDANT EXTENSIONS
# Run: chmod +x nuke_extensions.sh && ./nuke_extensions.sh

EXT_DIR="$HOME/.vscode/extensions"
BACKUP_DIR="$HOME/.vscode/extensions_backup_$(date +%Y%m%d_%H%M%S)"

echo "🔥 EXTENSION NUKE SCRIPT 🔥"
echo "================================"
echo "Extensions directory: $EXT_DIR"

# Create backup
echo "📦 Creating backup at: $BACKUP_DIR"
mkdir -p "$BACKUP_DIR"

# Extensions to NUKE (redundant AI assistants, old versions, duplicates)
NUKE_LIST=(
    # OLD VERSIONS (keep latest only)
    "anthropic.claude-code-2.0.37*"
    "anthropic.claude-code-2.0.72*"
    "openai.chatgpt-0.4.51"
    "saoudrizwan.claude-dev-3.44*"
    "vadimcn.vscode-lldb-1.11.7"
    "ms-python.python-2025.20.0*"
    "ms-vscode.powershell-2025.4*"
    
    # REDUNDANT AI ASSISTANTS (pick one, nuke the rest)
    "alvaai.alva*"
    "ayushsinghal.code-mate*"
    "bito.bito*"
    "codium.codium*"
    "danielsanmedium.dscodegpt*"
    "feiskyer.chatgpt-copilot*"
    "fittentech.fitten-code*"
    "genieai.chatgpt-vscode*"
    "kodezi.kodezi*"
    "maneetio.devpal*"
    "parallel-universe.gpt-copilot*"
    "sixth.sixth-ai*"
    "taldennis-unfoldai-chatgpt-copilot.unfoldai*"
    "visca-ai.visca-copilot*"
    "visca-ai.wirtual-remote*"
    "romyrianata.fix-augment*"
    
    # BUILT-IN FEATURES (now in VS Code core)
    "bracketpaircolordlw.bracket-pair-color-dlw*"
    "formulahendry.auto-close-tag*"
    "formulahendry.auto-complete-tag*"
    "formulahendry.auto-rename-tag*"
    
    # REDUNDANT ICON THEMES (keep one)
    "be5invis.vscode-icontheme-nomo-dark*"
    "emmanuelbeziat.vscode-great-icons*"
    "file-icons.file-icons*"
    # keeping: vscode-icons-team.vscode-icons + pkief.material-icon-theme
    
    # REDUNDANT THEMES (keep 2-3 favorites)
    "arcticicestudio.nord-visual-studio-code*"
    "daylerees.rainglow*"
    "drywolf.dark-plus-plus-theme*"
    "johnpapa.winteriscoming*"
    "robbowen.synthwave-vscode*"
    "rokoroku.vscode-theme-darcula*"
    "wesbos.theme-cobalt2*"
    "whizkydee.material-palenight-theme*"
    # keeping: dracula, tokyo-night, one-dark-pro, github-theme
    
    # ORPHANED/TEMP DIRECTORIES (GUID folders)
    ".0d4fe9d2*"
    ".0d54957d*"
    ".13022cf6*"
    ".1911bce9*"
    ".1ab1fc0d*"
    ".2599819a*"
    ".37703ddd*"
    ".40613873*"
    ".42bdc12a*"
    ".43dbf76f*"
    ".4cc47fe6*"
    ".4d995ccc*"
    ".4ee2c3b1*"
    ".529af3ab*"
    ".56905d42*"
    ".645ac35f*"
    ".70379a18*"
    ".738dab5d*"
    ".76139daa*"
    ".76dbb062*"
    ".79381df0*"
    ".9381282c*"
    ".95a5cd01*"
    ".96f5af40*"
    ".a278e64e*"
    ".a5e7c924*"
    ".a6e9d79e*"
    ".a84d27f7*"
    ".ab774350*"
    ".bd377afb*"
    ".c797022f*"
    ".cf1816ac*"
    ".cf249609*"
    ".e107cb3f*"
    ".e35f07f8*"
    ".e525f5d8*"
    ".ed5e5d3c*"
    ".ee0d76c0*"
    ".f3cc1f44*"
    ".f75a1f33*"
    
    # RARELY USED / NICHE
    "anzory.vscode-gppl-support*"
    "bmpenuelas.waveform-render*"
    "codestream.codestream*"
    "emrecebeci.soundsyntax*"
    "geli.spellinguo*"
    "huacnlee.autocorrect*"
    "hypnodroid.paper-cranes-shader*"
    "kennyreyes.vscode-sound-notification*"
    "loyio.nand2tetris-vscode*"
    "luckyxmobile.speechify*"
    "quantumpannonia.cue-sheet-audio*"
    "skyrocket-qy.whisper*"
    "speak-y.speech-to-text-whisper*"
    "spikespaz.vscode-smoothtype*"
    "vivekpal.sound-in-code*"
    "wsa.web-systems*"
    "xuangeaha.chartjs*"
    "xuangeaha.just-enough-git*"
    "xuangeaha.just-print-it*"
    "xuangeaha.print-divider*"
    "xuangeaha.vsmarketplace-badges*"
    
    # REDUNDANT EXTENSION PACKS (bloat)
    "4bde9604-932c-638d-b5d2-db273992f59c.front-end-extension-gold-pack*"
    "afractal.node-essentials*"
    "ajweb.aj-angular-php-r-plus-pack*"
    "c0der-himel.vscode-wev-dev-extension-pack*"
    "devboosts.angular-productivity-pack*"
    "donjayamanne.git-extension-pack*"
    "donjayamanne.python-extension-pack*"
    "gydunhn.angular-essentials*"
    "gydunhn.html-essentials*"
    "gydunhn.javascript-essentials*"
    "gydunhn.typescript-essentials*"
    "gydunhn.vsc-essentials*"
    "gydunhn.vsc-essentials-core*"
    "gydunhn.vsc-essentials-material-themes*"
    "gydunhn.vsc-essentials-themes-core*"
    "imgildev.vscode-angular-ts-pack*"
    "jabacchetta.vscode-essentials*"
    "jawandarajbir.react-vscode-extension-pack*"
    "kr4is.cpptools-extension-pack*"
    "leojhonsong.python-extension-pack*"
    "loiane.angular-extension-pack*"
    "mubaidr.vuejs-extension-pack*"
    "nodesource.vscode-for-node-js-development-pack*"
    "seyyedkhandon.epack*"
    "seyyedkhandon.fpack*"
    "seyyedkhandon.gpack*"
    "seyyedkhandon.qpack*"
    "seyyedkhandon.tpack*"
    "seyyedkhandon.zpack*"
    "sgryt.typescript-pack*"
    "vimlesai.front-end-ext-pack*"
    "walkme.games-dev-extension-pack*"
    "wallabyjs.wallaby-extension-pack*"
    "davidvfischer.python-essentials-extension*"
    "demystifying-javascript.python-extensions-pack*"
    "alishobeiri.swift-development*"
)

NUKED=0
FAILED=0

for pattern in "${NUKE_LIST[@]}"; do
    for ext in "$EXT_DIR"/$pattern; do
        if [ -e "$ext" ]; then
            name=$(basename "$ext")
            echo "🗑️  Nuking: $name"
            mv "$ext" "$BACKUP_DIR/" 2>/dev/null
            if [ $? -eq 0 ]; then
                ((NUKED++))
            else
                echo "   ⚠️  Failed to move: $name"
                ((FAILED++))
            fi
        fi
    done
done

echo ""
echo "================================"
echo "✅ NUKED: $NUKED extensions"
echo "⚠️  FAILED: $FAILED"
echo "📦 BACKUP: $BACKUP_DIR"
echo ""
echo "🔄 Restart VS Code to apply changes!"
echo ""
echo "To restore all: mv $BACKUP_DIR/* $EXT_DIR/"
echo "To permanently delete backup: rm -rf $BACKUP_DIR"
