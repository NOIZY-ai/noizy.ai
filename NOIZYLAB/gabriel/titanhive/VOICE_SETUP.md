# Voice Inbox Setup - iPhone to TitanHive

This guide sets up voice commands from iPhone to your GABRIEL Hive.

## How It Works

1. You record a Voice Memo on iPhone
2. An iOS Shortcut transcribes it and saves to iCloud
3. TitanHive polls the inbox and executes commands

## Step 1: Create iCloud Folder

The folder should already exist at:
```
iCloud Drive/TitanHive/inbox/
```

If not, create it manually in the Files app.

## Step 2: Create the iOS Shortcut

### Option A: Quick Voice Command

1. Open **Shortcuts** app on iPhone
2. Tap **+** to create new shortcut
3. Add these actions:

```
1. Dictate Text
   - Set: Stop Listening = After Pause

2. Save File
   - Save: Dictated Text
   - Path: /TitanHive/inbox/
   - Filename: voice_[Current Date].txt
   - Overwrite: Ask
```

4. Name it: **"Gabriel Command"**
5. Add to Home Screen or assign to Action Button

### Option B: Record & Transcribe

1. Open **Shortcuts** app
2. Create new shortcut with:

```
1. Record Audio
   - Quality: Normal
   - Start: On Tap
   - Finish: On Tap

2. Transcribe Audio

3. Save File
   - Save: Transcription
   - Path: /TitanHive/inbox/
   - Filename: voice_[Current Date].txt
```

4. Name it: **"Gabriel Voice"**

## Step 3: Action Button Setup (iPhone 15 Pro+)

1. Go to **Settings > Action Button**
2. Select **Shortcut**
3. Choose **"Gabriel Command"**

Now pressing the Action Button activates voice control.

## Step 4: Test the Setup

1. Trigger your shortcut
2. Say: "status"
3. Check the inbox folder for the .txt file
4. TitanHive will auto-execute it within 1.5 seconds

## Supported Voice Commands

| Command | Action |
|---------|--------|
| "status" | Show system status |
| "models" | List Ollama models |
| "ping" | Test connectivity |
| "speak hello world" | Text to speech |
| "omen" | Check HP Omen status |
| "wake" | Wake-on-LAN the Omen |
| "scan" | Scan network nodes |
| Any question | Ask Ollama AI |

## Advanced: Siri Shortcut

Add a Siri phrase to your shortcut:

1. Open your shortcut in Shortcuts app
2. Tap the **ⓘ** info button
3. Tap **"Add to Siri"**
4. Record phrase: **"Hey Siri, Gabriel"**

Now you can say "Hey Siri, Gabriel" and then your command.

## Troubleshooting

### Files not appearing?
- Ensure iCloud Drive is syncing
- Check the path is correct: `/TitanHive/inbox/`
- Open Files app and verify the folder exists

### Commands not executing?
- Ensure TitanHive TUI is running: `titan` or `cd ~/NOIZYLAB/GABRIEL/titanhive && uv run python main.py`
- Check VOICE_INBOX_DIR in `.env`
- Verify polling interval: `VOICE_POLL_SECONDS=1.5`

### Archive processed files
Run `archive` in TitanHive to move processed voice files to `/TitanHive/archive/`

## Environment Variables

In `titanhive/.env`:
```
VOICE_INBOX_DIR=/Users/m2ultra/Library/Mobile Documents/com~apple~CloudDocs/TitanHive/inbox
VOICE_POLL_SECONDS=1.5
```
