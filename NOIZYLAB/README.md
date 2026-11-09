# 🪐 GABRIEL SYSTEM OMEGA (NOIZYLAB)

**Version**: 2.5.0 (Native Bridge)
**Host**: M2 Ultra
**Status**: ZERO LATENCY / 100% OPTIMIZATION

## 🗺️ System Map

### 1. 🧠 Intelligence Core

- **`GABRIEL`**: The unified Python monorepo (`.gemini/antigravity/.../GABRIEL_UNIFIED`).
- **`MC96_MISSION_CONTROL`**: High-performance visualization dashboard (Three.js/WebGL).
- **`PORTAL`**: Remote diagnostic and support interface (Port 5173).
- **`REMOTE_AGENT`**: Standalone cross-platform telemetry agent (Port 5175).
- **`CORE_API`**: Infinity Kernel API (Port 5177).

### 2. ⚡ Native Bridge (`NATIVE/`)

*High-performance modules for M2 Ultra acceleration.*

- **`METAL/`**: C++ Prototyping for 76-core GPU compute.
- **`SECURITY/`**: FSEvents monitoring for instant file awareness.
- **`Makefile`**: Build automation (`make -C NATIVE`).
- **`APPLE_SAMPLE_CODE.md`**: Index of native functionality references.

### 3. 🛠️ Command Center (`bin/`)

- **`noizy`**: The Master CLI. Try `noizy status` or `noizy heal`.
- **`agent`**: MCP Server Management CLI. Try `agent mcp list`.
- **`deploy_gabriel_remote.sh`**: Setup script for remote agents (HP-OMEN).
- **`start_gabriel_service.sh`**: LaunchAgent entry point.
- **`gabriel_metal_proto`**: Compiled Metal prototype.
- **`gabriel_fsevents`**: Compiled Security sentry.

### 4. 🌐 Connectivity

- **MCP Server**: `mcp/noizylab_mcp_server.py` (Claude/Tools integration).
- **WebRTC**: Port 5181 (Signaling).
- **Portal**: <http://localhost:5173>
- **Core**: <http://localhost:5177>
- **Remote Agent**: <http://localhost:5175>

## 🚀 Quick Start

```bash
# Check System Health (Neural Doctor)
noizy status

# Fix Issues
noizy heal

# Chat with Gabriel Infinity
noizy ai "System status report"

# Manage MCP Servers
agent mcp list
agent mcp list-tools playwright
```

## 📚 Documentation

- **[MCP Overview](/docs/context/mcp.md)**: Configure Model Context Protocol servers
- **[MCP CLI Commands](/docs/cli/mcp.md)**: Manage MCP servers from the command line
- **[Available MCP Tools](/docs/context/mcp/directory.md)**: Browse pre-built MCP servers

*Architected by NoizyLab & The User.*
