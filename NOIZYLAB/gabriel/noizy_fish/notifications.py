"""
NOIZY Fish — Webhook & Notification System
============================================

Real-time notifications for:
- Consent rule changes
- Licensing inquiries (new, approved, denied)
- Work registrations
- Verification status changes
- Royalty thresholds met

Supports:
- HTTP webhooks (POST to external URLs)
- Email notifications (via email service)
- Internal event bus (for MCP tools)
"""

import asyncio
import json
import os
from dataclasses import dataclass, field
from datetime import datetime
from typing import Callable, Optional
from uuid import uuid4
import hashlib
import hmac

# Try aiohttp for async HTTP
try:
    import aiohttp
    AIOHTTP_AVAILABLE = True
except ImportError:
    AIOHTTP_AVAILABLE = False

# Try requests for sync HTTP
try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False


# ═══════════════════════════════════════════════════════════════════════════
# Event Types
# ═══════════════════════════════════════════════════════════════════════════

class EventType:
    """All NOIZY Fish event types."""
    # Creator events
    CREATOR_REGISTERED = "creator.registered"
    CREATOR_VERIFIED = "creator.verified"
    CREATOR_UPDATED = "creator.updated"

    # Consent events
    CONSENT_RULE_CREATED = "consent.rule.created"
    CONSENT_RULE_UPDATED = "consent.rule.updated"
    CONSENT_RULE_DELETED = "consent.rule.deleted"

    # Work events
    WORK_REGISTERED = "work.registered"
    WORK_UPDATED = "work.updated"
    WORK_DELETED = "work.deleted"

    # Inquiry events
    INQUIRY_RECEIVED = "inquiry.received"
    INQUIRY_APPROVED = "inquiry.approved"
    INQUIRY_DENIED = "inquiry.denied"
    INQUIRY_PENDING = "inquiry.pending"

    # License events
    LICENSE_CREATED = "license.created"
    LICENSE_ACTIVATED = "license.activated"
    LICENSE_EXPIRED = "license.expired"
    LICENSE_TERMINATED = "license.terminated"

    # Royalty events
    ROYALTY_EARNED = "royalty.earned"
    ROYALTY_THRESHOLD_MET = "royalty.threshold.met"
    ROYALTY_PAYOUT_INITIATED = "royalty.payout.initiated"
    ROYALTY_PAYOUT_COMPLETED = "royalty.payout.completed"


@dataclass
class Event:
    """A NOIZY Fish event."""
    event_id: str = field(default_factory=lambda: str(uuid4()))
    event_type: str = ""
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    data: dict = field(default_factory=dict)

    # Entity references
    creator_id: Optional[str] = None
    work_id: Optional[str] = None
    inquiry_id: Optional[str] = None
    license_id: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "event_id": self.event_id,
            "event_type": self.event_type,
            "timestamp": self.timestamp,
            "data": self.data,
            "creator_id": self.creator_id,
            "work_id": self.work_id,
            "inquiry_id": self.inquiry_id,
            "license_id": self.license_id
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict())


# ═══════════════════════════════════════════════════════════════════════════
# Webhook Configuration
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class WebhookConfig:
    """Configuration for a webhook endpoint."""
    webhook_id: str = field(default_factory=lambda: str(uuid4()))
    url: str = ""
    secret: str = field(default_factory=lambda: uuid4().hex)

    # Filtering
    event_types: list[str] = field(default_factory=list)  # Empty = all
    creator_ids: list[str] = field(default_factory=list)  # Empty = all

    # Settings
    enabled: bool = True
    retry_count: int = 3
    timeout_seconds: int = 10

    # Metadata
    name: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    def matches_event(self, event: Event) -> bool:
        """Check if this webhook should receive this event."""
        if not self.enabled:
            return False

        # Check event type filter
        if self.event_types and event.event_type not in self.event_types:
            return False

        # Check creator filter
        if self.creator_ids and event.creator_id not in self.creator_ids:
            return False

        return True

    def sign_payload(self, payload: str) -> str:
        """Sign payload with HMAC-SHA256."""
        signature = hmac.new(
            self.secret.encode(),
            payload.encode(),
            hashlib.sha256
        ).hexdigest()
        return f"sha256={signature}"


# ═══════════════════════════════════════════════════════════════════════════
# Email Notification Config
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class EmailNotificationConfig:
    """Configuration for email notifications."""
    config_id: str = field(default_factory=lambda: str(uuid4()))
    creator_id: str = ""
    email: str = ""

    # What to notify about
    notify_inquiries: bool = True
    notify_approvals: bool = True
    notify_denials: bool = True
    notify_royalties: bool = True
    notify_verification: bool = True

    # Thresholds
    royalty_threshold: float = 100.0  # Notify when earned this much

    enabled: bool = True


# ═══════════════════════════════════════════════════════════════════════════
# Notification Service
# ═══════════════════════════════════════════════════════════════════════════

class NotificationService:
    """
    Central notification service for NOIZY Fish.
    Handles webhooks, emails, and internal events.
    """

    def __init__(self, db=None):
        self.webhooks: dict[str, WebhookConfig] = {}
        self.email_configs: dict[str, EmailNotificationConfig] = {}
        self.event_handlers: dict[str, list[Callable]] = {}
        self.event_log: list[Event] = []
        self.db = db

    # ─────────────────────────────────────────────────────────────────────────
    # Webhook Management
    # ─────────────────────────────────────────────────────────────────────────

    def register_webhook(self, config: WebhookConfig) -> str:
        """Register a webhook endpoint."""
        self.webhooks[config.webhook_id] = config
        return config.webhook_id

    def remove_webhook(self, webhook_id: str) -> bool:
        """Remove a webhook."""
        if webhook_id in self.webhooks:
            del self.webhooks[webhook_id]
            return True
        return False

    def list_webhooks(self) -> list[dict]:
        """List all webhooks (without secrets)."""
        return [
            {
                "webhook_id": w.webhook_id,
                "url": w.url,
                "event_types": w.event_types,
                "enabled": w.enabled,
                "name": w.name
            }
            for w in self.webhooks.values()
        ]

    # ─────────────────────────────────────────────────────────────────────────
    # Event Handlers
    # ─────────────────────────────────────────────────────────────────────────

    def on(self, event_type: str, handler: Callable):
        """Register an internal event handler."""
        if event_type not in self.event_handlers:
            self.event_handlers[event_type] = []
        self.event_handlers[event_type].append(handler)

    def off(self, event_type: str, handler: Callable):
        """Remove an event handler."""
        if event_type in self.event_handlers:
            self.event_handlers[event_type].remove(handler)

    # ─────────────────────────────────────────────────────────────────────────
    # Event Emission
    # ─────────────────────────────────────────────────────────────────────────

    async def emit(self, event: Event):
        """
        Emit an event to all subscribers.
        - Calls internal handlers
        - Sends to webhooks
        - Queues email notifications
        """
        # Log event
        self.event_log.append(event)
        if len(self.event_log) > 1000:
            self.event_log = self.event_log[-500:]

        # Call internal handlers
        await self._call_handlers(event)

        # Send webhooks
        await self._send_webhooks(event)

        # Queue emails
        await self._queue_emails(event)

    def emit_sync(self, event: Event):
        """Synchronous emit for non-async contexts."""
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                asyncio.create_task(self.emit(event))
            else:
                loop.run_until_complete(self.emit(event))
        except RuntimeError:
            asyncio.run(self.emit(event))

    async def _call_handlers(self, event: Event):
        """Call internal event handlers."""
        handlers = self.event_handlers.get(event.event_type, [])
        handlers += self.event_handlers.get("*", [])  # Wildcard handlers

        for handler in handlers:
            try:
                result = handler(event)
                if asyncio.iscoroutine(result):
                    await result
            except Exception as e:
                print(f"Handler error: {e}")

    async def _send_webhooks(self, event: Event):
        """Send event to matching webhooks."""
        matching = [w for w in self.webhooks.values() if w.matches_event(event)]

        for webhook in matching:
            await self._send_webhook(webhook, event)

    async def _send_webhook(self, webhook: WebhookConfig, event: Event):
        """Send event to a single webhook."""
        payload = event.to_json()
        signature = webhook.sign_payload(payload)

        headers = {
            "Content-Type": "application/json",
            "X-NOIZY-Signature": signature,
            "X-NOIZY-Event": event.event_type,
            "X-NOIZY-Delivery": event.event_id
        }

        for attempt in range(webhook.retry_count):
            try:
                if AIOHTTP_AVAILABLE:
                    async with aiohttp.ClientSession() as session:
                        async with session.post(
                            webhook.url,
                            data=payload,
                            headers=headers,
                            timeout=aiohttp.ClientTimeout(total=webhook.timeout_seconds)
                        ) as response:
                            if response.status < 300:
                                return True
                elif REQUESTS_AVAILABLE:
                    response = requests.post(
                        webhook.url,
                        data=payload,
                        headers=headers,
                        timeout=webhook.timeout_seconds
                    )
                    if response.status_code < 300:
                        return True
                else:
                    print(f"No HTTP library available for webhook: {webhook.url}")
                    return False
            except Exception as e:
                if attempt < webhook.retry_count - 1:
                    await asyncio.sleep(2 ** attempt)  # Exponential backoff
                else:
                    print(f"Webhook failed after {webhook.retry_count} attempts: {e}")

        return False

    async def _queue_emails(self, event: Event):
        """Queue email notifications for event."""
        # Find matching email configs
        for config in self.email_configs.values():
            if not config.enabled:
                continue

            if config.creator_id and event.creator_id != config.creator_id:
                continue

            # Check notification preferences
            should_notify = False
            subject = ""
            body = ""

            if event.event_type == EventType.INQUIRY_RECEIVED and config.notify_inquiries:
                should_notify = True
                subject = f"New Licensing Inquiry - {event.data.get('use_category', 'Unknown')}"
                body = self._format_inquiry_email(event)

            elif event.event_type == EventType.INQUIRY_APPROVED and config.notify_approvals:
                should_notify = True
                subject = f"Inquiry Approved - {event.data.get('use_category', 'Unknown')}"
                body = self._format_approval_email(event)

            elif event.event_type == EventType.INQUIRY_DENIED and config.notify_denials:
                should_notify = True
                subject = f"Inquiry Denied - {event.data.get('use_category', 'Unknown')}"
                body = self._format_denial_email(event)

            elif event.event_type == EventType.ROYALTY_THRESHOLD_MET and config.notify_royalties:
                should_notify = True
                subject = f"Royalty Milestone - ${event.data.get('amount', 0):,.2f}"
                body = self._format_royalty_email(event)

            if should_notify:
                # Queue for sending
                print(f"📧 Email queued: {config.email} - {subject}")

    def _format_inquiry_email(self, event: Event) -> str:
        """Format inquiry notification email."""
        return f"""
New Licensing Inquiry

Requestor: {event.data.get('requestor_name', 'Unknown')}
Use Type: {event.data.get('use_category', 'Unknown')}
Offered Amount: ${event.data.get('offered_amount', 0):,.2f}
Territory: {event.data.get('territory', 'WW')}
Context: {event.data.get('context', 'Not provided')}

This inquiry is pending your review.

---
NOIZY Fish - Creator Consent Registry
"""

    def _format_approval_email(self, event: Event) -> str:
        """Format approval notification email."""
        return f"""
Licensing Inquiry Approved

Your consent rules automatically approved a licensing inquiry.

Requestor: {event.data.get('requestor_name', 'Unknown')}
Use Type: {event.data.get('use_category', 'Unknown')}
Amount: ${event.data.get('offered_amount', 0):,.2f}
Reason: {event.data.get('reason', 'Matched consent rules')}

---
NOIZY Fish - Creator Consent Registry
"""

    def _format_denial_email(self, event: Event) -> str:
        """Format denial notification email."""
        return f"""
Licensing Inquiry Denied

Your consent rules automatically denied a licensing inquiry.

Requestor: {event.data.get('requestor_name', 'Unknown')}
Use Type: {event.data.get('use_category', 'Unknown')}
Offered Amount: ${event.data.get('offered_amount', 0):,.2f}
Reason: {event.data.get('reason', 'Consent denied')}

---
NOIZY Fish - Creator Consent Registry
"""

    def _format_royalty_email(self, event: Event) -> str:
        """Format royalty notification email."""
        return f"""
Royalty Milestone Reached!

Congratulations! You've reached a royalty milestone.

Total Earned: ${event.data.get('amount', 0):,.2f}
Period: {event.data.get('period', 'This month')}
Top Work: {event.data.get('top_work', 'Unknown')}

---
NOIZY Fish - Creator Consent Registry
"""


# ═══════════════════════════════════════════════════════════════════════════
# Convenience Functions
# ═══════════════════════════════════════════════════════════════════════════

def create_inquiry_event(
    creator_id: str,
    inquiry_id: str,
    requestor_name: str,
    use_category: str,
    decision: str,
    offered_amount: float = 0,
    reasons: list[str] = None
) -> Event:
    """Create an inquiry event."""
    if decision in ["allowed", "allowed_terms"]:
        event_type = EventType.INQUIRY_APPROVED
    elif decision == "denied":
        event_type = EventType.INQUIRY_DENIED
    else:
        event_type = EventType.INQUIRY_PENDING

    return Event(
        event_type=event_type,
        creator_id=creator_id,
        inquiry_id=inquiry_id,
        data={
            "requestor_name": requestor_name,
            "use_category": use_category,
            "decision": decision,
            "offered_amount": offered_amount,
            "reasons": reasons or []
        }
    )


def create_consent_event(
    creator_id: str,
    use_category: str,
    old_decision: Optional[str],
    new_decision: str,
    created: bool = False
) -> Event:
    """Create a consent change event."""
    if created:
        event_type = EventType.CONSENT_RULE_CREATED
    else:
        event_type = EventType.CONSENT_RULE_UPDATED

    return Event(
        event_type=event_type,
        creator_id=creator_id,
        data={
            "use_category": use_category,
            "old_decision": old_decision,
            "new_decision": new_decision
        }
    )


def create_work_event(
    creator_id: str,
    work_id: str,
    title: str,
    work_type: str,
    isrc: Optional[str] = None
) -> Event:
    """Create a work registration event."""
    return Event(
        event_type=EventType.WORK_REGISTERED,
        creator_id=creator_id,
        work_id=work_id,
        data={
            "title": title,
            "work_type": work_type,
            "isrc": isrc
        }
    )


# ═══════════════════════════════════════════════════════════════════════════
# Global Instance
# ═══════════════════════════════════════════════════════════════════════════

# Singleton notification service
_notification_service: Optional[NotificationService] = None


def get_notification_service() -> NotificationService:
    """Get the global notification service."""
    global _notification_service
    if _notification_service is None:
        _notification_service = NotificationService()
    return _notification_service


async def emit_event(event: Event):
    """Emit an event through the global service."""
    service = get_notification_service()
    await service.emit(event)


def emit_event_sync(event: Event):
    """Emit an event synchronously."""
    service = get_notification_service()
    service.emit_sync(event)
