#!/bin/bash
# CREATE_SIRI_SHORTCUTS.sh
# Creates Siri shortcuts for email setup

echo "🎤 Creating Siri Shortcuts for Email Setup..."
echo ""

SHORTCUTS_DIR="$HOME/NOIZYLAB/email/automation/siri_shortcuts"
mkdir -p "$SHORTCUTS_DIR"

# Create shortcut files that can be imported into Shortcuts app
cat > "$SHORTCUTS_DIR/Open_Gmail_Settings.shortcut" << 'EOF'
{
  "WFWorkflowActions": [
    {
      "WFWorkflowActionIdentifier": "is.workflow.actions.openurl",
      "WFWorkflowActionParameters": {
        "WFURLActionURL": "https://mail.google.com/mail/u/0/#settings/accounts"
      }
    }
  ],
  "WFWorkflowClientRelease": "2.0",
  "WFWorkflowClientVersion": "900",
  "WFWorkflowIcon": {
    "WFWorkflowIconGlyphNumber": 59508,
    "WFWorkflowIconStartColor": 4282601983
  },
  "WFWorkflowInputContentItemClasses": [],
  "WFWorkflowMinimumClientVersion": 900,
  "WFWorkflowMinimumClientVersionString": "900",
  "WFWorkflowTypes": [
    "NCWidget"
  ]
}
EOF

cat > "$SHORTCUTS_DIR/Setup_Email_Aliases.shortcut" << 'EOF'
{
  "WFWorkflowActions": [
    {
      "WFWorkflowActionIdentifier": "is.workflow.actions.runsshscript",
      "WFWorkflowActionParameters": {
        "WFSSHUser": "$(whoami)",
        "WFSSHScript": "bash $HOME/NOIZYLAB/email/automation/auto_setup_all.sh"
      }
    }
  ],
  "WFWorkflowClientRelease": "2.0",
  "WFWorkflowClientVersion": "900",
  "WFWorkflowIcon": {
    "WFWorkflowIconGlyphNumber": 59508,
    "WFWorkflowIconStartColor": 4282601983
  },
  "WFWorkflowInputContentItemClasses": [],
  "WFWorkflowMinimumClientVersion": 900,
  "WFWorkflowMinimumClientVersionString": "900",
  "WFWorkflowTypes": [
    "NCWidget"
  ]
}
EOF

cat > "$SHORTCUTS_DIR/Open_ImprovMX.shortcut" << 'EOF'
{
  "WFWorkflowActions": [
    {
      "WFWorkflowActionIdentifier": "is.workflow.actions.openurl",
      "WFWorkflowActionParameters": {
        "WFURLActionURL": "https://improvmx.com/"
      }
    }
  ],
  "WFWorkflowClientRelease": "2.0",
  "WFWorkflowClientVersion": "900",
  "WFWorkflowIcon": {
    "WFWorkflowIconGlyphNumber": 59508,
    "WFWorkflowIconStartColor": 4282601983
  },
  "WFWorkflowInputContentItemClasses": [],
  "WFWorkflowMinimumClientVersion": 900,
  "WFWorkflowMinimumClientVersionString": "900",
  "WFWorkflowTypes": [
    "NCWidget"
  ]
}
EOF

echo "✅ Siri shortcuts created in: $SHORTCUTS_DIR"
echo ""
echo "📋 To use:"
echo "   1. Open Shortcuts app"
echo "   2. Import shortcuts from: $SHORTCUTS_DIR"
echo "   3. Say: 'Hey Siri, [shortcut name]'"
echo ""


