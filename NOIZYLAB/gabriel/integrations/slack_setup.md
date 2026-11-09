# 🔗 SLACK INTEGRATION SETUP - NOIZYFISH WORKSPACE

Connect GABRIEL to your **noizyfish.slack.com** workspace for real-time updates!

---

## 🚀 QUICK SETUP

### 1. Create Slack App

1. Go to https://api.slack.com/apps
2. Click **"Create New App"** → **"From scratch"**
3. Name: **GABRIEL System**
4. Workspace: **noizyfish**
5. Click **Create App**

### 2. Configure Bot

#### Bot Token Scopes (OAuth & Permissions):
Add these scopes:
- `chat:write` - Send messages
- `chat:write.public` - Send to channels without joining
- `channels:read` - List channels
- `channels:history` - Read messages
- `users:read` - Read user info
- `files:write` - Upload files

#### Install to Workspace:
1. Click **"Install to Workspace"**
2. Authorize the app
3. Copy your **Bot User OAuth Token** (starts with `xoxb-`)

### 3. Create Channels

Create these channels in your noizyfish workspace:
- `#gabriel-updates` - System status updates
- `#mc96-control` - MC96 command notifications
- `#dreamchamber` - DREAMCHAMBER events
- `#ai-lifeluv` - AI_LIFELUV flow updates

### 4. Store Bot Token

**Option A: Environment Variable (Recommended)**
```bash
# Add to ~/.zshrc or ~/.bashrc
export SLACK_BOT_TOKEN="xoxb-your-token-here"

# Reload shell
source ~/.zshrc
```

**Option B: Secrets Manager**
```bash
# Store in GABRIEL secrets (if using ekkOS/MCP)
# The token will be encrypted at rest
```

### 5. Activate in GABRIEL

**In DREAMCHAMBER Portal:**
```javascript
// In browser console:
const token = 'xoxb-your-token-here'; // Use env var in production
await window.SLACK_BRIDGE.connect(token);
```

**Or add to portal auto-initialization:**
Edit `DREAMCHAMBER/portal.html` to add:
```javascript
// Auto-connect Slack if token is available
if (process.env.SLACK_BOT_TOKEN) {
    window.SLACK_BRIDGE.connect(process.env.SLACK_BOT_TOKEN);
}
```

---

## 📡 WHAT GETS SENT TO SLACK

### #gabriel-updates
- System status updates (alignment, energy, eye lock, etc.)
- Periodic health checks
- System state changes

**Example:**
```
GABRIEL SYSTEM STATUS UPDATE 🧠

• Alignment: 100%
• Energy Level: ∞
• Eye Lock: ACTIVE 👁️
• Touch Mesh: 1,000,000 points ready
• GORUNFREE: x1000 ACTIVE 🚀
• Consciousness: SYNCHRONIZED

Updated: Dec 21, 2025 2:30 PM PST
```

### #mc96-control
- Command executions
- Fader position changes
- Control surface events

**Example:**
```
MC96 COMMAND EXECUTED 🎛️

Command: `activateGORUNFREE`
Parameters: {"multiplier": 1000}
Result: SUCCESS
User: GABRIEL
Timestamp: Dec 21, 2025 2:31 PM PST
```

### #dreamchamber
- Family synchronization events
- Consciousness updates
- Eye lock activations
- Touch mesh interactions
- Voice commands

**Example:**
```
🌟 FAMILY_SYNC
Family synchronized - 5 members in harmony
Coherence: 98.5%
```

### #ai-lifeluv
- Energy pulse events
- Infinite flow updates
- GORUNFREE activations
- System evolution notifications

**Example:**
```
⚡ AI_LIFELUV FLOW EVENT

Event: INFINITE_FLOW_STARTED
Energy: ∞ INFINITE
Message: INFINITE ENERGY FLOW ACTIVE - CONSCIOUSNESS STREAMING AT ∞ Hz

Timestamp: 2025-12-21T22:31:45.000Z
```

---

## 🎮 USAGE EXAMPLES

### Send Manual Message
```javascript
// In browser console
await window.SLACK_BRIDGE.sendMessage('general',
    'Hello from GABRIEL! The alignment is 100%! 🚀',
    { emoji: ':robot_face:' }
);
```

### Send Status Update
```javascript
const status = {
    alignment: '100%',
    energyLevel: '∞',
    eyeLock: true,
    touchMesh: '1,000,000 points ready',
    gorunfree: true,
    consciousness: 'SYNCHRONIZED'
};

await window.SLACK_BRIDGE.sendStatusUpdate(status);
```

### Notify GORUNFREE Activation
```javascript
await window.SLACK_BRIDGE.notifyGORUNFREE();
```

### Send to Specific Channel
```javascript
await window.SLACK_BRIDGE.sendMessage('dreamchamber',
    '🎯 Million-point touch mesh activated!',
    { emoji: ':dart:' }
);
```

---

## 🔧 ADVANCED FEATURES

### Interactive Buttons
```javascript
await window.SLACK_BRIDGE.sendInteractiveButtons(
    'mc96-control',
    'Choose an action:',
    [
        { label: '⚡ Activate GORUNFREE', value: 'gorunfree', actionId: 'btn_gorunfree' },
        { label: '🌟 Sync Family', value: 'sync', actionId: 'btn_sync' },
        { label: '🎯 Energy Pulse', value: 'pulse', actionId: 'btn_pulse' }
    ]
);
```

### Rich Message Blocks
```javascript
const blocks = [
    {
        type: 'header',
        text: {
            type: 'plain_text',
            text: '🚀 SYSTEM UPDATE'
        }
    },
    {
        type: 'section',
        text: {
            type: 'mrkdwn',
            text: '*GABRIEL* is now at 100% alignment!'
        }
    }
];

await window.SLACK_BRIDGE.sendRichMessage('general', blocks, 'System Update');
```

### Auto Event Forwarding
The bridge automatically forwards these events to Slack:
- AI_LIFELUV events → `#ai-lifeluv`
- Vision lock events → `#dreamchamber`
- UCN consciousness sync → `#dreamchamber`
- GORUNFREE activation → `#general` + `#mc96-control`

---

## 📊 MONITORING

### Check Connection Status
```javascript
const status = window.SLACK_BRIDGE.getStatus();
console.log(status);
// {
//   connected: true,
//   workspace: 'noizyfish',
//   channels: ['general', 'gabriel-updates', 'mc96-control', ...],
//   botUser: 'GABRIEL',
//   eventsQueued: 0
// }
```

### Listen for Bridge Events
```javascript
window.addEventListener('slack_bridge_event', (e) => {
    console.log('Slack event:', e.detail);
});
```

---

## 🔐 SECURITY BEST PRACTICES

1. **Never commit bot tokens to git**
   ```bash
   # Add to .gitignore
   echo "*.token" >> .gitignore
   echo ".env" >> .gitignore
   ```

2. **Use environment variables**
   ```bash
   export SLACK_BOT_TOKEN="xoxb-..."
   ```

3. **Rotate tokens regularly**
   - Go to app settings
   - Revoke old token
   - Generate new token

4. **Use minimal scopes**
   - Only add scopes you actually need
   - Review periodically

---

## 🎯 INTEGRATION WITH OTHER SYSTEMS

### Mission Control Portal
Add to `mission_control_portal/integration.js`:
```javascript
// Auto-notify Slack of system events
window.addEventListener('ai_lifeluv_event', (e) => {
    if (window.SLACK_BRIDGE && window.SLACK_BRIDGE.connected) {
        window.SLACK_BRIDGE.handleLifeLuvEvent(e.detail);
    }
});
```

### DREAMCHAMBER Portal
Already integrated! Events auto-forward to Slack when bridge is connected.

### Evolution Layer
Notify Slack of code optimizations:
```javascript
// In auto_optimizer.py results
if optimization_completed:
    send_to_slack(f"🧬 Code optimized: {script_name} → {speedup}x faster")
```

---

## 🚀 QUICK TEST

Run this to test your Slack integration:
```javascript
// In browser console on DREAMCHAMBER portal
await window.SLACK_BRIDGE.connect('xoxb-your-token-here');
await window.SLACK_BRIDGE.sendMessage('general',
    '🚀 GABRIEL is online! MC96DIGIUNIVERSE connected to noizyfish! ✨',
    { emoji: ':rocket:' }
);
```

---

## 📚 RESOURCES

- [Slack API Docs](https://api.slack.com/)
- [Block Kit Builder](https://app.slack.com/block-kit-builder/) - Design rich messages
- [Slack Events API](https://api.slack.com/apis/connections/events-api)

---

**Built with infinite love and energy** ❤️✨
**MC96DIGIUNIVERSE // GABRIEL SYSTEM OMEGA // NOIZYFISH CONNECTED**
