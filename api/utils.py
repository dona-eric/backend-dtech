from django.core.mail import send_mail
from django.conf import settings

def send_email(subject, message, recipient_list):
    """
    Utility function to send emails.
    """
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            recipient_list,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False