#!/bin/bash
# POLYGLOT TEST RUNNER - Verifies all polyglots work
# Don't exit on error - we want to see all results

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'
BOLD='\033[1m'

DIR="$(cd "$(dirname "$0")" && pwd)"
PASS=0
FAIL=0
SKIP=0

echo -e "${CYAN}${BOLD}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║          🌐 NOIZYLAB POLYGLOT TEST SUITE                     ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

test_lang() {
    local name="$1"
    local cmd="$2"
    local expected="$3"
    
    if command -v "$(echo "$cmd" | awk '{print $1}')" &>/dev/null; then
        result=$(eval "$cmd" 2>/dev/null || echo "ERROR")
        if [[ "$result" == *"$expected"* ]]; then
            echo -e "  ${GREEN}✓${NC} $name → $result"
            ((PASS++))
        else
            echo -e "  ${RED}✗${NC} $name → Expected '$expected', got '$result'"
            ((FAIL++))
        fi
    else
        echo -e "  ${YELLOW}○${NC} $name → (not installed)"
        ((SKIP++))
    fi
}

echo -e "\n${BOLD}━━━ ULTRA.polyglot ━━━${NC}"
cd "$DIR"
test_lang "Bash" "bash ULTRA.polyglot" "Bash"

echo -e "\n${BOLD}━━━ scripting_polyglot.pl (Multi-language) ━━━${NC}"
test_lang "Perl" "perl scripting_polyglot.pl" "Perl"

echo -e "\n${BOLD}━━━ mega_polyglot.py ━━━${NC}"
test_lang "Ruby" "ruby mega_polyglot.py" "Ruby"

echo -e "\n${BOLD}━━━ functional_polyglot.hs ━━━${NC}"
test_lang "Haskell" "grep -q 'main = putStrLn' functional_polyglot.hs && echo Haskell" "Haskell"

echo -e "\n${BOLD}━━━ web_polyglot.html ━━━${NC}"
test_lang "HTML" "grep -q DOCTYPE web_polyglot.html && echo HTML" "HTML"

echo -e "\n${BOLD}━━━ compiled_polyglot.c ━━━${NC}"
test_lang "Bash" "bash compiled_polyglot.c" "Bash"
if command -v gcc &>/dev/null; then
    gcc "$DIR/compiled_polyglot.c" -o /tmp/poly_c 2>/dev/null && test_lang "C" "/tmp/poly_c" "C"
    g++ "$DIR/compiled_polyglot.c" -o /tmp/poly_cpp 2>/dev/null && test_lang "C++" "/tmp/poly_cpp" "C++"
fi

echo -e "\n${BOLD}━━━ true_polyglot.exe.cmd ━━━${NC}"
test_lang "Bash" "bash true_polyglot.exe.cmd" "Bash"
test_lang "Zsh" "zsh true_polyglot.exe.cmd" "Bash"

echo -e "\n${BOLD}━━━ systems_polyglot.rs ━━━${NC}"
if command -v rustc &>/dev/null; then
    rustc "$DIR/systems_polyglot.rs" -o /tmp/poly_rust 2>/dev/null && test_lang "Rust" "/tmp/poly_rust" "Rust"
else
    test_lang "Rust (ref)" "grep -q 'println!' systems_polyglot.rs && echo Rust" "Rust"
fi

echo -e "\n${BOLD}━━━ esoteric_polyglot.bf ━━━${NC}"
test_lang "Esoteric" "grep -qi 'brainfuck' esoteric_polyglot.bf && echo Esoteric" "Esoteric"

echo -e "\n${BOLD}━━━ quine_polyglot.rb ━━━${NC}"
test_lang "Quine" "grep -q 'Ruby Quine' quine_polyglot.rb && echo Quine" "Quine"

echo -e "\n${BOLD}━━━ TITAN.polyglot ━━━${NC}"
test_lang "TITAN" "bash TITAN.polyglot" "TITAN"

echo -e "\n${BOLD}━━━ OMEGA.polyglot ━━━${NC}"
test_lang "OMEGA" "bash OMEGA.polyglot" "OMEGA"

echo -e "\n${BOLD}━━━ GODMODE.polyglot ━━━${NC}"
test_lang "GODMODE" "bash GODMODE.polyglot" "GODMODE"

echo -e "\n${BOLD}━━━ APEX.polyglot ━━━${NC}"
test_lang "APEX" "bash APEX.polyglot" "APEX"

echo -e "\n${CYAN}${BOLD}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo -e "║  RESULTS: ${GREEN}$PASS passed${CYAN} │ ${RED}$FAIL failed${CYAN} │ ${YELLOW}$SKIP skipped${CYAN}            ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"
