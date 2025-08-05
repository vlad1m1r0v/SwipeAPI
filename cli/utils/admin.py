from typing import cast, Sequence

import random

from dishka import AsyncContainer

from pydantic import EmailStr

from advanced_alchemy.filters import StatementFilter, ComparisonFilter

from cli.contstants import (
    TEST_USER_EMAIL,
    COMMON_PASSWORD,
    TEST_ADMIN_NAME,
    TEST_ADMIN_EMAIL,
)

from cli.schemas import CreateUserSchema, CreateComplaintSchema

from cli.utils.faker import fake

from src.admin.schemas import BlacklistUserSchema
from src.admin.services import BlacklistService

from src.user.enums import Role
from src.user.models import User
from src.user.services import UserService

from src.announcements.models import Announcement
from src.announcements.services import AnnouncementComplaintService


async def blacklist_users(
    blacklist_service: BlacklistService, user_service: UserService
) -> None:
    filters: list[StatementFilter] = [
        ComparisonFilter(field_name="email", operator="ne", value=TEST_USER_EMAIL),
        ComparisonFilter(field_name="role", operator="eq", value=Role.USER),
    ]

    users = await user_service.list(*filters)

    users_to_block: list[BlacklistUserSchema] = []

    for i, user in enumerate(users):
        if i % 3 == 0:
            users_to_block.append(BlacklistUserSchema(user_id=user.id))

    await blacklist_service.create_many(users_to_block)


def generate_complaints(
    admin: User, announcements: Sequence[Announcement]
) -> list[CreateComplaintSchema]:
    complaints: list[CreateComplaintSchema] = []

    bool_list: list[bool] = [True, False, False]

    for i, announcement in enumerate(announcements):
        if i % 3 == 0:
            random.shuffle(bool_list)

            complaints.append(
                CreateComplaintSchema(
                    user_id=admin.id,
                    announcement_id=announcement.id,
                    is_incorrect_photo=bool_list[0],
                    is_incorrect_price=bool_list[1],
                    is_incorrect_description=bool_list[2],
                )
            )

    return complaints


async def create_admin(
    container: AsyncContainer, announcements: Sequence[Announcement]
) -> None:
    user_service = await container.get(UserService)
    blacklist_service = await container.get(BlacklistService)
    complaint_service = await container.get(AnnouncementComplaintService)

    admin = await user_service.create(
        CreateUserSchema(
            name=TEST_ADMIN_NAME,
            email=cast(EmailStr, TEST_ADMIN_EMAIL),
            password=COMMON_PASSWORD,
            role=Role.ADMIN,
            phone=fake.ukrainian_phone(),
        )
    )

    await blacklist_users(blacklist_service, user_service)

    complaints_to_create = generate_complaints(admin, announcements)
    await complaint_service.create_many(complaints_to_create)
