import sys
import json
import os
import asyncio
from typing import Any, Dict, List, Optional
import mcp.types as types
from mcp.server import Server
from mcp.server.stdio import stdio_server

# Initialize GABRIEL MCP Server
app = Server("gabriel-mcp")

# Paths
INDEX_FILE = "/Users/m2ultra/NOIZYLAB/GABRIEL/gabriel_index.json"
GABRIEL_ROOT = "/Users/m2ultra/NOIZYLAB/GABRIEL"

@app.list_resources()
async def list_resources() -> list[types.Resource]:
    return [
        types.Resource(
            uri="gabriel://index",
            name="Gabriel Codebase Index",
            description="Full index of NOIZYLAB codebase files",
            mimeType="application/json",
        ),
        types.Resource(
            uri="gabriel://logs/server",
            name="Gabriel Server Log",
            description="Live logs from Gabriel Server",
            mimeType="text/plain",
        )
    ]

@app.read_resource()
async def read_resource(uri: str) -> str:
    if uri == "gabriel://index":
        if os.path.exists(INDEX_FILE):
            with open(INDEX_FILE, 'r') as f:
                return f.read()
        return json.dumps({"error": "Index not found"})
    
    if uri == "gabriel://logs/server":
        log_path = os.path.join(GABRIEL_ROOT, "server.log")
        if os.path.exists(log_path):
             with open(log_path, 'r') as f:
                # Return last 10kb
                f.seek(0, 2)
                size = f.tell()
                f.seek(max(0, size - 10240))
                return f.read()
        return "No logs found."
        
    raise ValueError(f"Unknown resource: {uri}")

@app.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="search_codebase",
            description="Search the indexed codebase for files matching a query",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search term"},
                    "limit": {"type": "integer", "description": "Max results", "default": 10}
                },
                "required": ["query"]
            }
        ),
        types.Tool(
            name="read_file_content",
            description="Read content of any file in the codebase",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Absolute path to file"}
                },
                "required": ["path"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    if name == "search_codebase":
        query = arguments.get("query", "").lower()
        limit = arguments.get("limit", 10)
        
        if not os.path.exists(INDEX_FILE):
             return [types.TextContent(type="text", text="Error: Index not built yet.")]
             
        with open(INDEX_FILE, 'r') as f:
            index = json.load(f)
            
        results = []
        for file in index.get("files", []):
            if query in file["path"].lower() or query in file["name"].lower():
                results.append(file)
                if len(results) >= limit:
                    break
                    
        return [types.TextContent(type="text", text=json.dumps(results, indent=2))]

    if name == "read_file_content":
        path = arguments.get("path")
        if not path or not os.path.exists(path):
            return [types.TextContent(type="text", text=f"Error: File not found: {path}")]
            
        try:
            with open(path, 'r') as f:
                content = f.read()
                return [types.TextContent(type="text", text=content)]
        except Exception as e:
            return [types.TextContent(type="text", text=f"Error reading file: {str(e)}")]

    raise ValueError(f"Unknown tool: {name}")

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
