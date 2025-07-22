from typing import List, Sequence, cast

from datetime import datetime, timedelta

from pydantic import EmailStr

from dishka import AsyncContainer

from .faker_instance import fake
from .media_utils import save_file_from_dataset
from .contstants import COMMON_PASSWORD, TEST_USER_NAME, TEST_USER_EMAIL, USERS_TOTAL

from src.user.enums import NotificationType
from src.user.schemas import (
    CreateUserSchema,
    CreateContactSchema,
    CreateAgentContactSchema,
    CreateBalanceSchema,
    CreateNotificationSettingsSchema,
    CreateSubscriptionSchema,
)
from src.user.services import (
    UserService,
    ContactService,
    AgentContactService,
    BalanceService,
    SubscriptionService,
    NotificationSettingsService,
)

from src.user.models import User


def generate_users() -> List[CreateUserSchema]:
    photo = save_file_from_dataset(fake.avatar_path())
    phone = fake.ukrainian_phone()

    users: List[CreateUserSchema] = [
        CreateUserSchema(
            name=TEST_USER_NAME,
            email=cast(EmailStr, TEST_USER_EMAIL),
            password=COMMON_PASSWORD,
            photo=photo,
            phone=phone,
        )
    ]

    for _ in range(USERS_TOTAL):
        name = fake.unique.name()
        email = fake.custom_email(name)
        photo = save_file_from_dataset(fake.avatar_path())
        phone = fake.ukrainian_phone()
        users.append(
            CreateUserSchema(
                name=name,
                email=cast(EmailStr, email),
                password=COMMON_PASSWORD,
                photo=photo,
                phone=phone,
            )
        )
    return users


def generate_user_contacts(users: Sequence[User]) -> List[CreateContactSchema]:
    contacts: List[CreateContactSchema] = []

    for user in users:
        parts = user.name.split(" ")
        contacts.append(
            CreateContactSchema(
                user_id=user.id,
                first_name=parts[0],
                last_name=parts[-1],
                phone=user.phone,
                email=user.email,
            )
        )

    return contacts


def generate_user_agent_contacts(
    users: Sequence[User],
) -> List[CreateAgentContactSchema]:
    agent_contacts: List[CreateAgentContactSchema] = []

    for user in users:
        first_name = fake.unique.first_name()
        last_name = fake.unique.last_name()
        email = fake.custom_email(f"{first_name} {last_name}")

        agent_contacts.append(
            CreateAgentContactSchema(
                user_id=user.id,
                first_name=first_name,
                last_name=last_name,
                phone=fake.ukrainian_phone(),
                email=email,
            )
        )

    return agent_contacts


def generate_balances(users: Sequence[User]) -> List[CreateBalanceSchema]:
    balances: List[CreateBalanceSchema] = []

    for user in users:
        balances.append(
            CreateBalanceSchema(
                user_id=user.id,
                value=fake.pydecimal(min_value=1000, max_value=10000, right_digits=2),
            )
        )

    return balances


def generate_notification_settings(
    users: Sequence[User],
) -> List[CreateNotificationSettingsSchema]:
    notification_settings: List[CreateNotificationSettingsSchema] = []

    for user in users:
        notification_settings.append(
            CreateNotificationSettingsSchema(
                user_id=user.id,
                redirect_notifications_to_agent=fake.boolean(),
                notification_type=fake.enum(NotificationType),
            )
        )

    return notification_settings


def generate_subscriptions(users: Sequence[User]) -> List[CreateSubscriptionSchema]:
    subscriptions: List[CreateSubscriptionSchema] = []

    now = datetime.now()

    for user in users:
        subscriptions.append(
            CreateSubscriptionSchema(
                user_id=user.id,
                is_auto_renewal=fake.boolean(),
                expiry_date=fake.date_time_between_dates(
                    now + timedelta(days=30), now + timedelta(days=90)
                ),
            )
        )

    return subscriptions


async def create_users(container: AsyncContainer) -> Sequence[User]:
    users_to_create = generate_users()
    user_service = await container.get(UserService)
    users = await user_service.create_many(users_to_create)

    user_contacts_to_create = generate_user_contacts(users)
    contact_service = await container.get(ContactService)
    await contact_service.create_many(user_contacts_to_create)

    user_agent_contacts_to_create = generate_user_agent_contacts(users)
    agent_contact_service = await container.get(AgentContactService)
    await agent_contact_service.create_many(user_agent_contacts_to_create)

    balances_to_create = generate_balances(users)
    balance_service = await container.get(BalanceService)
    await balance_service.create_many(balances_to_create)

    subscriptions_to_create = generate_subscriptions(users)
    subscription_service = await container.get(SubscriptionService)
    await subscription_service.create_many(subscriptions_to_create)

    notification_settings_to_create = generate_notification_settings(users)
    notification_settings_service = await container.get(NotificationSettingsService)
    await notification_settings_service.create_many(notification_settings_to_create)

    return users
