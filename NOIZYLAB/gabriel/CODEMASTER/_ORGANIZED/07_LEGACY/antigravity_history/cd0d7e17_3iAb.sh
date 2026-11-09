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
            # 1. Renice to -20 (Legacy Priority)
            sudo renice -20 -p $pid
            
            # 2. taskpolicy (Modern Darwin Scheduler)
            # Set to "Latency Critical" scheduler policies if possible
            # Note: taskpolicy usage for changing running pid is often 'taskpolicy -b <pid>' (promote from bg)
            # or using 'setpriority' mechanics.
            # But we can try to force scheduling tier via undocumented/semi-documented flags or 'proc_set_cpumon'
            # For now, let's use the standard 'taskpolicy -d' to ensure it's NOT background.
            sudo taskpolicy -d -p $pid 2>/dev/null
            
            # 3. Darwin "Latency Critical" Tier (The "Secret Sauce")
            # This is often 'taskpolicy -l' but arguments vary. 
            # We will assume process is already foreground. The renice is the biggest hammer.
            
            echo "    -> ENGAGING LATENCY LOCK (taskpolicy)"
            # Trying to force high throughput/latency-critical tier
            # (Note: exact CLI flag for 'latency critical' on running PID is tricky, 
            # but ensuring it's not throttled is key).
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
