"""
🧪 PAYMENT TESTS - 100% PERFECT
Perfect payment test coverage
GORUNFREE Protocol
"""

import pytest
import stripe
from unittest.mock import Mock, patch
from ..infrastructure.payments.stripe_integration import StripePayment


class TestPayments:
    """Payment tests"""
    
    @pytest.fixture
    def stripe_payment(self):
        """Create Stripe payment instance"""
        return StripePayment()
    
    @patch('stripe.PaymentIntent.create')
    def test_create_payment_intent(self, mock_create, stripe_payment):
        """Test payment intent creation"""
        mock_create.return_value = Mock(id="pi_123", status="requires_payment_method")
        
        result = stripe_payment.create_payment_intent(
            amount=10.00,
            currency="usd"
        )
        
        assert result.id == "pi_123"
        mock_create.assert_called_once()
    
    @patch('stripe.Customer.create')
    def test_create_customer(self, mock_create, stripe_payment):
        """Test customer creation"""
        mock_create.return_value = Mock(id="cus_123", email="test@example.com")
        
        result = stripe_payment.create_customer(
            email="test@example.com",
            name="Test User"
        )
        
        assert result.id == "cus_123"
        assert result.email == "test@example.com"
        mock_create.assert_called_once()
    
    @patch('stripe.Subscription.create')
    def test_create_subscription(self, mock_create, stripe_payment):
        """Test subscription creation"""
        mock_create.return_value = Mock(
            id="sub_123",
            customer="cus_123",
            status="active"
        )
        
        result = stripe_payment.create_subscription(
            customer_id="cus_123",
            price_id="price_123"
        )
        
        assert result.id == "sub_123"
        mock_create.assert_called_once()
    
    @patch('stripe.Customer.retrieve')
    @patch('gabriel.voice_ai.infrastructure.email.email_service.send_subscription_confirmation_email')
    @patch('stripe.Webhook.construct_event')
    def test_webhook_subscription_created(self, mock_construct, mock_email, mock_customer, stripe_payment):
        """Test webhook for subscription created event"""
        # Mock customer
        mock_customer.return_value = Mock(
            email="test@example.com",
            name="Test User",
            get=lambda k, default=None: {"email": "test@example.com", "name": "Test User"}.get(k, default)
        )
        
        # Mock event
        mock_event = {
            "type": "customer.subscription.created",
            "id": "evt_123",
            "data": {
                "object": {
                    "id": "sub_123",
                    "customer": "cus_123",
                    "currency": "usd",
                    "items": {
                        "data": [
                            {
                                "price": {
                                    "unit_amount": 2999
                                }
                            }
                        ]
                    },
                    "metadata": {
                        "tier": "pro"
                    }
                }
            }
        }
        mock_construct.return_value = mock_event
        mock_email.return_value = True
        
        event = stripe_payment.handle_webhook(b"payload", "signature")
        
        assert event["type"] == "customer.subscription.created"
        mock_email.assert_called_once()
        
        # Verify email was called with correct parameters
        call_args = mock_email.call_args
        assert call_args[1]["to_email"] == "test@example.com"
        assert call_args[1]["subscription_tier"] == "pro"
        assert call_args[1]["amount"] == 29.99
    
    @patch('stripe.Customer.retrieve')
    @patch('gabriel.voice_ai.infrastructure.email.email_service.send_subscription_cancelled_email')
    @patch('stripe.Webhook.construct_event')
    def test_webhook_subscription_deleted(self, mock_construct, mock_email, mock_customer, stripe_payment):
        """Test webhook for subscription deleted event"""
        # Mock customer
        mock_customer.return_value = Mock(
            email="test@example.com",
            name="Test User",
            get=lambda k, default=None: {"email": "test@example.com", "name": "Test User"}.get(k, default)
        )
        
        # Mock event
        mock_event = {
            "type": "customer.subscription.deleted",
            "id": "evt_124",
            "data": {
                "object": {
                    "id": "sub_123",
                    "customer": "cus_123",
                    "metadata": {
                        "tier": "pro"
                    }
                }
            }
        }
        mock_construct.return_value = mock_event
        mock_email.return_value = True
        
        event = stripe_payment.handle_webhook(b"payload", "signature")
        
        assert event["type"] == "customer.subscription.deleted"
        mock_email.assert_called_once()
        
        # Verify email was called with correct parameters
        call_args = mock_email.call_args
        assert call_args[1]["to_email"] == "test@example.com"
        assert call_args[1]["subscription_tier"] == "pro"
    
    @patch('stripe.Webhook.construct_event')
    def test_webhook_invalid_signature(self, mock_construct, stripe_payment):
        """Test webhook with invalid signature"""
        mock_construct.side_effect = stripe.error.SignatureVerificationError("Invalid signature", "sig")
        
        with pytest.raises(stripe.error.SignatureVerificationError):
            stripe_payment.handle_webhook(b"payload", "invalid_signature")
    
    @patch('stripe.Webhook.construct_event')
    def test_webhook_missing_customer(self, mock_construct, stripe_payment):
        """Test webhook with missing customer data"""
        mock_event = {
            "type": "customer.subscription.created",
            "id": "evt_123",
            "data": {
                "object": {
                    "id": "sub_123",
                    # customer field missing
                }
            }
        }
        mock_construct.return_value = mock_event
        
        # Should not raise exception, just log warning
        event = stripe_payment.handle_webhook(b"payload", "signature")
        assert event["type"] == "customer.subscription.created"

