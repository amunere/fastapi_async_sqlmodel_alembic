import logging
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import emails  # type: ignore
import jwt
from jinja2 import Template
from jwt.exceptions import InvalidTokenError
from PIL import Image 

from app.core.config import settings


@dataclass
class EmailData:
    html_content: str
    subject: str


def render_email_template(*, template_name: str, context: dict[str, Any]) -> str:
    template_str = (
        Path(__file__).parent / "email-templates" / template_name
    ).read_text()
    html_content = Template(template_str).render(context)
    return html_content


def send_email(
    *,
    email_to: str,
    subject: str = "",
    html_content: str = "",
) -> None:
    assert settings.EMAILS_ENABLED, "no provided configuration for email variables"
    message = emails.Message(
        subject=subject,
        html=html_content,
        mail_from=(settings.EMAILS_FROM_NAME, settings.EMAIL_FROM),
    )
    smtp_options = {"host": settings.EMAIL_SERVER, "port": settings.EMAIL_PORT}
    if settings.EMAIL_STARTTLS:
        smtp_options["tls"] = True
    elif settings.EMAIL_SSL_TLS:
        smtp_options["ssl"] = True
    if settings.EMAIL_FROM:
        smtp_options["user"] = settings.EMAIL_FROM
    if settings.EMAIL_PASSWORD:
        smtp_options["password"] = settings.EMAIL_PASSWORD
    response = message.send(to=email_to, smtp=smtp_options)
    logging.info(f"send email result: {response}")


def generate_test_email(email_to: str) -> EmailData:
    app_name = settings.APP_NAME
    subject = f"{app_name} - Test email"
    html_content = render_email_template(
        template_name="test_email.html",
        context={"app_name": settings.APP_NAME, "email": email_to},
    )
    return EmailData(html_content=html_content, subject=subject)


def generate_reset_password_email(email_to: str, email: str, token: str) -> EmailData:
    app_name = settings.APP_NAME
    subject = f"{app_name} - Password recovery for user {email}"
    link = f"{settings.APP_HOST}/reset-password?token={token}"
    html_content = render_email_template(
        template_name="reset_password.html",
        context={
            "app_name": settings.APP_NAME,
            "username": email,
            "email": email_to,
            "valid_hours": settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS,
            "link": link,
        },
    )
    return EmailData(html_content=html_content, subject=subject)


def generate_new_account_email(
    email_to: str, username: str, password: str
) -> EmailData:
    app_name = settings.APP_NAME
    subject = f"{app_name} - New account for user {username}"
    html_content = render_email_template(
        template_name="new_user.html",
        context={
            "app_name": settings.APP_NAME,
            "username": username,
            "password": password,
            "email": email_to,
            "link": settings.APP_HOST,
        },
    )
    return EmailData(html_content=html_content, subject=subject)


def generate_password_reset_token(email: str) -> str:
    delta = timedelta(hours=settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS)
    now = datetime.now(timezone.utc)
    expires = now + delta
    exp = expires.timestamp()
    encoded_jwt = jwt.encode(
        {"exp": exp, "nbf": now, "sub": email},
        settings.SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )
    return encoded_jwt


def verify_password_reset_token(token: str) -> str | None:
    try:
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.JWT_ALGORITHM)
        return str(decoded_token["sub"])
    except InvalidTokenError:
        return None
    

def thumbnail_post_image(file, email: str):
    try:
        img = Image.open(file.file)
    except:
        return None   
    img.thumbnail(settings.IMAGE_SIZE)
    file_path = settings.UPLOAD_PATH + "/" + email + "_" + settings.DATESTAMP + "." + img.format
    img.save(file_path)
    return file_path