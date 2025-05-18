from sqlalchemy import orm

from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService, ModelDictT

from src.auth.utils import hash_password, validate_password

import src.users.models as m
import src.users.repositories as r
import src.users.enums as e
import src.users.exceptions as ex


class UserService(SQLAlchemyAsyncRepositoryService[m.User, r.UserRepository]):
    repository_type = r.UserRepository

    async def get_user_profile(self, item_id: int) -> m.User:
        return await self.get(
            item_id=item_id,
            load=[
                orm.joinedload(m.User.contact),
                orm.joinedload(m.User.agent_contact),
                orm.joinedload(m.User.subscription),
                orm.joinedload(m.User.notification_settings),
                orm.joinedload(m.User.balance)
            ]
        )

    async def create_user(self, data: ModelDictT) -> m.User:
        data = data.model_dump(mode='json')
        return await super().create(data={**data, 'role': e.ROLE.USER})

    async def authenticate(self, data: ModelDictT) -> m.User:
        user = await self.get_one_or_none(email=data.email)

        if not user:
            raise ex.UserDoesNotExistException()

        if not validate_password(data.password, user.password.encode()):
            raise ex.IncorrectPasswordException()

        return user

    async def update_password(self, data: ModelDictT) -> None:
        user = await self.get_one_or_none(id=data['id'])

        if not user:
            raise ex.UserDoesNotExistException()

        if not validate_password(data['old_password'], user.password.encode()):
            raise ex.IncorrectPasswordException()

        await self.update(data={'password': data['new_password']}, item_id=user.id)

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


__all__ = [
    "UserService",
    "ContactService",
    "AgentContactService",
    "SubscriptionService",
    "NotificationSettingsService",
    "BalanceService",
]
