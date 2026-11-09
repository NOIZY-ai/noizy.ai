# Available MCP Tools

This directory contains pre-built MCP servers that you can easily integrate into your workflow. Each server provides specialized tools and capabilities.

## Official MCP Servers

### Playwright - Browser Automation

Control web browsers programmatically for testing, screenshots, and web scraping.

**Installation**:
```bash
npx -y @modelcontextprotocol/server-playwright
```

**Configuration**:
```json
{
  "mcpServers": {
    "playwright": {
      "transport": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-playwright"]
    }
  }
}
```

**Available Tools**:
- `playwright_navigate`: Navigate to URLs
- `playwright_screenshot`: Capture page screenshots
- `playwright_click`: Click elements
- `playwright_fill`: Fill form fields
- `playwright_evaluate`: Execute JavaScript

**Use Cases**: Web testing, screenshots, form automation, web scraping

---

### GitHub - Repository Management

Interact with GitHub repositories, issues, pull requests, and code.

**Installation**:
```bash
npx -y @modelcontextprotocol/server-github
```

**Configuration**:
```json
{
  "mcpServers": {
    "github": {
      "transport": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_PERSONAL_ACCESS_TOKEN}"
      }
    }
  }
}
```

**Authentication**: Requires GitHub personal access token

**Available Tools**:
- `github_list_repos`: List repositories
- `github_create_issue`: Create new issues
- `github_search_code`: Search code across repos
- `github_create_pr`: Create pull requests
- `github_get_file`: Read file contents

**Use Cases**: Repository management, code search, issue tracking, CI/CD

---

### Filesystem - File Operations

Read, write, and manage files and directories on your local system.

**Installation**:
```bash
npx -y @modelcontextprotocol/server-filesystem
```

**Configuration**:
```json
{
  "mcpServers": {
    "filesystem": {
      "transport": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/allowed/path"]
    }
  }
}
```

**Security Note**: Only provides access to specified paths

**Available Tools**:
- `read_file`: Read file contents
- `write_file`: Write to files
- `list_directory`: List directory contents
- `create_directory`: Create new directories
- `delete_file`: Remove files

**Use Cases**: File management, log analysis, configuration editing

---

### PostgreSQL - Database Access

Query and manage PostgreSQL databases.

**Installation**:
```bash
npx -y @modelcontextprotocol/server-postgres
```

**Configuration**:
```json
{
  "mcpServers": {
    "postgres": {
      "transport": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "POSTGRES_CONNECTION_STRING": "${DATABASE_URL}"
      }
    }
  }
}
```

**Authentication**: Requires PostgreSQL connection string

**Available Tools**:
- `query`: Execute SQL queries
- `list_tables`: Show all tables
- `describe_table`: Get table schema
- `insert_data`: Insert records
- `update_data`: Update records

**Use Cases**: Data analysis, database management, reporting

---

### Slack - Team Communication

Send messages and interact with Slack workspaces.

**Installation**:
```bash
npx -y @modelcontextprotocol/server-slack
```

**Configuration**:
```json
{
  "mcpServers": {
    "slack": {
      "transport": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-slack"],
      "env": {
        "SLACK_BOT_TOKEN": "${SLACK_TOKEN}"
      }
    }
  }
}
```

**Authentication**: Requires Slack bot token

**Available Tools**:
- `post_message`: Send messages to channels
- `list_channels`: Get available channels
- `get_channel_history`: Read message history
- `add_reaction`: React to messages
- `upload_file`: Share files

**Use Cases**: Team notifications, status updates, file sharing

---

### PowerToys - Windows Utilities Automation

Automate and control Microsoft PowerToys utilities for enhanced Windows productivity and system customization.

**About**: [Microsoft PowerToys](https://github.com/microsoft/PowerToys) is a set of utilities for power users to tune and streamline their Windows experience for greater productivity. This MCP server enables programmatic control over PowerToys features through automation scripts and command-line interfaces.

**Installation**:
```bash
# Install PowerToys if not already installed
winget install Microsoft.PowerToys -s winget

# Note: MCP server implementation may vary. 
# Check community repositories or build a custom server using:
# - Python with the MCP SDK and PowerToys CLI
# - PowerShell automation wrapper
# - Node.js with Windows automation libraries
```

**Configuration Example** (adjust based on your implementation):
```json
{
  "mcpServers": {
    "powertoys": {
      "transport": "stdio",
      "command": "python",
      "args": ["./servers/powertoys_server.py"],
      "env": {
        "POWERTOYS_PATH": "C:\\Program Files\\PowerToys"
      }
    }
  }
}
```

**Alternative Configuration** (using Node.js):
```json
{
  "mcpServers": {
    "powertoys": {
      "transport": "stdio",
      "command": "node",
      "args": ["./servers/powertoys-mcp-server.js"]
    }
  }
}
```

**Available Tools**:
- `powertoys_run`: Trigger PowerToys Run launcher with search query
- `color_picker`: Activate Color Picker utility
- `fancyzones_layout`: Configure and apply FancyZones window layouts
- `image_resize`: Batch resize images using Image Resizer
- `power_rename`: Execute bulk file renaming with PowerRename
- `text_extract`: Use Text Extractor (OCR) on screen regions
- `always_on_top`: Pin windows to stay on top
- `awake_mode`: Control Awake utility to prevent system sleep
- `keyboard_remap`: Manage keyboard shortcuts and remappings
- `mouse_utilities`: Control mouse highlighter and pointer features
- `screen_ruler`: Activate Screen Ruler for measurements
- `quick_accent`: Trigger Quick Accent for special characters

**Use Cases**: 
- **Workflow Automation**: Programmatically resize images, rename files, and manage windows
- **Screen Capture**: Extract text from images and screenshots via OCR
- **Window Management**: Apply custom FancyZones layouts and pin important windows
- **System Customization**: Automate keyboard remapping and mouse utility configurations
- **Developer Tools**: Quick access to color picking, screen measurement, and file management

**Requirements**:
- Windows 10/11
- PowerToys v0.97.0 or higher installed
- PowerToys must be running in the background

**Example Workflows**:

*Batch Image Processing*:
```json
{
  "action": "image_resize",
  "source": "C:/Photos",
  "width": 1920,
  "height": 1080,
  "format": "jpg"
}
```

*Automated File Renaming*:
```json
{
  "action": "power_rename",
  "path": "C:/Documents",
  "search": "document",
  "replace": "report",
  "regex": false
}
```

*Window Layout Management*:
```json
{
  "action": "fancyzones_layout",
  "layout": "three-column",
  "monitor": 0
}
```

**Security Note**: This server requires PowerToys to be installed and may need elevated permissions for certain operations. Only grant access to trusted automation scripts.

**Implementation Note**: As of now, there isn't an official PowerToys MCP server. However, you can build one using:
- The [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) with PowerToys CLI commands
- PowerShell automation scripts wrapped in an MCP server
- The [PowerToys Run API](https://learn.microsoft.com/windows/powertoys/run) for programmatic access
- Direct integration with PowerToys settings files and configuration

For building your own PowerToys MCP server, see the [Creating Custom Servers](#creating-custom-servers) section below and the [official MCP documentation](https://modelcontextprotocol.io/docs/).

---

## NOIZYLAB Custom Servers

### GABRIEL - AI System Integration

Access GABRIEL AI system capabilities, voice processing, and system monitoring.

**Configuration**:
```json
{
  "mcpServers": {
    "gabriel": {
      "transport": "stdio",
      "command": "python3",
      "args": ["/path/to/gabriel/mcp_servers/gabriel_mcp/server.py"]
    }
  }
}
```

**Available Tools**:
- `system_status`: Get GABRIEL system health
- `voice_process`: Process voice commands
- `ai_query`: Query AI models (Gemini, Groq, Ollama)
- `world_healer`: Run optimization tasks
- `portal_control`: Manage portal services

**Use Cases**: System administration, AI interactions, voice processing

---

### Vault - Secure Storage

Access and manage secure data vault.

**Configuration**:
```json
{
  "mcpServers": {
    "vault": {
      "transport": "stdio",
      "command": "python3",
      "args": ["./servers/vault_server.py"]
    }
  }
}
```

**Available Tools**:
- `store_secret`: Store encrypted data
- `retrieve_secret`: Get encrypted data
- `list_secrets`: Show available secrets
- `delete_secret`: Remove secrets

**Use Cases**: Credential management, secret storage, configuration

---

### OMEN - Remote System Management

Manage and monitor remote HP-OMEN system.

**Configuration**:
```json
{
  "mcpServers": {
    "omen": {
      "transport": "stdio",
      "command": "python3",
      "args": ["./servers/omen_server.py"]
    }
  }
}
```

**Available Tools**:
- `check_status`: Check OMEN system status
- `remote_execute`: Execute commands remotely
- `transfer_file`: Transfer files to/from OMEN
- `monitor_performance`: Get performance metrics

**Use Cases**: Remote administration, performance monitoring, file transfer

---

## Adding New Servers

To add a new MCP server to your configuration:

1. Install the server (if it's an npm package):
   ```bash
   npx -y @modelcontextprotocol/server-<name>
   ```

2. Add to your `mcp.json`:
   ```json
   {
     "mcpServers": {
       "server-name": {
         "transport": "stdio",
         "command": "npx",
         "args": ["-y", "@modelcontextprotocol/server-<name>"]
       }
     }
   }
   ```

3. Enable the server:
   ```bash
   agent mcp enable server-name
   ```

4. Verify it's working:
   ```bash
   agent mcp list
   agent mcp list-tools server-name
   ```

## Creating Custom Servers

You can create your own MCP servers to integrate custom tools and data sources. See the [official MCP documentation](https://modelcontextprotocol.io/docs/) for guides on building servers in:

- Python
- TypeScript/JavaScript
- Go
- Rust

## Related

- [MCP Overview](/docs/context/mcp.md): Configuration and authentication guide
- [MCP CLI Commands](/docs/cli/mcp.md): Command-line management
- [Official MCP Servers](https://github.com/modelcontextprotocol): Browse more servers
