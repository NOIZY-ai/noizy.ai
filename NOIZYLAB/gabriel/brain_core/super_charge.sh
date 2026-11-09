#!/bin/bash

# MC96Universe SUPER CHARGE Script
# "Instant Transmission" Module: UI and Filesystem Interaction Speedup
# Purpose: Remove "perceived" latency in macOS UI and speed up standard interactions.

echo ">>> SUPER CHARGE INITIALIZING..."
echo ">>> Disabling spacetime drag (UI Animations)..."

# 1. Window Animations (Instant Open/Close)
defaults write NSGlobalDomain NSAutomaticWindowAnimationsEnabled -bool false
defaults write NSGlobalDomain NSWindowResizeTime -float 0.001

# 2. Dock Instant Hide/Show
defaults write com.apple.dock autohide-time-modifier -float 0
defaults write com.apple.dock autohide-delay -float 0

# 3. Finder Transitions (No fade in/out)
defaults write com.apple.finder DisableAllAnimations -bool true
defaults write com.apple.finder AnimateWindowZoom -bool false

# 4. QuickLook (Instant)
defaults write NSGlobalDomain QLPanelAnimationDuration -float 0

# 5. Dialog Boxes (Instant)
defaults write NSGlobalDomain NSWindowResizeTime -float 0.001

# 6. Save Panel (Expand immediately)
defaults write NSGlobalDomain NSNavPanelExpandedStateForSaveMode -bool true
defaults write NSGlobalDomain NSNavPanelExpandedStateForSaveMode2 -bool true

echo ">>> FLUSHING SYSTEM CACHES (Purge)..."
# Force disk cache flush for a clean start
sudo purge

echo ">>> RESTARTING UI SUBSYSTEMS..."
killall Dock
killall Finder

echo ">>> SYSTEM IS NOW OPERATING AT LIGHT SPEED."
echo ">>> Note: Revert via 'defaults delete ...' if too fast to handle."
