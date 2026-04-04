# MC96ECO Support-AI Workflow

> Gabriel + Claude + NOIZY.AI as the triage system for MC96.
> Builder (Copilot in editor) + Mechanic (Gabriel on alerts).

---

## Architecture

```
[Telemetry Feed]         [Knowledge Base]
  Prometheus/Grafana       mc96-docs/
  System alerts            runbooks/
  Error logs               network-topology/
       │                        │
       └────────┬───────────────┘
                │
         [AI TRIAGE LAYER]
         Gabriel + Claude + NOIZY.AI
                │
    ┌───────────┼───────────┐
    │           │           │
 [Slack]    [Discord]    [CLI]
 #mc96-ops  #mc96-alerts  noizy-cli
```

## Two AI Roles

### Builder (GitHub Copilot in VS Code)
- Writes Python, Node.js, YAML, shell scripts
- Assists with infrastructure code
- Context: has CLAUDE.md + repo structure
- Tool: VS Code Insiders + Copilot Pro+

### Mechanic (Gabriel via n8n/Ollama)
- Receives system alerts
- Classifies severity
- Looks up runbooks in mc96-docs
- Suggests fixes
- Routes to human if needed
- Tool: n8n webhook + Ollama on GOD + Slack/Discord

## Prompt Engineering Rules

### Role + Constraint + Output
```
You are GABRIEL acting as MC96 system monitor.
Your constraint: only suggest fixes documented in mc96-docs.
Your output: severity classification + recommended action + runbook link.
```

### Context Injection
```
Current system state:
- GOD: online, load 2.4, disk 78%
- GABRIEL (HP Omen): online, GPU utilization 45%
- Network: DGS-1210-10 all ports up
- Alert: Ollama response time > 5s on model 'gabriel'

Based on mc96-docs/runbooks/ollama-slow.md, diagnose and suggest fix.
```

### Chain of Thought
```
Before suggesting a fix:
1. State what you think the problem is
2. State what evidence supports that
3. State what runbook applies
4. Then give the fix command
```

## n8n Workflow: MC96 Alert Triage

```
Webhook (alert) → Classify severity → Lookup runbook
  → IF critical: Slack alert + page Rob
  → IF warning: Slack notify + suggest fix
  → IF info: log only
  → ALL: append to D1 mc96-command-central
```

## Knowledge Base Structure

```
mc96-docs/
├── systems/
│   ├── god.md              ← M2 Ultra specs, services, ports
│   ├── gabriel-omen.md     ← HP Omen specs, GPU, Ollama
│   ├── dafixer.md          ← MacBook Pro, mobile ops
│   └── network.md          ← DGS-1210-10, topology, VLANs
├── runbooks/
│   ├── ollama-slow.md      ← diagnosis + fix for slow inference
│   ├── disk-full.md        ← cleanup procedures
│   ├── network-down.md     ← port check + restart sequence
│   ├── backup-failed.md    ← backup verification + retry
│   └── deploy-failed.md    ← wrangler deploy troubleshooting
├── alerts/
│   ├── severity-levels.md  ← critical/warning/info definitions
│   └── escalation.md       ← who gets paged when
└── architecture/
    └── mc96-topology.md    ← full network + service map
```

## CLI Tool (future)

```bash
noizy-mc96 status           # system health
noizy-mc96 alert <message>  # manual alert
noizy-mc96 diagnose <error> # AI diagnosis
noizy-mc96 runbook <topic>  # find runbook
noizy-mc96 fix <issue>      # apply suggested fix
```

## Chat App Integration

### Slack (#mc96-ops)
- Gabriel posts triage results
- Human responds with approve/reject/escalate
- All actions logged to D1

### Discord (#mc96-alerts)
- Real-time alert feed
- Gabriel provides one-line summaries
- Link to full diagnosis in Slack thread

## Both. Chat AND CLI. Gabriel speaks through all channels.

---

*MC96ECO Support-AI v1.0*
*Builder + Mechanic. Human in the loop.*
*GORUNFREE*
