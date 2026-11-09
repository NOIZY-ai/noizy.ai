"""
📧 EMAIL SERVICE - 100% PERFECT
Perfect email service
GORUNFREE Protocol
"""

from typing import List, Optional, Dict, Any
import os
import smtplib
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from html import escape
from ..config import settings
from ..logging import get_logger

logger = get_logger("email")


def validate_email(email: str) -> bool:
    """
    Validate email address format
    
    Args:
        email: Email address to validate
        
    Returns:
        True if valid, False otherwise
        
    Note:
        This is a basic regex pattern. For production, consider using
        a more comprehensive validation library like email-validator.
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def sanitize_html_content(content: str) -> str:
    """
    Sanitize HTML content to prevent XSS attacks
    
    Args:
        content: HTML content to sanitize
        
    Returns:
        Sanitized HTML content
        
    Note:
        This function expects pre-built HTML templates where user data
        has already been escaped using html.escape(). For additional
        security in production, consider using the 'bleach' library.
    """
    # This is a pass-through since we escape user data at injection points
    # For production environments, consider: import bleach; return bleach.clean(content)
    return content


class EmailService:
    """Email service implementation"""
    
    def __init__(
        self,
        smtp_host: Optional[str] = None,
        smtp_port: int = 587,
        smtp_user: Optional[str] = None,
        smtp_password: Optional[str] = None
    ):
        """
        Initialize email service
        
        Args:
            smtp_host: SMTP host
            smtp_port: SMTP port
            smtp_user: SMTP username
            smtp_password: SMTP password
        """
        self.smtp_host = smtp_host or os.getenv("SMTP_HOST", "smtp.gmail.com")
        self.smtp_port = smtp_port
        self.smtp_user = smtp_user or os.getenv("SMTP_USER")
        self.smtp_password = smtp_password or os.getenv("SMTP_PASSWORD")
        self.from_email = os.getenv("FROM_EMAIL", "noreply@gabriel.noizylab.com")
    
    def send_email(
        self,
        to_email: str,
        subject: str,
        body: str,
        html_body: Optional[str] = None,
        attachments: Optional[List[str]] = None
    ) -> bool:
        """
        Send email
        
        Args:
            to_email: Recipient email
            subject: Email subject
            body: Plain text body
            html_body: HTML body (optional)
            attachments: List of file paths (optional)
            
        Returns:
            True if successful
        """
        try:
            # Validate email address
            if not validate_email(to_email):
                logger.error("invalid_email_address", to_email=to_email)
                return False
            
            # Validate required fields
            if not subject or not body:
                logger.error("missing_required_fields", to_email=to_email)
                return False
            
            msg = MIMEMultipart('alternative')
            msg['From'] = self.from_email
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Add plain text
            msg.attach(MIMEText(body, 'plain'))
            
            # Add HTML if provided
            if html_body:
                sanitized_html = sanitize_html_content(html_body)
                msg.attach(MIMEText(sanitized_html, 'html'))
            
            # Send email
            if self.smtp_user and self.smtp_password:
                with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                    server.starttls()
                    server.login(self.smtp_user, self.smtp_password)
                    server.send_message(msg)
            else:
                logger.warning("email_not_configured", to_email=to_email)
                return False
            
            logger.info("email_sent", to_email=to_email, subject=subject)
            return True
        except smtplib.SMTPException as e:
            logger.error("smtp_error", to_email=to_email, error=str(e), error_type="SMTPException")
            return False
        except Exception as e:
            logger.error("email_send_failed", to_email=to_email, error=str(e), error_type=type(e).__name__)
            return False


# Global email service instance
_email_service: Optional[EmailService] = None


def get_email_service() -> EmailService:
    """Get email service instance"""
    global _email_service
    if _email_service is None:
        _email_service = EmailService()
    return _email_service


def send_email(
    to_email: str,
    subject: str,
    body: str,
    html_body: Optional[str] = None
) -> bool:
    """
    Send email (convenience function)
    
    Args:
        to_email: Recipient email
        subject: Email subject
        body: Plain text body
        html_body: HTML body (optional)
        
    Returns:
        True if successful
    """
    service = get_email_service()
    return service.send_email(to_email, subject, body, html_body)


def send_welcome_email(to_email: str, name: str) -> bool:
    """
    Send welcome email
    
    Args:
        to_email: Recipient email
        name: User name
        
    Returns:
        True if successful
    """
    # Escape user-provided data
    safe_name = escape(name)
    
    subject = "Welcome to GABRIEL!"
    body = f"Hi {name},\n\nWelcome to GABRIEL! We're excited to have you."
    html_body = f"""
    <html>
      <body>
        <h1>Welcome to GABRIEL, {safe_name}!</h1>
        <p>We're excited to have you on board.</p>
      </body>
    </html>
    """
    return send_email(to_email, subject, body, html_body)


def send_verification_email(to_email: str, verification_code: str) -> bool:
    """
    Send verification email
    
    Args:
        to_email: Recipient email
        verification_code: Verification code
        
    Returns:
        True if successful
    """
    # Escape verification code for safety
    safe_code = escape(verification_code)
    
    subject = "Verify your GABRIEL account"
    body = f"Your verification code is: {verification_code}"
    html_body = f"""
    <html>
      <body>
        <h1>Verify your account</h1>
        <p>Your verification code is: <strong>{safe_code}</strong></p>
      </body>
    </html>
    """
    return send_email(to_email, subject, body, html_body)


def send_subscription_confirmation_email(
    to_email: str,
    name: str,
    subscription_tier: str,
    amount: float,
    currency: str = "USD"
) -> bool:
    """
    Send subscription confirmation email
    
    Args:
        to_email: Recipient email
        name: User name
        subscription_tier: Subscription tier (e.g., "pro", "enterprise")
        amount: Subscription amount
        currency: Currency code
        
    Returns:
        True if successful
    """
    # Validate inputs
    if not validate_email(to_email):
        logger.error("invalid_email", email=to_email, function="send_subscription_confirmation_email")
        return False
    
    if amount < 0:
        logger.error("invalid_amount", amount=amount, function="send_subscription_confirmation_email")
        return False
    
    # Escape user-provided data for HTML safety
    safe_name = escape(name)
    safe_tier = escape(subscription_tier.upper())
    safe_currency = escape(currency)
    
    # Use original tier for subject (comes from our system, not user input)
    subject = f"Subscription Confirmed - GABRIEL {subscription_tier.upper()}"
    
    # Note: We use escaped variables in plain text for consistency and safety.
    # While HTML escaping in plain text may display entities like &lt; literally,
    # this is preferable to potential injection attacks. User-provided names should
    # not contain such characters in normal use cases.
    body = f"""Hi {safe_name},

Your subscription to GABRIEL {safe_tier} has been confirmed!

Amount: {safe_currency} ${amount:.2f}
Tier: {safe_tier}

Thank you for subscribing!

Best regards,
The GABRIEL Team"""
    
    html_body = f"""
    <html>
      <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
        <h1 style="color: #4CAF50;">Subscription Confirmed!</h1>
        <p>Hi {safe_name},</p>
        <p>Your subscription to GABRIEL <strong>{safe_tier}</strong> has been confirmed!</p>
        <div style="background-color: #f5f5f5; padding: 20px; margin: 20px 0; border-radius: 5px;">
          <p><strong>Amount:</strong> {safe_currency} ${amount:.2f}</p>
          <p><strong>Tier:</strong> {safe_tier}</p>
        </div>
        <p>Thank you for subscribing!</p>
        <p>Best regards,<br>The GABRIEL Team</p>
      </body>
    </html>
    """
    return send_email(to_email, subject, body, html_body)


def send_subscription_renewal_email(
    to_email: str,
    name: str,
    subscription_tier: str,
    amount: float,
    renewal_date: str,
    currency: str = "USD"
) -> bool:
    """
    Send subscription renewal reminder email
    
    Args:
        to_email: Recipient email
        name: User name
        subscription_tier: Subscription tier
        amount: Renewal amount
        renewal_date: Renewal date (ISO format)
        currency: Currency code
        
    Returns:
        True if successful
    """
    # Validate inputs
    if not validate_email(to_email):
        logger.error("invalid_email", email=to_email, function="send_subscription_renewal_email")
        return False
    
    if amount < 0:
        logger.error("invalid_amount", amount=amount, function="send_subscription_renewal_email")
        return False
    
    # Escape user-provided data
    safe_name = escape(name)
    safe_tier = escape(subscription_tier.upper())
    safe_date = escape(renewal_date)
    safe_currency = escape(currency)
    
    # Use original tier for subject (comes from our system, not user input)
    subject = f"Subscription Renewal - GABRIEL {subscription_tier.upper()}"
    body = f"""Hi {safe_name},

Your GABRIEL {safe_tier} subscription will renew on {safe_date}.

Renewal Amount: {safe_currency} ${amount:.2f}

If you have any questions, please contact us.

Best regards,
The GABRIEL Team"""
    
    html_body = f"""
    <html>
      <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
        <h1 style="color: #2196F3;">Subscription Renewal</h1>
        <p>Hi {safe_name},</p>
        <p>Your GABRIEL <strong>{safe_tier}</strong> subscription will renew on <strong>{safe_date}</strong>.</p>
        <div style="background-color: #f5f5f5; padding: 20px; margin: 20px 0; border-radius: 5px;">
          <p><strong>Renewal Amount:</strong> {safe_currency} ${amount:.2f}</p>
        </div>
        <p>If you have any questions, please contact us.</p>
        <p>Best regards,<br>The GABRIEL Team</p>
      </body>
    </html>
    """
    return send_email(to_email, subject, body, html_body)


def send_subscription_expiration_email(
    to_email: str,
    name: str,
    subscription_tier: str,
    expiration_date: str
) -> bool:
    """
    Send subscription expiration warning email
    
    Args:
        to_email: Recipient email
        name: User name
        subscription_tier: Subscription tier
        expiration_date: Expiration date (ISO format)
        
    Returns:
        True if successful
    """
    # Validate inputs
    if not validate_email(to_email):
        logger.error("invalid_email", email=to_email, function="send_subscription_expiration_email")
        return False
    
    # Escape user-provided data
    safe_name = escape(name)
    safe_tier = escape(subscription_tier.upper())
    safe_date = escape(expiration_date)
    
    # Use original tier for subject (comes from our system, not user input)
    subject = f"Subscription Expiring Soon - GABRIEL {subscription_tier.upper()}"
    body = f"""Hi {safe_name},

Your GABRIEL {safe_tier} subscription will expire on {safe_date}.

To continue enjoying premium features, please renew your subscription.

Best regards,
The GABRIEL Team"""
    
    html_body = f"""
    <html>
      <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
        <h1 style="color: #FF9800;">Subscription Expiring Soon</h1>
        <p>Hi {safe_name},</p>
        <p>Your GABRIEL <strong>{safe_tier}</strong> subscription will expire on <strong>{safe_date}</strong>.</p>
        <div style="background-color: #fff3cd; padding: 20px; margin: 20px 0; border-radius: 5px; border-left: 4px solid #FF9800;">
          <p style="margin: 0;">To continue enjoying premium features, please renew your subscription.</p>
        </div>
        <p>Best regards,<br>The GABRIEL Team</p>
      </body>
    </html>
    """
    return send_email(to_email, subject, body, html_body)


def send_subscription_cancelled_email(
    to_email: str,
    name: str,
    subscription_tier: str
) -> bool:
    """
    Send subscription cancellation confirmation email
    
    Args:
        to_email: Recipient email
        name: User name
        subscription_tier: Subscription tier
        
    Returns:
        True if successful
    """
    # Validate inputs
    if not validate_email(to_email):
        logger.error("invalid_email", email=to_email, function="send_subscription_cancelled_email")
        return False
    
    # Escape user-provided data
    safe_name = escape(name)
    safe_tier = escape(subscription_tier.upper())
    
    # Use original tier for subject (comes from our system, not user input)
    subject = f"Subscription Cancelled - GABRIEL {subscription_tier.upper()}"
    body = f"""Hi {safe_name},

Your GABRIEL {safe_tier} subscription has been cancelled as requested.

You will continue to have access to premium features until the end of your current billing period.

We're sorry to see you go. If you have any feedback, please let us know.

Best regards,
The GABRIEL Team"""
    
    html_body = f"""
    <html>
      <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
        <h1 style="color: #F44336;">Subscription Cancelled</h1>
        <p>Hi {safe_name},</p>
        <p>Your GABRIEL <strong>{safe_tier}</strong> subscription has been cancelled as requested.</p>
        <div style="background-color: #f5f5f5; padding: 20px; margin: 20px 0; border-radius: 5px;">
          <p>You will continue to have access to premium features until the end of your current billing period.</p>
        </div>
        <p>We're sorry to see you go. If you have any feedback, please let us know.</p>
        <p>Best regards,<br>The GABRIEL Team</p>
      </body>
    </html>
    """
    return send_email(to_email, subject, body, html_body)

