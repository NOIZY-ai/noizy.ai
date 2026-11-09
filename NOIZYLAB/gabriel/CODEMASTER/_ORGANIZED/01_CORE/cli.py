#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    NOIZYLAB CLI v1.0 - GABRIEL COMMAND LINE                  ║
║                    GORUNFREE x1000                                           ║
║                                                                              ║
║  One command. All power. Zero latency.                                       ║
║  Usage: noizylab <command> [args]                                           ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import sys
import os
import json
import argparse
from pathlib import Path
from datetime import datetime

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))


def cmd_status(args):
    """Show system status"""
    from core.turbo_dispatcher import get_dispatcher
    d = get_dispatcher()
    result = d.dispatch("status")
    
    print("\n🚀 GABRIEL SYSTEM STATUS")
    print("=" * 50)
    for k, v in result.items():
        print(f"  {k}: {v}")
    print()


def cmd_ask(args):
    """Ask GABRIEL a question"""
    prompt = " ".join(args.prompt)
    provider = args.provider or "Claude"
    
    print(f"\n🧠 Asking {provider}...")
    print("-" * 50)
    
    from core.turbo_dispatcher import dispatch
    result = dispatch("ask", prompt, provider)
    
    if "error" in result:
        print(f"⚠️ Error: {result['error']}")
    else:
        print(result.get("response", "No response"))


def cmd_dream(args):
    """Multi-AI dream session"""
    prompt = " ".join(args.prompt)
    providers = args.providers.split(",") if args.providers else ["Claude", "Gemini"]
    
    print(f"\n🌙 Dreaming with {', '.join(providers)}...")
    print("-" * 50)
    
    from core.turbo_dispatcher import dispatch
    result = dispatch("dream", prompt, providers)
    
    if "error" in result:
        print(f"⚠️ Error: {result['error']}")
    else:
        for provider, vision in result.get("visions", {}).items():
            print(f"\n### {provider}:")
            print(vision[:500])


def cmd_flow(args):
    """Full creative flow"""
    prompt = " ".join(args.prompt)
    
    print("\n⚡ FULL CREATIVE FLOW")
    print("-" * 50)
    
    from core.turbo_dispatcher import dispatch
    result = dispatch("flow", prompt)
    
    if "error" in result:
        print(f"⚠️ Error: {result['error']}")
    else:
        print(f"Agent: {result.get('agent', 'Unknown')}")
        print(f"\nMerged Vision:\n{result.get('merged', 'No merge')[:1000]}")


def cmd_scan(args):
    """Run visual scanner"""
    print("\n🔍 Running FISHNET Visual Scanner...")
    print("-" * 50)
    
    from core.turbo_dispatcher import dispatch
    result = dispatch("scan", args.path or "/Volumes")
    
    print(f"Status: {result.get('status', 'unknown')}")
    if result.get('output_lines'):
        print(f"Output lines: {result['output_lines']}")


def cmd_index(args):
    """Index code files"""
    print("\n📇 Running Forensic Scanner...")
    print("-" * 50)
    
    from core.turbo_dispatcher import dispatch
    result = dispatch("index")
    
    print(f"Status: {result.get('status', 'unknown')}")
    if result.get('output'):
        print(result['output'][-1000:])


def cmd_sovereign(args):
    """Run SOVEREIGN_FINAL_100"""
    print("\n🌟 ACTIVATING SOVEREIGN PROTOCOL...")
    print("-" * 50)
    
    from core.turbo_dispatcher import dispatch
    result = dispatch("sovereign")
    
    for k, v in result.items():
        print(f"  {k}: {v}")


def cmd_portal(args):
    """Open DREAMCHAMBER portal"""
    print("\n🚪 Opening DREAMCHAMBER Portal...")
    
    from core.turbo_dispatcher import dispatch
    result = dispatch("portal")
    
    print(f"Status: {result.get('status', 'unknown')}")


def cmd_slack(args):
    """Send message to Slack"""
    message = " ".join(args.message)
    channel = args.channel or "#social"
    
    print(f"\n💬 Sending to Slack ({channel})...")
    
    from core.turbo_dispatcher import dispatch
    result = dispatch("slack", message, channel)
    
    if result.get("ok"):
        print("✅ Message sent!")
    else:
        print(f"⚠️ Error: {result.get('error', 'Unknown')}")


def cmd_agents(args):
    """List available agents"""
    from core.agents import AGENT_PROMPTS, AGENT_INFO
    
    print("\n🤖 AVAILABLE AGENTS")
    print("=" * 60)
    
    for name, prompt in AGENT_PROMPTS.items():
        info = AGENT_INFO.get(name, {})
        cat = info.get("category", "unknown")
        prov = info.get("provider", "unknown")
        
        print(f"\n{name} [{cat}] → {prov}")
        print(f"  {prompt[:80]}...")


def cmd_help(args):
    """Show help"""
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    NOIZYLAB CLI v1.0 - GABRIEL COMMAND LINE                  ║
║                    GORUNFREE x1000                                           ║
╚══════════════════════════════════════════════════════════════════════════════╝

COMMANDS:
  status              Show system status
  ask <prompt>        Ask GABRIEL a question  
  dream <prompt>      Multi-AI dream session (parallel)
  flow <prompt>       Full creative flow (route → dream → merge)
  scan [path]         Run visual scanner
  index               Index code files (forensic scanner)
  sovereign           Run SOVEREIGN_FINAL_100 activation
  portal              Open DREAMCHAMBER portal
  slack <message>     Send message to MC96DIGIUNIVERSE Slack
  agents              List available agents
  help                Show this help

OPTIONS:
  --provider, -p      AI provider (Claude, Gemini, OpenAI, DeepSeek)
  --providers         Comma-separated providers for dream
  --channel, -c       Slack channel (default: #social)

EXAMPLES:
  noizylab ask "What is the meaning of life?"
  noizylab dream "Design a neural interface" --providers Claude,Gemini,OpenAI
  noizylab flow "Create a new microservice"
  noizylab slack "Hello from GABRIEL!" -c "#general"

GORUNFREE x1000 🚀
""")


def main():
    parser = argparse.ArgumentParser(
        description="NOIZYLAB CLI - GABRIEL Command Line",
        add_help=False
    )
    
    subparsers = parser.add_subparsers(dest="command")
    
    # Status
    subparsers.add_parser("status", help="Show system status")
    
    # Ask
    ask_parser = subparsers.add_parser("ask", help="Ask GABRIEL")
    ask_parser.add_argument("prompt", nargs="+")
    ask_parser.add_argument("-p", "--provider", default="Claude")
    
    # Dream
    dream_parser = subparsers.add_parser("dream", help="Multi-AI dream")
    dream_parser.add_argument("prompt", nargs="+")
    dream_parser.add_argument("--providers", default="Claude,Gemini")
    
    # Flow
    flow_parser = subparsers.add_parser("flow", help="Full creative flow")
    flow_parser.add_argument("prompt", nargs="+")
    
    # Scan
    scan_parser = subparsers.add_parser("scan", help="Run visual scanner")
    scan_parser.add_argument("path", nargs="?", default="/Volumes")
    
    # Index
    subparsers.add_parser("index", help="Index code files")
    
    # Sovereign
    subparsers.add_parser("sovereign", help="Run SOVEREIGN_FINAL_100")
    
    # Portal
    subparsers.add_parser("portal", help="Open DREAMCHAMBER portal")
    
    # Slack
    slack_parser = subparsers.add_parser("slack", help="Send to Slack")
    slack_parser.add_argument("message", nargs="+")
    slack_parser.add_argument("-c", "--channel", default="#social")
    
    # Agents
    subparsers.add_parser("agents", help="List available agents")
    
    # Help
    subparsers.add_parser("help", help="Show help")
    
    args = parser.parse_args()
    
    if not args.command or args.command == "help":
        cmd_help(args)
        return
    
    commands = {
        "status": cmd_status,
        "ask": cmd_ask,
        "dream": cmd_dream,
        "flow": cmd_flow,
        "scan": cmd_scan,
        "index": cmd_index,
        "sovereign": cmd_sovereign,
        "portal": cmd_portal,
        "slack": cmd_slack,
        "agents": cmd_agents,
    }
    
    handler = commands.get(args.command)
    if handler:
        try:
            handler(args)
        except Exception as e:
            print(f"⚠️ Error: {e}")
            sys.exit(1)
    else:
        print(f"Unknown command: {args.command}")
        cmd_help(args)
        sys.exit(1)


if __name__ == "__main__":
    main()
