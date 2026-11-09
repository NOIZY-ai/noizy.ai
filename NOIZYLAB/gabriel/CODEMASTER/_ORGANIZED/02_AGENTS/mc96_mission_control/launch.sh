#!/bin/bash
# MC96 MISSION CONTROL LAUNCHER
echo "===== MC96 MISSION CONTROL ====="
echo "Starting MemCell Tracker..."
python3 /Volumes/JOE/NKI/MC96_MISSION_CONTROL/memcell_tracker.py
echo "Starting Gabriel Server on port 8096..."
python3 /Volumes/JOE/NKI/MC96_MISSION_CONTROL/gabriel_server.py
