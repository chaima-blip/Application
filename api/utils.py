from django.core.mail import send_mail
import logging

logger = logging.getLogger(__name__)

def send_welcome_email(email, name):
    subject = 'Welcome to Our Service!'
    message = f'Hi {name},\n\nThank you for signing up with us!'
    from_email = 'your-email@example.com'  # Replace with your email
    recipient_list = [email]

    # Send email
    send_mail(subject, message, from_email, recipient_list)

    # Log for verification
    logger.info(f"Sent welcome email to {email} for user {name}")