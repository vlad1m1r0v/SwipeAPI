from advanced_alchemy.repository import SQLAlchemyAsyncRepository

import src.users.models as m


class UserRepository(SQLAlchemyAsyncRepository[m.User]):
    model_type = m.User


class ContactRepository(SQLAlchemyAsyncRepository[m.Contact]):
    model_type = m.Contact


class AgentContactRepository(SQLAlchemyAsyncRepository[m.AgentContact]):
    model_type = m.AgentContact


class SubscriptionRepository(SQLAlchemyAsyncRepository[m.Subscription]):
    model_type = m.Subscription


class NotificationSettingsRepository(SQLAlchemyAsyncRepository[m.NotificationSettings]):
    model_type = m.NotificationSettings


class BalanceRepository(SQLAlchemyAsyncRepository[m.Balance]):
    model_type = m.Balance


__all__ = [
    "UserRepository",
    "ContactRepository",
    "AgentContactRepository",
    "SubscriptionRepository",
    "NotificationSettingsRepository",
    "BalanceRepository",
]
