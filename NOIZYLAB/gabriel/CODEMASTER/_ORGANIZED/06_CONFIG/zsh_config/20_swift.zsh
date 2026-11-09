# ============================================================================
# Swift Development Environment Configuration
# ============================================================================
# Loaded automatically by ~/.zshrc modular configuration system

# Swiftly Swift Version Manager
export SWIFTLY_HOME_DIR="$HOME/.swiftly"
export SWIFTLY_BIN_DIR="$SWIFTLY_HOME_DIR/bin"
if [ -f "$SWIFTLY_HOME_DIR/env.sh" ]; then
    . "$SWIFTLY_HOME_DIR/env.sh"
fi

# Swift Package Manager cache
export SPM_CACHE_DIR="$HOME/.swiftpm"

# SourceKit-LSP for IDE support
export SOURCEKIT_TOOLCHAIN_PATH="$HOME/.swiftly/toolchains/swift-latest"

# Swift aliases
alias sw='swift'
alias swb='swift build'
alias swr='swift run'
alias swt='swift test'
alias swp='swift package'
alias swpi='swift package init'
alias swpx='swift package init --type executable'
alias swpl='swift package init --type library'
alias swpu='swift package update'
alias swpr='swift package resolve'
alias swpg='swift package generate-xcodeproj'
alias swpd='swift package describe'
alias swps='swift package show-dependencies'
alias swpc='swift package clean'

# Swiftly aliases
alias swy='swiftly'
alias swyl='swiftly list'
alias swyla='swiftly list-available'
alias swyi='swiftly install'
alias swyu='swiftly use'
alias swyup='swiftly update'

# Swift REPL
alias swrepl='swift repl'

# SwiftFormat aliases
alias sfmt='swiftformat .'
alias sfmtc='swiftformat --lint .'

# SwiftLint aliases
alias slint='swiftlint'
alias slintf='swiftlint --fix'
alias slinta='swiftlint analyze'

# Vapor aliases (if using Vapor framework)
alias vap='vapor'
alias vapn='vapor new'
alias vapb='vapor build'
alias vapr='vapor run'
alias vapt='vapor test'

# XcodeGen alias
alias xgen='xcodegen generate'

# Sourcery alias
alias srcry='sourcery'

# Periphery (dead code detection)
alias peri='periphery scan'

# Xcodes (Xcode version manager)
alias xc='xcodes'
alias xcl='xcodes list'
alias xci='xcodes install'

# ios-deploy
alias iod='ios-deploy'
alias iodr='ios-deploy --debug'

# Mint (Swift package manager for CLI tools)
alias mnt='mint'
alias mnti='mint install'
alias mntl='mint list'

# Quick build and run
swbr() {
    swift build && swift run "$@"
}

# Create new Swift executable package
swpnew() {
    local name="${1:-MyApp}"
    mkdir -p "$name" && cd "$name" && swift package init --type executable
    echo "Created new Swift executable package: $name"
}

# Create new Swift library package
swplib() {
    local name="${1:-MyLibrary}"
    mkdir -p "$name" && cd "$name" && swift package init --type library
    echo "Created new Swift library package: $name"
}

# Format and lint
swcheck() {
    echo "Running SwiftFormat..."
    swiftformat .
    echo "Running SwiftLint..."
    swiftlint
}

# Clean build artifacts
swclean() {
    rm -rf .build
    rm -rf .swiftpm
    rm -rf *.xcodeproj
    rm -rf Package.resolved
    echo "Swift build artifacts cleaned"
}

# Show current Swift version info
swinfo() {
    echo "=== Swift Environment Info ==="
    echo "Swiftly version: $(swiftly --version 2>/dev/null || echo 'Not found')"
    echo ""
    swiftly list
    echo ""
    echo "Active Swift:"
    swift --version
    echo ""
    echo "Swift path: $(which swift)"
    echo "SwiftFormat: $(swiftformat --version 2>/dev/null || echo 'Not found')"
    echo "SwiftLint: $(swiftlint version 2>/dev/null || echo 'Not found')"
}

echo "Swift Development Environment loaded."
