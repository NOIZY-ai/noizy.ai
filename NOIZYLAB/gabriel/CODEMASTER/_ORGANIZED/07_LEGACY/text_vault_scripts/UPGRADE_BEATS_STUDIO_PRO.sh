#!/bin/bash
# UPGRADE_BEATS_STUDIO_PRO.sh
# Optimize Beats Studio Pro for Voice Control

clear

echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║     🎧 UPGRADING BEATS STUDIO PRO                                    ║"
echo "║     Optimizing for Voice Control                                      ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo ""

echo "🎧 Optimizing Beats Studio Pro settings..."
echo ""

# Create Beats optimization script
cat > "$HOME/Desktop/OPTIMIZE_BEATS.command" << 'BEATS_EOF'
#!/bin/bash
# Optimize Beats Studio Pro

clear

echo "🎧 OPTIMIZING BEATS STUDIO PRO..."
echo ""

echo "📋 STEP 1: Connect your Beats Studio Pro via cable"
echo "   (USB-C or 3.5mm cable)"
echo ""
read -p "Press Enter when connected..."

echo ""
echo "📋 STEP 2: Setting up audio settings..."
echo ""

# Open Sound settings
open "x-apple.systempreferences:com.apple.preference.sound"

sleep 2

echo ""
echo "✅ Sound settings opened!"
echo ""
echo "📋 CONFIGURE:"
echo ""
echo "1. Click 'Input' tab"
echo "2. Select 'Beats Studio Pro' from the list"
echo "3. Adjust input volume (speak and watch the meter)"
echo "4. Make sure it's set as default input"
echo ""
echo "5. Click 'Output' tab"
echo "6. Select 'Beats Studio Pro' for output too"
echo "7. Adjust output volume"
echo ""

# Create optimization guide
cat > "$HOME/Desktop/BEATS_OPTIMIZATION.txt" << 'OPTIMIZE_EOF'
╔══════════════════════════════════════════════════════════════════════╗
║     🎧 BEATS STUDIO PRO OPTIMIZATION GUIDE                          ║
╚══════════════════════════════════════════════════════════════════════╝

CONNECTION:
───────────

✅ Connect via USB-C cable (best quality)
✅ OR connect via 3.5mm cable
✅ Make sure cable is fully inserted

OPTIMIZATION SETTINGS:
──────────────────────

INPUT SETTINGS (Microphone):
  • Select: Beats Studio Pro
  • Input Volume: 70-80% (adjust while speaking)
  • Watch the level meter - should move when you speak
  • Set as default input device

OUTPUT SETTINGS (Audio):
  • Select: Beats Studio Pro
  • Output Volume: Comfortable level
  • Balance: Center

VOICE CONTROL OPTIMIZATION:
───────────────────────────

1. Enable Voice Control:
   • System Preferences → Accessibility → Voice Control
   • Click "Enable"
   • It will automatically use Beats Studio Pro mic

2. Test Voice Control:
   • Say: "Show numbers"
   • If numbers appear → Working perfectly! ✅
   • If not → Check mic selection

3. Calibrate Microphone:
   • Speak normally into the mic
   • Watch input level meter
   • Adjust volume so meter is in green/yellow range
   • Not too low (red) or too high (maxed out)

ADVANCED OPTIMIZATION:
──────────────────────

For Best Voice Recognition:
  • Speak clearly and at normal volume
  • Reduce background noise
  • Keep mic close to your mouth (if possible)
  • Use noise cancellation (if available on Beats)

Audio Quality Settings:
  • Use USB-C connection (better than 3.5mm)
  • Check for firmware updates (if available)
  • Ensure cable is high-quality

TROUBLESHOOTING:
────────────────

If mic doesn't work:
  • Check cable connection
  • Try different USB port
  • Check System Preferences → Sound → Input
  • Make sure Beats Studio Pro is selected

If voice recognition is poor:
  • Increase input volume
  • Speak more clearly
  • Reduce background noise
  • Check Voice Control settings

If audio quality is poor:
  • Use USB-C instead of 3.5mm
  • Check cable quality
  • Adjust output volume
  • Check for interference

══════════════════════════════════════════════════════════════════════

OPTIMIZE_EOF

open "$HOME/Desktop/BEATS_OPTIMIZATION.txt"

echo ""
echo "✅ Optimization guide opened!"
echo ""
echo "📋 NEXT STEPS:"
echo "   1. Connect Beats Studio Pro via cable"
echo "   2. Configure in Sound settings (already open)"
echo "   3. Enable Voice Control"
echo "   4. Test with: 'Show numbers'"
echo ""

say "Beats Studio Pro optimization ready. Connect your headphones via cable. Configure in Sound settings. Then enable Voice Control."
BEATS_EOF

chmod +x "$HOME/Desktop/OPTIMIZE_BEATS.command"

# Create quick test script
cat > "$HOME/Desktop/TEST_BEATS_MIC.command" << 'TEST_EOF'
#!/bin/bash
# Test Beats Studio Pro microphone

clear

echo "🎤 TESTING BEATS STUDIO PRO MICROPHONE..."
echo ""

open "x-apple.systempreferences:com.apple.preference.sound"

sleep 2

echo ""
echo "📋 TEST STEPS:"
echo ""
echo "1. Sound settings opened"
echo "2. Click 'Input' tab"
echo "3. Select 'Beats Studio Pro'"
echo "4. Speak into your headphones"
echo "5. Watch the level meter - it should move"
echo ""
echo "If meter moves → Mic is working! ✅"
echo "If not → Check connection"
echo ""
echo "Then test Voice Control:"
echo "   Say: 'Show numbers'"
echo "   If numbers appear → Perfect! ✅"
echo ""

say "Testing Beats Studio Pro microphone. Speak into your headphones and watch the level meter. Then say Show numbers to test Voice Control."
TEST_EOF

chmod +x "$HOME/Desktop/TEST_BEATS_MIC.command"

# Create audio calibration script
cat > "$HOME/Desktop/CALIBRATE_BEATS.command" << 'CAL_EOF'
#!/bin/bash
# Calibrate Beats Studio Pro for Voice Control

clear

echo "🎧 CALIBRATING BEATS STUDIO PRO..."
echo ""

open "x-apple.systempreferences:com.apple.preference.sound"

sleep 2

echo ""
echo "📋 CALIBRATION STEPS:"
echo ""
echo "1. Sound settings opened"
echo "2. Click 'Input' tab"
echo "3. Select 'Beats Studio Pro'"
echo ""
echo "4. CALIBRATION TEST:"
echo "   • Speak at normal volume"
echo "   • Watch the input level meter"
echo "   • Adjust volume so meter is:"
echo "     - In green/yellow range (good)"
echo "     - Not too low (red = too quiet)"
echo "     - Not maxed out (too loud)"
echo ""
echo "5. OPTIMAL SETTING:"
echo "   • Meter should be 60-80% when speaking normally"
echo "   • This gives best voice recognition"
echo ""
echo "6. TEST VOICE CONTROL:"
echo "   • Say: 'Show numbers'"
echo "   • If numbers appear → Calibration perfect! ✅"
echo ""

say "Calibrating Beats Studio Pro. Speak at normal volume and adjust the input level so the meter is in the green to yellow range. This gives the best voice recognition."
CAL_EOF

chmod +x "$HOME/Desktop/CALIBRATE_BEATS.command"

# Create master Beats setup
cat > "$HOME/Desktop/BEATS_MASTER_SETUP.command" << 'MASTER_BEATS_EOF'
#!/bin/bash
# Beats Master Setup - Complete optimization

clear

echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║     🎧 BEATS STUDIO PRO - MASTER SETUP                              ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo ""

echo "📋 COMPLETE SETUP PROCESS:"
echo ""

echo "STEP 1: Connect Beats Studio Pro"
echo "  • Connect via USB-C cable (recommended)"
echo "  • OR connect via 3.5mm cable"
echo "  • Make sure cable is fully inserted"
echo ""
read -p "Press Enter when connected..."

echo ""
echo "STEP 2: Configure Audio Settings..."
open "x-apple.systempreferences:com.apple.preference.sound"
sleep 2

echo ""
echo "✅ Sound settings opened!"
echo ""
echo "CONFIGURE:"
echo "  • Input tab: Select 'Beats Studio Pro'"
echo "  • Adjust input volume: 70-80%"
echo "  • Output tab: Select 'Beats Studio Pro'"
echo "  • Adjust output volume: Comfortable level"
echo ""
read -p "Press Enter when configured..."

echo ""
echo "STEP 3: Enable Voice Control..."
open "x-apple.systempreferences:com.apple.preference.universalaccess"
sleep 2

echo ""
echo "✅ Accessibility settings opened!"
echo ""
echo "ENABLE:"
echo "  • Find 'Voice Control'"
echo "  • Click to enable"
echo "  • It will use Beats Studio Pro mic automatically"
echo ""
read -p "Press Enter when Voice Control is enabled..."

echo ""
echo "STEP 4: Test Everything..."
echo ""
echo "TEST VOICE CONTROL:"
echo "  Say: 'Show numbers'"
echo "  If numbers appear → Everything working! ✅"
echo ""

say "Beats Studio Pro master setup complete. Test by saying Show numbers. If numbers appear, everything is working perfectly."

echo ""
echo "✅ BEATS STUDIO PRO SETUP COMPLETE!"
echo ""
echo "🎤 READY FOR VOICE CONTROL!"
echo ""
MASTER_BEATS_EOF

chmod +x "$HOME/Desktop/BEATS_MASTER_SETUP.command"

echo "✅ Beats Studio Pro optimization scripts created!"
echo ""
echo "📋 DESKTOP SHORTCUTS:"
echo "   ✅ BEATS_MASTER_SETUP.command - Complete setup (USE THIS!)"
echo "   ✅ OPTIMIZE_BEATS.command - Quick optimization"
echo "   ✅ TEST_BEATS_MIC.command - Test microphone"
echo "   ✅ CALIBRATE_BEATS.command - Calibrate for voice"
echo ""
echo "🚀 QUICK START:"
echo "   1. Connect Beats Studio Pro via cable"
echo "   2. Double-click: BEATS_MASTER_SETUP.command"
echo "   3. Follow the steps"
echo "   4. Test with: 'Show numbers'"
echo ""

say "Beats Studio Pro upgrade scripts created. Connect your headphones via cable, then run Beats Master Setup to optimize everything."

