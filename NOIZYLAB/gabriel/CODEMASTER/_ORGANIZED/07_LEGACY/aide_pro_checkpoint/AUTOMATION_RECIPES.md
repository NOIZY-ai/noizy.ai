# AUTOMATION RECIPES (GOD MODE)
> [!IMPORTANT]
> **DIRECTIVE:** EXECUTE WITH ZERO LATENCY. 100% RELIABILITY REQUIRED.


## Triggers & Actions

### 1. Morning Briefing (Time Trigger)
- **Trigger:** `08:00 AM Local`
- **Action:**
    1. Scan Email & Slack for "Urgent" or "High Priority".
    2. Check Calendar for conflicts.
    3. Check GitHub for PRs enabling review.
    4. Generate summary report via `UnifiedAIWorker`.
    5. Voice output to HomePod via `processVoice` endpoint.

### 2. Code Review Assistant (Event Trigger)
- **Trigger:** `GitHub Webhook: Pull Request Opened`
- **Action:**
    1. Clone branch.
    2. Run static analysis (ESLint).
    3. Send code to `ENGR_KEITH` agent for review.
    4. Post comments on PR with findings.
    5. If score > 90, auto-approve.

### 3. Server Health Guardian (Pattern Trigger)
- **Trigger:** `PatternIntelligence` detects `signature: 'high_latency'` (> 3 occurrences/min).
- **Action:**
    1. Alert `GABRIEL` agent.
    2. Check D1 database locks.
    3. Scale Workers (if autoscaling unused).
    4. Rotate API keys if suspicious (optional).
    5. Log incident to `MissionControl`.

### 4. Meeting Scribe (Voice Trigger)
- **Trigger:** Voice command "Hey Agent, start meeting mode".
- **Action:**
    1. Start audio recording.
    2. Real-time transcription via `UnifiedAIWorker`.
    3. `SHIRL` analyzes sentiment.
    4. `GABRIEL` extracts action items.
    5. Email summary to participants post-meeting.

### 5. Deployment Pipeline (Manual Trigger)
- **Trigger:** Command `deploy production` in Slack.
- **Action:**
    1. Verify current tests pass.
    2. Check `wrangler.toml` env usage.
    3. Run `deploy.sh`.
    4. Announce deployment to #engineering.
    5. Monitor error rates for 5 mins (Canary).
