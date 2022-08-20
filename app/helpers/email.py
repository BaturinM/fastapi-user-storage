import smtplib
from email.mime.text import MIMEText

from ..config import settings
from ..logging import logger


def send_email(receiver_email, subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['To'] = receiver_email
    msg['From'] = settings.app_email
    with smtplib.SMTP(settings.smtp_host, port=settings.smtp_port) as smtp_server:
        smtp_server.send_message(msg)

    logger.info(f'{subject} email sent to {receiver_email}')
