#!/usr/bin/env python3
"""
🌙 
 MCP SERVER
Expose AI Council to Windsurf/Cascade via Model Context Protocol
"""

import os
import sys
import json
import asyncio
from pathlib import Path
from datetime import datetime
from typing import Any

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent))

import mcp.types as types
from mcp.server import Server
from mcp.server.stdio import stdio_server

from dreamchamber import DreamChamber

app = Server("dreamchamber")
chamber = DreamChamber()


@app.list_tools()
async def list_tools() -> list[types.Tool]:
    """List DREAMCHAMBER tools"""
    return [
        types.Tool(
            name="dream_ask",
            description="🌙 Ask the AI Council a question. Queries multiple models in parallel.",
            inputSchema={
                "type": "object",
                "properties": {
                    "question": {"type": "string", "description": "Your question for the council"},
                    "context": {"type": "string", "description": "Additional context (optional)"},
                },
                "required": ["question"]
            }
        ),
        types.Tool(
            name="dream_full",
            description="🌙 Full DREAMCHAMBER analysis: Ask → Synthesize → Insights → Consensus",
            inputSchema={
                "type": "object",
                "properties": {
                    "question": {"type": "string", "description": "Your question"},
                    "context": {"type": "string", "description": "Additional context (optional)"},
                },
                "required": ["question"]
            }
        ),
        types.Tool(
            name="dream_synthesize",
            description="🔮 Synthesize council responses into unified wisdom",
            inputSchema={
                "type": "object",
                "properties": {
                    "session_id": {"type": "string", "description": "Session ID (uses current if empty)"},
                },
            }
        ),
        types.Tool(
            name="dream_insights",
            description="💡 Extract key insights from council responses",
            inputSchema={
                "type": "object",
                "properties": {
                    "session_id": {"type": "string", "description": "Session ID (optional)"},
                    "count": {"type": "integer", "description": "Number of insights (default 5)"},
                },
            }
        ),
        types.Tool(
            name="dream_consensus",
            description="🤝 Find consensus among council members",
            inputSchema={
                "type": "object",
                "properties": {
                    "session_id": {"type": "string", "description": "Session ID (optional)"},
                },
            }
        ),
        types.Tool(
            name="dream_status",
            description="📊 Get DREAMCHAMBER and council status",
            inputSchema={"type": "object", "properties": {}}
        ),
        types.Tool(
            name="dream_sessions",
            description="📜 List recent DREAMCHAMBER sessions",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {"type": "integer", "description": "Number of sessions (default 10)"},
                },
            }
        ),
        types.Tool(
            name="dream_load",
            description="📂 Load a previous session",
            inputSchema={
                "type": "object",
                "properties": {
                    "session_id": {"type": "string", "description": "Session ID to load"},
                },
                "required": ["session_id"]
            }
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    """Handle DREAMCHAMBER tool calls"""
    
    try:
        if name == "dream_ask":
            question = arguments.get("question", "")
            context = arguments.get("context", "")
            session = chamber.convene(question, context)
            
            result = {
                "session_id": session["id"],
                "question": session["question"],
                "council_size": session["council_size"],
                "responses": [
                    {
                        "member": r["member"],
                        "model": r["model"],
                        "response": r["response"][:1000] + "..." if len(r["response"]) > 1000 else r["response"],
                        "success": r["success"],
                        "latency_ms": r["latency_ms"]
                    }
                    for r in session["responses"]
                ]
            }
            return [types.TextContent(type="text", text=json.dumps(result, indent=2))]
        
        elif name == "dream_full":
            question = arguments.get("question", "")
            context = arguments.get("context", "")
            session = chamber.full_analysis(question, context)
            
            result = {
                "session_id": session["id"],
                "question": session["question"],
                "responses_count": len(session["responses"]),
                "synthesis": session.get("synthesis", "")[:2000],
                "insights": session.get("insights", []),
                "consensus": session.get("consensus", "")[:1000],
                "best_member": session.get("best_member", "")
            }
            return [types.TextContent(type="text", text=json.dumps(result, indent=2))]
        
        elif name == "dream_synthesize":
            session_id = arguments.get("session_id", "")
            if session_id:
                session = chamber.load_session(session_id)
                if session:
                    chamber.current_session = session
            
            synthesis = chamber.synthesize()
            return [types.TextContent(type="text", text=synthesis)]
        
        elif name == "dream_insights":
            session_id = arguments.get("session_id", "")
            count = arguments.get("count", 5)
            
            if session_id:
                session = chamber.load_session(session_id)
                if session:
                    chamber.current_session = session
            
            insights = chamber.extract_insights(count=count)
            return [types.TextContent(type="text", text=json.dumps(insights, indent=2))]
        
        elif name == "dream_consensus":
            session_id = arguments.get("session_id", "")
            if session_id:
                session = chamber.load_session(session_id)
                if session:
                    chamber.current_session = session
            
            consensus = chamber.find_consensus()
            return [types.TextContent(type="text", text=consensus)]
        
        elif name == "dream_status":
            status = chamber.get_council_status()
            return [types.TextContent(type="text", text=json.dumps(status, indent=2))]
        
        elif name == "dream_sessions":
            limit = arguments.get("limit", 10)
            sessions = chamber.list_sessions(limit)
            return [types.TextContent(type="text", text=json.dumps(sessions, indent=2))]
        
        elif name == "dream_load":
            session_id = arguments.get("session_id", "")
            session = chamber.load_session(session_id)
            if session:
                chamber.current_session = session
                return [types.TextContent(type="text", text=f"Loaded session: {session_id}\nQuestion: {session['question']}\nResponses: {len(session.get('responses', []))}")]
            return [types.TextContent(type="text", text=f"Session not found: {session_id}")]
        
        else:
            return [types.TextContent(type="text", text=f"Unknown tool: {name}")]
    
    except Exception as e:
        return [types.TextContent(type="text", text=f"Error: {str(e)}")]


async def main():
    """Run DREAMCHAMBER MCP server"""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
