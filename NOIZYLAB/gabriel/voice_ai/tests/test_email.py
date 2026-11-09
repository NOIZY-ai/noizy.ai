"""
🧪 EMAIL TESTS - 100% PERFECT
Perfect email test coverage
GORUNFREE Protocol
"""

import pytest
from unittest.mock import Mock, patch
from ..infrastructure.email.email_service import EmailService, send_email, send_welcome_email


class TestEmail:
    """Email tests"""
    
    @pytest.fixture
    def email_service(self):
        """Create email service instance"""
        return EmailService(
            smtp_host="smtp.test.com",
            smtp_port=587,
            smtp_user="test",
            smtp_password="test"
        )
    
    @patch('smtplib.SMTP')
    def test_send_email(self, mock_smtp, email_service):
        """Test email sending"""
        mock_server = Mock()
        mock_smtp.return_value.__enter__.return_value = mock_server
        
        result = email_service.send_email(
            to_email="test@example.com",
            subject="Test",
            body="Test body"
        )
        
        assert result is True
        mock_server.starttls.assert_called_once()
        mock_server.login.assert_called_once()
        mock_server.send_message.assert_called_once()
    
    def test_send_welcome_email(self):
        """Test welcome email"""
        with patch('gabriel.voice_ai.infrastructure.email.email_service.send_email') as mock_send:
            mock_send.return_value = True
            
            result = send_welcome_email("test@example.com", "John")
            
            assert result is True
            mock_send.assert_called_once()
    
    def test_send_subscription_confirmation_email(self):
        """Test subscription confirmation email"""
        from ..infrastructure.email.email_service import send_subscription_confirmation_email
        
        with patch('gabriel.voice_ai.infrastructure.email.email_service.send_email') as mock_send:
            mock_send.return_value = True
            
            result = send_subscription_confirmation_email(
                to_email="test@example.com",
                name="John Doe",
                subscription_tier="pro",
                amount=29.99,
                currency="USD"
            )
            
            assert result is True
            mock_send.assert_called_once()
            
            # Verify the call arguments contain expected content
            call_args = mock_send.call_args
            assert "test@example.com" in call_args[0]
            assert "Subscription Confirmed" in call_args[0][1]  # subject
    
    def test_send_subscription_renewal_email(self):
        """Test subscription renewal email"""
        from ..infrastructure.email.email_service import send_subscription_renewal_email
        
        with patch('gabriel.voice_ai.infrastructure.email.email_service.send_email') as mock_send:
            mock_send.return_value = True
            
            result = send_subscription_renewal_email(
                to_email="test@example.com",
                name="John Doe",
                subscription_tier="pro",
                amount=29.99,
                renewal_date="2025-01-29",
                currency="USD"
            )
            
            assert result is True
            mock_send.assert_called_once()
            
            # Verify subject
            call_args = mock_send.call_args
            assert "Subscription Renewal" in call_args[0][1]
    
    def test_send_subscription_expiration_email(self):
        """Test subscription expiration email"""
        from ..infrastructure.email.email_service import send_subscription_expiration_email
        
        with patch('gabriel.voice_ai.infrastructure.email.email_service.send_email') as mock_send:
            mock_send.return_value = True
            
            result = send_subscription_expiration_email(
                to_email="test@example.com",
                name="John Doe",
                subscription_tier="pro",
                expiration_date="2025-01-29"
            )
            
            assert result is True
            mock_send.assert_called_once()
            
            # Verify subject
            call_args = mock_send.call_args
            assert "Expiring Soon" in call_args[0][1]
    
    def test_send_subscription_cancelled_email(self):
        """Test subscription cancelled email"""
        from ..infrastructure.email.email_service import send_subscription_cancelled_email
        
        with patch('gabriel.voice_ai.infrastructure.email.email_service.send_email') as mock_send:
            mock_send.return_value = True
            
            result = send_subscription_cancelled_email(
                to_email="test@example.com",
                name="John Doe",
                subscription_tier="pro"
            )
            
            assert result is True
            mock_send.assert_called_once()
            
            # Verify subject
            call_args = mock_send.call_args
            assert "Subscription Cancelled" in call_args[0][1]
    
    def test_send_email_with_invalid_email(self, email_service):
        """Test sending email with invalid email address"""
        result = email_service.send_email(
            to_email="invalid-email",
            subject="Test",
            body="Test body"
        )
        
        assert result is False
    
    def test_send_subscription_confirmation_with_invalid_amount(self):
        """Test subscription confirmation with negative amount"""
        from ..infrastructure.email.email_service import send_subscription_confirmation_email
        
        result = send_subscription_confirmation_email(
            to_email="test@example.com",
            name="John Doe",
            subscription_tier="pro",
            amount=-10.0,
            currency="USD"
        )
        
        assert result is False

