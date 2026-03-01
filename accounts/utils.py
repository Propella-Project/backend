"""Utility functions for the accounts app."""
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string


def send_verification_code(user, verification_code):
    """
    Send an email verification code to a user.
    
    Args:
        user: The User instance to send the code to
        verification_code: The 6-digit verification code or EmailVerification instance
    
    Returns:
        bool: True if email was sent successfully, False otherwise
    """
    from .models import EmailVerification
    
    # Handle both string code and EmailVerification instances
    if isinstance(verification_code, EmailVerification):
        code = verification_code.code
    else:
        code = verification_code
    
    subject = "Propella Email Verification Code"
    
    # Create HTML email body
    html_message = f"""
    <html>
        <body style="font-family:Arial,sans-serif;margin:20px">
            <h2>Email Verification</h2>
            <p>Hello {user.username},</p>
            <p>Thank you for registering with Propella! To complete your registration, please use the following verification code:</p>
            <h1 style="color:#0b76c2;letter-spacing:2px;font-size:2em;margin:30px 0">{code}</h1>
            <p>This code will expire in 15 minutes.</p>
            <p>If you did not create this account, please ignore this email.</p>
            <hr>
            <p style="color:#666;font-size:0.9em">Propella API • {settings.ALLOWED_HOSTS[0] if settings.ALLOWED_HOSTS else 'api.propella.com'}</p>
        </body>
    </html>
    """
    
    plain_message = f"""
Email Verification

Hello {user.username},

Thank you for registering with Propella! To complete your registration, please use the following verification code:

{code}

This code will expire in 15 minutes.

If you did not create this account, please ignore this email.

Propella API
    """
    
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Failed to send verification email to {user.email}: {str(e)}")
        return False
