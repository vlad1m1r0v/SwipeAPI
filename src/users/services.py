from decimal import Decimal
from typing import Sequence

from sqlalchemy import (
    orm,
    select
)

from advanced_alchemy.service import (
    SQLAlchemyAsyncRepositoryService,
    ModelDictT
)

from advanced_alchemy.filters import (
    LimitOffset
)

from src.auth.utils import (
    hash_password,
    validate_password
)

import src.users.models as m
import src.users.repositories as r
import src.users.enums as e
import src.users.exceptions as ex

from src.admins.models import Blacklist

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
        data = data.model_dump()
        return await super().create(data={**data, 'role': e.ROLE.USER})

    async def create_admin(self, data: ModelDictT) -> m.User:
        data = data.model_dump()
        return await super().create(data={**data, 'role': e.ROLE.ADMIN})

    async def get_blacklisted_users(
            self,
            limit: int = 20,
            offset: int = 0
    ) -> tuple[Sequence[m.User], int]:
        limit_offset = LimitOffset(limit=limit, offset=offset)

        stmt = (
            select(m.User)
            .join(Blacklist, m.User.id == Blacklist.user_id)
        )

        results, total = await self.list_and_count(
            limit_offset,
            statement=stmt.options(orm.joinedload(m.User.blacklist)),
        )

        return results, total

    async def authenticate(self, data: ModelDictT) -> m.User:
        user = await self.get_one_or_none(email=data.email)

        if not user:
            raise ex.UserDoesNotExistException()

        if not validate_password(data.password, user.password.encode()):
            raise ex.IncorrectPasswordException()

        return user

    async def update_password(self, item_id: int, data: ModelDictT) -> None:
        user = await self.get_one_or_none(id=item_id)

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

    async def deposit_money(self, item_id: int, amount: float) -> None:
        balance = await self.get_one_or_none(id=item_id)

        if not balance:
            raise ex.BalanceNotFoundException()

        await self.update(
            data={'value': balance.value + Decimal(amount)},
            item_id=item_id
        )


__all__ = [
    "UserService",
    "ContactService",
    "AgentContactService",
    "SubscriptionService",
    "NotificationSettingsService",
    "BalanceService",
]
