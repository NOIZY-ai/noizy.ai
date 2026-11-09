#!/bin/bash
echo "REQUESTING SUPERUSER PERMISSION TO FIX DRIVE..."
# 1. Take Ownership
sudo chown -R $(whoami) /Volumes/JOE/NKI
# 2. Grant Full Access (777)
sudo chmod -R 777 /Volumes/JOE/NKI
# 3. Clear Quarantine Attributes
sudo xattr -rc /Volumes/JOE/NKI
echo "SUCCESS: PERMISSIONS REPAIRED."
echo "YOU MAY NOW RUN: python3 /Volumes/JOE/NKI/turbo_bfa_god.py --execute --nuke"
