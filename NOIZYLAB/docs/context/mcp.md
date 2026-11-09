# Model Context Protocol (MCP)

## Overview

The Model Context Protocol (MCP) is an open standard that enables seamless integration between AI applications and external data sources and tools. MCP allows AI systems to securely connect to various services, databases, and APIs, providing enhanced context and capabilities.

In the NOIZYLAB ecosystem, both the editor and CLI support MCP servers through a unified configuration approach - any MCP servers you configure work across all tools.

## Key Benefits

- **Unified Configuration**: Configure once, use everywhere (editor and CLI)
- **Extensible**: Connect to any data source or tool that implements the MCP protocol
- **Secure**: Built-in authentication and permission management
- **Flexible**: Support for multiple transport methods (stdio, HTTP, SSE)

## Configuration

MCP servers are configured through `mcp.json` files. The system follows a configuration precedence model:

1. **Project-level**: `<project>/.cursor/mcp.json` or `<project>/mcp.json`
2. **Global-level**: `~/.cursor/mcp.json` or `~/.config/cursor/mcp.json`
3. **Nested**: Parent directories are automatically discovered

### Configuration File Structure

The `mcp.json` file defines available MCP servers and their connection details:

```json
{
  "mcpServers": {
    "server-name": {
      "transport": "stdio",
      "command": "python3",
      "args": ["path/to/server.py"],
      "env": {
        "API_KEY": "${YOUR_API_KEY}"
      }
    },
    "http-server": {
      "transport": "http",
      "url": "http://localhost:8080/mcp",
      "headers": {
        "Authorization": "Bearer ${TOKEN}"
      }
    },
    "sse-server": {
      "transport": "sse",
      "url": "http://localhost:8081/events"
    }
  }
}
```

### Configuration Fields

#### Required Fields

- **transport**: Connection method - `stdio`, `http`, or `sse`
- **command** (stdio only): Executable to run the MCP server
- **args** (stdio only): Arguments to pass to the command
- **url** (http/sse only): Server endpoint URL

#### Optional Fields

- **env**: Environment variables for the MCP server process
- **headers**: HTTP headers for http/sse transports
- **enabled**: Boolean to enable/disable server (default: true)

## Transport Methods

### stdio (Standard Input/Output)

The most common transport method, where the MCP server runs as a subprocess that communicates via stdin/stdout.

**Best for**: Local tools, command-line utilities, Python/Node.js servers

**Example**:
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

### HTTP

RESTful API-based communication for remote or web-based MCP servers.

**Best for**: Web services, remote APIs, cloud-hosted tools

**Example**:
```json
{
  "mcpServers": {
    "api-service": {
      "transport": "http",
      "url": "https://api.example.com/mcp",
      "headers": {
        "Authorization": "Bearer ${API_TOKEN}"
      }
    }
  }
}
```

### SSE (Server-Sent Events)

Real-time streaming communication for servers that need to push updates.

**Best for**: Real-time data feeds, monitoring services, live updates

**Example**:
```json
{
  "mcpServers": {
    "live-data": {
      "transport": "sse",
      "url": "http://localhost:8080/events"
    }
  }
}
```

## Authentication

MCP supports various authentication methods depending on the server implementation:

### Environment Variables

Store sensitive credentials in environment variables referenced in your config:

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

### OAuth/Token-Based

Some MCP servers support OAuth or token-based authentication. Use the `agent mcp login <identifier>` command to authenticate:

```bash
agent mcp login github
```

This launches an authentication flow and stores credentials securely.

### API Keys

For simple API key authentication, include the key in the configuration or environment:

```json
{
  "mcpServers": {
    "service": {
      "transport": "http",
      "url": "https://api.service.com/mcp",
      "headers": {
        "X-API-Key": "${SERVICE_API_KEY}"
      }
    }
  }
}
```

## Server States

MCP servers can be in different states:

- **connected**: Server is running and available
- **disconnected**: Server is not running or unavailable
- **disabled**: Server is explicitly disabled in configuration
- **error**: Server encountered an error

Use `agent mcp list` to view the current state of all configured servers.

## Best Practices

### Security

1. **Never commit credentials**: Use environment variables for all sensitive data
2. **Use project configs for team sharing**: Store non-sensitive server configs in project-level `mcp.json`
3. **Keep global configs private**: Store personal credentials in global config
4. **Review server permissions**: Understand what data each MCP server can access

### Performance

1. **Disable unused servers**: Keep only active servers enabled to reduce overhead
2. **Use local servers when possible**: stdio transport is typically faster than network-based
3. **Monitor server status**: Check `agent mcp list` regularly to ensure servers are healthy

### Organization

1. **Use descriptive names**: Choose clear, meaningful identifiers for servers
2. **Group related servers**: Keep related servers in the same config file
3. **Document custom servers**: Add comments in your config explaining server purposes
4. **Version your configs**: Track changes to project-level MCP configurations

## Troubleshooting

### Server Won't Connect

1. Verify the command and args are correct
2. Check that required dependencies are installed
3. Ensure environment variables are set
4. Review server logs for errors

### Authentication Failures

1. Verify credentials are correct and not expired
2. Check environment variable names match config
3. Try re-authenticating with `agent mcp login <identifier>`
4. Ensure the server supports the authentication method

### Performance Issues

1. Check if too many servers are enabled
2. Verify network connectivity for remote servers
3. Monitor system resources (CPU, memory)
4. Consider using local alternatives for remote servers

## Next Steps

- [MCP CLI Commands](/docs/cli/mcp.md): Learn how to manage MCP servers from the command line
- [Available MCP Servers](/docs/context/mcp/directory.md): Browse pre-built MCP servers
- [Creating Custom Servers](https://modelcontextprotocol.io/docs/): Build your own MCP servers

## Related Resources

- [Official MCP Specification](https://modelcontextprotocol.io/)
- [MCP SDK Documentation](https://modelcontextprotocol.io/docs/sdk/)
- [Community MCP Servers](https://github.com/modelcontextprotocol)
