# 🛡️ Endpoint Security & System Extension Plan

## Objective

Implement a "God-Mode" file system monitor that sees every file event on the Mac in real-time, replacing the polling-based `realtime_watcher.py`.

## Technology: Endpoint Security (ES) Framework

The ES framework allows a user-space extension to monitor and authorize system events (process execution, file access, mounting, etc.).

## Architecture

1. **`GabrielSentry` (System Extension)**:
   - Written in Swift/Objective-C.
   - Entitlement: `com.apple.developer.endpoint-security.client`.
   - Function: Hooks into `ES_EVENT_TYPE_NOTIFY_CREATE`, `ES_EVENT_TYPE_NOTIFY_WRITE`.

2. **Communication**:
   - Uses XPC to talk to the GABRIEL Python backend.

## Implementation Hurdles

- **Signing**: Requires a special Apple Developer Certificate with Endpoint Security entitlements (strict approval process).
- **SIP**: System Integrity Protection might limit loading unsigned extensions during dev.

## Alternatives for "No Code Signing" Mode

- **`fswatch` / `FSEvents`**: The standard macOS C API for file monitoring (very efficient).
- **Strategy**: Write a small C tool using FSEvents directly and pipe output to NOIZYLAB.

## Implementation Steps (Next Session)

1. Prototype `gabriel_fsevents` (C tool) as a lightweight substitute for full ES.
2. Usage:

   ```c
   FSEventStreamCreate(...)
   ```
