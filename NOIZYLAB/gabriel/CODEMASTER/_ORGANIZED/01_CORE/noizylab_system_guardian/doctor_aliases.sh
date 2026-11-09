#!/bin/zsh
#
# 🩺 QUICK SYSTEM DOCTOR ALIASES
# Add to your ~/.zshrc for quick access
#
# Usage: source /Users/m2ultra/NOIZYLAB/SystemGuardian/doctor_aliases.sh
#

DOCTOR_PATH="/Users/m2ultra/NOIZYLAB/SystemGuardian"

# Main commands
alias doctor="cd $DOCTOR_PATH && python3 -m modules.cli"
alias doctor-full="cd $DOCTOR_PATH && python3 -m modules.cli --full --export"
alias doctor-quick="cd $DOCTOR_PATH && python3 -m modules.cli --disk --memory --process"

# Individual scans
alias doctor-disk="cd $DOCTOR_PATH && python3 -m modules.cli --disk"
alias doctor-mem="cd $DOCTOR_PATH && python3 -m modules.cli --memory"
alias doctor-net="cd $DOCTOR_PATH && python3 -m modules.cli --network"
alias doctor-proc="cd $DOCTOR_PATH && python3 -m modules.cli --process"
alias doctor-temp="cd $DOCTOR_PATH && python3 -m modules.cli --thermal"
alias doctor-smart="cd $DOCTOR_PATH && python3 -m modules.cli --smart"

# Auto-fix commands
alias doctor-fix="cd $DOCTOR_PATH && python3 -m modules.cli --fix"
alias doctor-optimize="cd $DOCTOR_PATH && python3 -m modules.cli --optimize"
alias doctor-turbo="cd $DOCTOR_PATH && python3 -m modules.cli --optimize && python3 -m modules.cli --full"

# Helper
alias doctor-help="cd $DOCTOR_PATH && python3 -m modules.cli --help"

echo "🩺 System Doctor aliases loaded!"
echo "   doctor        - Run full diagnostic scan"
echo "   doctor-turbo  - Optimize + full scan"
echo "   doctor-fix    - Show available fixes"
