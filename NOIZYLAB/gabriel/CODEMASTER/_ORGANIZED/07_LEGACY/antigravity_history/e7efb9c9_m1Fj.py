#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    GITHUB WEBHOOK RECEIVER v1.0                              ║
║                    MC96DIGIUNIVERSE INTEGRATION                              ║
║                                                                              ║
║  Receive GitHub events → Process with GABRIEL → Send to Slack               ║
║  Full event-driven automation. Zero latency. GORUNFREE.                     ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import os
import json
import hashlib
import hmac
from typing import Optional, Callable, Any
from dataclasses import dataclass, field
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading


@dataclass
class WebhookConfig:
    """GitHub webhook configuration"""
    secret: Optional[str] = None
    port: int = 8080
    host: str = "0.0.0.0"


@dataclass
class GitHubEvent:
    """Parsed GitHub webhook event"""
    event_type: str
    action: Optional[str]
    repository: str
    sender: str
    payload: dict
    received_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def summary(self) -> str:
        """Generate human-readable summary"""
        summaries = {
            "push": lambda: f"🔀 Push to {self.repository} by {self.sender}",
            "pull_request": lambda: f"🔃 PR {self.action}: {self.payload.get('pull_request', {}).get('title', 'Unknown')}",
            "issues": lambda: f"📋 Issue {self.action}: {self.payload.get('issue', {}).get('title', 'Unknown')}",
            "create": lambda: f"✨ Created {self.payload.get('ref_type', 'ref')}: {self.payload.get('ref', 'Unknown')}",
            "delete": lambda: f"🗑️ Deleted {self.payload.get('ref_type', 'ref')}: {self.payload.get('ref', 'Unknown')}",
            "release": lambda: f"🚀 Release {self.action}: {self.payload.get('release', {}).get('tag_name', 'Unknown')}",
            "workflow_run": lambda: f"⚙️ Workflow {self.action}: {self.payload.get('workflow_run', {}).get('name', 'Unknown')}",
            "star": lambda: f"⭐ Repository {'starred' if self.action == 'created' else 'unstarred'} by {self.sender}",
            "fork": lambda: f"🍴 Repository forked by {self.sender}",
            "issue_comment": lambda: f"💬 Comment on issue by {self.sender}",
            "commit_comment": lambda: f"💬 Comment on commit by {self.sender}",
        }
        
        generator = summaries.get(self.event_type, lambda: f"📌 {self.event_type} event")
        return generator()


class GitHubWebhookHandler(BaseHTTPRequestHandler):
    """HTTP handler for GitHub webhooks"""
    
    receiver = None  # Set by GitHubWebhookReceiver
    
    def do_POST(self):
        """Handle incoming webhook POST"""
        # Get headers
        event_type = self.headers.get("X-GitHub-Event", "unknown")
        signature = self.headers.get("X-Hub-Signature-256", "")
        delivery_id = self.headers.get("X-GitHub-Delivery", "")
        
        # Read body
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)
        
        # Verify signature if secret configured
        if self.receiver.config.secret:
            if not self._verify_signature(body, signature):
                self.send_response(401)
                self.end_headers()
                self.wfile.write(b"Invalid signature")
                return
        
        # Parse payload
        try:
            payload = json.loads(body.decode())
        except json.JSONDecodeError:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Invalid JSON")
            return
        
        # Create event object
        event = GitHubEvent(
            event_type=event_type,
            action=payload.get("action"),
            repository=payload.get("repository", {}).get("full_name", "unknown"),
            sender=payload.get("sender", {}).get("login", "unknown"),
            payload=payload
        )
        
        # Process event
        self.receiver._process_event(event)
        
        # Send response
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"status": "received", "event": event_type}).encode())
    
    def _verify_signature(self, body: bytes, signature: str) -> bool:
        """Verify GitHub webhook signature"""
        if not signature.startswith("sha256="):
            return False
        
        expected = hmac.new(
            self.receiver.config.secret.encode(),
            body,
            hashlib.sha256
        ).hexdigest()
        
        return hmac.compare_digest(f"sha256={expected}", signature)
    
    def log_message(self, format, *args):
        """Suppress default logging"""
        pass


class GitHubWebhookReceiver:
    """
    GitHub Webhook Receiver
    
    Receives GitHub events and processes them through handlers.
    Integrates with Slack bridge for notifications.
    """
    
    def __init__(self, config: Optional[WebhookConfig] = None):
        self.config = config or WebhookConfig(
            secret=os.environ.get("GITHUB_WEBHOOK_SECRET"),
            port=int(os.environ.get("GITHUB_WEBHOOK_PORT", 8080))
        )
        self.handlers: dict[str, list[Callable]] = {}
        self.events: list[GitHubEvent] = []
        self.server: Optional[HTTPServer] = None
        self._running = False
        
        # Register default handlers
        self._register_defaults()
    
    def on(self, event_type: str, handler: Callable[[GitHubEvent], None]):
        """Register an event handler"""
        if event_type not in self.handlers:
            self.handlers[event_type] = []
        self.handlers[event_type].append(handler)
    
    def _register_defaults(self):
        """Register default event handlers"""
        
        def log_event(event: GitHubEvent):
            print(f"[GITHUB] {event.summary()}")
        
        # Log all events by default
        self.on("*", log_event)
    
    def _process_event(self, event: GitHubEvent):
        """Process an incoming event"""
        self.events.append(event)
        
        # Call wildcard handlers
        for handler in self.handlers.get("*", []):
            try:
                handler(event)
            except Exception as e:
                print(f"[ERROR] Handler failed: {e}")
        
        # Call specific handlers
        for handler in self.handlers.get(event.event_type, []):
            try:
                handler(event)
            except Exception as e:
                print(f"[ERROR] Handler failed: {e}")
    
    def start(self, blocking: bool = True):
        """Start the webhook server"""
        GitHubWebhookHandler.receiver = self
        
        self.server = HTTPServer(
            (self.config.host, self.config.port),
            GitHubWebhookHandler
        )
        
        self._running = True
        print(f"🚀 GitHub Webhook Receiver started on {self.config.host}:{self.config.port}")
        
        if blocking:
            try:
                self.server.serve_forever()
            except KeyboardInterrupt:
                self.stop()
        else:
            thread = threading.Thread(target=self.server.serve_forever)
            thread.daemon = True
            thread.start()
    
    def stop(self):
        """Stop the webhook server"""
        if self.server:
            self.server.shutdown()
            self._running = False
            print("🛑 GitHub Webhook Receiver stopped")
    
    def get_recent_events(self, limit: int = 10) -> list[GitHubEvent]:
        """Get recent events"""
        return self.events[-limit:]
    
    def integrate_slack(self, channel: str = "#github"):
        """
        Add Slack integration for GitHub events.
        Sends formatted notifications to Slack.
        """
        try:
            from .slack_bridge import create_slack_bridge
            bridge = create_slack_bridge()
            
            def slack_handler(event: GitHubEvent):
                # Create Slack blocks
                blocks = [
                    {
                        "type": "header",
                        "text": {"type": "plain_text", "text": f"GitHub: {event.event_type}", "emoji": True}
                    },
                    {
                        "type": "section",
                        "text": {"type": "mrkdwn", "text": event.summary()}
                    },
                    {
                        "type": "context",
                        "elements": [
                            {"type": "mrkdwn", "text": f"📦 `{event.repository}` | 👤 {event.sender} | {event.received_at}"}
                        ]
                    }
                ]
                
                bridge.send_message(
                    text=event.summary(),
                    channel=channel,
                    blocks=blocks
                )
            
            self.on("*", slack_handler)
            print(f"✅ Slack integration enabled for {channel}")
            
        except ImportError:
            print("⚠️ Slack bridge not available")
    
    def integrate_gabriel(self):
        """
        Add GABRIEL AI integration.
        Processes events through AI for smart responses.
        """
        try:
            from .turbo_dispatcher import dispatch
            
            def gabriel_handler(event: GitHubEvent):
                # Only process certain events
                if event.event_type not in ["issues", "pull_request"]:
                    return
                
                # Use GABRIEL to analyze
                prompt = f"Analyze this GitHub event and suggest actions:\n{event.summary()}\nDetails: {json.dumps(event.payload.get('issue', event.payload.get('pull_request', {})), indent=2)[:1000]}"
                
                result = dispatch("ask", prompt, "Claude")
                if "response" in result:
                    print(f"[GABRIEL] {result['response'][:200]}...")
            
            self.on("issues", gabriel_handler)
            self.on("pull_request", gabriel_handler)
            print("✅ GABRIEL AI integration enabled")
            
        except ImportError:
            print("⚠️ Turbo dispatcher not available")


# Factory function
def create_webhook_receiver(
    secret: Optional[str] = None,
    port: int = 8080
) -> GitHubWebhookReceiver:
    """Create a configured webhook receiver"""
    config = WebhookConfig(
        secret=secret or os.environ.get("GITHUB_WEBHOOK_SECRET"),
        port=port
    )
    return GitHubWebhookReceiver(config)


__all__ = [
    'WebhookConfig', 'GitHubEvent', 'GitHubWebhookReceiver',
    'create_webhook_receiver'
]


if __name__ == "__main__":
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║              GITHUB WEBHOOK RECEIVER v1.0                    ║")
    print("║              MC96DIGIUNIVERSE INTEGRATION                    ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print()
    
    receiver = create_webhook_receiver()
    
    # Add custom handler
    def my_handler(event: GitHubEvent):
        if event.event_type == "push":
            print(f"🔥 Code pushed! {event.repository}")
    
    receiver.on("push", my_handler)
    
    # Start server
    print("Starting webhook server...")
    print("Configure your GitHub webhook to point to: http://<your-ip>:8080")
    print("Press Ctrl+C to stop")
    print()
    
    receiver.start()
