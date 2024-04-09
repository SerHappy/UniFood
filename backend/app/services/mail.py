from datetime import datetime, timedelta, timezone
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from typing import Any

from aiosmtplib import SMTP
from app.core.config import settings
from jinja2 import Template
from jose import jwt
from jose.exceptions import JWTError


def render_email_template(template_name: str, context: dict[str, Any] = {}) -> str:
    template_str = (
        Path(__file__).parent.parent / "email-templates" / template_name
    ).read_text()
    html_content = Template(template_str).render(context)
    return html_content


async def send_email(
    email_to: str,
    subject: str = "",
    html_content: str = "",
) -> None:

    email_message = MIMEMultipart("alternative")
    email_message["From"] = settings.EMAILS_FROM_EMAIL
    email_message["To"] = (
        settings.EMAIL_TEST_USER if settings.EMAILS_FROM_NAME else email_to
    )
    email_message["Subject"] = subject

    email_message.attach(MIMEText(html_content, "html"))

    async with SMTP(
        hostname=settings.SMTP_HOST,
        port=settings.SMTP_PORT,
        use_tls=True,
    ) as smtp:
        await smtp.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        await smtp.send_message(email_message)


def generate_confirmation_email(token: str) -> str:
    context = {
        "link": f"http://127.0.0.1:8000{settings.API_V1_STR}/registration/confirm?token={token}",
    }
    html_content = render_email_template("verification.html", context)
    return html_content


def generate_confirmation_token(email: str) -> str:
    delta = timedelta(minutes=settings.EMAIL_VERIFICATION_TOKEN_EXPIRE_MINUTES)
    now = datetime.now(timezone.utc)
    expires = now + delta
    exp = expires.timestamp()
    encoded_jwt = jwt.encode(
        {
            "exp": exp,
            "nbf": now,
            "sub": email,
            "type": "email_confirmation",
        },
        settings.SECRET_KEY,
        algorithm="HS256",
    )
    return encoded_jwt


def verify_confirmation_token(token: str) -> str | None:
    try:
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        type = decoded_token["type"]
        if type != "email_confirmation":
            raise JWTError
        email = decoded_token["sub"]
        return email
    except JWTError:
        return None
