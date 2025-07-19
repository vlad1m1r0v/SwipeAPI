from dishka import AsyncContainer, Scope

from cli.faker_utils.generate_users import (
    generate_users,
    generate_user_contacts,
    generate_user_agent_contacts,
    generate_balances,
    generate_subscriptions,
    generate_notification_settings,
)
from src.user.services import (
    UserService,
    ContactService,
    AgentContactService,
    BalanceService,
    SubscriptionService,
    NotificationSettingsService,
)


async def generate_records(
    container: AsyncContainer,
):
    async with container(scope=Scope.REQUEST) as container:
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
