from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService, ModelDictT

from src.auth.utils import hash_password

import src.users.models as m
import src.users.repositories as r
import src.users.enums as e


class UserService(SQLAlchemyAsyncRepositoryService[m.User, r.UserRepository]):
    repository_type = r.UserRepository

    async def create_user(self, data: ModelDictT) -> m.User:
        data = data.model_dump(mode='json')
        return await super().create(data={**data, 'role': e.UserRoleEnum.USER})

    async def to_model(self, data: ModelDictT, operation: str | None = None) -> m.User:
        if isinstance(data, dict) and "password" in data:
            password: bytes | str | None = data.pop("password", None)
            if password is not None:
                hashed_password = hash_password(password)
                data.update({"password": hashed_password.decode()})
        return await super().to_model(data, operation)


class ContactService(SQLAlchemyAsyncRepositoryService[m.Contact, r.ContactRepository]):
    repository_type = r.ContactRepository


class AgentContactService(SQLAlchemyAsyncRepositoryService[m.AgentContact, r.AgentContactRepository]):
    repository_type = r.AgentContactRepository


class SubscriptionService(SQLAlchemyAsyncRepositoryService[m.Subscription, r.SubscriptionRepository]):
    repository_type = r.SubscriptionRepository


class NotificationSettingsService(
    SQLAlchemyAsyncRepositoryService[m.NotificationSettings, r.NotificationSettingsRepository]):
    repository_type = r.NotificationSettingsRepository


class BalanceService(
    SQLAlchemyAsyncRepositoryService[m.Balance, r.BalanceRepository]):
    repository_type = r.BalanceRepository

    async def create(self, data: ModelDictT, **kwargs) -> m.Balance:
        print(f"DATA: {data}")
        return await super().create(data=data)


__all__ = [
    "UserService",
    "ContactService",
    "AgentContactService",
    "SubscriptionService",
    "NotificationSettingsService",
    "BalanceService",
]
