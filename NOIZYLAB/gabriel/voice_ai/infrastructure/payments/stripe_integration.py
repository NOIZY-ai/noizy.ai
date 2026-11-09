"""
💳 STRIPE PAYMENT INTEGRATION - 100% PERFECT
Perfect Stripe integration
GORUNFREE Protocol
"""

import stripe
from typing import Optional, Dict, Any
from datetime import datetime
from ..config import settings
from ..logging import get_logger

logger = get_logger("stripe")

# Initialize Stripe
if settings.STRIPE_SECRET_KEY:
    stripe.api_key = settings.STRIPE_SECRET_KEY


class StripePayment:
    """Stripe payment integration"""
    
    def __init__(self):
        """Initialize Stripe"""
        if not settings.STRIPE_SECRET_KEY:
            logger.warning("stripe_not_configured")
        self.stripe = stripe
    
    def create_payment_intent(
        self,
        amount: float,
        currency: str = "usd",
        customer_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create payment intent
        
        Args:
            amount: Amount in cents
            currency: Currency code
            customer_id: Stripe customer ID
            metadata: Additional metadata
            
        Returns:
            Payment intent object
        """
        try:
            intent_data = {
                "amount": int(amount * 100),  # Convert to cents
                "currency": currency,
                "metadata": metadata or {}
            }
            
            if customer_id:
                intent_data["customer"] = customer_id
            
            intent = self.stripe.PaymentIntent.create(**intent_data)
            
            logger.info("payment_intent_created", intent_id=intent.id, amount=amount)
            return intent
        except Exception as e:
            logger.error("payment_intent_failed", error=str(e))
            raise
    
    def confirm_payment(self, payment_intent_id: str) -> Dict[str, Any]:
        """
        Confirm payment intent
        
        Args:
            payment_intent_id: Payment intent ID
            
        Returns:
            Confirmed payment intent
        """
        try:
            intent = self.stripe.PaymentIntent.retrieve(payment_intent_id)
            if intent.status == "requires_confirmation":
                intent = self.stripe.PaymentIntent.confirm(payment_intent_id)
            
            logger.info("payment_confirmed", intent_id=payment_intent_id, status=intent.status)
            return intent
        except Exception as e:
            logger.error("payment_confirmation_failed", error=str(e))
            raise
    
    def create_customer(
        self,
        email: str,
        name: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create Stripe customer
        
        Args:
            email: Customer email
            name: Customer name
            metadata: Additional metadata
            
        Returns:
            Customer object
        """
        try:
            customer_data = {
                "email": email,
                "metadata": metadata or {}
            }
            
            if name:
                customer_data["name"] = name
            
            customer = self.stripe.Customer.create(**customer_data)
            
            logger.info("customer_created", customer_id=customer.id, email=email)
            return customer
        except Exception as e:
            logger.error("customer_creation_failed", error=str(e))
            raise
    
    def create_subscription(
        self,
        customer_id: str,
        price_id: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create subscription
        
        Args:
            customer_id: Stripe customer ID
            price_id: Stripe price ID
            metadata: Additional metadata
            
        Returns:
            Subscription object
        """
        try:
            subscription_data = {
                "customer": customer_id,
                "items": [{"price": price_id}],
                "metadata": metadata or {}
            }
            
            subscription = self.stripe.Subscription.create(**subscription_data)
            
            logger.info("subscription_created", subscription_id=subscription.id)
            return subscription
        except Exception as e:
            logger.error("subscription_creation_failed", error=str(e))
            raise
    
    def handle_webhook(self, payload: bytes, signature: str) -> Dict[str, Any]:
        """
        Handle Stripe webhook
        
        Args:
            payload: Webhook payload
            signature: Webhook signature
            
        Returns:
            Event object
        """
        try:
            event = self.stripe.Webhook.construct_event(
                payload, signature, settings.STRIPE_WEBHOOK_SECRET
            )
            
            logger.info("webhook_received", event_type=event["type"], event_id=event["id"])
            
            # Process subscription events
            self._process_subscription_event(event)
            
            return event
        except ValueError as e:
            logger.error("webhook_invalid_payload", error=str(e))
            raise
        except stripe.error.SignatureVerificationError as e:
            logger.error("webhook_invalid_signature", error=str(e))
            raise
    
    def _process_subscription_event(self, event: Dict[str, Any]) -> None:
        """
        Process subscription-related webhook events
        
        Args:
            event: Stripe webhook event
        """
        from ..email.email_service import (
            send_subscription_confirmation_email,
            send_subscription_renewal_email,
            send_subscription_cancelled_email
        )
        
        event_type = event.get("type")
        if not event_type:
            logger.warning("event_type_missing")
            return
        
        data = event.get("data", {}).get("object", {})
        if not data:
            logger.warning("event_data_missing", event_type=event_type)
            return
        
        # Get customer email from Stripe
        customer_id = data.get("customer")
        if not customer_id:
            logger.warning("customer_id_missing", event_type=event_type)
            return
        
        try:
            customer = self.stripe.Customer.retrieve(customer_id)
            # Stripe objects support both dot notation and .get() method
            customer_email = getattr(customer, 'email', None) or customer.get('email')
            customer_name = getattr(customer, 'name', None) or customer.get('name', 'Valued Customer')
            
            if not customer_email:
                logger.warning("customer_email_not_found", customer_id=customer_id)
                return
            
            # Handle different subscription events
            if event_type == "customer.subscription.created":
                self._handle_subscription_created(data, customer_email, customer_name)
            
            elif event_type == "customer.subscription.updated":
                self._handle_subscription_updated(data, customer_email, customer_name)
            
            elif event_type == "customer.subscription.deleted":
                self._handle_subscription_deleted(data, customer_email, customer_name)
        
        except stripe.error.StripeError as e:
            logger.error("stripe_api_error", 
                        event_type=event_type,
                        error=str(e),
                        error_type="StripeError")
        except Exception as e:
            logger.error("subscription_event_processing_failed", 
                        event_type=event_type,
                        error=str(e),
                        error_type=type(e).__name__)
    
    def _handle_subscription_created(
        self,
        data: Dict[str, Any],
        customer_email: str,
        customer_name: str
    ) -> None:
        """Handle subscription created event"""
        from ..email.email_service import send_subscription_confirmation_email
        
        try:
            # Safely extract amount
            items_data = data.get("items", {}).get("data", [])
            if not items_data:
                logger.warning("subscription_items_missing", subscription_id=data.get("id"))
                return
            
            price_data = items_data[0].get("price", {})
            amount = price_data.get("unit_amount", 0) / 100
            currency = data.get("currency", "USD").upper()
            tier = data.get("metadata", {}).get("tier", "pro")
            
            send_subscription_confirmation_email(
                to_email=customer_email,
                name=customer_name,
                subscription_tier=tier,
                amount=amount,
                currency=currency
            )
            logger.info("subscription_confirmation_email_sent", 
                       customer_email=customer_email, 
                       subscription_id=data.get("id"))
        except Exception as e:
            logger.error("subscription_created_email_failed",
                        error=str(e),
                        subscription_id=data.get("id"))
    
    def _handle_subscription_updated(
        self,
        data: Dict[str, Any],
        customer_email: str,
        customer_name: str
    ) -> None:
        """Handle subscription updated event"""
        from ..email.email_service import send_subscription_renewal_email
        
        try:
            # Only send renewal email if subscription is active
            if data.get("status") != "active":
                return
            
            # Safely extract amount
            items_data = data.get("items", {}).get("data", [])
            if not items_data:
                logger.warning("subscription_items_missing", subscription_id=data.get("id"))
                return
            
            price_data = items_data[0].get("price", {})
            amount = price_data.get("unit_amount", 0) / 100
            currency = data.get("currency", "USD").upper()
            tier = data.get("metadata", {}).get("tier", "pro")
            
            # Get next billing date
            next_billing = data.get("current_period_end")
            if next_billing:
                renewal_date = datetime.fromtimestamp(next_billing).strftime("%Y-%m-%d")
                
                send_subscription_renewal_email(
                    to_email=customer_email,
                    name=customer_name,
                    subscription_tier=tier,
                    amount=amount,
                    renewal_date=renewal_date,
                    currency=currency
                )
                logger.info("subscription_renewal_email_sent",
                           customer_email=customer_email,
                           subscription_id=data.get("id"))
        except Exception as e:
            logger.error("subscription_updated_email_failed",
                        error=str(e),
                        subscription_id=data.get("id"))
    
    def _handle_subscription_deleted(
        self,
        data: Dict[str, Any],
        customer_email: str,
        customer_name: str
    ) -> None:
        """Handle subscription deleted event"""
        from ..email.email_service import send_subscription_cancelled_email
        
        try:
            tier = data.get("metadata", {}).get("tier", "pro")
            
            send_subscription_cancelled_email(
                to_email=customer_email,
                name=customer_name,
                subscription_tier=tier
            )
            logger.info("subscription_cancelled_email_sent",
                       customer_email=customer_email,
                       subscription_id=data.get("id"))
        except Exception as e:
            logger.error("subscription_deleted_email_failed",
                        error=str(e),
                        subscription_id=data.get("id"))

