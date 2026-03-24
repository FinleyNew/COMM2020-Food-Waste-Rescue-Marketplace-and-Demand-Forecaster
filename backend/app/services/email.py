from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from app.core.config import settings

# Sends an email to the specified email
def send_email(to_email: str, subject: str, body: str):
    message = Mail(
        from_email=settings.SENDGRID_FROM_EMAIL,
        to_emails=to_email,
        subject=subject,
        html_content=body
    )
    try:
        client = SendGridAPIClient(settings.SENDGRID_API_KEY)
        client.send(message)
    except Exception as e:
        print(f"Email failed: {e}")