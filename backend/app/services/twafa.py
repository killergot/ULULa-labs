import random
import smtplib
import uuid
from email.mime.text import MIMEText
from app.config.config import load_config

def generate_2fa_code() -> str:
    return str(random.randint(100000, 999999))

def generate_session_token() -> str:
    return str(uuid.uuid4())

config = load_config()

async def send_2fa_email(email: str, code: str):
    # Настройки SMTP
    SMTP_SERVER = "smtp.mail.ru"
    SMTP_PORT = 587
    SMTP_USER = config.smtp.USER
    SMTP_PASSWORD = config.smtp.PASS

    msg = MIMEText(f"Your verification code: {code}")
    msg["Subject"] = "Your 2FA Code"
    msg["From"] = SMTP_USER
    msg["To"] = email

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)
    except Exception as e:
        print(f"Error sending email: {e}")