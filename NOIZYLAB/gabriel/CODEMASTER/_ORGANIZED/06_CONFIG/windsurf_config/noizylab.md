---
description: NOIZYLAB
auto_execution_mode: 1
---

## Goal
Make Windsurf ready for NOIZYLAB work: correct workspace, rules active, MCP ready, and a repeatable command checklist.

## Steps
1. Open folder: `/Users/m2ultra`
2. Confirm rules are active:
   - Ensure `/Users/m2ultra/.windsurfrules` exists (global behavior)
3. Verify MCP bridge:
   - Extensions installed:
     - `yutengjing.vscode-mcp-bridge`
4. Restart Windsurf (required after rules/workflow changes)
5. Quick sanity checks (run in terminal from the project root):
   - `git status`
   - `python3 --version`
   - `node -v`

## Quick Actions
// turbo
- If you want this workflow + rules copied into the canonical location, ensure these files exist:
  - `/Users/m2ultra/.windsurf/workflows/noizylab.md`
