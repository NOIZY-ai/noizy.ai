#!/usr/bin/env python3
"""
🔐 Anthropic Admin API Manager
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Direct management of Anthropic API keys via the Admin API.

Features:
  - List all organization API keys
  - Get key details
  - Update key name/status
  - Create new API keys
  - Archive/deactivate keys
  - Track key usage

Requirements:
  - ANTHROPIC_ADMIN_API_KEY environment variable set
  - Admin access to your Anthropic organization

Usage:
  # List all API keys
  python anthropic_admin.py list
  
  # Get specific key details
  python anthropic_admin.py get <key_id>
  
  # Update key name
  python anthropic_admin.py update <key_id> --name "New Name"
  
  # Deactivate a key
  python anthropic_admin.py update <key_id> --status inactive
  
  # Archive a key
  python anthropic_admin.py update <key_id> --status archived
  
  # Interactive mode
  python anthropic_admin.py

API Reference:
  https://docs.anthropic.com/en/api/admin-api
"""

import argparse
import json
import os
import sys
from datetime import datetime
from typing import Optional, Dict, List, Any

try:
    import httpx
    HAS_HTTPX = True
except ImportError:
    HAS_HTTPX = False

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.prompt import Prompt, Confirm
    from rich.box import ROUNDED
    from rich.text import Text
    HAS_RICH = True
except ImportError:
    HAS_RICH = False

# =============================================================================
# Configuration
# =============================================================================

ANTHROPIC_ADMIN_API_BASE = "https://api.anthropic.com/v1/organizations"
console = Console() if HAS_RICH else None

# =============================================================================
# Admin API Client
# =============================================================================

class AnthropicAdminAPI:
    """Client for Anthropic Admin API."""
    
    def __init__(self, admin_api_key: Optional[str] = None):
        # Try ANTHROPIC_ADMIN_API_KEY first, then fall back to ANTHROPIC_API_KEY
        self.admin_api_key = (
            admin_api_key 
            or os.getenv("ANTHROPIC_ADMIN_API_KEY") 
            or os.getenv("ANTHROPIC_API_KEY")
        )
        if not self.admin_api_key:
            raise ValueError(
                "ANTHROPIC_ADMIN_API_KEY (or ANTHROPIC_API_KEY) not set. "
                "Get your admin key from https://console.anthropic.com/settings/admin-keys"
            )
        
        self.headers = {
            "X-Api-Key": self.admin_api_key,
            "Content-Type": "application/json",
        }
    
    def _request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict] = None,
    ) -> Dict:
        """Make API request."""
        url = f"{ANTHROPIC_ADMIN_API_BASE}/{endpoint}"
        
        if HAS_HTTPX:
            with httpx.Client(timeout=30.0) as client:
                if method == "GET":
                    response = client.get(url, headers=self.headers)
                elif method == "POST":
                    # POST requires Content-Type and body
                    response = client.post(url, headers=self.headers, json=data or {})
                elif method == "DELETE":
                    response = client.delete(url, headers=self.headers)
                else:
                    raise ValueError(f"Unknown method: {method}")
                
                response.raise_for_status()
                return response.json()
        else:
            # Fallback to urllib
            import urllib.request
            import urllib.error
            
            # For GET requests, don't include Content-Type
            headers = {"X-Api-Key": self.admin_api_key}
            if method == "POST":
                headers["Content-Type"] = "application/json"
            
            req = urllib.request.Request(url, headers=headers, method=method)
            if data and method == "POST":
                req.data = json.dumps(data).encode()
            
            try:
                with urllib.request.urlopen(req, timeout=30) as response:
                    return json.loads(response.read().decode())
            except urllib.error.HTTPError as e:
                error_body = e.read().decode()
                raise Exception(f"API Error {e.code}: {error_body}")
    
    # =========================================================================
    # API Key Management
    # =========================================================================
    
    def list_api_keys(
        self,
        limit: int = 100,
        status: Optional[str] = None,
    ) -> Dict:
        """
        List all API keys in the organization.
        
        Args:
            limit: Maximum number of keys to return
            status: Filter by status (active, inactive, archived)
        
        Returns:
            Dict with 'data' containing list of API keys
        """
        endpoint = f"api_keys?limit={limit}"
        if status:
            endpoint += f"&status={status}"
        return self._request("GET", endpoint)
    
    def get_api_key(self, key_id: str) -> Dict:
        """
        Get details of a specific API key.
        
        Args:
            key_id: ID of the API key
        
        Returns:
            API key details
        """
        return self._request("GET", f"api_keys/{key_id}")
    
    def update_api_key(
        self,
        key_id: str,
        name: Optional[str] = None,
        status: Optional[str] = None,
    ) -> Dict:
        """
        Update an API key's name or status.
        
        Args:
            key_id: ID of the API key
            name: New name for the key
            status: New status (active, inactive, archived)
        
        Returns:
            Updated API key details
        """
        data = {}
        if name:
            data["name"] = name
        if status:
            if status not in ("active", "inactive", "archived"):
                raise ValueError(f"Invalid status: {status}. Must be active, inactive, or archived")
            data["status"] = status
        
        return self._request("POST", f"api_keys/{key_id}", data)
    
    # =========================================================================
    # Organization Info
    # =========================================================================
    
    def get_organization(self) -> Dict:
        """Get organization details."""
        # Note: This endpoint may vary - adjust based on actual API
        return self._request("GET", "")
    
    # =========================================================================
    # Workspace Management
    # =========================================================================
    
    def list_workspaces(self, limit: int = 100) -> Dict:
        """List all workspaces."""
        return self._request("GET", f"workspaces?limit={limit}")
    
    def get_workspace(self, workspace_id: str) -> Dict:
        """Get workspace details."""
        return self._request("GET", f"workspaces/{workspace_id}")
    
    # =========================================================================
    # Member Management
    # =========================================================================
    
    def list_members(self, limit: int = 100) -> Dict:
        """List all organization members."""
        return self._request("GET", f"members?limit={limit}")
    
    def get_member(self, member_id: str) -> Dict:
        """Get member details."""
        return self._request("GET", f"members/{member_id}")
    
    # =========================================================================
    # Invite Management
    # =========================================================================
    
    def list_invites(self, limit: int = 100) -> Dict:
        """List all pending invites."""
        return self._request("GET", f"invites?limit={limit}")

# =============================================================================
# Display Functions
# =============================================================================

def display_api_keys(keys: List[Dict]):
    """Display API keys in a table."""
    if not console:
        print("\n📊 API Keys:")
        for key in keys:
            status_icon = {"active": "✅", "inactive": "⏸️", "archived": "📦"}.get(key.get("status"), "❓")
            print(f"  {status_icon} {key.get('name', 'Unnamed')}")
            print(f"     ID: {key.get('id')}")
            print(f"     Hint: {key.get('partial_key_hint', 'N/A')}")
            print(f"     Created: {key.get('created_at', 'N/A')}")
            print()
        return
    
    table = Table(title="🔐 Anthropic API Keys", box=ROUNDED)
    table.add_column("Name", style="cyan")
    table.add_column("ID", style="dim")
    table.add_column("Status", style="green")
    table.add_column("Key Hint", style="yellow")
    table.add_column("Created", style="blue")
    table.add_column("Workspace", style="magenta")
    
    for key in keys:
        status = key.get("status", "unknown")
        status_display = {
            "active": "[green]✅ Active[/green]",
            "inactive": "[yellow]⏸️ Inactive[/yellow]",
            "archived": "[dim]📦 Archived[/dim]",
        }.get(status, status)
        
        created = key.get("created_at", "")
        if created:
            try:
                dt = datetime.fromisoformat(created.replace("Z", "+00:00"))
                created = dt.strftime("%Y-%m-%d %H:%M")
            except:
                pass
        
        workspace = key.get("workspace_id") or "[dim]Default[/dim]"
        
        table.add_row(
            key.get("name", "[dim]Unnamed[/dim]"),
            key.get("id", "N/A"),
            status_display,
            key.get("partial_key_hint", "N/A"),
            created,
            workspace,
        )
    
    console.print(table)

def display_key_details(key: Dict):
    """Display detailed info for a single key."""
    if not console:
        print(f"\n🔑 API Key: {key.get('name', 'Unnamed')}")
        print(f"   ID: {key.get('id')}")
        print(f"   Status: {key.get('status')}")
        print(f"   Hint: {key.get('partial_key_hint')}")
        print(f"   Created: {key.get('created_at')}")
        print(f"   Workspace: {key.get('workspace_id', 'Default')}")
        return
    
    status = key.get("status", "unknown")
    status_color = {"active": "green", "inactive": "yellow", "archived": "dim"}.get(status, "white")
    
    info = f"""
[cyan]Name:[/cyan] {key.get('name', 'Unnamed')}
[cyan]ID:[/cyan] {key.get('id')}
[cyan]Status:[/cyan] [{status_color}]{status}[/{status_color}]
[cyan]Key Hint:[/cyan] {key.get('partial_key_hint', 'N/A')}
[cyan]Created:[/cyan] {key.get('created_at', 'N/A')}
[cyan]Created By:[/cyan] {key.get('created_by', {}).get('type', 'N/A')} ({key.get('created_by', {}).get('id', 'N/A')})
[cyan]Workspace:[/cyan] {key.get('workspace_id') or 'Default'}
"""
    
    console.print(Panel(info.strip(), title="🔑 API Key Details", border_style="cyan"))

# =============================================================================
# Interactive Mode
# =============================================================================

def interactive_mode(api: AnthropicAdminAPI):
    """Interactive management mode."""
    if console:
        console.print(Panel(
            "🔐 [cyan]Anthropic Admin API Manager[/cyan]\n"
            "Manage your organization's API keys\n\n"
            "Commands: [green]list[/green], [green]get[/green], [green]update[/green], [green]help[/green], [green]quit[/green]",
            title="Welcome",
            border_style="cyan",
        ))
    else:
        print("\n🔐 Anthropic Admin API Manager")
        print("Commands: list, get, update, help, quit\n")
    
    while True:
        try:
            if console:
                cmd = Prompt.ask("\n[cyan]admin[/cyan]").strip().lower()
            else:
                cmd = input("\nadmin> ").strip().lower()
            
            if not cmd:
                continue
            
            if cmd in ("quit", "exit", "q"):
                break
            
            elif cmd == "list":
                result = api.list_api_keys()
                keys = result.get("data", [])
                display_api_keys(keys)
                if console:
                    console.print(f"\n[dim]Total: {len(keys)} keys[/dim]")
            
            elif cmd.startswith("get "):
                key_id = cmd[4:].strip()
                key = api.get_api_key(key_id)
                display_key_details(key)
            
            elif cmd.startswith("update "):
                parts = cmd[7:].strip().split()
                if len(parts) < 3:
                    print("Usage: update <key_id> --name <name> OR update <key_id> --status <active|inactive|archived>")
                    continue
                
                key_id = parts[0]
                name = None
                status = None
                
                i = 1
                while i < len(parts):
                    if parts[i] == "--name" and i + 1 < len(parts):
                        name = parts[i + 1]
                        i += 2
                    elif parts[i] == "--status" and i + 1 < len(parts):
                        status = parts[i + 1]
                        i += 2
                    else:
                        i += 1
                
                result = api.update_api_key(key_id, name=name, status=status)
                display_key_details(result)
                if console:
                    console.print("[green]✅ Key updated successfully[/green]")
            
            elif cmd == "workspaces":
                result = api.list_workspaces()
                workspaces = result.get("data", [])
                if console:
                    table = Table(title="🏢 Workspaces", box=ROUNDED)
                    table.add_column("Name", style="cyan")
                    table.add_column("ID", style="dim")
                    for ws in workspaces:
                        table.add_row(ws.get("name", "Unnamed"), ws.get("id", "N/A"))
                    console.print(table)
                else:
                    print("\n🏢 Workspaces:")
                    for ws in workspaces:
                        print(f"  - {ws.get('name')}: {ws.get('id')}")
            
            elif cmd == "members":
                result = api.list_members()
                members = result.get("data", [])
                if console:
                    table = Table(title="👥 Members", box=ROUNDED)
                    table.add_column("Name", style="cyan")
                    table.add_column("Email", style="green")
                    table.add_column("Role", style="yellow")
                    for member in members:
                        table.add_row(
                            member.get("name", "Unknown"),
                            member.get("email", "N/A"),
                            member.get("role", "N/A"),
                        )
                    console.print(table)
                else:
                    print("\n👥 Members:")
                    for member in members:
                        print(f"  - {member.get('name')}: {member.get('email')}")
            
            elif cmd == "help":
                help_text = """
Commands:
  list              - List all API keys
  get <key_id>      - Get details of a specific key
  update <key_id> --name <name>     - Rename a key
  update <key_id> --status <status> - Change key status (active/inactive/archived)
  workspaces        - List workspaces
  members           - List organization members
  help              - Show this help
  quit              - Exit
"""
                if console:
                    console.print(Panel(help_text.strip(), title="📚 Help", border_style="cyan"))
                else:
                    print(help_text)
            
            else:
                print(f"Unknown command: {cmd}. Type 'help' for available commands.")
        
        except KeyboardInterrupt:
            break
        except Exception as e:
            if console:
                console.print(f"[red]Error: {e}[/red]")
            else:
                print(f"Error: {e}")

# =============================================================================
# CLI
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="🔐 Anthropic Admin API Manager",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python anthropic_admin.py list
  python anthropic_admin.py get apikey_01234567890
  python anthropic_admin.py update apikey_01234567890 --name "Production Key"
  python anthropic_admin.py update apikey_01234567890 --status inactive
        """,
    )
    
    parser.add_argument(
        "command",
        nargs="?",
        default="interactive",
        choices=["interactive", "list", "get", "update", "workspaces", "members"],
        help="Command to run",
    )
    parser.add_argument(
        "key_id",
        nargs="?",
        help="API key ID (for get/update commands)",
    )
    parser.add_argument(
        "--name",
        help="New name for the API key",
    )
    parser.add_argument(
        "--status",
        choices=["active", "inactive", "archived"],
        help="New status for the API key",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output as JSON",
    )
    
    args = parser.parse_args()
    
    try:
        api = AnthropicAdminAPI()
    except ValueError as e:
        print(f"❌ {e}")
        sys.exit(1)
    
    try:
        if args.command == "interactive":
            interactive_mode(api)
        
        elif args.command == "list":
            result = api.list_api_keys()
            if args.json:
                print(json.dumps(result, indent=2))
            else:
                display_api_keys(result.get("data", []))
        
        elif args.command == "get":
            if not args.key_id:
                print("❌ key_id required for 'get' command")
                sys.exit(1)
            result = api.get_api_key(args.key_id)
            if args.json:
                print(json.dumps(result, indent=2))
            else:
                display_key_details(result)
        
        elif args.command == "update":
            if not args.key_id:
                print("❌ key_id required for 'update' command")
                sys.exit(1)
            if not args.name and not args.status:
                print("❌ --name or --status required for 'update' command")
                sys.exit(1)
            result = api.update_api_key(args.key_id, name=args.name, status=args.status)
            if args.json:
                print(json.dumps(result, indent=2))
            else:
                display_key_details(result)
                if console:
                    console.print("[green]✅ Key updated successfully[/green]")
        
        elif args.command == "workspaces":
            result = api.list_workspaces()
            if args.json:
                print(json.dumps(result, indent=2))
            else:
                for ws in result.get("data", []):
                    print(f"  - {ws.get('name')}: {ws.get('id')}")
        
        elif args.command == "members":
            result = api.list_members()
            if args.json:
                print(json.dumps(result, indent=2))
            else:
                for member in result.get("data", []):
                    print(f"  - {member.get('name')}: {member.get('email')}")
    
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
