#!/bin/bash
################################################################################
# TURBO & GABRIEL Search Script
# 
# This script performs a comprehensive search for "TURBO" and "GABRIEL" 
# occurrences in the repository.
#
# Usage: ./find_turbo_gabriel.sh [repository_root]
#   If repository_root is not provided, auto-detects using git or uses current directory
################################################################################

set -e

# Determine repository root dynamically
REPO_ROOT="${1:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}"
REPORT_FILE="search_results_$(date +%Y%m%d_%H%M%S).txt"

echo "================================================================================"
echo "TURBO & GABRIEL Comprehensive Search"
echo "================================================================================"
echo "Repository: $REPO_ROOT"
echo "Date: $(date)"
echo "Report File: $REPORT_FILE"
echo ""

# Function to search for a term
search_term() {
    local term=$1
    local term_lower=$(echo "$term" | tr '[:upper:]' '[:lower:]')
    
    echo "--------------------------------------------------------------------------------"
    echo "Searching for: $term (case-insensitive)"
    echo "--------------------------------------------------------------------------------"
    
    # Count occurrences in all files
    echo "1. Searching in all files..."
    local count=$(grep -ri "$term_lower" "$REPO_ROOT" 2>/dev/null | grep -v ".git" | wc -l || echo "0")
    echo "   Total matches: $count"
    
    if [ "$count" -gt 0 ]; then
        echo ""
        echo "   Files containing '$term':"
        grep -ril "$term_lower" "$REPO_ROOT" 2>/dev/null | grep -v ".git" || echo "   (none)"
        echo ""
        echo "   Detailed matches:"
        grep -rin "$term_lower" "$REPO_ROOT" 2>/dev/null | grep -v ".git" || echo "   (none)"
    fi
    
    # Search in specific file types
    echo ""
    echo "2. Searching in C/C++ source files..."
    find "$REPO_ROOT" \( -name "*.c" -o -name "*.cpp" -o -name "*.h" -o -name "*.hpp" \) \
        -exec grep -l -i "$term_lower" {} \; 2>/dev/null || echo "   No matches in C/C++ files"
    
    echo ""
    echo "3. Searching in build files..."
    find "$REPO_ROOT" \( -name "Makefile" -o -name "*.mk" -o -name "*.gradle" -o -name "meson.build" \) \
        -exec grep -l -i "$term_lower" {} \; 2>/dev/null || echo "   No matches in build files"
    
    echo ""
    echo "4. Searching in documentation..."
    find "$REPO_ROOT" \( -name "*.md" -o -name "*.txt" -o -name "README*" -o -name "CONTRIBUTORS" \) \
        -exec grep -l -i "$term_lower" {} \; 2>/dev/null | grep -v ".git" || echo "   No matches in documentation"
    
    echo ""
    echo "5. Searching in git history..."
    cd "$REPO_ROOT"
    git log --all --format="%H %s" --grep="$term_lower" -i 2>/dev/null || echo "   No matches in git history"
    
    echo ""
    echo "6. Searching in git branches..."
    git branch -a | grep -i "$term_lower" || echo "   No matches in branch names"
    
    echo ""
    echo "7. Searching in git tags..."
    git tag -l | grep -i "$term_lower" || echo "   No matches in tags"
    
    echo ""
}

# Main execution
{
    echo "================================================================================"
    echo "STARTING COMPREHENSIVE SEARCH"
    echo "================================================================================"
    echo ""
    
    # Search for TURBO
    search_term "TURBO"
    echo ""
    
    # Search for GABRIEL
    search_term "GABRIEL"
    echo ""
    
    echo "================================================================================"
    echo "SEARCH COMPLETE"
    echo "================================================================================"
    echo ""
    echo "Summary:"
    echo "--------"
    
    # Generate summary
    turbo_count=$(grep -ri "turbo" "$REPO_ROOT" 2>/dev/null | grep -v ".git" | wc -l || echo "0")
    gabriel_count=$(grep -ri "gabriel" "$REPO_ROOT" 2>/dev/null | grep -v ".git" | wc -l || echo "0")
    
    echo "TURBO occurrences: $turbo_count"
    echo "GABRIEL occurrences: $gabriel_count"
    echo ""
    
    if [ "$turbo_count" -eq 0 ] && [ "$gabriel_count" -eq 0 ]; then
        echo "RESULT: Neither TURBO nor GABRIEL were found in the repository."
    else
        echo "RESULT: Found matches. See details above."
    fi
    
    echo ""
    echo "Report saved to: $REPORT_FILE"
    
} 2>&1 | tee "$REPORT_FILE"

echo ""
echo "Search complete!"
exit 0
