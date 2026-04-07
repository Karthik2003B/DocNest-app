from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv
import os

load_dotenv()

def send_email(to_email, subject, html_content, plain_text_content=None):

    message = Mail(
        from_email="DocNest <alerts@docnest.me>",  # 🔥 MUST BE VERIFIED
        to_emails=to_email,
        subject=subject,
        html_content=html_content,
        plain_text_content=plain_text_content or html_content
    )

    sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
    sg.send(message)
    
