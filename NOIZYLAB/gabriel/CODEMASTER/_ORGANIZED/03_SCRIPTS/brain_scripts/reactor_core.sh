#!/bin/bash

# MC96Universe REACTOR CORE Script
# "Infinite Power" Module: Power Management & I/O Unthrottling
# Purpose: Prevent the system from sleeping, napping, or throttling background I/O.

echo ">>> REACTOR CORE INITIALIZING..."

# 1. Disable Low Priority I/O Throttling
# macOS normally throttles background disk I/O (Time Machine, etc.).
# We disable this so ALL disk operations run at MAXIMUM SPEED.
echo ">>> Disabling I/O Throttling..."
sudo sysctl debug.lowpri_throttle_enabled=0

# 2. Power Management (Prevent Sleep/Nap)
# M2 Ultra should never rest during production.
echo ">>> Engaging High-Performance Power Plan..."
sudo pmset -a sleep 0
sudo pmset -a disksleep 0
sudo pmset -a powernap 0
# sudo pmset -a tcpkeepalive 1 # Ensure connections stay open

# 3. Disable App Nap (Global User Default)
# Prevent macOS from slowing down apps hidden behind others.
echo ">>> Disabling App Nap..."
defaults write NSGlobalDomain NSAppSleepDisabled -bool YES

echo ">>> REACTOR CORE ONLINE."
echo ">>> System will NO LONGER SLEEP or THROTTLE background tasks."
