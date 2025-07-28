from typing import cast

from dishka import AsyncContainer

from pydantic import EmailStr

from cli.contstants import COMMON_PASSWORD, TEST_ADMIN_NAME, TEST_ADMIN_EMAIL

from cli.schemas import CreateUserSchema

from cli.utils.faker import fake

from src.user.enums import Role
from src.user.services import UserService


async def create_admin(container: AsyncContainer):
    user_service = await container.get(UserService)

    await user_service.create(
        CreateUserSchema(
            name=TEST_ADMIN_NAME,
            email=cast(EmailStr, TEST_ADMIN_EMAIL),
            password=COMMON_PASSWORD,
            role=Role.ADMIN,
            phone=fake.ukrainian_phone(),
        )
    )
