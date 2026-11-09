#!/bin/bash
# QUICK_LAUNCH_ALL.sh
# Quick launcher for all Beats and email setup

# Open all necessary pages and settings
open "x-apple.systempreferences:com.apple.preference.sound"
open "x-apple.systempreferences:com.apple.preference.universalaccess"
open "https://dash.cloudflare.com/login"
open "https://app.improvmx.com/"
open "https://mail.google.com/mail/u/0/#settings/accounts"

# Open guides
[ -f "$HOME/Desktop/VOICE_COMMANDS_QUICK.txt" ] && open "$HOME/Desktop/VOICE_COMMANDS_QUICK.txt"
[ -f "$HOME/Desktop/BEATS_STATUS.txt" ] && open "$HOME/Desktop/BEATS_STATUS.txt"

echo "✅ All pages opened!"

