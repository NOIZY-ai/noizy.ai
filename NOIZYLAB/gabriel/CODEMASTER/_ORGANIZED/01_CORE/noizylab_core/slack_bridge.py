#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    SLACK BRIDGE v1.0 - MC96DIGIUNIVERSE                      ║
║                    GORUNFREE EDITION                                          ║
║                                                                              ║
║  Bridge GABRIEL to the MC96DIGIUNIVERSE Slack Workspace.                     ║
║  Real-time AI collaboration. Zero Latency Communication.                     ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import os
import json
import urllib.request
import urllib.error
from typing import Optional, Any
from dataclasses import dataclass
from datetime import datetime


@dataclass
class SlackConfig:
    """Slack configuration"""
    bot_token: Optional[str] = None
    app_token: Optional[str] = None
    webhook_url: Optional[str] = None
    default_channel: str = "#social"


class SlackBridge:
    """
    Bridge between GABRIEL and MC96DIGIUNIVERSE Slack workspace.
    Enables real-time collaboration and AI-powered responses.
    """
    
    BASE_URL = "https://slack.com/api"
    
    def __init__(self, config: Optional[SlackConfig] = None):
        self.config = config or SlackConfig(
            bot_token=os.environ.get("SLACK_BOT_TOKEN"),
            webhook_url=os.environ.get("SLACK_WEBHOOK_URL")
        )
    
    def send_message(
        self,
        text: str,
        channel: Optional[str] = None,
        blocks: Optional[list] = None
    ) -> dict:
        """Send a message to Slack channel"""
        
        # Try webhook first (simpler)
        if self.config.webhook_url:
            return self._send_webhook(text, blocks)
        
        # Fall back to API
        if self.config.bot_token:
            return self._send_api(text, channel or self.config.default_channel, blocks)
        
        return {"ok": False, "error": "No Slack credentials configured"}
    
    def _send_webhook(self, text: str, blocks: Optional[list] = None) -> dict:
        """Send via incoming webhook"""
        payload = {"text": text}
        if blocks:
            payload["blocks"] = blocks
        
        try:
            req = urllib.request.Request(
                self.config.webhook_url,
                data=json.dumps(payload).encode(),
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                return {"ok": True, "response": resp.read().decode()}
        except Exception as e:
            return {"ok": False, "error": str(e)}
    
    def _send_api(self, text: str, channel: str, blocks: Optional[list] = None) -> dict:
        """Send via Slack API"""
        url = f"{self.BASE_URL}/chat.postMessage"
        headers = {
            "Authorization": f"Bearer {self.config.bot_token}",
            "Content-Type": "application/json"
        }
        payload = {"channel": channel, "text": text}
        if blocks:
            payload["blocks"] = blocks
        
        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode(),
                headers=headers,
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                return json.loads(resp.read().decode())
        except Exception as e:
            return {"ok": False, "error": str(e)}
    
    def send_gabriel_response(
        self,
        prompt: str,
        response: str,
        agent: str = "GABRIEL",
        channel: Optional[str] = None
    ) -> dict:
        """Send a formatted GABRIEL response to Slack"""
        
        blocks = [
            {
                "type": "header",
                "text": {"type": "plain_text", "text": f"🧠 {agent} Response", "emoji": True}
            },
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"*Query:*\n```{prompt[:500]}```"}
            },
            {"type": "divider"},
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"*Response:*\n{response[:2900]}"}
            },
            {
                "type": "context",
                "elements": [
                    {"type": "mrkdwn", "text": f"⚡ GORUNFREE | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"}
                ]
            }
        ]
        
        return self.send_message(
            text=f"{agent}: {response[:200]}...",
            channel=channel,
            blocks=blocks
        )
    
    def send_status_update(
        self,
        title: str,
        status: str,
        details: dict,
        channel: Optional[str] = None
    ) -> dict:
        """Send a system status update"""
        
        details_text = "\n".join([f"• *{k}:* {v}" for k, v in details.items()])
        
        blocks = [
            {
                "type": "header",
                "text": {"type": "plain_text", "text": f"📊 {title}", "emoji": True}
            },
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"*Status:* {status}"}
            },
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": details_text}
            },
            {
                "type": "context",
                "elements": [
                    {"type": "mrkdwn", "text": f"🚀 MC96DIGIUNIVERSE | {datetime.now().isoformat()}"}
                ]
            }
        ]
        
        return self.send_message(
            text=f"{title}: {status}",
            channel=channel,
            blocks=blocks
        )
    
    def send_alert(
        self,
        alert_type: str,
        message: str,
        severity: str = "info",
        channel: Optional[str] = None
    ) -> dict:
        """Send an alert notification"""
        
        emoji_map = {
            "info": "ℹ️",
            "warning": "⚠️",
            "error": "🚨",
            "success": "✅"
        }
        emoji = emoji_map.get(severity, "ℹ️")
        
        blocks = [
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"{emoji} *{alert_type}*\n{message}"}
            }
        ]
        
        return self.send_message(
            text=f"{emoji} {alert_type}: {message}",
            channel=channel,
            blocks=blocks
        )


# Factory function
def create_slack_bridge(
    bot_token: Optional[str] = None,
    webhook_url: Optional[str] = None
) -> SlackBridge:
    """Create a configured SlackBridge"""
    config = SlackConfig(
        bot_token=bot_token or os.environ.get("SLACK_BOT_TOKEN"),
        webhook_url=webhook_url or os.environ.get("SLACK_WEBHOOK_URL")
    )
    return SlackBridge(config)


__all__ = ['SlackConfig', 'SlackBridge', 'create_slack_bridge']


if __name__ == "__main__":
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║              SLACK BRIDGE v1.0 - MC96DIGIUNIVERSE            ║")
    print("║                     GORUNFREE EDITION                        ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print()
    print("Usage:")
    print("  from noizylab.core.slack_bridge import create_slack_bridge")
    print("  bridge = create_slack_bridge()")
    print("  bridge.send_message('Hello from GABRIEL!')")
