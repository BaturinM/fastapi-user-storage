import smtplib
from email.mime.text import MIMEText
from ..logging import logger

from ..config import settings


def send_email(receiver_email, subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['To'] = receiver_email
    msg['From'] = settings.app_email

    print('Aaaaaa')

    with smtplib.SMTP(settings.smtp_host, port=settings.smtp_port) as smtp_server:
        smtp_server.send_message(msg)
