#!/bin/bash

# MC96Universe VELOCITY MODE
# "Zero G" Module: CPU Process Prioritization
# Purpose: Force macOS to give ABSOLUTE PRIORITY to creative apps.
# Target: Latency reduction "IN PROCESS".

echo ">>> VELOCITY MODE INITIALIZING..."
echo ">>> Scanning for High-Value Targets..."

# List of common heavy-hitter apps to boost
# feel free to add more here
APPS=("DaVinci Resolve" "Final Cut Pro" "Adobe Premiere Pro" "After Effects" "Cinema 4D" "Maya" "Blender" "Logic Pro X" "ProTools")

BOOSTED=0

for app in "${APPS[@]}"; do
    # Find PIDs for the app
    # pgrep -f matches patterns in full command line
    PIDS=$(pgrep -f "$app")
    
    if [ ! -z "$PIDS" ]; then
        echo ">>> Target Aquired: $app"
        for pid in $PIDS; do
            echo "    -> Boosting PID: $pid"
            # Renice to -20 (Maximum Priority)
            # Requires sudo
            sudo renice -20 -p $pid
            
            # Optional: Set thread priority policy? (Complex on macOS CLI, renice is standard)
        done
        BOOSTED=1
    fi
done

if [ $BOOSTED -eq 0 ]; then
    echo ">>> No primary creative apps found running."
    echo ">>> Launch your heavy apps (Resolve, FCP, etc.) and run this again!"
else
    echo ">>> SYSTEM VELOCITY INCREASED."
    echo ">>> Priority Levels have been maximized (-20)."
fi
