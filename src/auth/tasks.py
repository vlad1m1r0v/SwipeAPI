from src.core.celery_app import celery

import asyncio

from pydantic import EmailStr

from dishka import FromDishka
from dishka.integrations.celery import inject

from fastapi_mail import FastMail, MessageSchema, MessageType

from jinja2 import Environment


@celery.task
@inject
def send_forgot_password_email(
    email: EmailStr,
    token: str,
    jinja2_env: FromDishka[Environment],
    fastapi_mail: FromDishka[FastMail],
):
    template = jinja2_env.get_template("forgot_password.html")

    message = MessageSchema(
        subject="Reset Password",
        recipients=[email],
        body=template.render(token=token),
        subtype=MessageType.html,
    )

    asyncio.run(fastapi_mail.send_message(message))
